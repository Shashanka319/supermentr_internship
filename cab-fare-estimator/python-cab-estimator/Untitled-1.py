#!/usr/bin/env python3
"""
🚕 Cab Fare Estimator - No Authentication Version
===============================================
A simple command-line cab fare estimation system without authentication.
Focuses purely on fare calculation, trip management, and reporting.
"""

import json
import os
from datetime import datetime
from typing import List, Dict, Optional


def clear_screen():
    """Clear console screen."""
    os.system('cls' if os.name == 'nt' else 'clear')


class Trip:
    """Represents a single cab ride."""

    def __init__(self, distance, time, traffic, day_of_week, start_time):
        self.distance = float(distance)
        self.time = int(time)
        self.traffic = traffic.lower()
        self.day_of_week = day_of_week.lower()
        self.start_time = int(start_time)
        self.fare = 0
        self.breakdown = {}
        self.timestamp = datetime.now()
        self.trip_id = f"TRIP_{int(self.timestamp.timestamp())}"


class FareCalculator:
    """Handles dynamic fare calculation."""

    def __init__(self):
        self.base_fare = 50
        self.per_km_rate = 10
        self.per_min_rate = 2
        self.booking_fee = 20

    def calculate_fare(self, trip):
        """Calculate fare with all surcharges."""
        fare = self.base_fare
        breakdown = {
            'base_fare': self.base_fare,
            'distance_fare': trip.distance * self.per_km_rate,
            'time_fare': trip.time * self.per_min_rate,
            'booking_fee': self.booking_fee,
            'traffic_multiplier': 1,
            'peak_multiplier': 1,
            'weekend_multiplier': 1
        }

        fare += breakdown['distance_fare'] + breakdown['time_fare'] + breakdown['booking_fee']

        # Traffic surcharge
        if trip.traffic == 'medium':
            breakdown['traffic_multiplier'] = 1.1
        elif trip.traffic == 'heavy':
            breakdown['traffic_multiplier'] = 1.25

        # Peak hours (6-9 AM, 6-9 PM)
        if (6 <= trip.start_time <= 9) or (18 <= trip.start_time <= 21):
            breakdown['peak_multiplier'] = 1.2

        # Weekend surcharge
        if trip.day_of_week in ['saturday', 'sunday']:
            breakdown['weekend_multiplier'] = 1.15

        # Apply multipliers
        fare *= breakdown['traffic_multiplier'] * breakdown['peak_multiplier'] * breakdown['weekend_multiplier']

        trip.fare = round(fare)
        trip.breakdown = breakdown
        return trip.fare


class CabSystem:
    """Manages trips and reports."""

    def __init__(self):
        self.trips = []
        self.fare_calculator = FareCalculator()

    def add_trip(self, distance, time, traffic, day_of_week, start_time):
        """Add new trip with fare calculation."""
        trip = Trip(distance, time, traffic, day_of_week, start_time)
        self.fare_calculator.calculate_fare(trip)
        self.trips.append(trip)
        return trip

    def get_total_earnings(self):
        return sum(trip.fare for trip in self.trips)

    def get_average_fare(self):
        return round(self.get_total_earnings() / len(self.trips)) if self.trips else 0

    def get_traffic_summary(self):
        summary = {'light': 0, 'medium': 0, 'heavy': 0}
        for trip in self.trips:
            summary[trip.traffic] += 1
        return summary

    def get_highest_fare(self):
        return max(trip.fare for trip in self.trips) if self.trips else 0

    def get_lowest_fare(self):
        return min(trip.fare for trip in self.trips) if self.trips else 0

    def clear_all_trips(self):
        self.trips = []

    def save_trips(self, filename='trips_data.json'):
        """Save trips to JSON file."""
        try:
            trips_data = []
            for trip in self.trips:
                trips_data.append({
                    'distance': trip.distance,
                    'time': trip.time,
                    'traffic': trip.traffic,
                    'day_of_week': trip.day_of_week,
                    'start_time': trip.start_time,
                    'fare': trip.fare,
                    'timestamp': trip.timestamp.isoformat()
                })

            with open(filename, 'w') as f:
                json.dump(trips_data, f, indent=2)
            print(f"✅ Trips saved to {filename}")
        except Exception as e:
            print(f"⚠️ Could not save trips: {e}")

    def load_trips(self, filename='trips_data.json'):
        """Load trips from JSON file."""
        if not os.path.exists(filename):
            return

        try:
            with open(filename, 'r') as f:
                trips_data = json.load(f)

            for trip_data in trips_data:
                trip = Trip(
                    trip_data['distance'],
                    trip_data['time'],
                    trip_data['traffic'],
                    trip_data['day_of_week'],
                    trip_data['start_time']
                )
                trip.fare = trip_data['fare']
                if 'timestamp' in trip_data:
                    trip.timestamp = datetime.fromisoformat(trip_data['timestamp'])
                self.trips.append(trip)

            print(f"✅ Loaded {len(trips_data)} trips from {filename}")
        except Exception as e:
            print(f"⚠️ Could not load trips: {e}")


class CabEstimatorApp:
    """Main application without authentication."""

    def __init__(self):
        self.cab_system = CabSystem()
        # Load previous trips if available
        self.cab_system.load_trips()

    def run(self):
        print("🚕 CAB FARE ESTIMATOR")
        print("=" * 50)
        print("💡 Simple version - No login required!")
        print("📊 All project requirements implemented")

        while True:
            try:
                self._main_menu()
            except KeyboardInterrupt:
                print("\n👋 Goodbye!")
                # Auto-save trips before exit
                self.cab_system.save_trips()
                break

    def _main_menu(self):
        print(f"\n📋 MAIN MENU")
        print("1. Book a Trip")
        print("2. View Reports")
        print("3. Trip History")
        print("4. Clear All Trips")
        print("5. Save Trips")
        print("6. Sample Data")
        print("7. Exit")

        choice = input("Choice (1-7): ").strip()

        if choice == '1':
            self._book_trip()
        elif choice == '2':
            self._show_reports()
        elif choice == '3':
            self._show_history()
        elif choice == '4':
            self._clear_trips()
        elif choice == '5':
            self.cab_system.save_trips()
        elif choice == '6':
            self._add_sample_data()
        elif choice == '7':
            print("👋 Thank you for using Cab Fare Estimator!")
            self.cab_system.save_trips()
            exit()
        else:
            print("❌ Invalid choice. Please try again.")

    def _book_trip(self):
        print("\n🚗 BOOK A NEW TRIP")
        print("=" * 30)

        try:
            # Get distance
            distance = float(input("Enter distance in kilometers: "))
            if distance <= 0:
                print("❌ Distance must be positive")
                return

            # Get time
            time = int(input("Enter time in minutes: "))
            if time <= 0:
                print("❌ Time must be positive")
                return

            # Get traffic condition
            print("\n🚦 Traffic Condition:")
            print("1. Light Traffic (Normal fare)")
            print("2. Medium Traffic (+10% surcharge)")
            print("3. Heavy Traffic (+25% surcharge)")

            traffic_choice = input("Choose traffic condition (1-3): ").strip()
            traffic_map = {'1': 'light', '2': 'medium', '3': 'heavy'}
            traffic = traffic_map.get(traffic_choice, 'light')

            # Get day of week
            print("\n📅 Day of Week:")
            print("1. Monday     2. Tuesday    3. Wednesday  4. Thursday")
            print("5. Friday     6. Saturday (+15% weekend surcharge)")
            print("7. Sunday (+15% weekend surcharge)")

            day_choice = input("Choose day (1-7): ").strip()
            days = ['monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday']

            if day_choice.isdigit() and 1 <= int(day_choice) <= 7:
                day = days[int(day_choice) - 1]
            else:
                day = 'monday'

            # Get start time
            start_time = int(input("\nEnter start hour (0-23, Peak: 6-9AM & 6-9PM +20%): "))
            if not 0 <= start_time <= 23:
                print("⚠️ Invalid hour, using 12 (noon)")
                start_time = 12

            # Calculate fare and add trip
            trip = self.cab_system.add_trip(distance, time, traffic, day, start_time)
            self._display_fare(trip)

        except ValueError as e:
            print(f"❌ Invalid input. Please enter valid numbers.")
        except Exception as e:
            print(f"❌ Error booking trip: {e}")

    def _display_fare(self, trip):
        print(f"\n💰 FARE CALCULATION BREAKDOWN")
        print("=" * 40)

        b = trip.breakdown

        # Basic charges
        print(f"Base Fare:              ₹{b['base_fare']}")
        print(f"Distance ({trip.distance}km × ₹10):   ₹{b['distance_fare']}")
        print(f"Time ({trip.time}min × ₹2):       ₹{b['time_fare']}")
        print(f"Booking Fee:            ₹{b['booking_fee']}")

        subtotal = b['base_fare'] + b['distance_fare'] + b['time_fare'] + b['booking_fee']
        print(f"Subtotal:               ₹{subtotal}")

        # Surcharges
        print("\n📈 SURCHARGES:")
        if b['traffic_multiplier'] > 1:
            surcharge_pct = (b['traffic_multiplier'] - 1) * 100
            print(f"Traffic ({trip.traffic.title()}):      +{surcharge_pct:.0f}%")

        if b['peak_multiplier'] > 1:
            surcharge_pct = (b['peak_multiplier'] - 1) * 100
            print(f"Peak Hour ({trip.start_time}:00):    +{surcharge_pct:.0f}%")

        if b['weekend_multiplier'] > 1:
            surcharge_pct = (b['weekend_multiplier'] - 1) * 100
            print(f"Weekend ({trip.day_of_week.title()}):     +{surcharge_pct:.0f}%")

        if b['traffic_multiplier'] == 1 and b['peak_multiplier'] == 1 and b['weekend_multiplier'] == 1:
            print("No surcharges applied")

        print("=" * 40)
        print(f"🎯 FINAL FARE:           ₹{trip.fare}")
        print("=" * 40)

        # Trip details
        print(f"\n📋 Trip Details:")
        print(f"Trip ID: {trip.trip_id}")
        print(f"Date: {trip.timestamp.strftime('%Y-%m-%d %H:%M:%S')}")

        input("\n Press Enter to continue...")

    def _show_reports(self):
        print(f"\n📊 COMPREHENSIVE REPORTS")
        print("=" * 40)

        if not self.cab_system.trips:
            print("❌ No trips recorded yet!")
            print("💡 Book some trips first to see reports")
            input("Press Enter to continue...")
            return

        # Summary statistics
        total_trips = len(self.cab_system.trips)
        total_earnings = self.cab_system.get_total_earnings()
        avg_fare = self.cab_system.get_average_fare()
        highest = self.cab_system.get_highest_fare()
        lowest = self.cab_system.get_lowest_fare()

        print(f"📈 EARNINGS SUMMARY:")
        print(f"Total Trips:            {total_trips}")
        print(f"Total Earnings:         ₹{total_earnings}")
        print(f"Average Fare:           ₹{avg_fare}")
        print(f"Highest Fare:           ₹{highest}")
        print(f"Lowest Fare:            ₹{lowest}")

        # Traffic analysis
        traffic_summary = self.cab_system.get_traffic_summary()
        print(f"\n🚦 TRAFFIC ANALYSIS:")
        print(f"Light Traffic:          {traffic_summary['light']} trips")
        print(f"Medium Traffic:         {traffic_summary['medium']} trips")
        print(f"Heavy Traffic:          {traffic_summary['heavy']} trips")

        # Additional analytics
        if self.cab_system.trips:
            total_distance = sum(trip.distance for trip in self.cab_system.trips)
            total_time = sum(trip.time for trip in self.cab_system.trips)
            avg_distance = total_distance / total_trips
            avg_time = total_time / total_trips

            print(f"\n📏 TRIP ANALYTICS:")
            print(f"Total Distance:         {total_distance:.1f} km")
            print(f"Total Time:             {total_time} minutes")
            print(f"Average Distance:       {avg_distance:.1f} km")
            print(f"Average Time:           {avg_time:.1f} minutes")

        input("\nPress Enter to continue...")

    def _show_history(self):
        print(f"\n📚 TRIP HISTORY")
        print("=" * 50)

        if not self.cab_system.trips:
            print("❌ No trips recorded yet!")
            input("Press Enter to continue...")
            return

        # Show all trips (latest first)
        trips_to_show = list(reversed(self.cab_system.trips))

        print(f"Showing {len(trips_to_show)} trips (most recent first):")
        print("-" * 50)

        for i, trip in enumerate(trips_to_show, 1):
            # Traffic emoji
            traffic_emoji = {
                'light': '🟢',
                'medium': '🟡',
                'heavy': '🔴'
            }[trip.traffic]

            # Day emoji
            day_emoji = '🏢' if trip.day_of_week in ['monday', 'tuesday', 'wednesday', 'thursday', 'friday'] else '🏖️'

            # Peak hour indicator
            peak_indicator = '⏰' if (6 <= trip.start_time <= 9) or (18 <= trip.start_time <= 21) else '  '

            print(f"{i:2d}. {trip.distance:5.1f}km | {trip.time:3d}min | {traffic_emoji}{trip.traffic:6s} | "
                  f"{day_emoji}{trip.day_of_week:9s} | {peak_indicator}{trip.start_time:2d}:00 | ₹{trip.fare:4d}")

        # Show data storage format as required
        print(f"\n💾 DATA STORAGE FORMAT (Project Requirement):")
        sample_data = []
        for trip in self.cab_system.trips[-3:]:  # Show last 3 trips
            sample_data.append({
                'distance': trip.distance,
                'time': trip.time,
                'traffic': trip.traffic,
                'fare': trip.fare
            })

        print("[")
        for trip_data in sample_data:
            print(f"  {trip_data},")
        print("]")

        input("\nPress Enter to continue...")

    def _clear_trips(self):
        if not self.cab_system.trips:
            print("❌ No trips to clear!")
            return

        confirm = input(
            f"\n⚠️  Are you sure you want to clear all {len(self.cab_system.trips)} trips? (yes/no): ").lower()

        if confirm == 'yes':
            self.cab_system.clear_all_trips()
            print("✅ All trips cleared!")
        else:
            print("❌ Operation cancelled")

    def _add_sample_data(self):
        """Add sample trips for testing and demonstration."""
        print("\n📊 ADDING SAMPLE DATA")
        print("=" * 30)

        sample_trips = [
            {'distance': 12, 'time': 20, 'traffic': 'heavy', 'day': 'monday', 'start_hour': 8},
            {'distance': 7, 'time': 12, 'traffic': 'medium', 'day': 'saturday', 'start_hour': 19},
            {'distance': 5, 'time': 15, 'traffic': 'light', 'day': 'wednesday', 'start_hour': 14},
            {'distance': 15, 'time': 25, 'traffic': 'heavy', 'day': 'sunday', 'start_hour': 7}
        ]

        print(f"Adding {len(sample_trips)} sample trips...")

        for trip_data in sample_trips:
            trip = self.cab_system.add_trip(
                distance=trip_data['distance'],
                time=trip_data['time'],
                traffic=trip_data['traffic'],
                day_of_week=trip_data['day'],
                start_time=trip_data['start_hour']
            )
            print(f"✅ Added: {trip.distance}km, {trip.time}min, {trip.traffic} → ₹{trip.fare}")

        print(f"\n🎉 Sample data added successfully!")
        print(f"💡 Now you can view reports and history to see the data")
        input("Press Enter to continue...")


if __name__ == "__main__":
    app = CabEstimatorApp()
    app.run()