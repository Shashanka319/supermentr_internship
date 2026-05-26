from dataclasses import dataclass
from typing import List, Dict, Optional
from enum import Enum


class TrafficCondition(Enum):
    """Enum for traffic conditions"""
    LIGHT = "light"
    MEDIUM = "medium"
    HEAVY = "heavy"


class DayOfWeek(Enum):
    """Enum for days of the week"""
    MONDAY = "monday"
    TUESDAY = "tuesday"
    WEDNESDAY = "wednesday"
    THURSDAY = "thursday"
    FRIDAY = "friday"
    SATURDAY = "saturday"
    SUNDAY = "sunday"


@dataclass
class Trip:
    """Represents a single cab ride with all trip details"""
    distance: float
    time: int
    traffic: str
    day: str
    start_hour: int
    fare: float = 0.0
    
    def to_dict(self) -> Dict:
        """Convert trip to dictionary format"""
        return {
            'distance': self.distance,
            'time': self.time,
            'traffic': self.traffic,
            'day': self.day,
            'start_hour': self.start_hour,
            'fare': self.fare
        }


class FareCalculator:
    """Handles fare calculation logic with dynamic pricing rules"""
    
    BASE_FARE = 50
    PER_KM_RATE = 10
    PER_MINUTE_RATE = 2
    BOOKING_FEE = 20
    
    TRAFFIC_MULTIPLIERS = {
        'light': 1.0,
        'medium': 1.10,
        'heavy': 1.25
    }
    
    PEAK_HOURS = [(6, 9), (18, 21)]
    PEAK_HOUR_SURGE = 0.20
    
    WEEKEND_DAYS = ['saturday', 'sunday']
    WEEKEND_SURGE = 0.15
    
    def calculate_fare(self, trip: Trip) -> float:
        """
        Calculate fare for a trip based on distance, time, and dynamic pricing rules
        
        Args:
            trip: Trip object containing all trip details
            
        Returns:
            Calculated fare amount
        """
        base_amount = self.BASE_FARE
        distance_charge = trip.distance * self.PER_KM_RATE
        time_charge = trip.time * self.PER_MINUTE_RATE
        booking_fee = self.BOOKING_FEE
        
        subtotal = base_amount + distance_charge + time_charge + booking_fee
        
        traffic_multiplier = self.TRAFFIC_MULTIPLIERS.get(trip.traffic.lower(), 1.0)
        subtotal *= traffic_multiplier
        
        is_peak_hour = any(start <= trip.start_hour < end for start, end in self.PEAK_HOURS)
        if is_peak_hour:
            subtotal *= (1 + self.PEAK_HOUR_SURGE)
        
        is_weekend = trip.day.lower() in self.WEEKEND_DAYS
        if is_weekend:
            subtotal *= (1 + self.WEEKEND_SURGE)
        
        return round(subtotal, 2)


class CabSystem:
    """Manages multiple trips, stores records, and generates reports"""
    
    def __init__(self):
        self.trips: List[Trip] = []
        self.fare_calculator = FareCalculator()
    
    def add_trip(self, distance: float, time: int, traffic: str, day: str, start_hour: int) -> Trip:
        """
        Add a new trip to the system
        
        Args:
            distance: Distance traveled in kilometers
            time: Time taken in minutes
            traffic: Traffic condition (light/medium/heavy)
            day: Day of the week
            start_hour: Trip start hour (0-23)
            
        Returns:
            Created Trip object with calculated fare
        """
        trip = Trip(
            distance=distance,
            time=time,
            traffic=traffic.lower(),
            day=day.lower(),
            start_hour=start_hour
        )
        
        trip.fare = self.fare_calculator.calculate_fare(trip)
        self.trips.append(trip)
        
        return trip
    
    def get_total_earnings(self) -> float:
        """Calculate total earnings from all trips"""
        return sum(trip.fare for trip in self.trips)
    
    def get_average_fare(self) -> float:
        """Calculate average fare per trip"""
        if not self.trips:
            return 0.0
        return self.get_total_earnings() / len(self.trips)
    
    def get_trips_by_traffic(self) -> Dict[str, List[Trip]]:
        """Categorize trips by traffic condition"""
        categorized = {
            'light': [],
            'medium': [],
            'heavy': []
        }
        
        for trip in self.trips:
            traffic_key = trip.traffic.lower()
            if traffic_key in categorized:
                categorized[traffic_key].append(trip)
        
        return categorized
    
    def get_highest_fare_trip(self) -> Optional[Trip]:
        """Get the trip with the highest fare"""
        if not self.trips:
            return None
        return max(self.trips, key=lambda t: t.fare)
    
    def get_lowest_fare_trip(self) -> Optional[Trip]:
        """Get the trip with the lowest fare"""
        if not self.trips:
            return None
        return min(self.trips, key=lambda t: t.fare)
    
    def generate_report(self) -> str:
        """Generate comprehensive report of all trips and statistics"""
        if not self.trips:
            return "No trips recorded yet."
        
        report_lines = []
        report_lines.append("=" * 70)
        report_lines.append("CAB FARE ESTIMATOR - COMPREHENSIVE REPORT".center(70))
        report_lines.append("=" * 70)
        report_lines.append("")
        
        report_lines.append(f"Total Trips: {len(self.trips)}")
        report_lines.append(f"Total Earnings: ₹{self.get_total_earnings():.2f}")
        report_lines.append(f"Average Fare per Trip: ₹{self.get_average_fare():.2f}")
        report_lines.append("")
        
        report_lines.append("-" * 70)
        report_lines.append("TRIPS BY TRAFFIC CONDITION")
        report_lines.append("-" * 70)
        
        trips_by_traffic = self.get_trips_by_traffic()
        for traffic_type, trips in trips_by_traffic.items():
            count = len(trips)
            total_fare = sum(t.fare for t in trips)
            report_lines.append(f"{traffic_type.upper()}: {count} trips | Total Fare: ₹{total_fare:.2f}")
        
        report_lines.append("")
        report_lines.append("-" * 70)
        report_lines.append("HIGHEST AND LOWEST FARE TRIPS")
        report_lines.append("-" * 70)
        
        highest = self.get_highest_fare_trip()
        if highest:
            report_lines.append(f"HIGHEST FARE: ₹{highest.fare:.2f}")
            report_lines.append(f"  Distance: {highest.distance} km | Time: {highest.time} min")
            report_lines.append(f"  Traffic: {highest.traffic} | Day: {highest.day} | Hour: {highest.start_hour}")
        
        report_lines.append("")
        
        lowest = self.get_lowest_fare_trip()
        if lowest:
            report_lines.append(f"LOWEST FARE: ₹{lowest.fare:.2f}")
            report_lines.append(f"  Distance: {lowest.distance} km | Time: {lowest.time} min")
            report_lines.append(f"  Traffic: {lowest.traffic} | Day: {lowest.day} | Hour: {lowest.start_hour}")
        
        report_lines.append("")
        report_lines.append("-" * 70)
        report_lines.append("ALL TRIP DETAILS")
        report_lines.append("-" * 70)
        
        for i, trip in enumerate(self.trips, 1):
            report_lines.append(f"Trip #{i}:")
            report_lines.append(f"  Distance: {trip.distance} km | Time: {trip.time} min | Fare: ₹{trip.fare:.2f}")
            report_lines.append(f"  Traffic: {trip.traffic} | Day: {trip.day} | Start Hour: {trip.start_hour}")
            report_lines.append("")
        
        report_lines.append("=" * 70)
        
        return "\n".join(report_lines)


def display_menu():
    """Display the main menu"""
    print("\n" + "=" * 70)
    print("CAB FARE ESTIMATOR SYSTEM".center(70))
    print("=" * 70)
    print("\n1. Add New Trip")
    print("2. View All Trips")
    print("3. Generate Report")
    print("4. Exit")
    print("-" * 70)


def get_float_input(prompt: str) -> float:
    """Get validated float input from user"""
    while True:
        try:
            value = float(input(prompt))
            if value < 0:
                print("Please enter a positive number.")
                continue
            return value
        except ValueError:
            print("Invalid input. Please enter a valid number.")


def get_int_input(prompt: str, min_val: Optional[int] = None, max_val: Optional[int] = None) -> int:
    """Get validated integer input from user"""
    while True:
        try:
            value = int(input(prompt))
            if min_val is not None and value < min_val:
                print(f"Please enter a value >= {min_val}.")
                continue
            if max_val is not None and value > max_val:
                print(f"Please enter a value <= {max_val}.")
                continue
            return value
        except ValueError:
            print("Invalid input. Please enter a valid integer.")


def get_traffic_input() -> str:
    """Get validated traffic condition input"""
    while True:
        traffic = input("Traffic Condition (light/medium/heavy): ").strip().lower()
        if traffic in ['light', 'medium', 'heavy']:
            return traffic
        print("Invalid input. Please enter 'light', 'medium', or 'heavy'.")


def get_day_input() -> str:
    """Get validated day of week input"""
    valid_days = ['monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday']
    while True:
        day = input("Day of the Week (e.g., Monday, Saturday): ").strip().lower()
        if day in valid_days:
            return day
        print(f"Invalid input. Please enter a valid day: {', '.join(valid_days)}")


def add_new_trip(cab_system: CabSystem):
    """Handle adding a new trip"""
    print("\n" + "-" * 70)
    print("ADD NEW TRIP".center(70))
    print("-" * 70)
    
    distance = get_float_input("Enter Distance (km): ")
    time = get_int_input("Enter Time (minutes): ", min_val=0)
    traffic = get_traffic_input()
    day = get_day_input()
    start_hour = get_int_input("Enter Start Hour (0-23): ", min_val=0, max_val=23)
    
    trip = cab_system.add_trip(distance, time, traffic, day, start_hour)
    
    print("\n" + "=" * 70)
    print("TRIP ADDED SUCCESSFULLY!".center(70))
    print("=" * 70)
    print(f"\nTrip Details:")
    print(f"  Distance: {trip.distance} km")
    print(f"  Time: {trip.time} minutes")
    print(f"  Traffic: {trip.traffic}")
    print(f"  Day: {trip.day}")
    print(f"  Start Hour: {trip.start_hour}")
    print(f"\n  CALCULATED FARE: ₹{trip.fare:.2f}")
    print("=" * 70)


def view_all_trips(cab_system: CabSystem):
    """Display all recorded trips"""
    if not cab_system.trips:
        print("\nNo trips recorded yet.")
        return
    
    print("\n" + "=" * 70)
    print("ALL RECORDED TRIPS".center(70))
    print("=" * 70)
    
    for i, trip in enumerate(cab_system.trips, 1):
        print(f"\nTrip #{i}:")
        print(f"  Distance: {trip.distance} km | Time: {trip.time} min | Fare: ₹{trip.fare:.2f}")
        print(f"  Traffic: {trip.traffic} | Day: {trip.day} | Start Hour: {trip.start_hour}")
    
    print("\n" + "=" * 70)


def main():
    """Main application entry point"""
    cab_system = CabSystem()
    
    print("\n" + "=" * 70)
    print("WELCOME TO CAB FARE ESTIMATOR".center(70))
    print("=" * 70)
    print("\nThis system calculates cab fares based on:")
    print("  • Base Fare: ₹50")
    print("  • Per Kilometer: ₹10/km")
    print("  • Per Minute: ₹2/min")
    print("  • Booking Fee: ₹20")
    print("\nDynamic Pricing:")
    print("  • Traffic: Light (normal) | Medium (+10%) | Heavy (+25%)")
    print("  • Peak Hours (6-9 AM, 6-9 PM): +20% surge")
    print("  • Weekend (Sat/Sun): +15% extra")
    
    while True:
        display_menu()
        choice = input("Enter your choice (1-4): ").strip()
        
        if choice == '1':
            add_new_trip(cab_system)
        elif choice == '2':
            view_all_trips(cab_system)
        elif choice == '3':
            report = cab_system.generate_report()
            print("\n" + report)
        elif choice == '4':
            print("\n" + "=" * 70)
            print("Thank you for using Cab Fare Estimator!".center(70))
            print("=" * 70)
            break
        else:
            print("\nInvalid choice. Please enter a number between 1 and 4.")


if __name__ == "__main__":
    main()
