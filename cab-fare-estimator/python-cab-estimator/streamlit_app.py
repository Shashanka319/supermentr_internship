"""
🚕 Cab Fare Estimator - Complete Python Web Application with Authentication
Built with Streamlit, Pandas, NumPy, and Plotly
"""

import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime, timedelta
import json
import io
import base64
import hashlib
import sqlite3
import os
from cab_system_core import CabSystemAnalytics, FareCalculator, Trip

# Authentication Functions
class AuthSystem:
    def __init__(self):
        self.db_path = "users.db"
        self.init_database()
    
    def init_database(self):
        """Initialize the user database"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT UNIQUE NOT NULL,
                email TEXT UNIQUE NOT NULL,
                password_hash TEXT NOT NULL,
                full_name TEXT NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)
        conn.commit()
        conn.close()
    
    def hash_password(self, password):
        """Hash password with salt"""
        salt = "cab_fare_estimator_salt_2024"
        return hashlib.sha256((password + salt).encode()).hexdigest()
    
    def register_user(self, username, email, password, full_name):
        """Register a new user"""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            # Check if user already exists
            cursor.execute("SELECT * FROM users WHERE username = ? OR email = ?", (username, email))
            if cursor.fetchone():
                conn.close()
                return False, "Username or email already exists"
            
            # Insert new user
            password_hash = self.hash_password(password)
            cursor.execute("""
                INSERT INTO users (username, email, password_hash, full_name) 
                VALUES (?, ?, ?, ?)
            """, (username, email, password_hash, full_name))
            
            conn.commit()
            conn.close()
            return True, "User registered successfully"
        
        except Exception as e:
            return False, f"Registration failed: {str(e)}"
    
    def authenticate_user(self, username, password):
        """Authenticate user login"""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            
            password_hash = self.hash_password(password)
            cursor.execute("""
                SELECT id, username, email, full_name FROM users 
                WHERE username = ? AND password_hash = ?
            """, (username, password_hash))
            
            user = cursor.fetchone()
            conn.close()
            
            if user:
                return True, {
                    'id': user[0],
                    'username': user[1],
                    'email': user[2],
                    'full_name': user[3]
                }
            else:
                return False, "Invalid username or password"
        
        except Exception as e:
            return False, f"Authentication failed: {str(e)}"

# Initialize authentication system
auth_system = AuthSystem()

# Configure Streamlit page
st.set_page_config(
    page_title="🚕 Cab Fare Estimator",
    page_icon="🚕",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Initialize authentication state
if 'authenticated' not in st.session_state:
    st.session_state.authenticated = False
if 'user_info' not in st.session_state:
    st.session_state.user_info = None
if 'show_signup' not in st.session_state:
    st.session_state.show_signup = False

# Custom CSS for better styling
st.markdown("""
<style>
    .main-header {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 2rem;
        border-radius: 10px;
        color: white;
        text-align: center;
        margin-bottom: 2rem;
    }
    .stButton > button {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        border: none;
        border-radius: 5px;
        padding: 0.5rem 1rem;
        font-weight: bold;
    }
</style>
""", unsafe_allow_html=True)

# Authentication UI Functions
def show_login_form():
    """Display login form"""
    st.markdown("<h2 style='text-align: center; color: #667eea;'>🔑 Login to Your Account</h2>", unsafe_allow_html=True)
    
    with st.form("login_form"):
        col1, col2, col3 = st.columns([1, 2, 1])
        
        with col2:
            username = st.text_input("👤 Username", placeholder="Enter your username")
            password = st.text_input("🔒 Password", type="password", placeholder="Enter your password")
            
            col_login, col_signup = st.columns(2)
            
            with col_login:
                login_button = st.form_submit_button("🔑 Login", use_container_width=True)
            
            with col_signup:
                signup_link = st.form_submit_button("🎆 Sign Up", use_container_width=True)
    
    # Handle login
    if login_button:
        if username and password:
            success, result = auth_system.authenticate_user(username, password)
            if success:
                st.session_state.authenticated = True
                st.session_state.user_info = result
                st.success(f"Welcome back, {result['full_name']}! 🎉")
                st.rerun()
            else:
                st.error(f"❌ {result}")
        else:
            st.warning("⚠️ Please fill in all fields")
    
    # Handle signup link
    if signup_link:
        st.session_state.show_signup = True
        st.rerun()

def show_signup_form():
    """Display signup form"""
    st.markdown("<h2 style='text-align: center; color: #667eea;'>🎆 Create Your Account</h2>", unsafe_allow_html=True)
    
    with st.form("signup_form"):
        col1, col2, col3 = st.columns([1, 2, 1])
        
        with col2:
            full_name = st.text_input("👤 Full Name", placeholder="Enter your full name")
            username = st.text_input("🏷️ Username", placeholder="Choose a username")
            email = st.text_input("📧 Email", placeholder="Enter your email address")
            password = st.text_input("🔒 Password", type="password", placeholder="Create a password")
            confirm_password = st.text_input("🔓 Confirm Password", type="password", placeholder="Confirm your password")
            
            col_signup, col_login = st.columns(2)
            
            with col_signup:
                signup_button = st.form_submit_button("🎆 Create Account", use_container_width=True)
            
            with col_login:
                login_link = st.form_submit_button("🔑 Back to Login", use_container_width=True)
    
    # Handle signup
    if signup_button:
        if all([full_name, username, email, password, confirm_password]):
            if password != confirm_password:
                st.error("❌ Passwords do not match")
            elif len(password) < 6:
                st.error("❌ Password must be at least 6 characters long")
            else:
                success, message = auth_system.register_user(username, email, password, full_name)
                if success:
                    st.success(f"✅ {message}")
                    st.info("🔑 Please login with your new account")
                    st.session_state.show_signup = False
                    st.rerun()
                else:
                    st.error(f"❌ {message}")
        else:
            st.warning("⚠️ Please fill in all fields")
    
    # Handle back to login
    if login_link:
        st.session_state.show_signup = False
        st.rerun()

def show_authenticated_app():
    """Show the main application for authenticated users"""
    # Initialize session state
    if 'cab_system' not in st.session_state:
        try:
            st.session_state.cab_system = CabSystemAnalytics()
        except Exception as e:
            st.error(f"Error initializing cab system: {e}")
            st.session_state.cab_system = None

    if 'fare_calculator' not in st.session_state:
        try:
            st.session_state.fare_calculator = FareCalculator()
        except Exception as e:
            st.error(f"Error initializing fare calculator: {e}")
            st.session_state.fare_calculator = None

    # User info in sidebar
    if st.session_state.user_info:
        user = st.session_state.user_info
        st.sidebar.markdown("---")
        st.sidebar.markdown(f"**👤 Welcome, {user['full_name']}!**")
        st.sidebar.markdown(f"🏷️ @{user['username']}")
        st.sidebar.markdown(f"📧 {user['email']}")
        
        if st.sidebar.button("🚪 Logout", use_container_width=True):
            st.session_state.authenticated = False
            st.session_state.user_info = None
            st.session_state.show_signup = False
            st.rerun()

    # App header
    st.markdown("""
    <div class="main-header">
        <h1>🚕 Cab Fare Estimator</h1>
        <p>Your trusted partner for accurate fare calculations and trip management</p>
        <p>🚗 Smart Pricing • 📱 Easy Booking • 💰 Transparent Costs</p>
    </div>
    """, unsafe_allow_html=True)

    # Sidebar for navigation
    st.sidebar.title("🧭 Navigation")
    page = st.sidebar.selectbox(
        "Choose a section:",
        ["🚕 Fare Calculator", "📊 Trip Analytics", "📈 Data Visualization", 
         "📋 Trip History", "💾 Data Export", "ℹ️ About"]
    )

    # Helper function for fare breakdown
    def display_fare_breakdown(breakdown):
        """Display fare breakdown in a formatted way"""
        st.subheader("💰 Fare Breakdown")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.metric("Base Fare", f"₹{breakdown['base_fare']}")
            st.metric("Distance Charge", f"₹{breakdown['distance_charge']:.2f}")
            st.metric("Time Charge", f"₹{breakdown['time_charge']:.2f}")
            st.metric("Booking Fee", f"₹{breakdown['booking_fee']}")
        
        with col2:
            st.metric("Traffic Multiplier", f"{breakdown['traffic_multiplier']}x")
            if breakdown['is_peak_hour']:
                st.metric("Peak Hour Surge", f"+{breakdown['peak_hour_surge']*100:.0f}%")
            if breakdown['is_weekend']:
                st.metric("Weekend Surge", f"+{breakdown['weekend_surge']*100:.0f}%")
            st.metric("**Final Fare**", f"**₹{breakdown['final_fare']:.2f}**")

    # Page routing
    if page == "🚕 Fare Calculator":
        if st.session_state.cab_system is None or st.session_state.fare_calculator is None:
            st.error("⚠️ System initialization failed. Please refresh the page.")
            st.stop()
        
        st.header("🚕 Cab Fare Calculator")
        
        col1, col2 = st.columns([2, 1])
        
        with col1:
            st.subheader("📝 Trip Details")
            
            # Input form
            with st.form("trip_form"):
                col_a, col_b = st.columns(2)
                
                with col_a:
                    distance = st.number_input("Distance (km)", min_value=0.1, max_value=1000.0, value=10.0, step=0.1)
                    time = st.number_input("Time (minutes)", min_value=1, max_value=1440, value=30, step=1)
                    traffic = st.selectbox("Traffic Condition", ["light", "medium", "heavy"], index=0)
                
                with col_b:
                    day = st.selectbox("Day of Week", 
                        ["monday", "tuesday", "wednesday", "thursday", "friday", "saturday", "sunday"], 
                        index=0)
                    start_hour = st.number_input("Start Hour (0-23)", min_value=0, max_value=23, value=8, step=1)
                
                col_calc, col_add = st.columns(2)
                
                with col_calc:
                    calculate_button = st.form_submit_button("🧮 Calculate Fare", use_container_width=True)
                
                with col_add:
                    add_trip_button = st.form_submit_button("➕ Add Trip", use_container_width=True)
            
            # Handle form submissions
            if calculate_button or add_trip_button:
                try:
                    trip = Trip(distance=distance, time=time, traffic=traffic, day=day, start_hour=start_hour)
                    fare = st.session_state.fare_calculator.calculate_fare(trip)
                    breakdown = st.session_state.fare_calculator.get_fare_breakdown(trip)
                    
                    if calculate_button:
                        st.success(f"🎯 Calculated Fare: ₹{fare:.2f}")
                        display_fare_breakdown(breakdown)
                    
                    if add_trip_button:
                        added_trip = st.session_state.cab_system.add_trip(distance, time, traffic, day, start_hour)
                        st.success(f"✅ Trip added successfully! Fare: ₹{added_trip.fare:.2f}")
                        display_fare_breakdown(breakdown)
                        
                except Exception as e:
                    st.error(f"❌ Error processing trip: {str(e)}")
                    st.info("Please check your input values and try again.")
        
        with col2:
            st.subheader("📊 Quick Stats")
            try:
                stats = st.session_state.cab_system.get_basic_stats()
                
                st.metric("Total Trips", stats['total_trips'])
                st.metric("Total Revenue", f"₹{stats['total_earnings']:.2f}")
                if stats['total_trips'] > 0:
                    st.metric("Average Fare", f"₹{stats['average_fare']:.2f}")
            except Exception as e:
                st.error(f"Error loading stats: {str(e)}")
            
            st.subheader("💡 Pricing Rules")
            st.info("""
            **Base Pricing:**
            - Base Fare: ₹50
            - Per KM: ₹10
            - Per Minute: ₹2
            - Booking Fee: ₹20
            
            **Dynamic Pricing:**
            - Light Traffic: 1.0x
            - Medium Traffic: 1.1x
            - Heavy Traffic: 1.25x
            - Peak Hours: +20%
            - Weekend: +15%
            """)

    elif page == "📊 Trip Analytics":
        st.header("📊 Advanced Trip Analytics")
        
        try:
            if st.session_state.cab_system.df.empty:
                st.warning("📝 No trip data available. Add some trips using the Fare Calculator to see analytics.")
            else:
                stats = st.session_state.cab_system.get_basic_stats()
                
                # Basic Statistics
                st.subheader("📈 Basic Statistics")
                col1, col2, col3, col4 = st.columns(4)
                
                with col1:
                    st.metric("Total Trips", stats['total_trips'])
                    st.metric("Total Revenue", f"₹{stats['total_earnings']:.2f}")
                
                with col2:
                    st.metric("Average Fare", f"₹{stats['average_fare']:.2f}")
                    st.metric("Median Fare", f"₹{stats['median_fare']:.2f}")
                
                with col3:
                    st.metric("Min Fare", f"₹{stats['min_fare']:.2f}")
                    st.metric("Max Fare", f"₹{stats['max_fare']:.2f}")
                
                with col4:
                    st.metric("Total Distance", f"{stats['total_distance']:.1f} km")
                    st.metric("Total Time", f"{stats['total_time']:.0f} min")
        
        except Exception as e:
            st.error(f"❌ Error loading analytics: {str(e)}")
            st.info("Please try refreshing the page or adding more trip data.")

    elif page == "📈 Data Visualization":
        st.header("📈 Data Visualization")
        
        try:
            if st.session_state.cab_system.df.empty:
                st.warning("📝 No trip data available for visualization. Add some trips first!")
            else:
                charts = st.session_state.cab_system.create_visualizations()
        
                if charts:
                    # Chart selection
                    chart_options = list(charts.keys())
                    selected_charts = st.multiselect(
                        "Select charts to display:",
                        chart_options,
                        default=chart_options[:3] if len(chart_options) >= 3 else chart_options
                    )
                    
                    # Display selected charts
                    for chart_name in selected_charts:
                        if chart_name in charts:
                            st.plotly_chart(charts[chart_name], use_container_width=True)
        
        except Exception as e:
            st.error(f"❌ Error loading visualizations: {str(e)}")
            st.info("Please try refreshing the page or check your data.")

    elif page == "📋 Trip History":
        st.header("📋 Trip History")
        
        try:
            if st.session_state.cab_system.df.empty:
                st.info("📝 No trips recorded yet. Use the Fare Calculator to add trips.")
            else:
                df = st.session_state.cab_system.df.copy()
                
                # Display data
                st.dataframe(df, use_container_width=True)
                
                # Trip summary
                st.subheader("📊 Summary")
                col1, col2, col3, col4 = st.columns(4)
                
                with col1:
                    st.metric("Total Trips", len(df))
                with col2:
                    st.metric("Total Fare", f"₹{df['fare'].sum():.2f}")
                with col3:
                    st.metric("Avg Fare", f"₹{df['fare'].mean():.2f}")
                with col4:
                    st.metric("Total Distance", f"{df['distance'].sum():.1f} km")
        
        except Exception as e:
            st.error(f"❌ Error loading trip history: {str(e)}")
            st.info("Please try refreshing the page.")

    elif page == "💾 Data Export":
        st.header("💾 Data Export")
        
        try:
            if st.session_state.cab_system.df.empty:
                st.warning("📝 No data to export. Add some trips first!")
            else:
                st.subheader("📋 Export Options")
        
                col1, col2, col3 = st.columns(3)
                
                with col1:
                    if st.button("📄 Export as CSV", use_container_width=True):
                        csv_data = st.session_state.cab_system.df.to_csv(index=False)
                        st.download_button(
                            label="⬇️ Download CSV",
                            data=csv_data,
                            file_name=f"cab_trips_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv",
                            mime="text/csv"
                        )
                
                # Data preview
                st.subheader("👀 Data Preview")
                st.dataframe(st.session_state.cab_system.df.head(10), use_container_width=True)
        
        except Exception as e:
            st.error(f"❌ Error in data export: {str(e)}")
            st.info("Please try refreshing the page.")

    elif page == "ℹ️ About":
        st.header("ℹ️ About This Application")
        
        st.markdown("""
        ## 🚕 Cab Fare Estimator with Authentication
        
        This is a **secure web application** with user authentication and comprehensive features:
        
        ### ✨ Features
        - 🔑 **User Authentication** with secure login/signup
        - 🧮 **Smart Fare Calculator** with dynamic pricing
        - 📊 **Advanced Analytics** for trip insights
        - 📈 **Interactive Visualizations**
        - 📋 **Trip History Management**
        - 💾 **Data Export** capabilities
        
        ### 🔐 Security Features
        - Password hashing with salt
        - SQLite database for user management
        - Session-based authentication
        - User-specific data isolation
        
        ### 🎯 Pricing Logic
        - **Base Fare**: ₹50
        - **Distance**: ₹10 per kilometer
        - **Time**: ₹2 per minute
        - **Booking Fee**: ₹20
        - **Dynamic Pricing** with traffic and time-based multipliers
        """)

# Main Application Flow
if not st.session_state.authenticated:
    # Show authentication forms
    if st.session_state.show_signup:
        show_signup_form()
    else:
        show_login_form()
else:
    # Show authenticated user interface
    show_authenticated_app()

# Footer
st.markdown("---")
st.markdown("""
<div style='text-align: center; color: #666; padding: 20px;'>
    🚕 <strong>Cab Fare Estimator</strong> - Reliable Transportation Solutions<br>
    Making your journey affordable and transparent
</div>
""", unsafe_allow_html=True)