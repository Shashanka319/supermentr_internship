# 🚕 Enhanced Cab Fare Estimator - Complete Python Web Application

A powerful, feature-rich cab fare estimation system built entirely with Python! This application demonstrates the capabilities of Python's data science ecosystem for building complete web applications without needing separate frontend technologies.

## 🚀 Features

### 📊 Core Functionality
- Smart Fare Calculator with dynamic pricing algorithms
- Advanced Analytics powered by pandas and numpy
- Interactive Data Visualizations using plotly
- Comprehensive Trip Management with full CRUD operations
- Multi-format Data Export** (CSV, Excel, JSON)
- **Bulk Data Import** from CSV files
- **Automated Report Generation** with detailed insights

### 🎯 Pricing Intelligence
- **Base Pricing**: ₹50 base fare + ₹10/km + ₹2/minute + ₹20 booking fee
- **Dynamic Surge Pricing**:
  - Traffic-based multipliers (Light: 1x, Medium: 1.1x, Heavy: 1.25x)
  - Peak hour surge: +20% (6-9 AM, 6-9 PM)
  - Weekend surge: +15% (Saturday, Sunday)

### 📈 Advanced Analytics
- **Statistical Analysis**: Mean, median, standard deviation, quartiles, skewness, kurtosis
- **Correlation Analysis**: Multi-variate correlation matrices
- **Peak Hours Analysis**: Time-based usage patterns
- **Weekend vs Weekday**: Comparative analysis
- **Traffic Impact Analysis**: Revenue by traffic conditions
- **Efficiency Metrics**: Fare per km, fare per minute optimization

## 🛠️ Technology Stack

This application is built entirely with Python using these amazing libraries:

### 🖥️ Frontend & UI
- **Streamlit**: Modern web app framework for Python
- **Custom CSS**: Beautiful styling and responsive design
- **Plotly**: Interactive charts and visualizations

### 📊 Data Processing & Analytics
- **Pandas**: Data manipulation and analysis
- **NumPy**: Numerical computing and statistics
- **SciPy**: Advanced scientific computing

### 🎨 Visualization
- **Plotly**: Interactive charts (histograms, box plots, scatter plots, heatmaps)
- **Matplotlib**: Statistical plotting
- **Seaborn**: Advanced statistical visualizations

### 🔌 Backend API
- **FastAPI**: High-performance REST API framework
- **Pydantic**: Data validation and serialization
- **Uvicorn**: ASGI server for FastAPI

### 💾 Data Export/Import
- **OpenPyXL**: Excel file operations
- **JSON**: Native Python JSON handling
- **CSV**: Pandas-powered CSV operations

## 📦 Installation & Setup

### Prerequisites
- Python 3.8 or higher
- pip package manager

### 1. Clone or Download
```bash
# Create project directory
mkdir python-cab-estimator
cd python-cab-estimator
```

### 2. Install Dependencies
```bash
pip install -r requirements.txt
```

### 3. Run the Application

#### Option A: Streamlit Web App (Recommended)
```bash
streamlit run streamlit_app.py
```
The app will open in your browser at `http://localhost:8501`

#### Option B: FastAPI Backend + Frontend
```bash
# Terminal 1: Start FastAPI backend
python fastapi_backend.py

# Terminal 2: Start Streamlit frontend
streamlit run streamlit_app.py
```
- FastAPI docs: `http://localhost:8000/docs`
- Streamlit app: `http://localhost:8501`

## 🖥️ User Interface

### 🚕 Fare Calculator
- Intuitive form for trip details input
- Real-time fare calculation with detailed breakdown
- One-click trip addition to database
- Visual fare breakdown showing all pricing components

### 📊 Trip Analytics
- **Basic Statistics**: Total trips, revenue, averages
- **Advanced Analytics**: Statistical distributions, correlations
- **Peak Hours Analysis**: Morning/evening/off-peak comparisons
- **Weekend vs Weekday**: Detailed comparative metrics
- **Traffic Analysis**: Revenue and efficiency by traffic conditions
- **Efficiency Metrics**: Performance indicators and optimization insights

### 📈 Data Visualization
- **Interactive Charts**: Powered by Plotly with zoom, pan, hover
- **Multiple Chart Types**: Histograms, box plots, scatter plots, heatmaps, trend lines
- **Customizable Views**: Select which charts to display
- **Real-time Updates**: Charts update automatically with new data

### 📋 Trip History
- **Comprehensive Trip List**: All trip details in tabular format
- **Sorting & Filtering**: Sort by any column, filter by trip count
- **Data Preview**: Quick overview with summary statistics

### 💾 Data Export
- **CSV Export**: Standard comma-separated values
- **Excel Export**: Multi-sheet workbooks with summaries and analysis
- **JSON Export**: Structured data with metadata and analytics
- **One-click Downloads**: Instant file generation and download

### 📄 Reports
- **Automated Reports**: Comprehensive text-based analytics reports
- **Downloadable**: Save reports as text files
- **Insights**: AI-powered insights and recommendations

## 🔌 API Endpoints (FastAPI)

### Trip Management
- `POST /trips` - Add single trip
- `POST /trips/bulk` - Add multiple trips
- `GET /trips` - Retrieve trips with pagination
- `DELETE /trips` - Clear all trips

### Analytics
- `GET /stats` - Basic statistics
- `GET /analytics` - Advanced analytics
- `GET /visualizations` - Chart data

### Data Operations
- `GET /export/csv` - Export as CSV
- `GET /export/excel` - Export as Excel
- `GET /export/json` - Export as JSON
- `POST /import/csv` - Import from CSV
- `POST /pandas-operations` - Custom pandas operations

### Utilities
- `GET /health` - Health check
- `GET /report` - Generate report
- `POST /calculate-fare` - Calculate fare without saving

## 📊 Sample Data & Usage

### Adding Your First Trip
1. Navigate to "🚕 Fare Calculator"
2. Enter trip details:
   - Distance: 15.5 km
   - Time: 45 minutes
   - Traffic: heavy
   - Day: friday
   - Start Hour: 18 (6 PM)
3. Click "➕ Add Trip"
4. View calculated fare with detailed breakdown

### Exploring Analytics
1. Add several trips with different parameters
2. Go to "📊 Trip Analytics" to see statistics
3. Check "📈 Data Visualization" for interactive charts
4. Export your data using "💾 Data Export"

## 🔧 Configuration

### Customizing Pricing
Edit `cab_system_core.py` to modify pricing parameters:

```python
class FareCalculator:
    BASE_FARE = 50          # Base fare in rupees
    PER_KM_RATE = 10        # Rate per kilometer
    PER_MINUTE_RATE = 2     # Rate per minute
    BOOKING_FEE = 20        # Fixed booking fee
    
    TRAFFIC_MULTIPLIERS = {
        'light': 1.0,
        'medium': 1.10,
        'heavy': 1.25
    }
    
    PEAK_HOUR_SURGE = 0.20  # 20% surge
    WEEKEND_SURGE = 0.15    # 15% surge
```

## 🎨 Customization

### Streamlit Theme
Modify the CSS in `streamlit_app.py` to change colors, fonts, and layout.

### Adding New Analytics
Extend the `CabSystemAnalytics` class in `cab_system_core.py` to add custom analysis methods.

### New Visualizations
Add new chart types by extending the `create_visualizations()` method.

## 🚀 Deployment Options

### Local Development
- Run with `streamlit run streamlit_app.py`
- Access at `http://localhost:8501`

### Streamlit Cloud
1. Push code to GitHub
2. Connect to Streamlit Cloud
3. Deploy automatically

### Docker
```dockerfile
FROM python:3.9
COPY . /app
WORKDIR /app
RUN pip install -r requirements.txt
EXPOSE 8501
CMD ["streamlit", "run", "streamlit_app.py"]
```

### Heroku
1. Add `Procfile`: `web: streamlit run streamlit_app.py --server.port=$PORT`
2. Deploy to Heroku

## 🤝 Contributing

Contributions are welcome! Here are some ideas:

### Features to Add
- **User Authentication**: Multi-user support
- **Database Integration**: PostgreSQL/MongoDB support
- **Machine Learning**: Fare prediction models
- **Real-time Data**: Live traffic API integration
- **Mobile App**: React Native frontend
- **Advanced Visualizations**: 3D charts, geographic maps

### Code Improvements
- **Unit Tests**: pytest-based testing
- **Type Hints**: Complete type annotation
- **Performance**: Caching and optimization
- **Documentation**: API documentation

## 📝 License

This project is open source and available under the MIT License.

## 🙏 Acknowledgments

Built with these amazing Python libraries:
- **Streamlit** - For making web apps in Python simple
- **Pandas** - For powerful data manipulation
- **NumPy** - For numerical computing
- **Plotly** - For beautiful interactive visualizations
- **FastAPI** - For high-performance APIs
- **SciPy** - For scientific computing

## 📞 Support

For questions, issues, or contributions:
1. Check the documentation above
2. Review the code comments
3. Test with sample data
4. Experiment with different configurations

---

**🚕 Happy fare calculating with Python! 🐍**

*This project demonstrates the incredible power of Python's ecosystem for building complete, production-ready web applications entirely in Python. No JavaScript, no separate frontend frameworks - just pure Python magic!*