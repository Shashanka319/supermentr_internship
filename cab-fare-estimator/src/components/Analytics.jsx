import React, { useState, useEffect } from 'react'

const Analytics = () => {
  const [analytics, setAnalytics] = useState(null)
  const [advancedAnalytics, setAdvancedAnalytics] = useState(null)
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState('')

  useEffect(() => {
    fetchAnalytics()
  }, [])

  const fetchAnalytics = async () => {
    setLoading(true)
    try {
      const [analyticsRes, advancedRes] = await Promise.all([
        fetch('http://localhost:5000/api/stats'),
        fetch('http://localhost:5000/api/advanced-analytics')
      ])

      if (analyticsRes.ok && advancedRes.ok) {
        const analyticsData = await analyticsRes.json()
        const advancedData = await advancedRes.json()
        setAnalytics(analyticsData)
        setAdvancedAnalytics(advancedData)
      } else {
        setError('Failed to fetch analytics data')
      }
    } catch (err) {
      setError('Error connecting to server')
    } finally {
      setLoading(false)
    }
  }

  const downloadExport = async (format) => {
    try {
      const response = await fetch(`http://localhost:5000/api/export/${format}`)
      
      if (response.ok) {
        const blob = await response.blob()
        const url = window.URL.createObjectURL(blob)
        const a = document.createElement('a')
        a.style.display = 'none'
        a.href = url
        a.download = `cab_trips_${new Date().toISOString().split('T')[0]}.${format}`
        document.body.appendChild(a)
        a.click()
        window.URL.revokeObjectURL(url)
        document.body.removeChild(a)
      } else {
        alert('Export failed')
      }
    } catch (err) {
      alert('Export error: ' + err.message)
    }
  }

  const downloadJSON = async () => {
    try {
      const response = await fetch('http://localhost:5000/api/export/json')
      if (response.ok) {
        const data = await response.json()
        const blob = new Blob([JSON.stringify(data, null, 2)], { type: 'application/json' })
        const url = window.URL.createObjectURL(blob)
        const a = document.createElement('a')
        a.href = url
        a.download = `cab_trips_${new Date().toISOString().split('T')[0]}.json`
        document.body.appendChild(a)
        a.click()
        window.URL.revokeObjectURL(url)
        document.body.removeChild(a)
      }
    } catch (err) {
      alert('JSON export error: ' + err.message)
    }
  }

  if (loading) {
    return (
      <div className="analytics-container">
        <div className="loading-state">
          <h2>📊 Loading Advanced Analytics...</h2>
          <p>Crunching your trip data with pandas...</p>
        </div>
      </div>
    )
  }

  if (error) {
    return (
      <div className="analytics-container">
        <div className="error-state">
          <h2>❌ Analytics Error</h2>
          <p>{error}</p>
          <button className="btn btn-primary" onClick={fetchAnalytics}>
            Retry
          </button>
        </div>
      </div>
    )
  }

  if (!analytics || analytics.total_trips === 0) {
    return (
      <div className="analytics-container">
        <div className="empty-state">
          <h2>📈 No Data for Analytics</h2>
          <p>Add some trips to see powerful pandas-driven analytics here.</p>
        </div>
      </div>
    )
  }

  const StatBlock = ({ title, value, subtitle, icon, color = '#3b82f6' }) => (
    <div className="stat-block" style={{ borderColor: color }}>
      <div className="stat-icon" style={{ color }}>{icon}</div>
      <div className="stat-content">
        <h4>{title}</h4>
        <div className="stat-main-value">{value}</div>
        {subtitle && <div className="stat-subtitle">{subtitle}</div>}
      </div>
    </div>
  )

  return (
    <div className="analytics-container">
      <div className="analytics-header">
        <h2>📊 Advanced Analytics</h2>
        <p>Powered by pandas, numpy, and advanced data science</p>
        
        <div className="export-buttons">
          <button className="btn btn-secondary" onClick={() => downloadExport('csv')}>
            📄 Export CSV
          </button>
          <button className="btn btn-secondary" onClick={() => downloadExport('excel')}>
            📊 Export Excel
          </button>
          <button className="btn btn-secondary" onClick={downloadJSON}>
            📋 Export JSON
          </button>
          <button className="btn btn-primary" onClick={fetchAnalytics}>
            🔄 Refresh
          </button>
        </div>
      </div>

      {/* Fare Statistics */}
      {analytics.fare_statistics && (
        <div className="analytics-section">
          <h3>💰 Fare Statistics (Pandas Analytics)</h3>
          <div className="stats-grid">
            <StatBlock
              title="Mean Fare"
              value={`₹${analytics.fare_statistics.mean.toFixed(2)}`}
              icon="📊"
              color="#10b981"
            />
            <StatBlock
              title="Median Fare"
              value={`₹${analytics.fare_statistics.median.toFixed(2)}`}
              icon="📈"
              color="#f59e0b"
            />
            <StatBlock
              title="Standard Deviation"
              value={`₹${analytics.fare_statistics.std.toFixed(2)}`}
              subtitle="Fare Variability"
              icon="📏"
              color="#8b5cf6"
            />
            <StatBlock
              title="Fare Range"
              value={`₹${analytics.fare_statistics.min.toFixed(2)} - ₹${analytics.fare_statistics.max.toFixed(2)}`}
              icon="📋"
              color="#ef4444"
            />
          </div>
          
          <div className="quartile-info">
            <h4>Quartile Analysis</h4>
            <div className="quartile-bars">
              <div className="quartile-item">
                <span>25th Percentile</span>
                <span>₹{analytics.fare_statistics.q25.toFixed(2)}</span>
              </div>
              <div className="quartile-item">
                <span>75th Percentile</span>
                <span>₹{analytics.fare_statistics.q75.toFixed(2)}</span>
              </div>
            </div>
          </div>
        </div>
      )}

      {/* Advanced Analytics */}
      {advancedAnalytics && (
        <>
          {/* Peak Hours Analysis */}
          {advancedAnalytics.peak_hours && (
            <div className="analytics-section">
              <h3>⏰ Peak Hours Analysis</h3>
              <div className="peak-hours-grid">
                <div className="peak-card morning">
                  <h4>🌅 Morning Peak (6-9 AM)</h4>
                  <div className="peak-value">{advancedAnalytics.peak_hours.morning_peak} trips</div>
                </div>
                <div className="peak-card evening">
                  <h4>🌆 Evening Peak (6-9 PM)</h4>
                  <div className="peak-value">{advancedAnalytics.peak_hours.evening_peak} trips</div>
                </div>
                <div className="peak-card off-peak">
                  <h4>😴 Off-Peak Hours</h4>
                  <div className="peak-value">{advancedAnalytics.peak_hours.off_peak} trips</div>
                </div>
              </div>
            </div>
          )}

          {/* Weekend vs Weekday */}
          {advancedAnalytics.weekend_vs_weekday && (
            <div className="analytics-section">
              <h3>📅 Weekend vs Weekday Analysis</h3>
              <div className="comparison-grid">
                <div className="comparison-card">
                  <h4>🗓️ Weekday Trips</h4>
                  <div className="comparison-stats">
                    <div>Count: {advancedAnalytics.weekend_vs_weekday.weekday.count}</div>
                    <div>Total: ₹{advancedAnalytics.weekend_vs_weekday.weekday.total_fare.toFixed(2)}</div>
                    <div>Average: ₹{advancedAnalytics.weekend_vs_weekday.weekday.avg_fare.toFixed(2)}</div>
                  </div>
                </div>
                <div className="comparison-card">
                  <h4>🎉 Weekend Trips</h4>
                  <div className="comparison-stats">
                    <div>Count: {advancedAnalytics.weekend_vs_weekday.weekend.count}</div>
                    <div>Total: ₹{advancedAnalytics.weekend_vs_weekday.weekend.total_fare.toFixed(2)}</div>
                    <div>Average: ₹{advancedAnalytics.weekend_vs_weekday.weekend.avg_fare.toFixed(2)}</div>
                  </div>
                </div>
              </div>
            </div>
          )}

          {/* Correlation Analysis */}
          {advancedAnalytics.correlations && (
            <div className="analytics-section">
              <h3>🔗 Correlation Analysis</h3>
              <div className="correlation-grid">
                <div className="correlation-item">
                  <span>Distance ↔ Time</span>
                  <span className={`correlation-value ${Math.abs(advancedAnalytics.correlations.distance_time) > 0.7 ? 'strong' : 'weak'}`}>
                    {advancedAnalytics.correlations.distance_time.toFixed(3)}
                  </span>
                </div>
                <div className="correlation-item">
                  <span>Distance ↔ Fare</span>
                  <span className={`correlation-value ${Math.abs(advancedAnalytics.correlations.distance_fare) > 0.7 ? 'strong' : 'weak'}`}>
                    {advancedAnalytics.correlations.distance_fare.toFixed(3)}
                  </span>
                </div>
                <div className="correlation-item">
                  <span>Time ↔ Fare</span>
                  <span className={`correlation-value ${Math.abs(advancedAnalytics.correlations.time_fare) > 0.7 ? 'strong' : 'weak'}`}>
                    {advancedAnalytics.correlations.time_fare.toFixed(3)}
                  </span>
                </div>
              </div>
            </div>
          )}

          {/* Efficiency Metrics */}
          {advancedAnalytics.efficiency_metrics && (
            <div className="analytics-section">
              <h3>⚡ Efficiency Metrics</h3>
              <div className="efficiency-grid">
                <StatBlock
                  title="Avg Fare per KM"
                  value={`₹${advancedAnalytics.efficiency_metrics.avg_fare_per_km.toFixed(2)}`}
                  icon="🛣️"
                  color="#06b6d4"
                />
                <StatBlock
                  title="Avg Fare per Minute"
                  value={`₹${advancedAnalytics.efficiency_metrics.avg_fare_per_minute.toFixed(2)}`}
                  icon="⏱️"
                  color="#84cc16"
                />
              </div>
            </div>
          )}
        </>
      )}

      {/* Data Distribution */}
      {analytics.traffic_analysis && (
        <div className="analytics-section">
          <h3>📈 Data Distribution</h3>
          <div className="distribution-grid">
            <div className="distribution-card">
              <h4>🚦 Traffic Distribution</h4>
              <div className="distribution-items">
                {Object.entries(analytics.traffic_analysis).map(([traffic, count]) => (
                  <div key={traffic} className="distribution-item">
                    <span>{traffic.charAt(0).toUpperCase() + traffic.slice(1)}</span>
                    <span className="count-badge">{count}</span>
                  </div>
                ))}
              </div>
            </div>
            
            {analytics.day_analysis && (
              <div className="distribution-card">
                <h4>📅 Day Distribution</h4>
                <div className="distribution-items">
                  {Object.entries(analytics.day_analysis).map(([day, count]) => (
                    <div key={day} className="distribution-item">
                      <span>{day.charAt(0).toUpperCase() + day.slice(1)}</span>
                      <span className="count-badge">{count}</span>
                    </div>
                  ))}
                </div>
              </div>
            )}
          </div>
        </div>
      )}
    </div>
  )
}

export default Analytics