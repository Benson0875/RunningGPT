import pytest
import os
import sys
from pathlib import Path
import pandas as pd
from unittest.mock import patch, MagicMock
from datetime import datetime
import logging

# Add the parent directory to the Python path
sys.path.append(str(Path(__file__).parent.parent))

from decode_fit import decode_fit_file

# Configure logging
logger = logging.getLogger(__name__)

@pytest.fixture
def sample_fit_file(tmp_path):
    """Create a sample FIT file for testing"""
    # Use the existing sample FIT file from the tests directory
    sample_fit = Path(__file__).parent / "12129115726_ACTIVITY.fit"
    if not sample_fit.exists():
        pytest.skip("Sample FIT file not found")
    return str(sample_fit)

@pytest.fixture
def mock_fitfile():
    """Create a mock FitFile object"""
    mock = MagicMock()
    
    # Mock record messages
    record_data = {
        'timestamp': pd.Timestamp('2024-01-01 10:00:00'),
        'distance': 100.0,
        'heart_rate': 150,
        'cadence': 170,
        'enhanced_speed': 3.0,
        'enhanced_altitude': 150.0
    }
    
    record_mock = MagicMock()
    record_mock.get_values.return_value = record_data
    record_mock.__iter__ = lambda self: iter([
        MagicMock(name=k, value=v) for k, v in record_data.items()
    ])
    
    # Mock activity messages
    activity_data = {
        'timestamp': pd.Timestamp('2024-01-01 10:00:00'),
        'total_timer_time': 3600.0,
        'type': 'running'
    }
    activity_mock = MagicMock()
    activity_mock.__iter__ = lambda self: iter([
        MagicMock(name=k, value=v) for k, v in activity_data.items()
    ])
    
    # Mock device messages
    device_data = {
        'manufacturer': 'garmin',
        'product': 'forerunner',
        'serial_number': '12345'
    }
    device_mock = MagicMock()
    device_mock.__iter__ = lambda self: iter([
        MagicMock(name=k, value=v) for k, v in device_data.items()
    ])
    
    def get_messages(message_type):
        if message_type == "record":
            return [record_mock]
        elif message_type == "activity":
            return [activity_mock]
        elif message_type == "device_info":
            return [device_mock]
        return []
    
    mock.get_messages = get_messages
    return mock

def test_decode_fit_file(sample_fit_file, tmp_path):
    """Test decoding a real FIT file"""
    output_path = tmp_path / "output.csv"
    try:
        df = decode_fit_file(sample_fit_file, str(output_path))
        assert df is not None
        assert isinstance(df, pd.DataFrame)
        assert len(df) > 0
        
        # Check for some expected columns that should be present
        expected_columns = ['timestamp', 'heart_rate', 'temperature']
        for col in expected_columns:
            assert col in df.columns
            
    except Exception as e:
        pytest.fail(f"Failed to decode FIT file: {str(e)}")

@pytest.mark.skip(reason="Mock test needs to be redesigned")
@patch('fitparse.base.FitFile._parse_file_header')
@patch('fitparse.FitFile')
def test_decode_fit_file_with_mock(mock_fitfile_class, mock_parse_header, tmp_path, caplog):
    """Test decoding with mocked FIT file data"""
    # Enable debug logging
    caplog.set_level(logging.DEBUG)
    
    output_path = tmp_path / "output.csv"
    mock_file = tmp_path / "mock_file.fit"
    
    # Create a real file with mock FIT data
    mock_data = bytes([
        # Header (14 bytes)
        0x0E,  # Header size
        0x10,  # Protocol version
        0x6A, 0x00,  # Profile version
        0x00, 0x00, 0x00, 0x00,  # Data size
        0x2E, 0x46, 0x49, 0x54,  # .FIT
        0x00, 0x00,  # CRC
        # Data records (32 bytes of dummy data)
        *([0x00] * 32)
    ])
    mock_file.write_bytes(mock_data)
    
    # Create a mock FitFile instance
    mock_fitfile = MagicMock()
    mock_fitfile_class.return_value = mock_fitfile
    
    # Set required attributes
    mock_fitfile._complete = True
    mock_fitfile._messages = []
    mock_fitfile._accumulators = {}
    mock_fitfile._compressed_ts_accumulator = 0
    mock_fitfile._crc = 0
    mock_fitfile._crc_calculated = 0
    mock_fitfile._data_bytes = mock_data
    mock_fitfile._file = None
    mock_fitfile._file_header_size = 14
    mock_fitfile._file_size = len(mock_data)
    mock_fitfile._local_mesgs = {}
    mock_fitfile._processor = None
    mock_fitfile._profile_version = 0x6A
    mock_fitfile._protocol_version = 0x10
    
    # Mock record data
    record_data = {
        'timestamp': datetime.now(),
        'heart_rate': 150,
        'temperature': 25,
        'distance': 100.0
    }
    
    # Mock the get_messages method
    def mock_get_messages(message_type):
        logger.debug(f"Getting messages for type: {message_type}")
        if message_type == "record":
            mock_record_msg = MagicMock()
            mock_record_msg.__iter__ = lambda self: iter([
                MagicMock(name=k, value=v) for k, v in record_data.items()
            ])
            return [mock_record_msg]
        elif message_type == "activity":
            activity_data = {
                'timestamp': datetime.now(),
                'total_timer_time': 3600.0,
                'type': 'running'
            }
            mock_activity = MagicMock()
            mock_activity.__iter__ = lambda self: iter([
                MagicMock(name=k, value=v) for k, v in activity_data.items()
            ])
            return [mock_activity]
        elif message_type == "device_info":
            device_data = {
                'manufacturer': 'garmin',
                'product': 'forerunner',
                'serial_number': '12345'
            }
            mock_device = MagicMock()
            mock_device.__iter__ = lambda self: iter([
                MagicMock(name=k, value=v) for k, v in device_data.items()
            ])
            return [mock_device]
        return []
    
    mock_fitfile.get_messages = mock_get_messages
    
    try:
        # Execute the function
        df = decode_fit_file(str(mock_file), str(output_path))
        
        # Verify the DataFrame
        assert df is not None
        assert not df.empty
        assert 'heart_rate' in df.columns
        assert 'temperature' in df.columns
        assert 'distance' in df.columns
        assert len(df) == 1
        
        # Verify the CSV file was created
        assert output_path.exists()
        
        logger.debug("Test completed successfully")
        
    except Exception as e:
        logger.error(f"Error in test: {str(e)}")
        logger.error(f"Error type: {type(e)}")
        raise

def test_decode_fit_file_missing_file(tmp_path):
    """Test handling of missing FIT file"""
    output_path = tmp_path / "output.csv"
    with pytest.raises(FileNotFoundError):
        decode_fit_file("nonexistent.fit", str(output_path))

def test_decode_fit_file_invalid_file(tmp_path):
    """Test handling of invalid FIT file"""
    # Create an invalid file
    invalid_file = tmp_path / "invalid.fit"
    invalid_file.write_text("This is not a FIT file")
    output_path = tmp_path / "output.csv"
    
    with pytest.raises(Exception):
        decode_fit_file(str(invalid_file), str(output_path)) 