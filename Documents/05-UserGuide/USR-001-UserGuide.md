# Running Analysis Tool User Guide

## 1. Introduction
The Running Analysis Tool helps runners analyze their workout data by integrating with Garmin Connect. The tool downloads FIT files, converts them to CSV format, and generates detailed workout reports through a three-step process.

## 2. Getting Started

### 2.1 Installation
```bash
# Clone the repository
git clone https://github.com/yourusername/running-analysis-tool.git
cd running-analysis-tool

# Install dependencies
pip install -r requirements.txt
```

### 2.2 Configuration
Create a `.env` file in the project root with your Garmin Connect credentials:
```
GARMIN_USERNAME=your_username
GARMIN_PASSWORD=your_password
```

## 3. Basic Usage

### 3.1 Step 1: Download Workout Data
Use `Get_workouts_data.py` to download your workout data from Garmin Connect:

```bash
# Download recent workouts
python Get_workouts_data.py

# The script will:
# 1. Connect to Garmin Connect using your credentials
# 2. Download FIT files for your workouts
# 3. Save the files in the data directory
```

### 3.2 Step 2: Convert FIT to CSV
Use `decode_fit.py` to convert the downloaded FIT files to CSV format:

```bash
# Convert FIT files to CSV
python decode_fit.py

# The script will:
# 1. Process all FIT files in the data directory
# 2. Convert them to CSV format
# 3. Save the CSV files in the same directory
```

### 3.3 Step 3: Analyze Workouts
Use `analysis_running_CSV.py` to analyze the CSV files and generate reports:

```bash
# Analyze workout data
python analysis_running_CSV.py

# The script will:
# 1. Process all CSV files
# 2. Generate detailed analysis reports
# 3. Create visualization plots
# 4. Save reports and plots in the output directory
```

## 4. Output Files

### 4.1 Generated Files
After running all three scripts, you'll find:
- FIT files: Raw workout data from Garmin Connect
- CSV files: Converted workout data in tabular format
- Text reports: Detailed analysis of each workout
- Plot files: Visualizations of pace, heart rate, and elevation

### 4.2 Report Format
Example workout report:
```
Workout Summary
--------------
Date: [Activity Date]
Distance: [Total Distance] km
Duration: [Total Time]
Average Pace: [Pace] min/km
Average Heart Rate: [HR] bpm
Maximum Heart Rate: [Max HR] bpm
Elevation Gain: [Gain] m

Detailed Analysis:
- Fastest km: [Time] at km [Number]
- Slowest km: [Time] at km [Number]
- Heart Rate Zones Distribution
- Elevation Profile Analysis
```

## 5. Troubleshooting

### 5.1 Common Issues
1. Garmin Connect Access
```bash
# If Get_workouts_data.py fails:
- Check your internet connection
- Verify your Garmin credentials in .env
- Ensure you have proper permissions
```

2. File Processing
```bash
# If decode_fit.py fails:
- Check if FIT files exist in data directory
- Verify file permissions
- Ensure fitparse library is installed

# If analysis_running_CSV.py fails:
- Check if CSV files were generated
- Verify CSV file format
- Check available disk space for outputs
```

### 5.2 Error Messages
- "Authentication failed": Check your Garmin Connect credentials in .env
- "No FIT files found": Run Get_workouts_data.py first
- "Invalid CSV format": Ensure decode_fit.py completed successfully
- "Missing data": Some workout metrics may be unavailable

## 6. Best Practices

### 6.1 Data Management
- Keep the data directory organized
- Backup your FIT and CSV files regularly
- Clean up old files periodically

### 6.2 Processing Tips
- Run the scripts in order:
  1. Get_workouts_data.py
  2. decode_fit.py
  3. analysis_running_CSV.py
- Process new workouts regularly
- Keep your Python environment updated

## 7. Version History
| Version | Date | Description | Author |
|---------|------|-------------|---------|
| 1.0 | 2024-03-20 | Initial user guide | Lead Developer |
| 1.1 | 2024-03-21 | Added Garmin Connect features | Lead Developer |
| 1.2 | 2024-03-21 | Updated workflow with three main scripts | Lead Developer | 