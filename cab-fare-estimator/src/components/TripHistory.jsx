import React from 'react'

const TripHistory = ({ trips }) => {
  if (!trips || trips.length === 0) {
    return (
      <div className="trip-history-container">
        <div className="empty-state">
          <h2>No Trips Yet</h2>
          <p>Start by adding your first trip using the Fare Calculator.</p>
        </div>
      </div>
    )
  }

  const formatDay = (day) => {
    return day.charAt(0).toUpperCase() + day.slice(1)
  }

  const formatTraffic = (traffic) => {
    return traffic.charAt(0).toUpperCase() + traffic.slice(1)
  }

  const formatTime = (hour) => {
    if (hour === 0) return '12:00 AM'
    if (hour < 12) return `${hour}:00 AM`
    if (hour === 12) return '12:00 PM'
    return `${hour - 12}:00 PM`
  }

  const getTrafficColor = (traffic) => {
    switch (traffic.toLowerCase()) {
      case 'light': return '#22c55e'
      case 'medium': return '#f59e0b'
      case 'heavy': return '#ef4444'
      default: return '#6b7280'
    }
  }

  return (
    <div className="trip-history-container">
      <div className="history-header">
        <h2>Trip History</h2>
        <div className="trip-count">
          Total Trips: {trips.length}
        </div>
      </div>

      <div className="trips-grid">
        {trips.map((trip, index) => (
          <div key={trip.id || index} className="trip-card">
            <div className="trip-header">
              <h3>Trip #{trip.id || index + 1}</h3>
              <div className="fare-badge">₹{trip.fare}</div>
            </div>
            
            <div className="trip-details">
              <div className="detail-row">
                <div className="detail-item">
                  <span className="detail-label">📏 Distance:</span>
                  <span className="detail-value">{trip.distance} km</span>
                </div>
                <div className="detail-item">
                  <span className="detail-label">⏱️ Time:</span>
                  <span className="detail-value">{trip.time} min</span>
                </div>
              </div>
              
              <div className="detail-row">
                <div className="detail-item">
                  <span className="detail-label">🚦 Traffic:</span>
                  <span 
                    className="detail-value traffic-badge"
                    style={{ color: getTrafficColor(trip.traffic) }}
                  >
                    {formatTraffic(trip.traffic)}
                  </span>
                </div>
                <div className="detail-item">
                  <span className="detail-label">📅 Day:</span>
                  <span className="detail-value">{formatDay(trip.day)}</span>
                </div>
              </div>
              
              <div className="detail-row">
                <div className="detail-item">
                  <span className="detail-label">🕐 Start Time:</span>
                  <span className="detail-value">{formatTime(trip.start_hour)}</span>
                </div>
                <div className="detail-item">
                  <span className="detail-label">💰 Fare:</span>
                  <span className="detail-value fare-highlight">₹{trip.fare}</span>
                </div>
              </div>
            </div>
          </div>
        ))}
      </div>
    </div>
  )
}

export default TripHistory