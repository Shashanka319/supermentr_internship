import React, { useState, useEffect } from 'react'

const PricingInfo = () => {
  const [pricingData, setPricingData] = useState(null)
  const [loading, setLoading] = useState(true)

  useEffect(() => {
    const fetchPricingInfo = async () => {
      try {
        const response = await fetch('http://localhost:5000/api/pricing-info')
        if (response.ok) {
          const data = await response.json()
          setPricingData(data)
        }
      } catch (error) {
        console.error('Error fetching pricing info:', error)
      } finally {
        setLoading(false)
      }
    }

    fetchPricingInfo()
  }, [])

  if (loading) {
    return (
      <div className="pricing-container">
        <div className="loading-state">
          <h2>Loading Pricing Information...</h2>
        </div>
      </div>
    )
  }

  if (!pricingData) {
    return (
      <div className="pricing-container">
        <div className="error-state">
          <h2>Failed to Load Pricing Information</h2>
          <p>Please check if the backend server is running.</p>
        </div>
      </div>
    )
  }

  const PricingCard = ({ title, children, icon }) => (
    <div className="pricing-card">
      <div className="pricing-card-header">
        <span className="pricing-icon">{icon}</span>
        <h3>{title}</h3>
      </div>
      <div className="pricing-card-content">
        {children}
      </div>
    </div>
  )

  const PriceItem = ({ label, value, highlight = false }) => (
    <div className={`price-item ${highlight ? 'highlight' : ''}`}>
      <span className="price-label">{label}:</span>
      <span className="price-value">{value}</span>
    </div>
  )

  const formatHours = (hours) => {
    return hours.map(([start, end]) => {
      const formatHour = (hour) => {
        if (hour === 0) return '12 AM'
        if (hour < 12) return `${hour} AM`
        if (hour === 12) return '12 PM'
        return `${hour - 12} PM`
      }
      return `${formatHour(start)} - ${formatHour(end)}`
    }).join(', ')
  }

  return (
    <div className="pricing-container">
      <div className="pricing-header">
        <h2>Pricing Information</h2>
        <p>Understand how your cab fares are calculated</p>
      </div>

      <div className="pricing-grid">
        <PricingCard title="Base Rates" icon="💳">
          <PriceItem label="Base Fare" value={`₹${pricingData.base_fare}`} highlight />
          <PriceItem label="Per Kilometer" value={`₹${pricingData.per_km_rate}/km`} />
          <PriceItem label="Per Minute" value={`₹${pricingData.per_minute_rate}/min`} />
          <PriceItem label="Booking Fee" value={`₹${pricingData.booking_fee}`} />
        </PricingCard>

        <PricingCard title="Traffic Multipliers" icon="🚦">
          {Object.entries(pricingData.traffic_multipliers).map(([traffic, multiplier]) => (
            <PriceItem 
              key={traffic}
              label={traffic.charAt(0).toUpperCase() + traffic.slice(1)} 
              value={`${multiplier}x`}
              highlight={multiplier > 1}
            />
          ))}
        </PricingCard>

        <PricingCard title="Peak Hours" icon="⏰">
          <PriceItem 
            label="Peak Times" 
            value={formatHours(pricingData.peak_hours)} 
          />
          <PriceItem 
            label="Peak Hour Surge" 
            value={`+${(pricingData.peak_hour_surge * 100).toFixed(0)}%`} 
            highlight 
          />
        </PricingCard>

        <PricingCard title="Weekend Pricing" icon="🎉">
          <PriceItem 
            label="Weekend Days" 
            value={pricingData.weekend_days.map(day => 
              day.charAt(0).toUpperCase() + day.slice(1)
            ).join(', ')} 
          />
          <PriceItem 
            label="Weekend Surge" 
            value={`+${(pricingData.weekend_surge * 100).toFixed(0)}%`} 
            highlight 
          />
        </PricingCard>
      </div>

      <div className="pricing-example">
        <div className="example-card">
          <h3>💡 Example Calculation</h3>
          <div className="example-content">
            <p><strong>Trip Details:</strong> 10 km, 30 minutes, Heavy traffic, Friday 8 PM</p>
            
            <div className="calculation-steps">
              <div className="step">
                <span>Base Amount:</span>
                <span>₹{pricingData.base_fare} + ₹{pricingData.per_km_rate * 10} + ₹{pricingData.per_minute_rate * 30} + ₹{pricingData.booking_fee} = ₹{pricingData.base_fare + (pricingData.per_km_rate * 10) + (pricingData.per_minute_rate * 30) + pricingData.booking_fee}</span>
              </div>
              <div className="step">
                <span>Heavy Traffic (+25%):</span>
                <span>₹{pricingData.base_fare + (pricingData.per_km_rate * 10) + (pricingData.per_minute_rate * 30) + pricingData.booking_fee} × 1.25 = ₹{((pricingData.base_fare + (pricingData.per_km_rate * 10) + (pricingData.per_minute_rate * 30) + pricingData.booking_fee) * 1.25).toFixed(2)}</span>
              </div>
              <div className="step">
                <span>Peak Hour (+20%):</span>
                <span>₹{((pricingData.base_fare + (pricingData.per_km_rate * 10) + (pricingData.per_minute_rate * 30) + pricingData.booking_fee) * 1.25).toFixed(2)} × 1.20 = ₹{((pricingData.base_fare + (pricingData.per_km_rate * 10) + (pricingData.per_minute_rate * 30) + pricingData.booking_fee) * 1.25 * 1.20).toFixed(2)}</span>
              </div>
              <div className="step total">
                <span><strong>Final Fare:</strong></span>
                <span><strong>₹{((pricingData.base_fare + (pricingData.per_km_rate * 10) + (pricingData.per_minute_rate * 30) + pricingData.booking_fee) * 1.25 * 1.20).toFixed(2)}</strong></span>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  )
}

export default PricingInfo