import axios from 'axios'

const API_BASE = import.meta.env.VITE_API_BASE || 'http://localhost:8000'

export const api = axios.create({ baseURL: API_BASE })

export async function runPrediction(symbol, assetType, token) {
  const { data } = await api.post('/api/market/predict', { symbol, asset_type: assetType }, { headers: { Authorization: `Bearer ${token}` } })
  return data
}
