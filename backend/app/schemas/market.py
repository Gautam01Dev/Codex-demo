from pydantic import BaseModel, Field


class PredictionRequest(BaseModel):
    symbol: str = Field(min_length=1, max_length=20)
    asset_type: str = Field(pattern="^(stock|crypto)$")


class PredictionResponse(BaseModel):
    symbol: str
    latest_price: float
    short_term_prediction: float
    mid_term_prediction: float
    confidence_score: float
    indicators: dict[str, float]


class RecommendationResponse(BaseModel):
    symbol: str
    action: str
    risk_level: str
    investment_duration: str
    portfolio_allocation_pct: float


class InsightResponse(BaseModel):
    symbol: str
    pros: list[str]
    cons: list[str]


class WatchlistItemCreate(BaseModel):
    symbol: str
    asset_type: str = Field(pattern="^(stock|crypto)$")


class AlertCreate(BaseModel):
    symbol: str
    target_price: float
    prediction_threshold: float | None = None
