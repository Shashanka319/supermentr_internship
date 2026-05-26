import React, { useState } from 'react'

const TripForm = ({ onAddTrip, onCalculateFare, loading }) => {
  const [formData, setFormData] = useState({
    distance: '',
    time: '',
    traffic: 'light',
    day: 'monday',
    start_hour: ''
  })
  
  const [calculatedFare, setCalculatedFare] = useState(null)
  const [error, setError] = useState('')

  const trafficOptions = [
    { value: 'light', label: 'Light Traffic' },
    { value: 'medium', label: 'Medium Traffic' },
    { value: 'heavy', label: 'Heavy Traffic' }
  ]

  const dayOptions = [
    { value: 'monday', label: 'Monday' },
    { value: 'tuesday', label: 'Tuesday' },
    { value: 'wednesday', label: 'Wednesday' },
    { value: 'thursday', label: 'Thursday' },
    { value: 'friday', label: 'Friday' },
    { value: 'saturday', label: 'Saturday' },
    { value: 'sunday', label: 'Sunday' }
  ]

  const handleInputChange = (e) => {
    const { name, value } = e.target
    setFormData(prev => ({
      ...prev,
      [name]: value
    }))
    setError('')
    setCalculatedFare(null)
  }

  const validateForm = () => {
    if (!formData.distance || formData.distance <= 0) {
      setError('Distance must be greater than 0')
      return false
    }
    if (!formData.time || formData.time <= 0) {
      setError('Time must be greater than 0')
      return false
    }
    if (!formData.start_hour || formData.start_hour < 0 || formData.start_hour > 23) {
      setError('Start hour must be between 0 and 23')
      return false
    }
    return true
  }

  const handleCalculate = async (e) => {
    e.preventDefault()
    
    if (!validateForm()) return

    try {
      const result = await onCalculateFare(formData)
      setCalculatedFare(result)
      setError('')
    } catch (err) {
      setError(err.message)
      setCalculatedFare(null)
    }
  }

  const handleAddTrip = async (e) => {
    e.preventDefault()
    
    if (!validateForm()) return

    try {
      await onAddTrip(formData)
      setFormData({
        distance: '',
        time: '',
        traffic: 'light',
        day: 'monday',
        start_hour: ''
      })
      setCalculatedFare(null)
      setError('')
      alert('Trip added successfully!')
    } catch (err) {
      setError(err.message)
    }
  }

  const FareBreakdown = ({ breakdown, fare }) => (
    <div className="fare-breakdown">
      <h3>Fare Breakdown</h3>
      <div className="breakdown-items">
        <div className="breakdown-item">
          <span>Base Fare:</span>
          <span>₹{breakdown.base_fare}</span>
        </div>
        <div className="breakdown-item">
          <span>Distance Charge:</span>
          <span>₹{breakdown.distance_charge.toFixed(2)}</span>
        </div>
        <div className="breakdown-item">
          <span>Time Charge:</span>
          <span>₹{breakdown.time_charge.toFixed(2)}</span>
        </div>
        <div className="breakdown-item">
          <span>Booking Fee:</span>
          <span>₹{breakdown.booking_fee}</span>
        </div>
        <div className="breakdown-item">
          <span>Traffic Multiplier:</span>
          <span>{breakdown.traffic_multiplier}x</span>
        </div>
        {breakdown.is_peak_hour && (
          <div className="breakdown-item surge">
            <span>Peak Hour Surge:</span>
            <span>+20%</span>
          </div>
        )}
        {breakdown.is_weekend && (
          <div className="breakdown-item surge">
            <span>Weekend Surge:</span>
            <span>+15%</span>
          </div>
        )}
        <div className="breakdown-total">
          <span>Total Fare:</span>
          <span>₹{fare}</span>
        </div>
      </div>
    </div>
  )

  return (
    <div className="trip-form-container">
      <div className="form-card">
        <h2>Calculate Cab Fare</h2>
        
        <form className="trip-form">
          <div className="form-row">
            <div className="form-group">
              <label htmlFor="distance">Distance (km)</label>
              <input
                type="number"
                id="distance"
                name="distance"
                value={formData.distance}
                onChange={handleInputChange}
                placeholder="Enter distance in kilometers"
                step="0.1"
                min="0"
                required
              />
            </div>
            
            <div className="form-group">
              <label htmlFor="time">Time (minutes)</label>
              <input
                type="number"
                id="time"
                name="time"
                value={formData.time}
                onChange={handleInputChange}
                placeholder="Enter time in minutes"
                min="1"
                required
              />
            </div>
          </div>

          <div className="form-row">
            <div className="form-group">
              <label htmlFor="traffic">Traffic Condition</label>
              <select
                id="traffic"
                name="traffic"
                value={formData.traffic}
                onChange={handleInputChange}
                required
              >
                {trafficOptions.map(option => (
                  <option key={option.value} value={option.value}>
                    {option.label}
                  </option>
                ))}
              </select>
            </div>
            
            <div className="form-group">
              <label htmlFor="day">Day of Week</label>
              <select
                id="day"
                name="day"
                value={formData.day}
                onChange={handleInputChange}
                required
              >
                {dayOptions.map(option => (
                  <option key={option.value} value={option.value}>
                    {option.label}
                  </option>
                ))}
              </select>
            </div>
          </div>

          <div className="form-row">
            <div className="form-group">
              <label htmlFor="start_hour">Start Hour (0-23)</label>
              <input
                type="number"
                id="start_hour"
                name="start_hour"
                value={formData.start_hour}
                onChange={handleInputChange}
                placeholder="Enter hour (24-hour format)"
                min="0"
                max="23"
                required
              />
            </div>
          </div>

          {error && (
            <div className="error-message">
              {error}
            </div>
          )}

          <div className="form-actions">
            <button
              type="button"
              className="btn btn-secondary"
              onClick={handleCalculate}
              disabled={loading}
            >
              Calculate Fare
            </button>
            
            <button
              type="button"
              className="btn btn-primary"
              onClick={handleAddTrip}
              disabled={loading || !calculatedFare}
            >
              {loading ? 'Adding...' : 'Add Trip'}
            </button>
          </div>
        </form>
      </div>

      {calculatedFare && (
        <div className="fare-result-card">
          <div className="fare-display">
            <h3>Estimated Fare</h3>
            <div className="fare-amount">₹{calculatedFare.fare}</div>
          </div>
          
          <FareBreakdown 
            breakdown={calculatedFare.breakdown} 
            fare={calculatedFare.fare} 
          />
        </div>
      )}
    </div>
  )
}

export default TripForm