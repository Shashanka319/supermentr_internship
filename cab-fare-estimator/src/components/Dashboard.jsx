import React from 'react'

const Dashboard = ({ stats }) => {
  if (!stats) {
    return (
      <div className="dashboard-container">
        <div className="loading-state">
          <h2>Loading Dashboard...</h2>
          <p>Fetching your trip statistics...</p>
        </div>
      </div>
    )
  }

  if (stats.total_trips === 0) {
    return (
      <div className="dashboard-container">
        <div className="empty-state">
          <h2>No Data Available</h2>
          <p>Add some trips to see your statistics here.</p>
        </div>
      </div>
    )
  }

  const formatCurrency = (amount) => `₹${amount.toFixed(2)}`

  const StatCard = ({ title, value, icon, color = '#3b82f6' }) => (
    <div className="stat-card" style={{ borderColor: color }}>
      <div className="stat-icon" style={{ color }}>
        {icon}
      </div>
      <div className="stat-content">
        <h3>{title}</h3>
        <div className="stat-value">{value}</div>
      </div>
    </div>
  )

  const TrafficBreakdown = ({ tripsByTraffic }) => (
    <div className="traffic-breakdown">
      <h3>Trips by Traffic Condition</h3>
      <div className="traffic-items">
        {Object.entries(tripsByTraffic).map(([traffic, trips]) => {
          const totalFare = trips.reduce((sum, trip) => sum + trip.fare, 0)
          const getColor = (traffic) => {
            switch (traffic) {
              case 'light': return '#22c55e'
              case 'medium': return '#f59e0b'
              case 'heavy': return '#ef4444'
              default: return '#6b7280'
            }
          }
          
          return (
            <div key={traffic} className="traffic-item">
              <div className="traffic-header">
                <span 
                  className="traffic-dot" 
                  style={{ backgroundColor: getColor(traffic) }}
                ></span>
                <span className="traffic-name">
                  {traffic.charAt(0).toUpperCase() + traffic.slice(1)} Traffic
                </span>
              </div>
              <div className="traffic-stats">
                <span>{trips.length} trips</span>
                <span>{formatCurrency(totalFare)}</span>
              </div>
            </div>
          )
        })}
      </div>
    </div>
  )

  const ExtremeFares = ({ highest, lowest }) => (
    <div className="extreme-fares">
      <h3>Fare Extremes</h3>
      
      {highest && (
        <div className="extreme-fare highest">
          <h4>🏆 Highest Fare</h4>
          <div className="fare-amount">{formatCurrency(highest.fare)}</div>
          <div className="fare-details">
            <span>{highest.distance} km • {highest.time} min</span>
            <span>{highest.traffic} traffic • {highest.day}</span>
          </div>
        </div>
      )}
      
      {lowest && (
        <div className="extreme-fare lowest">
          <h4>💰 Lowest Fare</h4>
          <div className="fare-amount">{formatCurrency(lowest.fare)}</div>
          <div className="fare-details">
            <span>{lowest.distance} km • {lowest.time} min</span>
            <span>{lowest.traffic} traffic • {lowest.day}</span>
          </div>
        </div>
      )}
    </div>
  )

  return (
    <div className="dashboard-container">
      <div className="dashboard-header">
        <h2>Dashboard</h2>
        <p>Overview of your trip statistics</p>
      </div>

      <div className="stats-grid">
        <StatCard
          title="Total Trips"
          value={stats.total_trips}
          icon="🚗"
          color="#3b82f6"
        />
        
        <StatCard
          title="Total Earnings"
          value={formatCurrency(stats.total_earnings)}
          icon="💰"
          color="#10b981"
        />
        
        <StatCard
          title="Average Fare"
          value={formatCurrency(stats.average_fare)}
          icon="📊"
          color="#f59e0b"
        />
        
        <StatCard
          title="Trip Categories"
          value={Object.keys(stats.trips_by_traffic).length}
          icon="🚦"
          color="#8b5cf6"
        />
      </div>

      <div className="dashboard-details">
        <div className="dashboard-section">
          <TrafficBreakdown tripsByTraffic={stats.trips_by_traffic} />
        </div>
        
        <div className="dashboard-section">
          <ExtremeFares 
            highest={stats.highest_fare_trip} 
            lowest={stats.lowest_fare_trip} 
          />
        </div>
      </div>
    </div>
  )
}

export default Dashboard