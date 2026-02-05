import { useMemo, useState } from 'react'
import PredictionChart from '../components/PredictionChart'

const sample = {
  symbol: 'AAPL',
  latest_price: 193.2,
  short_term_prediction: 201.1,
  mid_term_prediction: 214.8,
  confidence_score: 78.4,
  indicators: { volume: 56000000, rsi: 59.3, macd: 1.24, sma_20: 194.1, sma_50: 189.6 },
}

export default function App() {
  const [darkMode, setDarkMode] = useState(true)
  const [asset, setAsset] = useState(sample)

  const recommendation = useMemo(() => {
    const upside = ((asset.short_term_prediction - asset.latest_price) / asset.latest_price) * 100
    if (upside > 4) return 'Buy'
    if (upside < -3) return 'Sell'
    return 'Hold'
  }, [asset])

  return (
    <main className={darkMode ? 'app dark' : 'app'}>
      <header className="topbar">
        <h1>SmartInvest AI Dashboard</h1>
        <button onClick={() => setDarkMode((v) => !v)}>Toggle {darkMode ? 'Light' : 'Dark'} Mode</button>
      </header>

      <section className="grid">
        <article className="card">
          <h2>{asset.symbol} Prediction Engine</h2>
          <PredictionChart latest={asset.latest_price} shortTerm={asset.short_term_prediction} midTerm={asset.mid_term_prediction} />
          <p>Confidence: <strong>{asset.confidence_score}%</strong></p>
        </article>

        <article className="card">
          <h2>Investment Recommendation</h2>
          <ul>
            <li>Action: <strong>{recommendation}</strong></li>
            <li>Risk Level: <strong>Medium</strong></li>
            <li>Suggested Duration: <strong>1-3 months</strong></li>
            <li>Portfolio Allocation: <strong>18%</strong></li>
          </ul>
        </article>

        <article className="card">
          <h2>Pros & Cons Analyzer</h2>
          <p>✅ Pros: Growth potential, stable fundamentals, positive sentiment.</p>
          <p>❌ Cons: Volatility spikes, policy risk, sentiment reversals.</p>
        </article>

        <article className="card">
          <h2>Real-Time Snapshot</h2>
          <ul>
            <li>Top Gainer: BTC (+3.2%)</li>
            <li>Top Loser: ETH (-1.1%)</li>
            <li>Fear & Greed: Neutral</li>
            <li>News: "Tech earnings beat estimates across the board"</li>
          </ul>
        </article>
      </section>
    </main>
  )
}
