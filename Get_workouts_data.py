#!/usr/bin/env python3
"""
Download workouts from Garmin Connect and save them as .FIT files.
Allows selecting specific workout types (Run, Cycling, Swim) and customizing the number of workouts to download.

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

# Define workout types
WORKOUT_TYPES = {
    1: "running",
    2: "cycling", 
    3: "swimming"
}

def get_workout_type():
    """Get workout type from user input."""
    print("\nSelect workout type:")
    for key, value in WORKOUT_TYPES.items():
        print(f"{key}. {value.capitalize()}")
    
    while True:
        try:
            choice = int(input("\nEnter your choice (1-3): "))
            if choice in WORKOUT_TYPES:
                return WORKOUT_TYPES[choice]
            print("Error: Please select a number between 1 and 3")
        except ValueError:
            print("Error: Please enter a valid number")

def get_workout_count():
    """Get number of workouts to retrieve."""
    while True:
        try:
            count = int(input("\nHow many workouts do you want to get? (1-20): "))
            if 1 <= count <= 20:
                return count
            print("Error: Please enter a number between 1 and 20")
        except ValueError:
            print("Error: Please enter a valid number")

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
    """
    Initialize the Garmin Connect API.
    
    Args:
        email (str): Garmin Connect email
        password (str): Garmin Connect password
        
    Returns:
        Garmin: Authenticated Garmin Connect client
        
    Raises:
        GarminConnectAuthenticationError: If authentication fails
        GarminConnectConnectionError: If connection fails
        GarminConnectTooManyRequestsError: If too many requests
        Exception: For other errors
    """
    try:
        api = Garmin(email, password)
        api.login()
        return api
    except (GarminConnectAuthenticationError, 
            GarminConnectConnectionError,
            GarminConnectTooManyRequestsError,
            Exception) as err:
        logger.error("Error initializing Garmin Connect API: %s", err)
        if 'pytest' not in sys.modules:
            sys.exit(1)
        raise

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

def download_workouts(api, workout_type, workout_count):
    """
    Download the specified number of workouts of a given type and save them as .FIT files.
    
    Args:
        api: Garmin Connect API client
        workout_type (str): Type of workout to download (running, cycling, swimming)
        workout_count (int): Number of workouts to download
        
    Returns:
        int: Number of workouts successfully downloaded
    """
    try:
        # Get activities with a buffer (3x requested count) to ensure we find enough of the right type
        buffer_count = workout_count * 3
        activities = api.get_activities(0, buffer_count)
        
        # Filter activities by type
        filtered_activities = [
            activity for activity in activities 
            if activity["activityType"]["typeKey"].lower() == workout_type
        ]

        if not filtered_activities:
            logger.error(f"No {workout_type} activities found in the last {buffer_count} activities")
            return 0

        # Take only the requested number of activities
        activities_to_download = filtered_activities[:workout_count]
        
        # Create a directory for the workouts if it doesn't exist
        output_dir = "workouts"
        if not os.path.exists(output_dir):
            os.makedirs(output_dir)
        
        # Download each activity
        downloaded_count = 0
        for activity in activities_to_download:
            activity_id = activity["activityId"]
            start_time = datetime.fromisoformat(activity["startTimeLocal"].replace("Z", "+00:00"))
            filename = f"{output_dir}/{workout_type}_{activity_id}.fit"
            
            logger.info(f"Downloading {workout_type} activity {activity_id} to {filename}")
            
            try:
                # Download the activity data
                activity_data = api.download_activity(activity_id, dl_fmt=api.ActivityDownloadFormat.ORIGINAL)
                
                # Check if the data is a ZIP file
                if activity_data.startswith(b'PK\x03\x04'):
                    logger.info(f"Activity data is a ZIP file, extracting FIT file...")
                    if extract_fit_from_zip(activity_data, filename):
                        logger.info(f"Successfully extracted and saved {filename}")
                        downloaded_count += 1
                    else:
                        logger.error(f"Failed to extract FIT file from ZIP for activity {activity_id}")
                else:
                    # Save FIT file directly
                    with open(filename, "wb") as fit_file:
                        fit_file.write(activity_data)
                    logger.info(f"Successfully saved {filename}")
                    downloaded_count += 1
            except Exception as e:
                logger.error(f"Error downloading activity {activity_id}: {e}")
                continue
        
        logger.info(f"Successfully downloaded {downloaded_count} {workout_type} workouts to the '{output_dir}' directory")
        return downloaded_count
        
    except Exception as err:
        logger.error("Error downloading workouts: %s", err)
        return 0

def main():
    """Main function."""
    # Get credentials and initialize API
    email, password = get_credentials()
    api = init_api(email, password)
    
    # Get user selections
    workout_type = get_workout_type()
    workout_count = get_workout_count()
    
    # Download workouts
    downloaded_count = download_workouts(api, workout_type, workout_count)
    if downloaded_count == 0:
        print("No workouts downloaded. Exiting.")
        sys.exit(1)

if __name__ == "__main__":
    main() 