import axios from 'axios'

const API_BASE = import.meta.env.VITE_API_BASE || 'http://localhost:8000'

export const api = axios.create({ baseURL: API_BASE })

export async function listPosts() {
  const { data } = await api.get('/api/blog/posts')
  return data
}

export async function createPost(payload) {
  const { data } = await api.post('/api/blog/posts', payload)
  return data
}
