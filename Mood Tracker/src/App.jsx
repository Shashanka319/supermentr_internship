import { useState, useEffect } from 'react'
import './App.css'

function App() {
  const [mood, setMood] = useState('')
  const [history, setHistory] = useState([])
  const [darkMode, setDarkMode] = useState(false)

  const moods = [
    { name: 'Happy', emoji: '😊', color: '#FFD700', score: 5 },
    { name: 'Sad', emoji: '😢', color: '#87CEEB', score: 2 },
    { name: 'Angry', emoji: '😠', color: '#FF6347', score: 1 },
    { name: 'Excited', emoji: '🤩', color: '#FF69B4', score: 4 },
    { name: 'Calm', emoji: '😌', color: '#98FB98', score: 3 }
  ]

  const quotes = {
    Happy: ["Happiness is not something ready made. It comes from your own actions. - Dalai Lama", "The best way to cheer yourself is to try to cheer someone else up. - Mark Twain"],
    Sad: ["The way sadness works is one of the strange riddles of the world. - Lemony Snicket", "Tears are words that need to be written. - Paulo Coelho"],
    Angry: ["For every minute you remain angry, you give up sixty seconds of peace of mind. - Ralph Waldo Emerson", "Anger is an acid that can do more harm to the vessel in which it is stored than to anything on which it is poured. - Mark Twain"],
    Excited: ["The only way to do great work is to love what you do. - Steve Jobs", "Life is either a daring adventure or nothing at all. - Helen Keller"],
    Calm: ["Peace comes from within. Do not seek it without. - Buddha", "Calmness is the cradle of power. - Josiah Gilbert Holland"]
  }

  useEffect(() => {
    const savedHistory = localStorage.getItem('moodHistory')
    if (savedHistory) {
      setHistory(JSON.parse(savedHistory))
    }
    const savedDarkMode = localStorage.getItem('darkMode')
    if (savedDarkMode) {
      setDarkMode(JSON.parse(savedDarkMode))
    }
  }, [])

  const selectMood = (selectedMood) => {
    setMood(selectedMood.name)
    const newEntry = {
      mood: selectedMood.name,
      emoji: selectedMood.emoji,
      score: selectedMood.score,
      timestamp: new Date().toLocaleString()
    }
    const updatedHistory = [newEntry, ...history]
    setHistory(updatedHistory)
    localStorage.setItem('moodHistory', JSON.stringify(updatedHistory))
  }

  const clearHistory = () => {
    setHistory([])
    localStorage.removeItem('moodHistory')
  }

  const toggleDarkMode = () => {
    setDarkMode(!darkMode)
    localStorage.setItem('darkMode', JSON.stringify(!darkMode))
  }

  const getStats = () => {
    if (history.length === 0) return null
    const totalScore = history.reduce((sum, entry) => sum + entry.score, 0)
    const averageScore = (totalScore / history.length).toFixed(1)
    const moodCounts = history.reduce((counts, entry) => {
      counts[entry.mood] = (counts[entry.mood] || 0) + 1
      return counts
    }, {})
    const mostCommonMood = Object.keys(moodCounts).reduce((a, b) => moodCounts[a] > moodCounts[b] ? a : b)
    return { totalEntries: history.length, averageScore, mostCommonMood }
  }

  const getRandomQuote = (moodName) => {
    const moodQuotes = quotes[moodName] || []
    return moodQuotes[Math.floor(Math.random() * moodQuotes.length)] || "Keep tracking your moods to understand yourself better!"
  }

  const stats = getStats()

  return (
    <div className={`App ${darkMode ? 'dark' : ''}`}>
      <button className="theme-toggle" onClick={toggleDarkMode}>
        {darkMode ? '☀️ Light' : '🌙 Dark'}
      </button>
      <h1>🌟 Mood Tracker 🌟</h1>
      <p>How are you feeling today?</p>
      <div className="mood-buttons">
        {moods.map(m => (
          <button
            key={m.name}
            className="mood-btn"
            style={{ backgroundColor: m.color }}
            onClick={() => selectMood(m)}
          >
            {m.emoji} {m.name}
          </button>
        ))}
      </div>
      {mood && (
        <div className="current-mood">
          <h2>Your Current Mood: {moods.find(m => m.name === mood)?.emoji} {mood}</h2>
          <p className="quote">"{getRandomQuote(mood)}"</p>
        </div>
      )}
      {stats && (
        <div className="stats">
          <h2>📊 Your Mood Statistics</h2>
          <div className="stat-grid">
            <div className="stat-item">
              <span className="stat-number">{stats.totalEntries}</span>
              <span className="stat-label">Total Entries</span>
            </div>
            <div className="stat-item">
              <span className="stat-number">{stats.averageScore}</span>
              <span className="stat-label">Average Score</span>
            </div>
            <div className="stat-item">
              <span className="stat-number">{moods.find(m => m.name === stats.mostCommonMood)?.emoji}</span>
              <span className="stat-label">Most Common: {stats.mostCommonMood}</span>
            </div>
          </div>
        </div>
      )}
      <div className="history">
        <h2>📅 Mood History</h2>
        {history.length > 0 ? (
          <>
            <button className="clear-btn" onClick={clearHistory}>🗑️ Clear History</button>
            <ul>
              {history.map((entry, index) => (
                <li key={index} className="history-item">
                  {entry.emoji} {entry.mood} (Score: {entry.score}) - {entry.timestamp}
                </li>
              ))}
            </ul>
          </>
        ) : (
          <p>No moods tracked yet. Select a mood to get started! 🌈</p>
        )}
      </div>
    </div>
  )
}

export default App