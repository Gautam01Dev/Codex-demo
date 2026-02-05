from __future__ import annotations

from collections import Counter

import httpx

from app.core.config import settings

POSITIVE = {"surge", "beat", "growth", "bullish", "upgrade", "record", "partnership"}
NEGATIVE = {"drop", "miss", "bearish", "downgrade", "lawsuit", "hack", "ban"}


async def fetch_news_headlines(symbol: str) -> list[str]:
    if not settings.news_api_key:
        return [f"{symbol} market outlook remains mixed as macro conditions evolve"]

    url = "https://newsapi.org/v2/everything"
    params = {"q": symbol, "pageSize": 10, "language": "en", "apiKey": settings.news_api_key}
    async with httpx.AsyncClient(timeout=10) as client:
        response = await client.get(url, params=params)
        response.raise_for_status()
        articles = response.json().get("articles", [])
        return [article.get("title", "") for article in articles if article.get("title")]


def score_sentiment(headlines: list[str]) -> dict[str, float | str]:
    score = 0
    tokens = Counter()
    for title in headlines:
        words = {word.strip(".,!?").lower() for word in title.split()}
        for word in words:
            if word in POSITIVE:
                score += 1
            elif word in NEGATIVE:
                score -= 1
            tokens[word] += 1

    label = "positive" if score > 1 else "negative" if score < -1 else "neutral"
    return {"label": label, "score": float(score), "headline_count": float(len(headlines))}
