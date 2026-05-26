"""
Enhanced Cab Fare Estimator System using Python Data Science Libraries
"""

import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import matplotlib.pyplot as plt
import seaborn as sns
from datetime import datetime, timedelta
from dataclasses import dataclass, asdict
from typing import List, Dict, Optional, Tuple
from enum import Enum
import json
import io
import base64


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
    created_at: Optional[datetime] = None
    
    def to_dict(self) -> Dict:
        """Convert trip to dictionary format"""
        return {
            'id': self.id,
            'distance': self.distance,
            'time': self.time,
            'traffic': self.traffic,
            'day': self.day,
            'start_hour': self.start_hour,
            'fare': self.fare,
            'created_at': self.created_at.isoformat() if self.created_at else None
        }


class FareCalculator:
    """Enhanced fare calculation logic with dynamic pricing rules"""
    
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
        """Calculate fare for a trip based on distance, time, and dynamic pricing rules"""
        base_amount = self.BASE_FARE
        distance_charge = trip.distance * self.PER_KM_RATE
        time_charge = trip.time * self.PER_MINUTE_RATE
        booking_fee = self.BOOKING_FEE
        
        subtotal = base_amount + distance_charge + time_charge + booking_fee
        
        # Apply traffic multiplier
        traffic_multiplier = self.TRAFFIC_MULTIPLIERS.get(trip.traffic.lower(), 1.0)
        subtotal *= traffic_multiplier
        
        # Apply peak hour surge
        is_peak_hour = any(start <= trip.start_hour < end for start, end in self.PEAK_HOURS)
        if is_peak_hour:
            subtotal *= (1 + self.PEAK_HOUR_SURGE)
        
        # Apply weekend surge
        is_weekend = trip.day.lower() in self.WEEKEND_DAYS
        if is_weekend:
            subtotal *= (1 + self.WEEKEND_SURGE)
        
        return round(subtotal, 2)
    
    def get_fare_breakdown(self, trip: Trip) -> Dict:
        """Get detailed fare breakdown"""
        base_amount = self.BASE_FARE
        distance_charge = trip.distance * self.PER_KM_RATE
        time_charge = trip.time * self.PER_MINUTE_RATE
        booking_fee = self.BOOKING_FEE
        
        subtotal = base_amount + distance_charge + time_charge + booking_fee
        traffic_multiplier = self.TRAFFIC_MULTIPLIERS.get(trip.traffic.lower(), 1.0)
        
        is_peak_hour = any(start <= trip.start_hour < end for start, end in self.PEAK_HOURS)
        is_weekend = trip.day.lower() in self.WEEKEND_DAYS
        
        breakdown = {
            'base_fare': base_amount,
            'distance_charge': distance_charge,
            'time_charge': time_charge,
            'booking_fee': booking_fee,
            'subtotal_before_multipliers': subtotal,
            'traffic_multiplier': traffic_multiplier,
            'is_peak_hour': is_peak_hour,
            'is_weekend': is_weekend,
            'peak_hour_surge': self.PEAK_HOUR_SURGE if is_peak_hour else 0,
            'weekend_surge': self.WEEKEND_SURGE if is_weekend else 0,
            'final_fare': self.calculate_fare(trip)
        }
        
        return breakdown


class CabSystemAnalytics:
    """Advanced analytics system using pandas and scientific libraries"""
    
    def __init__(self):
        self.fare_calculator = FareCalculator()
        self.next_id = 1
        
        # Initialize DataFrame with proper column types
        self.df = pd.DataFrame(columns=[
            'id', 'distance', 'time', 'traffic', 'day', 'start_hour', 'fare', 'created_at'
        ])
        
        # Set proper data types - only when DataFrame has data
        # Empty DataFrame will be handled when data is added
    
    def add_trip(self, distance: float, time: int, traffic: str, day: str, start_hour: int) -> Trip:
        """Add a new trip to the system"""
        trip = Trip(
            distance=distance,
            time=time,
            traffic=traffic.lower(),
            day=day.lower(),
            start_hour=start_hour,
            id=str(self.next_id),
            created_at=datetime.now()
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
            'created_at': trip.created_at
        }])
        
        self.df = pd.concat([self.df, new_row], ignore_index=True)
        self.next_id += 1
        
        return trip
    
    def get_basic_stats(self) -> Dict:
        """Get basic statistics"""
        if self.df.empty:
            return {
                'total_trips': 0,
                'total_earnings': 0.0,
                'average_fare': 0.0,
                'total_distance': 0.0,
                'total_time': 0.0
            }
        
        return {
            'total_trips': len(self.df),
            'total_earnings': float(self.df['fare'].sum()),
            'average_fare': float(self.df['fare'].mean()),
            'total_distance': float(self.df['distance'].sum()),
            'total_time': float(self.df['time'].sum()),
            'min_fare': float(self.df['fare'].min()),
            'max_fare': float(self.df['fare'].max()),
            'median_fare': float(self.df['fare'].median())
        }
    
    def get_advanced_analytics(self) -> Dict:
        """Get advanced analytics using pandas and numpy"""
        if self.df.empty:
            return {}
        
        analytics = {}
        
        # Statistical analysis
        analytics['fare_statistics'] = {
            'mean': float(self.df['fare'].mean()),
            'median': float(self.df['fare'].median()),
            'std': float(self.df['fare'].std()),
            'variance': float(self.df['fare'].var()),
            'skewness': float(self.df['fare'].skew()),
            'kurtosis': float(self.df['fare'].kurtosis()),
            'q25': float(self.df['fare'].quantile(0.25)),
            'q75': float(self.df['fare'].quantile(0.75)),
            'iqr': float(self.df['fare'].quantile(0.75) - self.df['fare'].quantile(0.25))
        }
        
        # Time-based analysis
        analytics['peak_hours_analysis'] = {
            'morning_peak': len(self.df[(self.df['start_hour'] >= 6) & (self.df['start_hour'] <= 9)]),
            'evening_peak': len(self.df[(self.df['start_hour'] >= 18) & (self.df['start_hour'] <= 21)]),
            'off_peak': len(self.df[~((self.df['start_hour'] >= 6) & (self.df['start_hour'] <= 9)) & 
                                  ~((self.df['start_hour'] >= 18) & (self.df['start_hour'] <= 21))])
        }
        
        # Weekend vs Weekday analysis
        weekend_mask = self.df['day'].isin(['saturday', 'sunday'])
        analytics['weekend_weekday_analysis'] = {
            'weekend': {
                'trips': int(weekend_mask.sum()),
                'total_fare': float(self.df[weekend_mask]['fare'].sum()),
                'avg_fare': float(self.df[weekend_mask]['fare'].mean()) if weekend_mask.any() else 0
            },
            'weekday': {
                'trips': int((~weekend_mask).sum()),
                'total_fare': float(self.df[~weekend_mask]['fare'].sum()),
                'avg_fare': float(self.df[~weekend_mask]['fare'].mean()) if (~weekend_mask).any() else 0
            }
        }
        
        # Traffic analysis
        traffic_stats = self.df.groupby('traffic').agg({
            'fare': ['count', 'sum', 'mean'],
            'distance': ['sum', 'mean'],
            'time': ['sum', 'mean']
        }).round(2)
        
        analytics['traffic_analysis'] = {}
        for traffic in ['light', 'medium', 'heavy']:
            if traffic in traffic_stats.index:
                analytics['traffic_analysis'][traffic] = {
                    'count': int(traffic_stats.loc[traffic, ('fare', 'count')]),
                    'total_fare': float(traffic_stats.loc[traffic, ('fare', 'sum')]),
                    'avg_fare': float(traffic_stats.loc[traffic, ('fare', 'mean')]),
                    'avg_distance': float(traffic_stats.loc[traffic, ('distance', 'mean')]),
                    'avg_time': float(traffic_stats.loc[traffic, ('time', 'mean')])
                }
        
        # Correlation analysis
        if len(self.df) > 1:
            numeric_cols = ['distance', 'time', 'fare', 'start_hour']
            corr_matrix = self.df[numeric_cols].corr()
            analytics['correlations'] = {
                'distance_time': float(corr_matrix.loc['distance', 'time']),
                'distance_fare': float(corr_matrix.loc['distance', 'fare']),
                'time_fare': float(corr_matrix.loc['time', 'fare']),
                'hour_fare': float(corr_matrix.loc['start_hour', 'fare'])
            }
        
        # Efficiency metrics
        if not self.df.empty:
            self.df['fare_per_km'] = self.df['fare'] / self.df['distance']
            self.df['fare_per_minute'] = self.df['fare'] / self.df['time']
            
            analytics['efficiency_metrics'] = {
                'avg_fare_per_km': float(self.df['fare_per_km'].mean()),
                'avg_fare_per_minute': float(self.df['fare_per_minute'].mean()),
                'efficiency_variance': {
                    'fare_per_km_std': float(self.df['fare_per_km'].std()),
                    'fare_per_minute_std': float(self.df['fare_per_minute'].std())
                }
            }
        
        return analytics
    
    def create_visualizations(self) -> Dict:
        """Create comprehensive visualizations using plotly"""
        if self.df.empty:
            return {}
        
        charts = {}
        
        try:
            # 1. Fare Distribution Histogram
            fig_hist = px.histogram(
                self.df, x='fare', nbins=20,
                title='Fare Distribution',
                labels={'fare': 'Fare (₹)', 'count': 'Number of Trips'},
                color_discrete_sequence=['#3b82f6']
            )
            fig_hist.update_layout(showlegend=False)
            charts['fare_histogram'] = fig_hist
            
            # 2. Traffic vs Fare Box Plot
            fig_box = px.box(
                self.df, x='traffic', y='fare',
                title='Fare Distribution by Traffic Condition',
                labels={'traffic': 'Traffic Condition', 'fare': 'Fare (₹)'},
                color='traffic',
                color_discrete_map={'light': '#22c55e', 'medium': '#f59e0b', 'heavy': '#ef4444'}
            )
            charts['traffic_boxplot'] = fig_box
            
            # 3. Hourly Trip Distribution
            hourly_data = self.df['start_hour'].value_counts().sort_index().reset_index()
            hourly_data.columns = ['hour', 'trips']
            
            fig_hourly = px.bar(
                hourly_data, x='hour', y='trips',
                title='Trip Distribution by Hour of Day',
                labels={'hour': 'Hour of Day', 'trips': 'Number of Trips'},
                color='trips',
                color_continuous_scale='viridis'
            )
            charts['hourly_distribution'] = fig_hourly
            
            # 4. Day of Week Analysis
            day_order = ['monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday']
            day_data = self.df['day'].value_counts().reindex(day_order, fill_value=0).reset_index()
            day_data.columns = ['day', 'trips']
            
            fig_day = px.bar(
                day_data, x='day', y='trips',
                title='Trip Distribution by Day of Week',
                labels={'day': 'Day of Week', 'trips': 'Number of Trips'},
                color='trips',
                color_continuous_scale='plasma'
            )
            charts['day_distribution'] = fig_day
            
            # 5. Distance vs Fare Scatter Plot
            fig_scatter = px.scatter(
                self.df, x='distance', y='fare', color='traffic',
                hover_data=['day', 'start_hour'],
                title='Distance vs Fare (colored by traffic)',
                labels={'distance': 'Distance (km)', 'fare': 'Fare (₹)'},
                color_discrete_map={'light': '#22c55e', 'medium': '#f59e0b', 'heavy': '#ef4444'}
            )
            charts['distance_fare_scatter'] = fig_scatter
            
            # 6. Correlation Heatmap
            if len(self.df) > 1:
                numeric_cols = ['distance', 'time', 'fare', 'start_hour']
                corr_matrix = self.df[numeric_cols].corr()
                
                fig_heatmap = go.Figure(data=go.Heatmap(
                    z=corr_matrix.values,
                    x=corr_matrix.columns,
                    y=corr_matrix.columns,
                    colorscale='RdBu',
                    zmid=0,
                    text=corr_matrix.round(3).values,
                    texttemplate='%{text}',
                    textfont={"size": 12},
                    hoverongaps=False
                ))
                fig_heatmap.update_layout(
                    title='Correlation Matrix',
                    xaxis_title='Variables',
                    yaxis_title='Variables'
                )
                charts['correlation_heatmap'] = fig_heatmap
            
            # 7. Revenue Trend (if we have timestamps)
            if 'created_at' in self.df.columns and not self.df['created_at'].isna().all():
                self.df['date'] = pd.to_datetime(self.df['created_at']).dt.date
                daily_revenue = self.df.groupby('date')['fare'].sum().reset_index()
                
                fig_trend = px.line(
                    daily_revenue, x='date', y='fare',
                    title='Daily Revenue Trend',
                    labels={'date': 'Date', 'fare': 'Total Revenue (₹)'},
                    line_shape='spline'
                )
                charts['revenue_trend'] = fig_trend
        
        except Exception as e:
            print(f"Error creating charts: {e}")
            # Return empty charts on error
            return {}
        
        return charts
    
    def export_data(self, format: str = 'csv') -> str:
        """Export data in various formats"""
        if self.df.empty:
            return None
        
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        
        if format == 'csv':
            filename = f'cab_trips_{timestamp}.csv'
            self.df.to_csv(filename, index=False)
            return filename
        
        elif format == 'excel':
            filename = f'cab_trips_{timestamp}.xlsx'
            with pd.ExcelWriter(filename, engine='openpyxl') as writer:
                self.df.to_excel(writer, sheet_name='All Trips', index=False)
                
                # Summary sheet
                summary = pd.DataFrame([
                    {'Metric': 'Total Trips', 'Value': len(self.df)},
                    {'Metric': 'Total Revenue', 'Value': self.df['fare'].sum()},
                    {'Metric': 'Average Fare', 'Value': self.df['fare'].mean()},
                    {'Metric': 'Total Distance', 'Value': self.df['distance'].sum()},
                    {'Metric': 'Total Time', 'Value': self.df['time'].sum()}
                ])
                summary.to_excel(writer, sheet_name='Summary', index=False)
                
                # Traffic analysis sheet
                traffic_summary = self.df.groupby('traffic').agg({
                    'fare': ['count', 'sum', 'mean'],
                    'distance': ['sum', 'mean'],
                    'time': ['sum', 'mean']
                }).round(2)
                traffic_summary.to_excel(writer, sheet_name='Traffic Analysis')
            
            return filename
        
        elif format == 'json':
            filename = f'cab_trips_{timestamp}.json'
            export_data = {
                'export_date': datetime.now().isoformat(),
                'total_trips': len(self.df),
                'summary': self.get_basic_stats(),
                'analytics': self.get_advanced_analytics(),
                'trips': self.df.to_dict('records')
            }
            
            with open(filename, 'w') as f:
                json.dump(export_data, f, indent=2, default=str)
            
            return filename
        
        return None
    
    def generate_report(self) -> str:
        """Generate comprehensive text report"""
        if self.df.empty:
            return "No trips recorded yet."
        
        stats = self.get_basic_stats()
        analytics = self.get_advanced_analytics()
        
        report_lines = []
        report_lines.append("=" * 80)
        report_lines.append("🚕 ENHANCED CAB FARE ESTIMATOR - COMPREHENSIVE ANALYTICS REPORT".center(80))
        report_lines.append("=" * 80)
        report_lines.append(f"📊 Generated on: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        report_lines.append("")
        
        # Basic Statistics
        report_lines.append("📈 BASIC STATISTICS")
        report_lines.append("-" * 50)
        report_lines.append(f"Total Trips: {stats['total_trips']}")
        report_lines.append(f"Total Revenue: ₹{stats['total_earnings']:.2f}")
        report_lines.append(f"Average Fare: ₹{stats['average_fare']:.2f}")
        report_lines.append(f"Total Distance: {stats['total_distance']:.2f} km")
        report_lines.append(f"Total Time: {stats['total_time']:.0f} minutes")
        report_lines.append("")
        
        # Fare Analytics
        if 'fare_statistics' in analytics:
            fare_stats = analytics['fare_statistics']
            report_lines.append("💰 FARE ANALYTICS")
            report_lines.append("-" * 50)
            report_lines.append(f"Median Fare: ₹{fare_stats['median']:.2f}")
            report_lines.append(f"Standard Deviation: ₹{fare_stats['std']:.2f}")
            report_lines.append(f"25th Percentile: ₹{fare_stats['q25']:.2f}")
            report_lines.append(f"75th Percentile: ₹{fare_stats['q75']:.2f}")
            report_lines.append(f"Fare Range (IQR): ₹{fare_stats['iqr']:.2f}")
            report_lines.append("")
        
        # Traffic Analysis
        if 'traffic_analysis' in analytics:
            report_lines.append("🚦 TRAFFIC ANALYSIS")
            report_lines.append("-" * 50)
            for traffic, data in analytics['traffic_analysis'].items():
                report_lines.append(f"{traffic.upper()}: {data['count']} trips | "
                                  f"Total: ₹{data['total_fare']:.2f} | "
                                  f"Avg: ₹{data['avg_fare']:.2f}")
            report_lines.append("")
        
        # Peak Hours Analysis
        if 'peak_hours_analysis' in analytics:
            peak_data = analytics['peak_hours_analysis']
            report_lines.append("⏰ PEAK HOURS ANALYSIS")
            report_lines.append("-" * 50)
            report_lines.append(f"Morning Peak (6-9 AM): {peak_data['morning_peak']} trips")
            report_lines.append(f"Evening Peak (6-9 PM): {peak_data['evening_peak']} trips")
            report_lines.append(f"Off-Peak Hours: {peak_data['off_peak']} trips")
            report_lines.append("")
        
        # Efficiency Metrics
        if 'efficiency_metrics' in analytics:
            eff_data = analytics['efficiency_metrics']
            report_lines.append("⚡ EFFICIENCY METRICS")
            report_lines.append("-" * 50)
            report_lines.append(f"Average Fare per KM: ₹{eff_data['avg_fare_per_km']:.2f}")
            report_lines.append(f"Average Fare per Minute: ₹{eff_data['avg_fare_per_minute']:.2f}")
            report_lines.append("")
        
        report_lines.append("=" * 80)
        report_lines.append("📊 Report generated using pandas, numpy, and Python data science tools")
        report_lines.append("=" * 80)
        
        return "\n".join(report_lines)


# Global instance for the Streamlit app
cab_system = CabSystemAnalytics()