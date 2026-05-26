@echo off
echo 🚕 Starting Cab Fare Estimator...
echo ====================================

echo Installing dependencies...
pip install -r requirements.txt

echo.
echo Starting Streamlit application...
echo Open your browser to: http://localhost:8501
echo.
echo Press Ctrl+C to stop the application
echo ====================================

streamlit run streamlit_app.py