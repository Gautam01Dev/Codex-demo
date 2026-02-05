from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.api.deps import get_current_user
from app.db.session import get_db
from app.models.models import Alert, Watchlist
from app.schemas.market import (
    AlertCreate,
    InsightResponse,
    PredictionRequest,
    PredictionResponse,
    RecommendationResponse,
    WatchlistItemCreate,
)
from app.services.market_service import (
    generate_ai_insights,
    generate_market_prediction,
    recommendation_from_prediction,
)
from app.services.sentiment_service import fetch_news_headlines, score_sentiment

router = APIRouter(prefix="/api/market", tags=["market"])


@router.post("/predict", response_model=PredictionResponse)
def predict(payload: PredictionRequest, user=Depends(get_current_user)):
    try:
        prediction = generate_market_prediction(payload.symbol, payload.asset_type)
        return PredictionResponse(
            symbol=payload.symbol.upper(),
            latest_price=prediction.latest_price,
            short_term_prediction=prediction.short_term_prediction,
            mid_term_prediction=prediction.mid_term_prediction,
            confidence_score=prediction.confidence_score,
            indicators=prediction.indicators,
        )
    except ValueError as exc:
        raise HTTPException(status_code=404, detail=str(exc)) from exc


@router.post("/recommend", response_model=RecommendationResponse)
def recommend(payload: PredictionRequest, user=Depends(get_current_user)):
    prediction = generate_market_prediction(payload.symbol, payload.asset_type)
    return recommendation_from_prediction(payload.symbol.upper(), prediction)


@router.post("/insights", response_model=InsightResponse)
async def insights(payload: PredictionRequest, user=Depends(get_current_user)):
    prediction = generate_market_prediction(payload.symbol, payload.asset_type)
    base = generate_ai_insights(payload.symbol.upper(), prediction)
    headlines = await fetch_news_headlines(payload.symbol)
    sentiment = score_sentiment(headlines)

    base["pros"].append(f"News sentiment currently {sentiment['label']} ({sentiment['score']:+.0f} score).")
    base["cons"].append("Headline momentum may reverse quickly in high-volatility sessions.")
    return InsightResponse(symbol=payload.symbol.upper(), pros=base["pros"], cons=base["cons"])


@router.post("/watchlist")
def add_watchlist(payload: WatchlistItemCreate, db: Session = Depends(get_db), user=Depends(get_current_user)):
    item = Watchlist(symbol=payload.symbol.upper(), asset_type=payload.asset_type, user_id=user.id)
    db.add(item)
    db.commit()
    db.refresh(item)
    return {"id": item.id, "symbol": item.symbol, "asset_type": item.asset_type}


@router.get("/watchlist")
def get_watchlist(db: Session = Depends(get_db), user=Depends(get_current_user)):
    items = db.query(Watchlist).filter(Watchlist.user_id == user.id).all()
    return [{"id": x.id, "symbol": x.symbol, "asset_type": x.asset_type} for x in items]


@router.post("/alerts")
def create_alert(payload: AlertCreate, db: Session = Depends(get_db), user=Depends(get_current_user)):
    alert = Alert(
        symbol=payload.symbol.upper(),
        target_price=payload.target_price,
        prediction_threshold=payload.prediction_threshold,
        user_id=user.id,
    )
    db.add(alert)
    db.commit()
    db.refresh(alert)
    return {"id": alert.id, "symbol": alert.symbol, "target_price": alert.target_price}
