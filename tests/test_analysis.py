import pytest
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import os
import sys
from pathlib import Path

# Add the parent directory to the Python path
sys.path.append(str(Path(__file__).parent.parent))

from analysis_running_CSV import (
    sec_to_min_sec,
    format_pace_ticks,
    analyze_csv_file,
    write_analysis_to_file
)

@pytest.fixture
def sample_csv_data(tmp_path):
    """Create a sample CSV file with workout data"""
    # Create sample data
    timestamps = pd.date_range(start='2024-01-01 10:00:00', periods=100, freq='10S')
    data = {
        'timestamp': timestamps,
        'distance': np.linspace(0, 5000, 100),  # 0 to 5000 meters
        'enhanced_speed': np.ones(100) * 3.0,  # 3 m/s constant speed
        'heart_rate': np.random.randint(140, 180, 100),
        'cadence': np.random.randint(160, 180, 100),
        'enhanced_altitude': np.random.uniform(100, 200, 100)
    }
    df = pd.DataFrame(data)
    
    # Create CSV file
    csv_path = tmp_path / "test_workout.csv"
    df.to_csv(csv_path, index=False)
    return str(csv_path)

def test_sec_to_min_sec():
    """Test conversion of seconds to minutes:seconds format"""
    assert sec_to_min_sec(65) == "1:05"
    assert sec_to_min_sec(3600) == "60:00"
    assert sec_to_min_sec(0) == "0:00"
    assert sec_to_min_sec(np.nan) == "N/A"

def test_format_pace_ticks():
    """Test formatting of pace ticks"""
    assert format_pace_ticks(300, None) == "5:00"
    assert format_pace_ticks(360, None) == "6:00"
    assert format_pace_ticks(np.nan, None) == "N/A"

def test_analyze_csv_file(sample_csv_data):
    """Test analysis of a CSV file"""
    stats, df = analyze_csv_file(sample_csv_data)
    
    assert stats is not None
    assert df is not None
    
    # Check if all expected statistics are present
    expected_keys = [
        'Total Distance (meters)',
        'Total Time (seconds)',
        'Average Pace (sec/km)',
        'Fastest Pace (sec/km)',
        'Average Heart Rate',
        'Maximum Heart Rate',
        'Average Cadence',
        'Maximum Altitude',
        'Minimum Altitude',
        'Altitude Difference (Enhanced Estimate)'
    ]
    
    for key in expected_keys:
        assert key in stats
    
    # Check specific values
    assert float(stats['Total Distance (meters)']) == pytest.approx(5000.0, rel=1e-2)
    assert float(stats['Total Time (seconds)']) == pytest.approx(990.0, rel=1e-2)  # 99 intervals * 10 seconds

def test_write_analysis_to_file(tmp_path, sample_csv_data):
    """Test writing analysis results to a file"""
    # Analyze sample data
    stats, _ = analyze_csv_file(sample_csv_data)
    
    # Create output file
    output_file = tmp_path / "test_analysis.txt"
    write_analysis_to_file(stats, "test_workout.csv", str(output_file))
    
    # Check if file exists and contains expected content
    assert output_file.exists()
    
    content = output_file.read_text(encoding='utf-8')
    assert "Analysis Results for: test_workout.csv" in content
    assert "Total Distance (meters)" in content
    assert "Heart Rate" in content 