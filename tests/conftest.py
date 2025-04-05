import json
import os
import re

import pytest
from pathlib import Path
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
from unittest.mock import patch


@pytest.fixture
def vcr(vcr):
    """Mock VCR fixture to avoid requiring GARMINTOKENS environment variable"""
    with patch.dict('os.environ', {'GARMINTOKENS': 'D:\\GitHub\\RunningGPT\\.garminconnect'}):
        yield vcr


def sanitize_cookie(cookie_value) -> str:
    return re.sub(r"=[^;]*", "=SANITIZED", cookie_value)


def sanitize_request(request):
    if request.body:
        try:
            body = request.body.decode("utf8")
        except UnicodeDecodeError:
            ...
        else:
            for key in ["username", "password", "refresh_token"]:
                body = re.sub(key + r"=[^&]*", f"{key}=SANITIZED", body)
            request.body = body.encode("utf8")

    if "Cookie" in request.headers:
        cookies = request.headers["Cookie"].split("; ")
        sanitized_cookies = [sanitize_cookie(cookie) for cookie in cookies]
        request.headers["Cookie"] = "; ".join(sanitized_cookies)
    return request


def sanitize_response(response):
    for key in ["set-cookie", "Set-Cookie"]:
        if key in response["headers"]:
            cookies = response["headers"][key]
            sanitized_cookies = [sanitize_cookie(cookie) for cookie in cookies]
            response["headers"][key] = sanitized_cookies

    body = response["body"]["string"].decode("utf8")
    patterns = [
        "oauth_token=[^&]*",
        "oauth_token_secret=[^&]*",
        "mfa_token=[^&]*",
    ]
    for pattern in patterns:
        body = re.sub(pattern, pattern.split("=")[0] + "=SANITIZED", body)
    try:
        body_json = json.loads(body)
    except json.JSONDecodeError:
        pass
    else:
        for field in [
            "access_token",
            "refresh_token",
            "jti",
            "consumer_key",
            "consumer_secret",
        ]:
            if field in body_json:
                body_json[field] = "SANITIZED"

        body = json.dumps(body_json)
    response["body"]["string"] = body.encode("utf8")

    return response


@pytest.fixture(scope="session")
def vcr_config():
    return {
        "filter_headers": [("Authorization", "Bearer SANITIZED")],
        "before_record_request": sanitize_request,
        "before_record_response": sanitize_response,
    }


@pytest.fixture
def sample_workout_data():
    """Create sample workout data for testing"""
    return {
        'activityId': '12345678',
        'activityType': {'typeKey': 'running'},
        'startTimeLocal': '2024-01-01 10:00:00',
        'distance': 5000.0,
        'duration': 1800.0,
        'averageHR': 150,
        'maxHR': 170,
        'averageCadence': 170
    }


@pytest.fixture
def sample_fit_data():
    """Create sample FIT file data structure"""
    timestamps = pd.date_range(start='2024-01-01 10:00:00', periods=100, freq='10S')
    return {
        'timestamp': timestamps,
        'distance': np.linspace(0, 5000, 100),
        'heart_rate': np.random.randint(140, 180, 100),
        'cadence': np.random.randint(160, 180, 100),
        'enhanced_speed': np.ones(100) * 3.0,
        'enhanced_altitude': np.random.uniform(100, 200, 100)
    }


@pytest.fixture
def temp_workouts_directory(tmp_path):
    """Create a temporary workouts directory structure"""
    # Create main workouts directory
    workouts_dir = tmp_path / "workouts"
    workouts_dir.mkdir()
    
    # Create CSV subdirectory
    csv_dir = workouts_dir / "CSV"
    csv_dir.mkdir()
    
    return workouts_dir


@pytest.fixture
def sample_credentials_file(tmp_path):
    """Create a sample credentials file"""
    creds_file = tmp_path / "USERNAMEPASSWORD.txt"
    creds_file.write_text("test@example.com\ntestpassword")
    return creds_file


@pytest.fixture
def mock_garmin_response():
    """Create mock Garmin Connect API response"""
    return [
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


@pytest.fixture
def mock_environment(monkeypatch, tmp_path):
    """Setup mock environment variables and paths"""
    # Set up mock GARMINTOKENS environment variable
    tokens_dir = tmp_path / ".garminconnect"
    tokens_dir.mkdir()
    monkeypatch.setenv("GARMINTOKENS", str(tokens_dir))
    
    # Create mock tokens file
    tokens_file = tokens_dir / "tokens.json"
    tokens_data = {
        "access_token": "mock_access_token",
        "refresh_token": "mock_refresh_token"
    }
    tokens_file.write_text(json.dumps(tokens_data))
    
    return {
        "tokens_dir": tokens_dir,
        "tokens_file": tokens_file
    }
