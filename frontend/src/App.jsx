import { useState } from 'react'
import './App.css'

const API_BASE = import.meta.env.VITE_API_BASE_URL || 'http://localhost:8000'

const MOODS = [
  { key: 'focus', label: 'focus', text: 'I need to concentrate and study' },
  { key: 'chill', label: 'chill', text: 'I just want to relax' },
  { key: 'energize', label: 'energize', text: 'I need energy to work out' },
  { key: 'destress', label: 'destress', text: "I'm stressed and anxious" },
]

function App() {
  const [moodText, setMoodText] = useState('')
  const [activeMood, setActiveMood] = useState('destress')
  const [result, setResult] = useState(null)
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState('')

  async function getPlaylist(textToSend) {
    setLoading(true)
    setError('')
    try {
      const res = await fetch(`${API_BASE}/api/playlist`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ mood_text: textToSend }),
      })
      if (!res.ok) throw new Error('Server error')
      const data = await res.json()
      setResult(data)
    } catch {
      setError('Could not reach the backend.')
    } finally {
      setLoading(false)
    }
  }

  function handleChipClick(mood) {
    setActiveMood(mood.key)
    setMoodText(mood.text)
    getPlaylist(mood.text)
  }

  function handleSubmit(e) {
    e.preventDefault()
    if (moodText.trim()) getPlaylist(moodText)
  }

  const [playingTrack, setPlayingTrack] = useState(null)
  const [videoId, setVideoId] = useState(null)
  const [videoLoading, setVideoLoading] = useState(false)

  async function playTrack(track) {
    setPlayingTrack(track.title)
    setVideoId(null)
    setVideoLoading(true)
    try {
      const params = `title=${encodeURIComponent(track.title)}&artist=${encodeURIComponent(track.artist)}`
      const res = await fetch(`${API_BASE}/api/video?${params}`)
      const data = await res.json()
      setVideoId(data.video_id)
    } catch {
      setVideoId(null)
    } finally {
      setVideoLoading(false)
    }
  }

  return (
    <div className="console" data-mood={activeMood}>
      <div className="label">
        <span className="mark">MoodTune</span>
        <span className="tag">AI curated</span>
      </div>

      <form className="prompt-row" onSubmit={handleSubmit}>
        <input
          value={moodText}
          onChange={(e) => setMoodText(e.target.value)}
          placeholder="How are you feeling right now?"
        />
        <button type="submit" disabled={loading}>
          {loading ? '...' : 'Tune in'}
        </button>
      </form>

      <div className="chips">
        {MOODS.map((mood) => (
          <button
            key={mood.key}
            type="button"
            className="chip"
            data-active={activeMood === mood.key}
            onClick={() => handleChipClick(mood)}
          >
            {mood.label}
          </button>
        ))}
      </div>

      {error && <p className="error">{error}</p>}

      {result && (
        <>
          <div className="ai-line">
            <p>
              {result.message}
              <span className="src">Interpreted mood: {result.interpreted_mood}</span>
            </p>
          </div>

          <div className="tracklist">
            {result.playlist.map((track, i) => (
              <div key={i}>
                <div className="track">
                  <div className="n">{String(i + 1).padStart(2, '0')}</div>
                  <div className="meta">
                    <a
                      className="title"
                      href={track.search_url}
                      target="_blank"
                      rel="noopener noreferrer"
                    >
                      {track.title}
                    </a>
                    <div className="artist">{track.artist}</div>
                  </div>
                  <div className="reason">{track.reason}</div>
                  <button
                    type="button"
                    className="play-btn"
                    onClick={() => playTrack(track)}
                  >
                    ▶
                  </button>
                </div>

                {playingTrack === track.title && (
                  <div className="player">
                    {videoLoading ? (
                      <p className="player-status">Loading…</p>
                    ) : videoId ? (
                      <iframe
                        src={`https://www.youtube-nocookie.com/embed/${videoId}?autoplay=1`}
                        title={track.title}
                        allow="autoplay; encrypted-media"
                        allowFullScreen
                      />
                    ) : (
                      <p className="player-status">
                        Couldn't find a video —{' '}
                        <a href={track.search_url} target="_blank" rel="noopener noreferrer">
                          search YouTube instead
                        </a>
                      </p>
                    )}
                  </div>
                )}
              </div>
            ))}
          </div>
        </>
      )}
    </div>
  )
}

export default App
