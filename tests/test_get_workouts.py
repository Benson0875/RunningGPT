import pytest
import os
import sys
from pathlib import Path
from unittest.mock import patch, MagicMock, PropertyMock
import json
import logging

# Add the parent directory to the Python path
sys.path.append(str(Path(__file__).parent.parent))

from Get_workouts_data import (
    get_credentials,
    init_api,
    download_workouts
)

# Configure logging
logger = logging.getLogger(__name__)

@pytest.fixture
def mock_credentials():
    """Mock credentials for testing"""
    return {
        'email': 'test@example.com',
        'password': 'testpassword'
    }

@pytest.fixture
def mock_garmin_client():
    """Mock Garmin client for testing"""
    client = MagicMock()
    # Mock activities list
    client.get_activities.return_value = [
        {
            'activityId': '12345678',
            'activityType': {'typeKey': 'running'},
            'startTimeLocal': '2024-01-01 10:00:00'
        },
        {
            'activityId': '87654321',
            'activityType': {'typeKey': 'cycling'},
            'startTimeLocal': '2024-01-01 11:00:00'
        }
    ]
    return client

@pytest.fixture
def temp_workouts_dir(tmp_path):
    """Create a temporary workouts directory"""
    workouts_dir = tmp_path / "workouts"
    workouts_dir.mkdir()
    return workouts_dir

def test_get_credentials(tmp_path):
    """Test reading credentials from file"""
    # Create a temporary credentials file
    creds_file = tmp_path / "USERNAMEPASSWORD.txt"
    creds_file.write_text("test@example.com:test@example.com\npassword:testpassword")
    
    with patch('os.path.exists') as mock_exists:
        mock_exists.return_value = True
        with patch('builtins.open', create=True) as mock_open:
            mock_open.return_value.__enter__.return_value.readlines.return_value = [
                "test@example.com:test@example.com\n",
                "password:testpassword\n"
            ]
            email, password = get_credentials()
            assert email == "test@example.com"
            assert password == "testpassword"

@pytest.mark.skip(reason="SSO authentication needs to be redesigned")
def test_connect_to_garmin(mock_credentials, caplog):
    """Test Garmin Connect client creation"""
    # Enable debug logging
    caplog.set_level(logging.DEBUG)
    
    with patch('garminconnect.Garmin') as mock_client:
        # Mock Garmin client
        mock_instance = MagicMock()
        mock_client.return_value = mock_instance
        
        # Mock successful login
        mock_instance.login.return_value = None
        
        # Mock profile data
        mock_instance.get_full_name.return_value = "Test User"
        mock_instance.get_user_summary.return_value = {
            "displayName": "Test User",
            "fullName": "Test User",
            "id": "12345678"
        }
        
        # Mock the garth property and its methods
        mock_garth = MagicMock()
        mock_garth.login.return_value = None
        mock_garth.profile = {
            "displayName": "Test User",
            "fullName": "Test User",
            "id": "12345678"
        }
        type(mock_instance).garth = PropertyMock(return_value=mock_garth)
        
        try:
            client = init_api(mock_credentials['email'], mock_credentials['password'])
            logger.debug("API initialization successful")
            
            # Verify the client was created
            assert client is not None
            mock_client.assert_called_once_with(
                mock_credentials['email'],
                mock_credentials['password']
            )
            mock_instance.login.assert_called_once()
            
            logger.debug("Test completed successfully")
            
        except Exception as e:
            logger.error(f"Test failed with error: {str(e)}")
            logger.error(f"Error type: {type(e)}")
            raise

def test_download_workouts(mock_garmin_client, temp_workouts_dir):
    """Test downloading workouts"""
    workout_type = "running"
    count = 1
    
    with patch('os.path.exists') as mock_exists:
        mock_exists.return_value = True
        
        # Mock the download_activity method
        mock_garmin_client.download_activity.return_value = b"mock_fit_data"
        mock_garmin_client.ActivityDownloadFormat = MagicMock()
        mock_garmin_client.ActivityDownloadFormat.ORIGINAL = 'fit'
        
        downloaded = download_workouts(mock_garmin_client, workout_type, count)
        
        assert downloaded == 1
        mock_garmin_client.get_activities.assert_called_once()
        mock_garmin_client.download_activity.assert_called_once_with('12345678', dl_fmt='fit')

def test_download_workouts_no_activities(mock_garmin_client, temp_workouts_dir):
    """Test downloading workouts when no activities are found"""
    mock_garmin_client.get_activities.return_value = []
    
    with patch('os.path.exists') as mock_exists:
        mock_exists.return_value = True
        
        downloaded = download_workouts(mock_garmin_client, "running", 1)
        assert downloaded == 0 