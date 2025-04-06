# Garmin Connect Integration API

## 1. Overview
This document describes the integration with Garmin Connect API for retrieving workout data, downloading FIT files, and processing workout information.

## 2. Authentication

### 2.1 Login
```python
from garminconnect import Garmin

def connect_to_garmin(username: str, password: str) -> Garmin:
    """
    Authenticate with Garmin Connect.
    
    Args:
        username: Garmin Connect username
        password: Garmin Connect password
        
    Returns:
        Authenticated Garmin client instance
        
    Raises:
        GarminConnectAuthError: If authentication fails
        GarminConnectConnectionError: If connection fails
    """
```

### 2.2 Session Management
- Sessions are maintained automatically
- Token refresh is handled by the client
- Rate limiting is implemented to prevent API abuse

## 3. Activity Retrieval

### 3.1 Get Recent Activities
```python
def get_activities(
    client: Garmin,
    limit: int = 10,
    start_date: Optional[datetime] = None
) -> List[Dict]:
    """
    Retrieve recent activities from Garmin Connect.
    
    Args:
        client: Authenticated Garmin client
        limit: Maximum number of activities to retrieve
        start_date: Optional start date filter
        
    Returns:
        List of activity dictionaries containing:
        - activityId: Unique activity identifier
        - activityName: Name of the activity
        - distance: Distance in meters
        - duration: Duration in seconds
        - startTime: Activity start time
        - averageHR: Average heart rate
    """
```

### 3.2 Get Activity Details
```python
def get_activity_details(
    client: Garmin,
    activity_id: str
) -> Dict:
    """
    Get detailed information for a specific activity.
    
    Args:
        client: Authenticated Garmin client
        activity_id: Activity identifier
        
    Returns:
        Dictionary containing detailed activity information:
        - Basic metrics (distance, duration, etc.)
        - Split information
        - Heart rate zones
        - GPS data
        - Weather conditions
    """
```

## 4. FIT File Operations

### 4.1 Download FIT File
```python
def download_fit_file(
    client: Garmin,
    activity_id: str,
    output_dir: str
) -> str:
    """
    Download FIT file for an activity.
    
    Args:
        client: Authenticated Garmin client
        activity_id: Activity identifier
        output_dir: Directory to save the file
        
    Returns:
        Path to downloaded FIT file
        
    Raises:
        GarminConnectConnectionError: If download fails
        IOError: If file cannot be saved
    """
```

### 4.2 Decode FIT File
```python
def decode_fit_file(
    fit_file: str
) -> pd.DataFrame:
    """
    Decode FIT file into a pandas DataFrame.
    
    Args:
        fit_file: Path to FIT file
        
    Returns:
        DataFrame containing:
        - timestamp: Data point timestamp
        - position_lat: Latitude
        - position_long: Longitude
        - distance: Cumulative distance
        - heart_rate: Heart rate
        - altitude: Altitude
        - speed: Current speed
        - cadence: Running cadence
        - temperature: Ambient temperature
    """
```

## 5. Data Processing

### 5.1 Process Workout Data
```python
def process_workout(
    fit_data: pd.DataFrame
) -> Dict:
    """
    Process workout data from FIT file.
    
    Args:
        fit_data: DataFrame from decoded FIT file
        
    Returns:
        Dictionary containing:
        - total_distance: Total distance in meters
        - total_time: Total time in seconds
        - average_pace: Average pace (min/km)
        - average_hr: Average heart rate
        - max_hr: Maximum heart rate
        - elevation_gain: Total elevation gain
        - splits: Kilometer splits
    """
```

### 5.2 Generate Workout Report
```python
def generate_workout_report(
    workout_data: Dict,
    output_file: str
) -> str:
    """
    Generate a text report for the workout.
    
    Args:
        workout_data: Processed workout data
        output_file: Path to save the report
        
    Returns:
        Path to generated report file
        
    Report Format:
    --------------
    Workout Summary
    Date: [Activity Date]
    Type: [Activity Type]
    
    Distance: [Total Distance] km
    Duration: [Total Time]
    Avg Pace: [Average Pace] min/km
    Avg HR: [Average HR] bpm
    Max HR: [Maximum HR] bpm
    Elevation Gain: [Total Gain] m
    
    Splits:
    1 km: [Split Time] ([Split Pace])
    2 km: [Split Time] ([Split Pace])
    ...
    """
```

## 6. Error Handling

### 6.1 Exception Types
```python
class GarminConnectError(Exception):
    """Base exception for Garmin Connect errors"""
    pass

class GarminConnectAuthError(GarminConnectError):
    """Authentication failed"""
    pass

class GarminConnectConnectionError(GarminConnectError):
    """Connection to Garmin Connect failed"""
    pass

class FitDecodeError(Exception):
    """Error decoding FIT file"""
    pass
```

### 6.2 Error Recovery
- Automatic retry on connection errors
- Token refresh on authentication errors
- Graceful degradation for missing data
- Detailed error logging

## 7. Rate Limiting

### 7.1 API Limits
- Maximum 10 requests per minute
- Session timeout after 1 hour
- Maximum 100 activities per request

### 7.2 Implementation
```python
from ratelimit import limits, sleep_and_retry

@sleep_and_retry
@limits(calls=10, period=60)
def rate_limited_api_call(client: Garmin, *args, **kwargs):
    """
    Rate-limited API call to Garmin Connect.
    
    Implements exponential backoff on failure.
    """
```

## 8. Security Considerations

### 8.1 Credential Storage
- Use environment variables or secure credential storage
- Never store passwords in plain text
- Implement secure session management

### 8.2 Data Protection
- Secure storage of downloaded FIT files
- Proper file permissions
- Regular cleanup of temporary files

## 9. Version History
| Version | Date | Description | Author |
|---------|------|-------------|---------|
| 1.0 | 2024-03-21 | Initial API documentation | Lead Developer | 