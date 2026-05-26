import React, { useState, useEffect } from 'react'
import TripForm from './components/TripForm'
import TripHistory from './components/TripHistory'
import Dashboard from './components/Dashboard'
import PricingInfo from './components/PricingInfo'
import Analytics from './components/Analytics'
import './App.css'

const API_BASE_URL = 'http://localhost:5000/api'

function App() {
  const [activeTab, setActiveTab] = useState('calculator')
  const [trips, setTrips] = useState([])
  const [stats, setStats] = useState(null)
  const [loading, setLoading] = useState(false)

  // Fetch trips from backend
  const fetchTrips = async () => {
    try {
      const response = await fetch(`${API_BASE_URL}/trips`)
      if (response.ok) {
        const data = await response.json()
        setTrips(data.trips)
      }
    } catch (error) {
      console.error('Error fetching trips:', error)
    }
  }

  // Fetch statistics from backend
  const fetchStats = async () => {
    try {
      const response = await fetch(`${API_BASE_URL}/stats`)
      if (response.ok) {
        const data = await response.json()
        setStats(data)
      }
    } catch (error) {
      console.error('Error fetching stats:', error)
    }
  }

  // Add new trip
  const addTrip = async (tripData) => {
    setLoading(true)
    try {
      const response = await fetch(`${API_BASE_URL}/trips`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify(tripData),
      })

      if (response.ok) {
        const data = await response.json()
        await fetchTrips()
        await fetchStats()
        return data.trip
      } else {
        const error = await response.json()
        throw new Error(error.error || 'Failed to add trip')
      }
    } catch (error) {
      console.error('Error adding trip:', error)
      throw error
    } finally {
      setLoading(false)
    }
  }

  // Calculate fare without adding trip
  const calculateFare = async (tripData) => {
    try {
      const response = await fetch(`${API_BASE_URL}/calculate-fare`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify(tripData),
      })

      if (response.ok) {
        const data = await response.json()
        return data
      } else {
        const error = await response.json()
        throw new Error(error.error || 'Failed to calculate fare')
      }
    } catch (error) {
      console.error('Error calculating fare:', error)
      throw error
    }
  }

  // Load initial data
  useEffect(() => {
    fetchTrips()
    fetchStats()
  }, [])

  const TabButton = ({ id, label, isActive, onClick }) => (
    <button
      className={`tab-button ${isActive ? 'active' : ''}`}
      onClick={() => onClick(id)}
    >
      {label}
    </button>
  )

  return (
    <div className="app">
      <header className="app-header">
        <div className="header-content">
          <h1 className="app-title">
            🚕 Cab Fare Estimator
          </h1>
          <p className="app-subtitle">
            Calculate and track your cab fares with dynamic pricing
          </p>
        </div>
      </header>

      <nav className="tab-navigation">
        <div className="tab-container">
          <TabButton
            id="calculator"
            label="Fare Calculator"
            isActive={activeTab === 'calculator'}
            onClick={setActiveTab}
          />
          <TabButton
            id="history"
            label="Trip History"
            isActive={activeTab === 'history'}
            onClick={setActiveTab}
          />
          <TabButton
            id="analytics"
            label="Advanced Analytics"
            isActive={activeTab === 'analytics'}
            onClick={setActiveTab}
          />
          <TabButton
            id="dashboard"
            label="Dashboard"
            isActive={activeTab === 'dashboard'}
            onClick={setActiveTab}
          />
          <TabButton
            id="pricing"
            label="Pricing Info"
            isActive={activeTab === 'pricing'}
            onClick={setActiveTab}
          />
        </div>
      </nav>

      <main className="main-content">
        {activeTab === 'calculator' && (
          <TripForm
            onAddTrip={addTrip}
            onCalculateFare={calculateFare}
            loading={loading}
          />
        )}
        {activeTab === 'history' && (
          <TripHistory trips={trips} />
        )}
        {activeTab === 'analytics' && (
          <Analytics />
        )}
        {activeTab === 'dashboard' && (
          <Dashboard stats={stats} />
        )}
        {activeTab === 'pricing' && (
          <PricingInfo />
        )}
      </main>

      <footer className="app-footer">
        <p>&copy; 2024 Cab Fare Estimator. Built with React and Flask.</p>
      </footer>
    </div>
  )
}

export default App