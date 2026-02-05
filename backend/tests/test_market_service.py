from app.services.market_service import MarketPrediction, recommendation_from_prediction


def test_recommendation_logic_buy_signal():
    prediction = MarketPrediction(
        latest_price=100,
        short_term_prediction=110,
        mid_term_prediction=120,
        confidence_score=82,
        indicators={"macd": 1.0, "rsi": 55, "volume": 1000000, "sma_20": 101, "sma_50": 99},
    )

    result = recommendation_from_prediction("AAPL", prediction)

    assert result["action"] == "Buy"
    assert result["risk_level"] in {"Low", "Medium", "High"}
    assert 5 <= result["portfolio_allocation_pct"] <= 35
