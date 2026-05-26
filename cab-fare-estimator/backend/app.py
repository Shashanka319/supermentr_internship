from flask import Flask, request, jsonify, send_file
from flask_cors import CORS
from dataclasses import dataclass, asdict
from typing import List, Dict, Optional
from enum import Enum
import json
import pandas as pd
import numpy as np
import matplotlib
matplotlib.use('Agg')  # Use non-interactive backend
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.graph_objects as go
import plotly.express as px
from plotly.utils import PlotlyJSONEncoder
from datetime import datetime, timedelta
import io
import base64
import os


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
    id: Optional[str] = None
    
    def to_dict(self) -> Dict:
        """Convert trip to dictionary format"""
        return {
            'id': self.id,
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
    """Manages multiple trips using pandas DataFrame for enhanced data analysis"""
    
    def __init__(self):
        self.fare_calculator = FareCalculator()
        self.next_id = 1
        # Initialize empty DataFrame with proper column types
        self.df = pd.DataFrame(columns=[
            'id', 'distance', 'time', 'traffic', 'day', 'start_hour', 'fare', 'created_at'
        ])
        # Set proper data types
        self.df = self.df.astype({
            'id': 'int64',
            'distance': 'float64',
            'time': 'int64',
            'traffic': 'object',
            'day': 'object',
            'start_hour': 'int64',
            'fare': 'float64',
            'created_at': 'datetime64[ns]'
        })
    
    def add_trip(self, distance: float, time: int, traffic: str, day: str, start_hour: int) -> Trip:
        """
        Add a new trip to the system using pandas DataFrame
        
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
            start_hour=start_hour,
            id=str(self.next_id)
        )
        
        trip.fare = self.fare_calculator.calculate_fare(trip)
        
        # Add to DataFrame
        new_row = pd.DataFrame([{
            'id': int(trip.id),
            'distance': trip.distance,
            'time': trip.time,
            'traffic': trip.traffic,
            'day': trip.day,
            'start_hour': trip.start_hour,
            'fare': trip.fare,
            'created_at': datetime.now()
        }])
        
        self.df = pd.concat([self.df, new_row], ignore_index=True)
        self.next_id += 1
        
        return trip
    
    @property
    def trips(self) -> List[Trip]:
        """Convert DataFrame back to Trip objects for compatibility"""
        trip_list = []
        for _, row in self.df.iterrows():
            trip = Trip(
                distance=row['distance'],
                time=row['time'],
                traffic=row['traffic'],
                day=row['day'],
                start_hour=row['start_hour'],
                fare=row['fare'],
                id=str(int(row['id']))
            )
            trip_list.append(trip)
        return trip_list
    
    def get_total_earnings(self) -> float:
        """Calculate total earnings from all trips using pandas"""
        if self.df.empty:
            return 0.0
        return float(self.df['fare'].sum())
    
    def get_average_fare(self) -> float:
        """Calculate average fare per trip using pandas"""
        if self.df.empty:
            return 0.0
        return float(self.df['fare'].mean())
    
    def get_trips_by_traffic(self) -> Dict[str, List[Dict]]:
        """Categorize trips by traffic condition using pandas"""
        if self.df.empty:
            return {'light': [], 'medium': [], 'heavy': []}
        
        categorized = {'light': [], 'medium': [], 'heavy': []}
        
        for traffic_type in ['light', 'medium', 'heavy']:
            traffic_df = self.df[self.df['traffic'] == traffic_type]
            trips_list = []
            for _, row in traffic_df.iterrows():
                trips_list.append({
                    'id': str(int(row['id'])),
                    'distance': row['distance'],
                    'time': row['time'],
                    'traffic': row['traffic'],
                    'day': row['day'],
                    'start_hour': row['start_hour'],
                    'fare': row['fare']
                })
            categorized[traffic_type] = trips_list
        
        return categorized
    
    def get_highest_fare_trip(self) -> Optional[Dict]:
        """Get the trip with the highest fare using pandas"""
        if self.df.empty:
            return None
        
        max_row = self.df.loc[self.df['fare'].idxmax()]
        return {
            'id': str(int(max_row['id'])),
            'distance': max_row['distance'],
            'time': max_row['time'],
            'traffic': max_row['traffic'],
            'day': max_row['day'],
            'start_hour': max_row['start_hour'],
            'fare': max_row['fare']
        }
    
    def get_lowest_fare_trip(self) -> Optional[Dict]:
        """Get the trip with the lowest fare using pandas"""
        if self.df.empty:
            return None
        
        min_row = self.df.loc[self.df['fare'].idxmin()]
        return {
            'id': str(int(min_row['id'])),
            'distance': min_row['distance'],
            'time': min_row['time'],
            'traffic': min_row['traffic'],
            'day': min_row['day'],
            'start_hour': min_row['start_hour'],
            'fare': min_row['fare']
        }
    
    def get_stats(self) -> Dict:
        """Get comprehensive statistics using pandas analytics"""
        basic_stats = {
            'total_trips': len(self.df),
            'total_earnings': self.get_total_earnings(),
            'average_fare': self.get_average_fare(),
            'trips_by_traffic': self.get_trips_by_traffic(),
            'highest_fare_trip': self.get_highest_fare_trip(),
            'lowest_fare_trip': self.get_lowest_fare_trip()
        }
        
        if not self.df.empty:
            # Add pandas-powered analytics
            basic_stats.update({
                'fare_statistics': {
                    'mean': float(self.df['fare'].mean()),
                    'median': float(self.df['fare'].median()),
                    'std': float(self.df['fare'].std()),
                    'min': float(self.df['fare'].min()),
                    'max': float(self.df['fare'].max()),
                    'q25': float(self.df['fare'].quantile(0.25)),
                    'q75': float(self.df['fare'].quantile(0.75))
                },
                'distance_statistics': {
                    'mean': float(self.df['distance'].mean()),
                    'median': float(self.df['distance'].median()),
                    'total': float(self.df['distance'].sum())
                },
                'time_statistics': {
                    'mean': float(self.df['time'].mean()),
                    'median': float(self.df['time'].median()),
                    'total': float(self.df['time'].sum())
                },
                'traffic_analysis': self.df['traffic'].value_counts().to_dict(),
                'day_analysis': self.df['day'].value_counts().to_dict(),
                'hour_analysis': self.df['start_hour'].value_counts().to_dict()
            })
        
        return basic_stats
    
    def export_to_csv(self) -> str:
        """Export trip data to CSV using pandas"""
        if self.df.empty:
            return None
        
        # Create a temporary CSV file
        csv_filename = f'trips_export_{datetime.now().strftime("%Y%m%d_%H%M%S")}.csv'
        csv_path = os.path.join('/tmp', csv_filename) if os.path.exists('/tmp') else csv_filename
        
        # Export DataFrame to CSV
        self.df.to_csv(csv_path, index=False)
        return csv_path
    
    def export_to_excel(self) -> str:
        """Export trip data to Excel using pandas"""
        if self.df.empty:
            return None
        
        # Create a temporary Excel file
        excel_filename = f'trips_export_{datetime.now().strftime("%Y%m%d_%H%M%S")}.xlsx'
        excel_path = os.path.join('/tmp', excel_filename) if os.path.exists('/tmp') else excel_filename
        
        # Export DataFrame to Excel with multiple sheets
        with pd.ExcelWriter(excel_path, engine='openpyxl') as writer:
            self.df.to_excel(writer, sheet_name='All Trips', index=False)
            
            # Create summary sheet
            summary_df = pd.DataFrame([
                {'Metric': 'Total Trips', 'Value': len(self.df)},
                {'Metric': 'Total Earnings', 'Value': self.df['fare'].sum()},
                {'Metric': 'Average Fare', 'Value': self.df['fare'].mean()},
                {'Metric': 'Total Distance', 'Value': self.df['distance'].sum()},
                {'Metric': 'Total Time', 'Value': self.df['time'].sum()}
            ])
            summary_df.to_excel(writer, sheet_name='Summary', index=False)
            
            # Traffic analysis sheet
            traffic_summary = self.df.groupby('traffic').agg({
                'fare': ['count', 'sum', 'mean'],
                'distance': 'sum',
                'time': 'sum'
            }).round(2)
            traffic_summary.to_excel(writer, sheet_name='Traffic Analysis')
        
        return excel_path
    
    def get_advanced_analytics(self) -> Dict:
        """Get advanced analytics using pandas and numpy"""
        if self.df.empty:
            return {}
        
        analytics = {}
        
        # Time-based analysis
        analytics['peak_hours'] = {
            'morning_peak': len(self.df[(self.df['start_hour'] >= 6) & (self.df['start_hour'] <= 9)]),
            'evening_peak': len(self.df[(self.df['start_hour'] >= 18) & (self.df['start_hour'] <= 21)]),
            'off_peak': len(self.df[~((self.df['start_hour'] >= 6) & (self.df['start_hour'] <= 9)) & 
                                  ~((self.df['start_hour'] >= 18) & (self.df['start_hour'] <= 21))])
        }
        
        # Weekend vs Weekday analysis
        weekend_trips = self.df[self.df['day'].isin(['saturday', 'sunday'])]
        weekday_trips = self.df[~self.df['day'].isin(['saturday', 'sunday'])]
        
        analytics['weekend_vs_weekday'] = {
            'weekend': {
                'count': len(weekend_trips),
                'total_fare': float(weekend_trips['fare'].sum()) if not weekend_trips.empty else 0,
                'avg_fare': float(weekend_trips['fare'].mean()) if not weekend_trips.empty else 0
            },
            'weekday': {
                'count': len(weekday_trips),
                'total_fare': float(weekday_trips['fare'].sum()) if not weekday_trips.empty else 0,
                'avg_fare': float(weekday_trips['fare'].mean()) if not weekday_trips.empty else 0
            }
        }
        
        # Distance and time correlation
        if len(self.df) > 1:
            correlation_matrix = self.df[['distance', 'time', 'fare']].corr()
            analytics['correlations'] = {
                'distance_time': float(correlation_matrix.loc['distance', 'time']),
                'distance_fare': float(correlation_matrix.loc['distance', 'fare']),
                'time_fare': float(correlation_matrix.loc['time', 'fare'])
            }
        
        # Efficiency metrics
        self.df['fare_per_km'] = self.df['fare'] / self.df['distance']
        self.df['fare_per_minute'] = self.df['fare'] / self.df['time']
        
        analytics['efficiency_metrics'] = {
            'avg_fare_per_km': float(self.df['fare_per_km'].mean()),
            'avg_fare_per_minute': float(self.df['fare_per_minute'].mean()),
            'most_efficient_trip': {
                'highest_fare_per_km': float(self.df['fare_per_km'].max()),
                'highest_fare_per_minute': float(self.df['fare_per_minute'].max())
            }
        }
        
        return analytics
    
    def generate_charts_data(self) -> Dict:
        """Generate data for various charts using plotly"""
        if self.df.empty:
            return {}
        
        charts_data = {}
        
        # Fare distribution histogram
        fig_hist = px.histogram(self.df, x='fare', nbins=20, title='Fare Distribution')
        charts_data['fare_histogram'] = json.loads(fig_hist.to_json())
        
        # Traffic vs Fare box plot
        fig_box = px.box(self.df, x='traffic', y='fare', title='Fare by Traffic Condition')
        charts_data['traffic_boxplot'] = json.loads(fig_box.to_json())
        
        # Day of week analysis
        day_stats = self.df.groupby('day')['fare'].agg(['count', 'mean']).reset_index()
        fig_day = px.bar(day_stats, x='day', y='count', title='Trips by Day of Week')
        charts_data['day_bar_chart'] = json.loads(fig_day.to_json())
        
        # Hour analysis
        hour_stats = self.df.groupby('start_hour')['fare'].agg(['count', 'mean']).reset_index()
        fig_hour = px.line(hour_stats, x='start_hour', y='count', title='Trips by Hour of Day')
        charts_data['hour_line_chart'] = json.loads(fig_hour.to_json())
        
        # Distance vs Fare scatter plot
        fig_scatter = px.scatter(self.df, x='distance', y='fare', color='traffic', 
                                title='Distance vs Fare (colored by traffic)')
        charts_data['distance_fare_scatter'] = json.loads(fig_scatter.to_json())
        
        return charts_data


# Initialize Flask app
app = Flask(__name__)
CORS(app)  # Enable CORS for all domains

# Global cab system instance
cab_system = CabSystem()


@app.route('/api/health', methods=['GET'])
def health_check():
    """Health check endpoint"""
    return jsonify({'status': 'healthy', 'message': 'Cab Fare Estimator API is running'})


@app.route('/api/calculate-fare', methods=['POST'])
def calculate_fare():
    """Calculate fare for a trip without adding it to the system"""
    try:
        data = request.json
        
        # Validate required fields
        required_fields = ['distance', 'time', 'traffic', 'day', 'start_hour']
        for field in required_fields:
            if field not in data:
                return jsonify({'error': f'Missing required field: {field}'}), 400
        
        # Create temporary trip for calculation
        temp_trip = Trip(
            distance=float(data['distance']),
            time=int(data['time']),
            traffic=data['traffic'].lower(),
            day=data['day'].lower(),
            start_hour=int(data['start_hour'])
        )
        
        # Calculate fare
        fare_calculator = FareCalculator()
        fare = fare_calculator.calculate_fare(temp_trip)
        
        # Prepare response with breakdown
        response = {
            'fare': fare,
            'breakdown': {
                'base_fare': fare_calculator.BASE_FARE,
                'distance_charge': temp_trip.distance * fare_calculator.PER_KM_RATE,
                'time_charge': temp_trip.time * fare_calculator.PER_MINUTE_RATE,
                'booking_fee': fare_calculator.BOOKING_FEE,
                'traffic_multiplier': fare_calculator.TRAFFIC_MULTIPLIERS.get(temp_trip.traffic, 1.0),
                'is_peak_hour': any(start <= temp_trip.start_hour < end for start, end in fare_calculator.PEAK_HOURS),
                'is_weekend': temp_trip.day in fare_calculator.WEEKEND_DAYS
            }
        }
        
        return jsonify(response)
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/api/trips', methods=['POST'])
def add_trip():
    """Add a new trip to the system"""
    try:
        data = request.json
        
        # Validate required fields
        required_fields = ['distance', 'time', 'traffic', 'day', 'start_hour']
        for field in required_fields:
            if field not in data:
                return jsonify({'error': f'Missing required field: {field}'}), 400
        
        # Add trip to system
        trip = cab_system.add_trip(
            distance=float(data['distance']),
            time=int(data['time']),
            traffic=data['traffic'],
            day=data['day'],
            start_hour=int(data['start_hour'])
        )
        
        return jsonify({
            'success': True,
            'trip': trip.to_dict(),
            'message': 'Trip added successfully'
        })
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/api/trips', methods=['GET'])
def get_trips():
    """Get all trips"""
    try:
        trips_data = [trip.to_dict() for trip in cab_system.trips]
        return jsonify({
            'trips': trips_data,
            'count': len(trips_data)
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/api/stats', methods=['GET'])
def get_stats():
    """Get comprehensive statistics"""
    try:
        stats = cab_system.get_stats()
        return jsonify(stats)
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/api/advanced-analytics', methods=['GET'])
def get_advanced_analytics():
    """Get advanced analytics and insights"""
    try:
        analytics = cab_system.get_advanced_analytics()
        return jsonify(analytics)
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/api/export/csv', methods=['GET'])
def export_csv():
    """Export trip data to CSV file"""
    try:
        csv_path = cab_system.export_to_csv()
        if csv_path is None:
            return jsonify({'error': 'No data to export'}), 400
        
        return send_file(csv_path, as_attachment=True, 
                        download_name=f'cab_trips_{datetime.now().strftime("%Y%m%d")}.csv')
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/api/export/excel', methods=['GET'])
def export_excel():
    """Export trip data to Excel file"""
    try:
        excel_path = cab_system.export_to_excel()
        if excel_path is None:
            return jsonify({'error': 'No data to export'}), 400
        
        return send_file(excel_path, as_attachment=True,
                        download_name=f'cab_trips_{datetime.now().strftime("%Y%m%d")}.xlsx')
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/api/export/json', methods=['GET'])
def export_json():
    """Export trip data as JSON"""
    try:
        if cab_system.df.empty:
            return jsonify({'error': 'No data to export'}), 400
        
        # Convert DataFrame to JSON with proper formatting
        trips_data = cab_system.df.to_dict('records')
        
        # Convert datetime objects to strings
        for trip in trips_data:
            if 'created_at' in trip and pd.notna(trip['created_at']):
                trip['created_at'] = trip['created_at'].isoformat()
        
        export_data = {
            'export_date': datetime.now().isoformat(),
            'total_trips': len(trips_data),
            'trips': trips_data,
            'summary': {
                'total_earnings': float(cab_system.df['fare'].sum()),
                'average_fare': float(cab_system.df['fare'].mean()),
                'total_distance': float(cab_system.df['distance'].sum()),
                'total_time': float(cab_system.df['time'].sum())
            }
        }
        
        return jsonify(export_data)
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/api/charts', methods=['GET'])
def get_charts():
    """Get chart data for visualizations"""
    try:
        charts_data = cab_system.generate_charts_data()
        return jsonify(charts_data)
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/api/data-analysis', methods=['GET'])
def get_data_analysis():
    """Get comprehensive data analysis"""
    try:
        if cab_system.df.empty:
            return jsonify({'message': 'No data available for analysis'})
        
        analysis = {
            'basic_stats': cab_system.get_stats(),
            'advanced_analytics': cab_system.get_advanced_analytics(),
            'data_quality': {
                'total_records': len(cab_system.df),
                'complete_records': len(cab_system.df.dropna()),
                'missing_values': cab_system.df.isnull().sum().to_dict(),
                'data_types': cab_system.df.dtypes.astype(str).to_dict()
            }
        }
        
        return jsonify(analysis)
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/api/pandas-operations', methods=['POST'])
def pandas_operations():
    """Perform custom pandas operations on trip data"""
    try:
        data = request.json
        operation = data.get('operation')
        
        if cab_system.df.empty:
            return jsonify({'error': 'No data available'}), 400
        
        result = {}
        
        if operation == 'group_by_day':
            grouped = cab_system.df.groupby('day').agg({
                'fare': ['count', 'sum', 'mean'],
                'distance': 'sum',
                'time': 'sum'
            }).round(2)
            result = grouped.to_dict()
        
        elif operation == 'group_by_traffic':
            grouped = cab_system.df.groupby('traffic').agg({
                'fare': ['count', 'sum', 'mean'],
                'distance': 'sum',
                'time': 'sum'
            }).round(2)
            result = grouped.to_dict()
        
        elif operation == 'hourly_analysis':
            grouped = cab_system.df.groupby('start_hour').agg({
                'fare': ['count', 'sum', 'mean'],
                'distance': 'mean',
                'time': 'mean'
            }).round(2)
            result = grouped.to_dict()
        
        elif operation == 'describe':
            result = cab_system.df.describe().to_dict()
        
        elif operation == 'correlation':
            numeric_cols = ['distance', 'time', 'fare', 'start_hour']
            corr_matrix = cab_system.df[numeric_cols].corr()
            result = corr_matrix.to_dict()
        
        else:
            return jsonify({'error': 'Invalid operation'}), 400
        
        return jsonify({'operation': operation, 'result': result})
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/api/pricing-info', methods=['GET'])
def get_pricing_info():
    """Get pricing information"""
    return jsonify({
        'base_fare': FareCalculator.BASE_FARE,
        'per_km_rate': FareCalculator.PER_KM_RATE,
        'per_minute_rate': FareCalculator.PER_MINUTE_RATE,
        'booking_fee': FareCalculator.BOOKING_FEE,
        'traffic_multipliers': FareCalculator.TRAFFIC_MULTIPLIERS,
        'peak_hours': FareCalculator.PEAK_HOURS,
        'peak_hour_surge': FareCalculator.PEAK_HOUR_SURGE,
        'weekend_days': FareCalculator.WEEKEND_DAYS,
        'weekend_surge': FareCalculator.WEEKEND_SURGE
    })


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)