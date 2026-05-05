import { useEffect, useState } from 'react'
import { createPost, listPosts } from '../services/api'

const initialForm = { title: '', summary: '', content: '', author: '' }

export default function App() {
  const [posts, setPosts] = useState([])
  const [form, setForm] = useState(initialForm)
  const [loading, setLoading] = useState(true)

  const loadPosts = async () => {
    setLoading(true)
    try {
      setPosts(await listPosts())
    } finally {
      setLoading(false)
    }
  }

  useEffect(() => {
    loadPosts()
  }, [])

  const handleSubmit = async (e) => {
    e.preventDefault()
    await createPost(form)
    setForm(initialForm)
    await loadPosts()
  }

  return (
    <main className="app">
      <header className="topbar">
        <h1>Three-Tier Blog Platform</h1>
        <p>Presentation (React) • API (FastAPI) • Data (PostgreSQL/SQLite)</p>
      </header>

      <section className="card">
        <h2>Create Post</h2>
        <form className="post-form" onSubmit={handleSubmit}>
          <input placeholder="Title" value={form.title} onChange={(e) => setForm({ ...form, title: e.target.value })} required />
          <input placeholder="Author" value={form.author} onChange={(e) => setForm({ ...form, author: e.target.value })} required />
          <input placeholder="Summary" value={form.summary} onChange={(e) => setForm({ ...form, summary: e.target.value })} required />
          <textarea placeholder="Write your blog content..." rows={6} value={form.content} onChange={(e) => setForm({ ...form, content: e.target.value })} required />
          <button type="submit">Publish</button>
        </form>
      </section>

      <section className="card">
        <h2>Recent Posts</h2>
        {loading ? <p>Loading posts...</p> : (
          <div className="posts">
            {posts.map((post) => (
              <article key={post.id} className="post-item">
                <h3>{post.title}</h3>
                <p><strong>{post.author}</strong> • {new Date(post.created_at).toLocaleString()}</p>
                <p>{post.summary}</p>
                <details>
                  <summary>Read more</summary>
                  <p>{post.content}</p>
                </details>
              </article>
            ))}
            {posts.length === 0 && <p>No posts yet. Publish your first one.</p>}
          </div>
        )}
      </section>
    </main>
  )
}
