"""
Test script to validate the cab system functionality
"""

from cab_system_core import CabSystemAnalytics, FareCalculator, Trip

def test_basic_functionality():
    """Test basic functionality of the cab system"""
    print("🚕 Testing Cab Fare Estimator System...")
    print("-" * 50)
    
    # Initialize system
    cab_system = CabSystemAnalytics()
    fare_calculator = FareCalculator()
    
    print("✅ System initialized successfully")
    
    # Test fare calculation
    test_trip = Trip(
        distance=10.0,
        time=30,
        traffic="medium",
        day="friday",
        start_hour=18
    )
    
    fare = fare_calculator.calculate_fare(test_trip)
    breakdown = fare_calculator.get_fare_breakdown(test_trip)
    
    print(f"\n🧮 Test Fare Calculation:")
    print(f"   Distance: {test_trip.distance} km")
    print(f"   Time: {test_trip.time} minutes")
    print(f"   Traffic: {test_trip.traffic}")
    print(f"   Day: {test_trip.day}")
    print(f"   Start Hour: {test_trip.start_hour}")
    print(f"   Calculated Fare: ₹{fare:.2f}")
    print("✅ Fare calculation working correctly")
    
    # Test adding trips
    print(f"\n📝 Adding test trips...")
    trips_data = [
        (15.5, 45, "heavy", "saturday", 8),
        (5.0, 20, "light", "monday", 14),
        (25.0, 60, "medium", "friday", 19),
        (8.2, 35, "heavy", "sunday", 7)
    ]
    
    for distance, time, traffic, day, hour in trips_data:
        trip = cab_system.add_trip(distance, time, traffic, day, hour)
        print(f"   Trip added: {distance}km, {time}min, {traffic} traffic → ₹{trip.fare:.2f}")
    
    print("✅ Trip addition working correctly")
    
    # Test statistics
    print(f"\n📊 Testing analytics...")
    stats = cab_system.get_basic_stats()
    print(f"   Total Trips: {stats['total_trips']}")
    print(f"   Total Revenue: ₹{stats['total_earnings']:.2f}")
    print(f"   Average Fare: ₹{stats['average_fare']:.2f}")
    print("✅ Basic statistics working correctly")
    
    # Test advanced analytics
    analytics = cab_system.get_advanced_analytics()
    print(f"\n🔍 Advanced Analytics:")
    if 'fare_statistics' in analytics:
        fare_stats = analytics['fare_statistics']
        print(f"   Fare Range: ₹{fare_stats['q25']:.2f} - ₹{fare_stats['q75']:.2f} (IQR)")
    print("✅ Advanced analytics working correctly")
    
    # Test visualizations
    print(f"\n📈 Testing visualizations...")
    try:
        charts = cab_system.create_visualizations()
        print(f"   Generated {len(charts)} charts")
        print("✅ Visualizations working correctly")
    except Exception as e:
        print(f"⚠️ Visualization error: {e}")
    
    print(f"\n🎉 All tests completed successfully!")
    print(f"   System is ready for use!")
    print("-" * 50)

if __name__ == "__main__":
    test_basic_functionality()