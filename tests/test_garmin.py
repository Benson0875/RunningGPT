import pytest
from unittest.mock import patch, MagicMock
from datetime import datetime, timedelta
import json

import garminconnect

DATE = "2023-07-01"


@pytest.fixture
def garmin():
    """Create a mock Garmin client"""
    with patch('garminconnect.Garmin') as mock_garmin:
        mock_instance = MagicMock()
        mock_garmin.return_value = mock_instance
        
        # Mock successful login
        mock_instance.login.return_value = None
        
        # Mock activity data
        mock_instance.get_activities.return_value = [
            {
                'activityId': '12345678',
                'activityType': {'typeKey': 'running'},
                'startTimeLocal': '2024-01-01 10:00:00'
            }
        ]
        
        # Mock stats data
        mock_instance.get_stats.return_value = {
            'totalSteps': 10000,
            'totalDistance': 10.5
        }
        
        # Mock user data
        mock_instance.get_user_summary.return_value = {
            'displayName': 'Test User',
            'location': 'Test Location'
        }
        
        # Mock steps data
        mock_instance.get_steps_data.return_value = {
            'steps': [{'startGMT': '2024-01-01', 'steps': 1000}]
        }
        
        # Mock floors data
        mock_instance.get_floors_data.return_value = {
            'floors': [{'startGMT': '2024-01-01', 'floors': 10}]
        }
        
        # Mock daily steps
        mock_instance.get_daily_steps.return_value = [
            {'calendarDate': '2024-01-01', 'steps': 1000}
        ]
        
        # Mock heart rates
        mock_instance.get_heart_rates.return_value = {
            'heartRateValues': [[1704067200000, 60]]
        }
        
        # Mock body composition
        mock_instance.get_body_composition.return_value = {
            'weight': 70.0,
            'bodyFat': 15.0
        }
        
        # Mock body battery
        mock_instance.get_body_battery.return_value = {
            'bodyBattery': [{'startGMT': '2024-01-01', 'value': 80}]
        }
        
        # Mock hydration data
        mock_instance.get_hydration_data.return_value = {
            'hydration': [{'startGMT': '2024-01-01', 'valueInML': 2000}]
        }
        
        # Mock respiration data
        mock_instance.get_respiration_data.return_value = {
            'respiration': [{'startGMT': '2024-01-01', 'avgWakingRespirationValue': 15}]
        }
        
        # Mock SpO2 data
        mock_instance.get_spo2_data.return_value = {
            'spo2': [{'startGMT': '2024-01-01', 'avgSpo2Value': 98}]
        }
        
        # Mock HRV data
        mock_instance.get_hrv_data.return_value = {
            'hrvSummary': [{'startGMT': '2024-01-01', 'weeklyAvg': 50}]
        }
        
        # Mock stress data
        mock_instance.get_stress_data.return_value = {
            'stressLevel': {'value': 25}
        }
        
        yield mock_instance


@pytest.mark.vcr
def test_stats(garmin):
    """Test getting user stats"""
    stats = garmin.get_stats()
    assert stats is not None
    assert stats['totalSteps'] == 10000
    assert stats['totalDistance'] == 10.5


@pytest.mark.vcr
def test_user_summary(garmin):
    """Test getting user summary"""
    summary = garmin.get_user_summary()
    assert summary is not None
    assert summary['displayName'] == 'Test User'
    assert summary['location'] == 'Test Location'


@pytest.mark.vcr
def test_steps_data(garmin):
    """Test getting steps data"""
    steps = garmin.get_steps_data()
    assert steps is not None
    assert steps['steps'][0]['steps'] == 1000


@pytest.mark.vcr
def test_floors(garmin):
    """Test getting floors data"""
    floors = garmin.get_floors_data()
    assert floors is not None
    assert floors['floors'][0]['floors'] == 10


@pytest.mark.vcr
def test_daily_steps(garmin):
    """Test getting daily steps"""
    steps = garmin.get_daily_steps()
    assert steps is not None
    assert steps[0]['steps'] == 1000


@pytest.mark.vcr
def test_heart_rates(garmin):
    """Test getting heart rates"""
    heart_rates = garmin.get_heart_rates()
    assert heart_rates is not None
    assert heart_rates['heartRateValues'][0][1] == 60


@pytest.mark.vcr
def test_stats_and_body(garmin):
    """Test getting stats and body data"""
    stats = garmin.get_stats()
    assert stats is not None
    assert stats['totalSteps'] == 10000


@pytest.mark.vcr
def test_body_composition(garmin):
    """Test getting body composition"""
    body = garmin.get_body_composition()
    assert body is not None
    assert body['weight'] == 70.0
    assert body['bodyFat'] == 15.0


@pytest.mark.vcr
def test_body_battery(garmin):
    """Test getting body battery"""
    battery = garmin.get_body_battery()
    assert battery is not None
    assert battery['bodyBattery'][0]['value'] == 80


@pytest.mark.vcr
def test_hydration_data(garmin):
    """Test getting hydration data"""
    hydration = garmin.get_hydration_data()
    assert hydration is not None
    assert hydration['hydration'][0]['valueInML'] == 2000


@pytest.mark.vcr
def test_respiration_data(garmin):
    """Test getting respiration data"""
    respiration = garmin.get_respiration_data()
    assert respiration is not None
    assert respiration['respiration'][0]['avgWakingRespirationValue'] == 15


@pytest.mark.vcr
def test_spo2_data(garmin):
    """Test getting SpO2 data"""
    spo2 = garmin.get_spo2_data()
    assert spo2 is not None
    assert spo2['spo2'][0]['avgSpo2Value'] == 98


@pytest.mark.vcr
def test_hrv_data(garmin):
    """Test getting HRV data"""
    hrv = garmin.get_hrv_data()
    assert hrv is not None
    assert hrv['hrvSummary'][0]['weeklyAvg'] == 50


@pytest.mark.vcr
def test_download_activity(garmin):
    """Test downloading an activity"""
    activity_id = '12345678'
    data = garmin.download_activity(activity_id)
    assert data is not None


@pytest.mark.vcr
def test_all_day_stress(garmin):
    """Test getting all day stress data"""
    stress = garmin.get_stress_data()
    assert stress is not None
    assert stress['stressLevel']['value'] == 25


@pytest.mark.vcr
def test_upload(garmin):
    """Test uploading an activity"""
    with patch('builtins.open', create=True) as mock_open:
        mock_open.return_value.__enter__.return_value.read.return_value = b'test data'
        garmin.upload_activity.return_value = {'detailedImportResult': {'successes': [{'internalId': 12345}]}}
        result = garmin.upload_activity('test.fit')
        assert result is not None
        assert result['detailedImportResult']['successes'][0]['internalId'] == 12345


@pytest.mark.vcr
def test_request_reload(garmin):
    """Test requesting a reload"""
    garmin.modern_rest_client.return_value = {'status': 'success'}
    result = garmin.modern_rest_client
    assert result is not None
