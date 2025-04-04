#!/usr/bin/env python3
"""
Download the last 10 workouts from Garmin Connect and save them as .FIT files.

Usage:
    Set your Garmin Connect credentials as environment variables:
    EMAIL=<your garmin email>
    PASSWORD=<your garmin password>

    Or create a USERNAMEPASSWORD.txt file with:
    email:your_email
    password:your_password

    Or enter them when prompted.
"""

import os
import sys
import logging
import zipfile
import io
from datetime import datetime
from getpass import getpass

from garminconnect import (
    Garmin,
    GarminConnectAuthenticationError,
    GarminConnectConnectionError,
    GarminConnectTooManyRequestsError,
)

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def read_credentials_from_file():
    """Read credentials from USERNAMEPASSWORD.txt if it exists."""
    try:
        if os.path.exists("USERNAMEPASSWORD.txt"):
            with open("USERNAMEPASSWORD.txt", "r") as f:
                lines = f.readlines()
                email = lines[0].split(":")[1].strip()
                password = lines[1].split(":")[1].strip()
                return email, password
    except Exception as e:
        logger.warning(f"Error reading credentials file: {e}")
    return None, None

def get_credentials():
    """Get Garmin Connect credentials from file, environment variables, or user input."""
    # Try to read from file first
    email, password = read_credentials_from_file()
    if email and password:
        return email, password
    
    # Try environment variables next
    email = os.getenv("EMAIL")
    password = os.getenv("PASSWORD")
    
    # If still not found, ask user
    if not email:
        email = input("Enter your Garmin Connect email: ")
    if not password:
        password = getpass("Enter your Garmin Connect password: ")
    
    return email, password

def init_api(email, password):
    """Initialize the Garmin Connect API."""
    try:
        api = Garmin(email, password)
        api.login()
        return api
    except GarminConnectAuthenticationError as err:
        logger.error("Authentication error: %s", err)
        sys.exit(1)
    except GarminConnectConnectionError as err:
        logger.error("Connection error: %s", err)
        sys.exit(1)
    except GarminConnectTooManyRequestsError as err:
        logger.error("Too many requests error: %s", err)
        sys.exit(1)
    except Exception as err:
        logger.error("Unknown error: %s", err)
        sys.exit(1)

def extract_fit_from_zip(zip_data, output_path):
    """Extract the FIT file from a ZIP archive."""
    try:
        with zipfile.ZipFile(io.BytesIO(zip_data)) as zip_file:
            # Find the .fit file in the ZIP
            fit_files = [f for f in zip_file.namelist() if f.lower().endswith('.fit')]
            if not fit_files:
                logger.error("No FIT file found in the ZIP archive")
                return False
            
            # Extract the first FIT file
            fit_file = fit_files[0]
            with zip_file.open(fit_file) as source, open(output_path, 'wb') as target:
                target.write(source.read())
            return True
    except Exception as e:
        logger.error(f"Error extracting FIT file from ZIP: {e}")
        return False

def download_workouts(api, limit=10):
    """Download the last N workouts and save them as .FIT files."""
    try:
        # Get the last N activities
        activities = api.get_activities(0, limit)
        
        # Create a directory for the workouts if it doesn't exist
        output_dir = "workouts"
        if not os.path.exists(output_dir):
            os.makedirs(output_dir)
        
        # Download each activity
        for activity in activities:
            activity_id = activity["activityId"]
            activity_type = activity["activityType"]["typeKey"]
            start_time = datetime.fromisoformat(activity["startTimeLocal"].replace("Z", "+00:00"))
            filename = f"{output_dir}/{start_time.strftime('%Y%m%d_%H%M%S')}_{activity_type}.fit"
            
            logger.info(f"Downloading activity {activity_id} to {filename}")
            
            # Download the activity data (which might be a ZIP file containing the FIT file)
            activity_data = api.download_activity(activity_id, dl_fmt=api.ActivityDownloadFormat.ORIGINAL)
            
            # Check if the data is a ZIP file (common for Garmin Connect downloads)
            if activity_data.startswith(b'PK\x03\x04'):  # ZIP file signature
                logger.info(f"Activity data is a ZIP file, extracting FIT file...")
                if extract_fit_from_zip(activity_data, filename):
                    logger.info(f"Successfully extracted and saved {filename}")
                else:
                    logger.error(f"Failed to extract FIT file from ZIP for activity {activity_id}")
            else:
                # If it's not a ZIP, assume it's a FIT file and save it directly
                with open(filename, "wb") as fit_file:
                    fit_file.write(activity_data)
                logger.info(f"Successfully saved {filename}")
        
        logger.info(f"Downloaded {len(activities)} workouts to the '{output_dir}' directory")
        
    except Exception as err:
        logger.error("Error downloading workouts: %s", err)
        sys.exit(1)

def main():
    """Main function."""
    # Get credentials
    email, password = get_credentials()
    
    # Initialize API
    api = init_api(email, password)
    
    # Download workouts
    download_workouts(api)

if __name__ == "__main__":
    main() 