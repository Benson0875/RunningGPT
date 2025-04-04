from fitparse import FitFile
import os
import pandas as pd
import matplotlib.pyplot as plt
from datetime import datetime

def decode_fit_file(fit_file_path):
    """
    Decode a .fit file and return a pandas DataFrame with the data.
    
    Args:
        fit_file_path (str): Path to the .fit file
        
    Returns:
        pandas.DataFrame: DataFrame containing the decoded data
    """
    # Load the .fit file
    fitfile = FitFile(fit_file_path)
    
    # Get all data messages that are of type "record"
    records = []
    for record in fitfile.get_messages("record"):
        # Get all data for this record
        record_data = {}
        for data in record:
            record_data[data.name] = data.value
        records.append(record_data)
    
    # Convert to DataFrame
    df = pd.DataFrame(records)
    
    # Get activity metadata
    activity_data = {}
    for activity in fitfile.get_messages("activity"):
        for data in activity:
            activity_data[data.name] = data.value
        break  # Only get the first activity message
    
    # Get device info
    device_data = {}
    for device in fitfile.get_messages("device_info"):
        for data in device:
            device_data[data.name] = data.value
        break  # Only get the first device message
    
    return df, activity_data, device_data

def plot_data(df, activity_type):
    """
    Create plots based on the activity type and available data.
    
    Args:
        df (pandas.DataFrame): DataFrame containing the decoded data
        activity_type (str): Type of activity (e.g., 'running', 'cycling')
    """
    # Create a figure with subplots
    fig, axes = plt.subplots(2, 2, figsize=(15, 10))
    fig.suptitle(f'Activity Analysis: {activity_type.capitalize()}', fontsize=16)
    
    # Plot 1: Heart Rate (if available)
    if 'heart_rate' in df.columns:
        axes[0, 0].plot(df['timestamp'], df['heart_rate'])
        axes[0, 0].set_title('Heart Rate Over Time')
        axes[0, 0].set_xlabel('Time')
        axes[0, 0].set_ylabel('Heart Rate (bpm)')
        axes[0, 0].grid(True)
    
    # Plot 2: Speed (if available)
    if 'speed' in df.columns:
        axes[0, 1].plot(df['timestamp'], df['speed'])
        axes[0, 1].set_title('Speed Over Time')
        axes[0, 1].set_xlabel('Time')
        axes[0, 1].set_ylabel('Speed (m/s)')
        axes[0, 1].grid(True)
    
    # Plot 3: Distance (if available)
    if 'distance' in df.columns:
        axes[1, 0].plot(df['timestamp'], df['distance'])
        axes[1, 0].set_title('Distance Over Time')
        axes[1, 0].set_xlabel('Time')
        axes[1, 0].set_ylabel('Distance (m)')
        axes[1, 0].grid(True)
    
    # Plot 4: Cadence (if available)
    if 'cadence' in df.columns:
        axes[1, 1].plot(df['timestamp'], df['cadence'])
        axes[1, 1].set_title('Cadence Over Time')
        axes[1, 1].set_xlabel('Time')
        axes[1, 1].set_ylabel('Cadence (steps/min)')
        axes[1, 1].grid(True)
    
    # Adjust layout
    plt.tight_layout(rect=[0, 0, 1, 0.96])
    
    # Save the figure
    plot_path = os.path.splitext(fit_file_path)[0] + '_analysis.png'
    plt.savefig(plot_path)
    print(f"Plot saved to {plot_path}")
    
    # Show the plot
    plt.show()

def main():
    # Get the directory where the script is located
    script_dir = os.path.dirname(os.path.abspath(__file__))
    
    # Ask for the .fit file path
    fit_file_path = input("Enter the path to the .fit file: ")
    
    # If the path is relative, make it absolute
    if not os.path.isabs(fit_file_path):
        fit_file_path = os.path.join(script_dir, fit_file_path)
    
    # Check if the file exists
    if not os.path.exists(fit_file_path):
        print(f"Error: File '{fit_file_path}' does not exist.")
        return
    
    # Decode the .fit file
    try:
        print(f"Decoding {fit_file_path}...")
        df, activity_data, device_data = decode_fit_file(fit_file_path)
        
        # Print activity metadata
        print("\nActivity Metadata:")
        for key, value in activity_data.items():
            print(f"{key}: {value}")
        
        # Print device info
        print("\nDevice Info:")
        for key, value in device_data.items():
            print(f"{key}: {value}")
        
        # Print DataFrame info
        print(f"\nDataFrame Shape: {df.shape}")
        print("\nDataFrame Columns:")
        for col in df.columns:
            print(f"- {col}")
        
        # Ask if the user wants to save the DataFrame to a CSV file
        save_csv = input("\nDo you want to save the data to a CSV file? (y/n): ")
        if save_csv.lower() == 'y':
            csv_path = os.path.splitext(fit_file_path)[0] + '.csv'
            df.to_csv(csv_path, index=False)
            print(f"Data saved to {csv_path}")
        
        # Ask if the user wants to create plots
        create_plots = input("\nDo you want to create plots? (y/n): ")
        if create_plots.lower() == 'y':
            # Get activity type from metadata or ask the user
            activity_type = activity_data.get('sport', 'unknown')
            if activity_type == 'unknown':
                activity_type = input("Enter the activity type (e.g., running, cycling): ")
            
            # Create plots
            plot_data(df, activity_type)
        
    except Exception as e:
        print(f"Error decoding .fit file: {e}")

if __name__ == "__main__":
    main() 