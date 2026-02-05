from fastapi import APIRouter, Depends

from app.api.deps import get_current_user
from app.services.market_service import generate_market_prediction

router = APIRouter(prefix="/api/dashboard", tags=["dashboard"])


@router.get("/overview")
def overview(user=Depends(get_current_user)):
    tracked = ["AAPL", "MSFT", "BTC", "ETH"]
    cards = []
    for symbol in tracked:
        asset_type = "crypto" if symbol in {"BTC", "ETH"} else "stock"
        prediction = generate_market_prediction(symbol, asset_type)
        cards.append(
            {
                "symbol": symbol,
                "latest_price": prediction.latest_price,
                "predicted_7d": prediction.short_term_prediction,
                "confidence_score": prediction.confidence_score,
            }
        )

    return {
        "top_gainers": sorted(cards, key=lambda c: c["predicted_7d"] - c["latest_price"], reverse=True)[:2],
        "top_losers": sorted(cards, key=lambda c: c["predicted_7d"] - c["latest_price"])[:2],
        "fear_greed_index": "Neutral",
        "news_feed": [
            "US inflation cools, lifting risk assets.",
            "Crypto market consolidates ahead of macro events.",
            "Tech earnings continue to surprise positively.",
        ],
    }
