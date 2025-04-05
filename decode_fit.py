from fitparse import FitFile
import os
import pandas as pd
import matplotlib.pyplot as plt
from datetime import datetime
import logging

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

def ensure_output_directory():
    """Create CSV output directory if it doesn't exist."""
    csv_dir = os.path.join("workouts", "CSV")
    if not os.path.exists(csv_dir):
        os.makedirs(csv_dir)
        logger.info(f"Created output directory: {csv_dir}")
    return csv_dir

def get_fit_files():
    """Get list of all .FIT files in workouts directory."""
    workouts_dir = "workouts"
    if not os.path.exists(workouts_dir):
        logger.error(f"Workouts directory '{workouts_dir}' not found")
        return []
    
    fit_files = [f for f in os.listdir(workouts_dir) 
                 if f.lower().endswith('.fit') and os.path.isfile(os.path.join(workouts_dir, f))]
    logger.info(f"Found {len(fit_files)} .FIT files in {workouts_dir}")
    return fit_files

def decode_fit_file(input_path, output_path):
    """
    Decode a .fit file and save as CSV.
    
    Args:
        input_path (str): Path to the input .fit file
        output_path (str): Path where to save the CSV file
        
    Returns:
        pd.DataFrame: DataFrame containing the decoded data
    """
    logger.debug(f"Starting to decode FIT file: {input_path}")
    
    try:
        # Load the .fit file
        logger.debug("Creating FitFile object")
        fitfile = FitFile(input_path)
        
        # Get all data messages that are of type "record"
        logger.debug("Getting record messages")
        records = []
        for record in fitfile.get_messages("record"):
            # Get all data for this record
            record_data = {}
            for data in record:
                record_data[data.name] = data.value
            records.append(record_data)
        
        logger.debug(f"Found {len(records)} record messages")
        
        # Convert to DataFrame
        df = pd.DataFrame(records)
        logger.debug(f"Created DataFrame with columns: {df.columns.tolist()}")
        
        if len(df) == 0:
            logger.warning("No records found in FIT file, creating empty DataFrame")
            df = pd.DataFrame(columns=['timestamp', 'distance', 'heart_rate', 'cadence', 'enhanced_speed', 'enhanced_altitude'])
        
        # Get activity metadata
        logger.debug("Getting activity metadata")
        activity_data = {}
        for activity in fitfile.get_messages("activity"):
            for data in activity:
                activity_data[f'activity_{data.name}'] = [data.value] * len(df)
            break  # Only get the first activity message
        
        # Get device info
        logger.debug("Getting device info")
        device_data = {}
        for device in fitfile.get_messages("device_info"):
            for data in device:
                device_data[f'device_{data.name}'] = [data.value] * len(df)
            break  # Only get the first device message
        
        # Add metadata as columns
        logger.debug("Adding metadata columns")
        for key, value in activity_data.items():
            df[key] = value
        for key, value in device_data.items():
            df[key] = value
        
        # Save to CSV
        logger.debug(f"Saving DataFrame to CSV: {output_path}")
        df.to_csv(output_path, index=False)
        logger.info(f"Successfully decoded FIT file and saved to {output_path}")
        
        return df
        
    except Exception as e:
        logger.error(f"Error decoding FIT file: {str(e)}")
        logger.error(f"Error type: {type(e)}")
        raise

def process_fit_files():
    """Process all FIT files in workouts directory."""
    # Ensure output directory exists
    csv_dir = ensure_output_directory()
    
    # Get list of FIT files
    fit_files = get_fit_files()
    if not fit_files:
        logger.info("No .FIT files found in workouts directory")
        return
    
    # Process each file
    for fit_file in fit_files:
        input_path = os.path.join("workouts", fit_file)
        output_file = fit_file.replace('.fit', '.csv')
        output_path = os.path.join(csv_dir, output_file)
        
        try:
            logger.info(f"Processing {fit_file}...")
            decode_fit_file(input_path, output_path)
            logger.info(f"Successfully decoded {fit_file} to {output_file}")
        except Exception as e:
            logger.error(f"Error processing {fit_file}: {e}")
            continue

def main():
    """Main function to process all FIT files."""
    try:
        logger.info("Starting FIT file processing")
        process_fit_files()
        logger.info("Completed processing all FIT files")
    except Exception as e:
        logger.error(f"An error occurred during processing: {e}")

if __name__ == "__main__":
    main() 