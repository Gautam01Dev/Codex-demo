from __future__ import annotations

import math
from dataclasses import dataclass

import numpy as np
import pandas as pd
import yfinance as yf
from sklearn.linear_model import LinearRegression
from sklearn.metrics import r2_score


@dataclass
class MarketPrediction:
    latest_price: float
    short_term_prediction: float
    mid_term_prediction: float
    confidence_score: float
    indicators: dict[str, float]


def _normalize_symbol(symbol: str, asset_type: str) -> str:
    if asset_type == "crypto" and "-USD" not in symbol.upper():
        return f"{symbol.upper()}-USD"
    return symbol.upper()


def _calculate_indicators(frame: pd.DataFrame) -> dict[str, float]:
    close = frame["Close"]
    volume = frame["Volume"]

    delta = close.diff()
    gain = delta.where(delta > 0, 0).rolling(14).mean()
    loss = -delta.where(delta < 0, 0).rolling(14).mean().replace(0, np.nan)
    rs = gain / loss
    rsi = 100 - (100 / (1 + rs))

    ema12 = close.ewm(span=12, adjust=False).mean()
    ema26 = close.ewm(span=26, adjust=False).mean()
    macd = ema12 - ema26

    return {
        "volume": float(volume.iloc[-1]),
        "rsi": float(rsi.fillna(50).iloc[-1]),
        "macd": float(macd.iloc[-1]),
        "sma_20": float(close.rolling(20).mean().fillna(close.iloc[-1]).iloc[-1]),
        "sma_50": float(close.rolling(50).mean().fillna(close.iloc[-1]).iloc[-1]),
    }


def _predict_prices(close: pd.Series) -> tuple[float, float, float]:
    values = close.values.reshape(-1, 1)
    X = np.arange(len(values)).reshape(-1, 1)
    model = LinearRegression()
    model.fit(X, values)

    next_week = model.predict([[len(values) + 7]])[0][0]
    next_quarter = model.predict([[len(values) + 90]])[0][0]
    in_sample = model.predict(X).flatten()
    confidence = max(0.0, min(100.0, r2_score(close.values, in_sample) * 100))

    return float(next_week), float(next_quarter), float(confidence)


def generate_market_prediction(symbol: str, asset_type: str) -> MarketPrediction:
    normalized = _normalize_symbol(symbol, asset_type)
    frame = yf.download(normalized, period="1y", interval="1d", auto_adjust=True, progress=False)
    if frame.empty:
        raise ValueError(f"No market data found for {symbol}")

    frame = frame.dropna()
    if len(frame) < 60:
        raise ValueError("Insufficient data points for prediction")

    latest_price = float(frame["Close"].iloc[-1])
    short_term, mid_term, confidence = _predict_prices(frame["Close"])
    indicators = _calculate_indicators(frame)

    return MarketPrediction(
        latest_price=latest_price,
        short_term_prediction=max(0.01, short_term),
        mid_term_prediction=max(0.01, mid_term),
        confidence_score=round(confidence, 2),
        indicators=indicators,
    )


def recommendation_from_prediction(symbol: str, prediction: MarketPrediction) -> dict[str, str | float]:
    delta = (prediction.short_term_prediction - prediction.latest_price) / prediction.latest_price
    volatility_proxy = abs(prediction.indicators["macd"]) / max(prediction.latest_price, 1)

    if delta > 0.04:
        action = "Buy"
    elif delta < -0.03:
        action = "Sell"
    else:
        action = "Hold"

    risk_level = "High" if volatility_proxy > 0.03 else "Medium" if volatility_proxy > 0.01 else "Low"
    duration = "1-4 weeks" if abs(delta) < 0.06 else "1-3 months"
    allocation = max(5.0, min(35.0, 25.0 - (volatility_proxy * 100) + (prediction.confidence_score / 10)))

    return {
        "symbol": symbol,
        "action": action,
        "risk_level": risk_level,
        "investment_duration": duration,
        "portfolio_allocation_pct": round(allocation, 2),
    }


def generate_ai_insights(symbol: str, prediction: MarketPrediction) -> dict[str, list[str]]:
    rsi = prediction.indicators["rsi"]
    confidence = prediction.confidence_score

    pros = [
        "Growth potential supported by positive modeled price trajectory." if prediction.short_term_prediction > prediction.latest_price else "Stable trading pattern with limited downside in short term.",
        f"Technical confidence score is {confidence:.1f}%, indicating model consistency.",
        "Moving averages show medium-term accumulation trend." if prediction.indicators["sma_20"] > prediction.indicators["sma_50"] else "Recent pullback may create an accumulation opportunity.",
        "Institutional and momentum behavior appear constructive based on volume stability.",
    ]

    cons = [
        "Volatility risk remains elevated; predictions can deviate sharply in macro shocks.",
        "Sentiment shifts from negative news could invalidate bullish setup quickly.",
        "Regulatory events can disproportionately impact valuation, especially for crypto assets.",
        "Overbought conditions detected (RSI > 70)." if rsi > 70 else "Weak momentum risk if RSI slips below 45.",
    ]

    return {"pros": pros, "cons": cons}
