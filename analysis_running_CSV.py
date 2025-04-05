import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import os
from datetime import datetime

def sec_to_min_sec(sec):
    """Convert seconds to minutes:seconds format"""
    if pd.isna(sec):
        return "N/A"
    minutes = int(sec // 60)
    seconds = int(sec % 60)
    return f"{minutes}:{seconds:02d}"

def format_pace_ticks(x, _):
    """Convert seconds to MM:SS format for y-axis ticks"""
    return sec_to_min_sec(x)

def analyze_csv_file(file_path):
    """Analyze a single CSV file and return the statistics"""
    try:
        # Read CSV file
        df = pd.read_csv(file_path)
        
        # Convert timestamp to datetime
        df['timestamp'] = pd.to_datetime(df['timestamp'])
        
        # Calculate statistics
        stats = {}
        
        # 1. Total distance
        stats['Total Distance (meters)'] = df['distance'].iloc[-1] if 'distance' in df.columns else "N/A"
        
        # 2. Total time
        if 'timestamp' in df.columns:
            total_time = (df['timestamp'].iloc[-1] - df['timestamp'].iloc[0]).total_seconds()
            stats['Total Time (seconds)'] = total_time
        else:
            stats['Total Time (seconds)'] = "N/A"
        
        # 3. Average pace
        if isinstance(stats['Total Distance (meters)'], (int, float)) and isinstance(stats['Total Time (seconds)'], (int, float)):
            avg_pace_sec_per_km = stats['Total Time (seconds)'] / (stats['Total Distance (meters)'] / 1000)
            stats['Average Pace (sec/km)'] = f"{avg_pace_sec_per_km:.1f} ({sec_to_min_sec(avg_pace_sec_per_km)})"
        else:
            stats['Average Pace (sec/km)'] = "N/A"
        
        # 4. Fastest pace
        if 'enhanced_speed' in df.columns:
            # Convert speed (m/s) to pace (min:sec/km)
            # First convert to seconds per kilometer: (1000m/speed) gives seconds for 1km
            # Then convert to minutes:seconds format for display
            df['instant_pace'] = np.where(df['enhanced_speed'] > 0, (1000 / df['enhanced_speed']), np.nan)
            fastest_pace = df['instant_pace'].min()
            stats['Fastest Pace (sec/km)'] = f"{fastest_pace:.1f} ({sec_to_min_sec(fastest_pace)})"
            
            # Add a column for pace in minutes for better readability
            df['instant_pace_min'] = df['instant_pace'] / 60
        else:
            stats['Fastest Pace (sec/km)'] = "N/A"
        
        # 5. Heart rate
        if 'heart_rate' in df.columns:
            stats['Average Heart Rate'] = f"{df['heart_rate'].mean():.1f}"
            stats['Maximum Heart Rate'] = f"{df['heart_rate'].max():.1f}"
        else:
            stats['Average Heart Rate'] = "N/A"
            stats['Maximum Heart Rate'] = "N/A"
        
        # 6. Cadence
        if 'cadence' in df.columns:
            stats['Average Cadence'] = f"{df['cadence'].mean():.1f}"
        else:
            stats['Average Cadence'] = "N/A"
        
        # 7. Altitude
        if 'enhanced_altitude' in df.columns:
            stats['Maximum Altitude'] = f"{df['enhanced_altitude'].max():.1f}"
            stats['Minimum Altitude'] = f"{df['enhanced_altitude'].min():.1f}"
            stats['Altitude Difference (Enhanced Estimate)'] = f"{df['enhanced_altitude'].max() - df['enhanced_altitude'].min():.1f}"
        else:
            stats['Maximum Altitude'] = "N/A"
            stats['Minimum Altitude'] = "N/A"
            stats['Altitude Difference (Enhanced Estimate)'] = "N/A"
        
        return stats, df
        
    except Exception as e:
        print(f"Error analyzing {file_path}: {str(e)}")
        return None, None

def write_analysis_to_file(stats, filename, output_file):
    """Write analysis results to a text file"""
    with open(output_file, 'a', encoding='utf-8') as f:
        # Write header for this file's analysis
        f.write(f"\nAnalysis Results for: {filename}\n")
        f.write("=" * 50 + "\n")
        
        # Write timestamp
        f.write(f"Analysis Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
        f.write("-" * 50 + "\n")
        
        # Write statistics
        for key, value in stats.items():
            f.write(f"{key}: {value}\n")
        
        # Write separator
        f.write("=" * 50 + "\n\n")

def main():
    # Get the CSV directory path
    csv_dir = os.path.join("workouts", "CSV")
    
    # Check if directory exists
    if not os.path.exists(csv_dir):
        print(f"Error: Directory {csv_dir} does not exist!")
        return
    
    # Get all CSV files
    csv_files = [f for f in os.listdir(csv_dir) if f.endswith('.csv')]
    
    if not csv_files:
        print(f"No CSV files found in {csv_dir}")
        return
    
    print(f"Found {len(csv_files)} CSV files to analyze\n")
    
    # Create output text file with timestamp
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    output_file = os.path.join(csv_dir, f"workout_analysis_{timestamp}.txt")
    
    # Write header to the output file
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write("Workout Analysis Report\n")
        f.write("=" * 50 + "\n")
        f.write(f"Generated on: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
        f.write(f"Number of files analyzed: {len(csv_files)}\n")
        f.write("=" * 50 + "\n\n")
    
    # Analyze each file
    for csv_file in csv_files:
        file_path = os.path.join(csv_dir, csv_file)
        print(f"\nAnalyzing: {csv_file}")
        print("-" * 50)
        
        stats, df = analyze_csv_file(file_path)
        
        if stats:
            # Print statistics to console
            for key, value in stats.items():
                print(f"{key}: {value}")
            
            # Write statistics to file
            write_analysis_to_file(stats, csv_file, output_file)
            
            # Create, save and display pace plot
            if df is not None and 'instant_pace' in df.columns:
                fig, ax1 = plt.subplots(figsize=(12, 6))
                
                # Plot pace data
                color_pace = 'tab:blue'
                ax1.set_xlabel('Time')
                ax1.set_ylabel('Instant Pace (min:sec/km)', color=color_pace)
                # Plot the pace in minutes for better scale
                ax1.plot(df['timestamp'], df['instant_pace_min'], color=color_pace)
                ax1.tick_params(axis='y', labelcolor=color_pace)
                
                # Format y-axis ticks to show MM:SS
                def format_min_pace(x, _):
                    """Convert minutes to MM:SS format for y-axis ticks"""
                    minutes = int(x)
                    seconds = int((x - minutes) * 60)
                    return f"{minutes}:{seconds:02d}"
                
                ax1.yaxis.set_major_formatter(plt.FuncFormatter(format_min_pace))
                
                # Add heart rate if available
                if 'heart_rate' in df.columns:
                    ax2 = ax1.twinx()  # Create second y-axis sharing same x-axis
                    color_hr = 'tab:red'
                    ax2.set_ylabel('Heart Rate (bpm)', color=color_hr)
                    ax2.plot(df['timestamp'], df['heart_rate'], color=color_hr)
                    ax2.tick_params(axis='y', labelcolor=color_hr)
                
                plt.title(f'Instant Pace and Heart Rate - {os.path.splitext(csv_file)[0]}')
                plt.grid(True)  # Add grid for better readability
                
                # Rotate x-axis labels for better readability
                plt.xticks(rotation=45)
                
                # Adjust layout to prevent label cutoff
                plt.tight_layout()
                
                # Save plot
                plot_filename = os.path.splitext(csv_file)[0] + '_pace_plot.png'
                plot_path = os.path.join(csv_dir, plot_filename)
                plt.savefig(plot_path)
                print(f"\nPace plot saved as: {plot_filename}")
                
                # Display plot
                plt.show()
                
                # Close the figure to free memory
                plt.close()
        
        print("-" * 50)
    
    print(f"\nAnalysis report saved to: {output_file}")

if __name__ == "__main__":
    main() 