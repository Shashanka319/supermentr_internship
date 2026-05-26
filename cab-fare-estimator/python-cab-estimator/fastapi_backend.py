"""
FastAPI Backend for Advanced Cab Fare Estimator APIs
Provides REST endpoints for data processing and analytics
"""

from fastapi import FastAPI, HTTPException, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse, JSONResponse
from pydantic import BaseModel
from typing import List, Dict, Optional
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from plotly.utils import PlotlyJSONEncoder
import json
import io
import os
from datetime import datetime
from cab_system_core import CabSystemAnalytics, FareCalculator, Trip

# Initialize FastAPI app
app = FastAPI(
    title="🚕 Cab Fare Estimator API",
    description="Advanced REST API for cab fare calculation and analytics",
    version="1.0.0"
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Global instances
cab_system = CabSystemAnalytics()
fare_calculator = FareCalculator()

# Pydantic models
class TripCreate(BaseModel):
    distance: float
    time: int
    traffic: str
    day: str
    start_hour: int

class TripResponse(BaseModel):
    id: str
    distance: float
    time: int
    traffic: str
    day: str
    start_hour: int
    fare: float
    created_at: Optional[str] = None

class FareCalculationRequest(BaseModel):
    distance: float
    time: int
    traffic: str
    day: str
    start_hour: int

class FareCalculationResponse(BaseModel):
    fare: float
    breakdown: Dict

class BulkTripUpload(BaseModel):
    trips: List[TripCreate]

# API Endpoints

@app.get("/", tags=["Root"])
async def root():
    """Welcome endpoint"""
    return {
        "message": "🚕 Cab Fare Estimator API",
        "version": "1.0.0",
        "docs": "/docs",
        "total_trips": len(cab_system.df)
    }

@app.get("/health", tags=["Health"])
async def health_check():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "timestamp": datetime.now().isoformat(),
        "total_trips": len(cab_system.df),
        "memory_usage_kb": cab_system.df.memory_usage().sum() / 1024
    }

@app.post("/calculate-fare", response_model=FareCalculationResponse, tags=["Fare Calculation"])
async def calculate_fare(request: FareCalculationRequest):
    """Calculate fare without adding trip to database"""
    try:
        trip = Trip(
            distance=request.distance,
            time=request.time,
            traffic=request.traffic.lower(),
            day=request.day.lower(),
            start_hour=request.start_hour
        )
        
        fare = fare_calculator.calculate_fare(trip)
        breakdown = fare_calculator.get_fare_breakdown(trip)
        
        return FareCalculationResponse(fare=fare, breakdown=breakdown)
    
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.post("/trips", response_model=TripResponse, tags=["Trip Management"])
async def add_trip(trip_data: TripCreate):
    """Add a new trip to the system"""
    try:
        trip = cab_system.add_trip(
            distance=trip_data.distance,
            time=trip_data.time,
            traffic=trip_data.traffic,
            day=trip_data.day,
            start_hour=trip_data.start_hour
        )
        
        return TripResponse(
            id=trip.id,
            distance=trip.distance,
            time=trip.time,
            traffic=trip.traffic,
            day=trip.day,
            start_hour=trip.start_hour,
            fare=trip.fare,
            created_at=trip.created_at.isoformat() if trip.created_at else None
        )
    
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.post("/trips/bulk", tags=["Trip Management"])
async def add_bulk_trips(bulk_data: BulkTripUpload):
    """Add multiple trips in bulk"""
    try:
        added_trips = []
        for trip_data in bulk_data.trips:
            trip = cab_system.add_trip(
                distance=trip_data.distance,
                time=trip_data.time,
                traffic=trip_data.traffic,
                day=trip_data.day,
                start_hour=trip_data.start_hour
            )
            added_trips.append(trip.to_dict())
        
        return {
            "message": f"Successfully added {len(added_trips)} trips",
            "trips": added_trips
        }
    
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.get("/trips", tags=["Trip Management"])
async def get_trips(limit: Optional[int] = None, offset: Optional[int] = 0):
    """Get all trips with optional pagination"""
    try:
        df = cab_system.df.copy()
        
        if df.empty:
            return {"trips": [], "total": 0}
        
        # Apply pagination
        total = len(df)
        if limit:
            df = df.iloc[offset:offset + limit]
        
        trips = df.to_dict('records')
        
        # Convert datetime objects to strings
        for trip in trips:
            if 'created_at' in trip and pd.notna(trip['created_at']):
                trip['created_at'] = trip['created_at'].isoformat()
        
        return {
            "trips": trips,
            "total": total,
            "limit": limit,
            "offset": offset
        }
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/stats", tags=["Analytics"])
async def get_basic_stats():
    """Get basic statistics"""
    try:
        return cab_system.get_basic_stats()
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/analytics", tags=["Analytics"])
async def get_advanced_analytics():
    """Get advanced analytics"""
    try:
        return cab_system.get_advanced_analytics()
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/visualizations", tags=["Analytics"])
async def get_visualizations():
    """Get visualization data in JSON format"""
    try:
        if cab_system.df.empty:
            return {"message": "No data available for visualizations"}
        
        charts = cab_system.create_visualizations()
        
        # Convert plotly figures to JSON
        json_charts = {}
        for name, fig in charts.items():
            json_charts[name] = json.loads(fig.to_json())
        
        return json_charts
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/export/csv", tags=["Data Export"])
async def export_csv():
    """Export trip data as CSV"""
    try:
        if cab_system.df.empty:
            raise HTTPException(status_code=400, detail="No data to export")
        
        # Create temporary CSV file
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"cab_trips_{timestamp}.csv"
        filepath = f"/tmp/{filename}" if os.path.exists("/tmp") else filename
        
        cab_system.df.to_csv(filepath, index=False)
        
        return FileResponse(
            path=filepath,
            filename=filename,
            media_type="text/csv"
        )
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/export/excel", tags=["Data Export"])
async def export_excel():
    """Export trip data as Excel"""
    try:
        if cab_system.df.empty:
            raise HTTPException(status_code=400, detail="No data to export")
        
        # Create Excel file in memory
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"cab_trips_{timestamp}.xlsx"
        
        output = io.BytesIO()
        with pd.ExcelWriter(output, engine='openpyxl') as writer:
            cab_system.df.to_excel(writer, sheet_name='All Trips', index=False)
            
            # Add summary sheet
            stats = cab_system.get_basic_stats()
            summary_df = pd.DataFrame([
                {'Metric': 'Total Trips', 'Value': stats['total_trips']},
                {'Metric': 'Total Revenue', 'Value': stats['total_earnings']},
                {'Metric': 'Average Fare', 'Value': stats['average_fare']},
                {'Metric': 'Total Distance', 'Value': stats['total_distance']},
                {'Metric': 'Total Time', 'Value': stats['total_time']}
            ])
            summary_df.to_excel(writer, sheet_name='Summary', index=False)
            
            # Traffic analysis sheet
            analytics = cab_system.get_advanced_analytics()
            if 'traffic_analysis' in analytics:
                traffic_df = pd.DataFrame(analytics['traffic_analysis']).T
                traffic_df.to_excel(writer, sheet_name='Traffic Analysis')
        
        # Save to temporary file
        filepath = f"/tmp/{filename}" if os.path.exists("/tmp") else filename
        with open(filepath, 'wb') as f:
            f.write(output.getvalue())
        
        return FileResponse(
            path=filepath,
            filename=filename,
            media_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
        )
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/export/json", tags=["Data Export"])
async def export_json():
    """Export trip data as JSON"""
    try:
        if cab_system.df.empty:
            raise HTTPException(status_code=400, detail="No data to export")
        
        trips_data = cab_system.df.to_dict('records')
        
        # Convert datetime objects to strings
        for trip in trips_data:
            if 'created_at' in trip and pd.notna(trip['created_at']):
                trip['created_at'] = trip['created_at'].isoformat()
        
        export_data = {
            'export_date': datetime.now().isoformat(),
            'total_trips': len(trips_data),
            'summary': cab_system.get_basic_stats(),
            'analytics': cab_system.get_advanced_analytics(),
            'trips': trips_data
        }
        
        return export_data
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/import/csv", tags=["Data Import"])
async def import_csv(file: UploadFile = File(...)):
    """Import trip data from CSV file"""
    try:
        if not file.filename.endswith('.csv'):
            raise HTTPException(status_code=400, detail="File must be a CSV")
        
        # Read CSV file
        content = await file.read()
        df = pd.read_csv(io.StringIO(content.decode('utf-8')))
        
        # Validate required columns
        required_columns = ['distance', 'time', 'traffic', 'day', 'start_hour']
        missing_columns = [col for col in required_columns if col not in df.columns]
        
        if missing_columns:
            raise HTTPException(
                status_code=400, 
                detail=f"Missing required columns: {missing_columns}"
            )
        
        # Add trips to system
        added_count = 0
        for _, row in df.iterrows():
            try:
                cab_system.add_trip(
                    distance=float(row['distance']),
                    time=int(row['time']),
                    traffic=str(row['traffic']),
                    day=str(row['day']),
                    start_hour=int(row['start_hour'])
                )
                added_count += 1
            except Exception as row_error:
                continue  # Skip invalid rows
        
        return {
            "message": f"Successfully imported {added_count} trips from {len(df)} rows",
            "imported_trips": added_count,
            "total_rows": len(df)
        }
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/report", tags=["Reports"])
async def generate_report():
    """Generate comprehensive text report"""
    try:
        if cab_system.df.empty:
            return {"message": "No data available for report generation"}
        
        report = cab_system.generate_report()
        
        return {
            "report": report,
            "generated_at": datetime.now().isoformat(),
            "total_trips": len(cab_system.df)
        }
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/pandas-operations", tags=["Advanced Analytics"])
async def pandas_operations(operation: str, group_by: Optional[str] = None):
    """Perform custom pandas operations"""
    try:
        if cab_system.df.empty:
            raise HTTPException(status_code=400, detail="No data available")
        
        df = cab_system.df
        result = {}
        
        if operation == "describe":
            result = df.describe().to_dict()
        
        elif operation == "correlation":
            numeric_cols = ['distance', 'time', 'fare', 'start_hour']
            corr_matrix = df[numeric_cols].corr()
            result = corr_matrix.to_dict()
        
        elif operation == "group_statistics" and group_by:
            if group_by in df.columns:
                grouped = df.groupby(group_by).agg({
                    'fare': ['count', 'sum', 'mean', 'std'],
                    'distance': ['sum', 'mean'],
                    'time': ['sum', 'mean']
                }).round(2)
                result = grouped.to_dict()
            else:
                raise HTTPException(status_code=400, detail=f"Column '{group_by}' not found")
        
        elif operation == "outliers":
            # Detect outliers using IQR method
            Q1 = df['fare'].quantile(0.25)
            Q3 = df['fare'].quantile(0.75)
            IQR = Q3 - Q1
            lower_bound = Q1 - 1.5 * IQR
            upper_bound = Q3 + 1.5 * IQR
            
            outliers = df[(df['fare'] < lower_bound) | (df['fare'] > upper_bound)]
            result = {
                "outlier_count": len(outliers),
                "total_trips": len(df),
                "outlier_percentage": (len(outliers) / len(df)) * 100,
                "outliers": outliers.to_dict('records')
            }
        
        else:
            raise HTTPException(status_code=400, detail="Invalid operation")
        
        return {
            "operation": operation,
            "group_by": group_by,
            "result": result
        }
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.delete("/trips", tags=["Trip Management"])
async def clear_all_trips():
    """Clear all trip data"""
    try:
        total_trips = len(cab_system.df)
        cab_system.df = cab_system.df.iloc[0:0]  # Clear DataFrame
        cab_system.next_id = 1  # Reset ID counter
        
        return {
            "message": f"Successfully cleared {total_trips} trips",
            "cleared_trips": total_trips
        }
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# Run the app
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)