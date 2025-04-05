# Function Modification Document: Get_latest_10_workout.py

## Overview
This document outlines the proposed modifications to the Get_latest_10_workout.py script to enhance its functionality with user interaction and specific workout type filtering.

## Current vs. New Functionality

### Current Functionality
- Gets the latest 10 workouts from Garmin Connect
- Downloads all workout types without filtering
- No user interaction for workout type or count selection

### New Functionality
- Interactive workout type selection (Run, Cycling, Swim)
- Customizable number of workouts to retrieve (1-20)
- Input validation for user selections
- Downloads workouts to /workouts folder by type

## Detailed Modifications

### 1. Add Workout Type Selection
```python
WORKOUT_TYPES = {
    1: "Run",
    2: "Cycling", 
    3: "Swim"
}

def get_workout_type():
    """Get workout type from user input."""
    print("\nSelect workout type:")
    for key, value in WORKOUT_TYPES.items():
        print(f"{key}. {value}")
    
    while True:
        try:
            choice = int(input("\nEnter your choice (1-3): "))
            if choice in WORKOUT_TYPES:
                return WORKOUT_TYPES[choice]
            print("Error: Please select a number between 1 and 3")
        except ValueError:
            print("Error: Please enter a valid number")
```

### 2. Add Workout Count Selection
```python
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
```

### 3. Modify Main Function
```python
def main():
    """Main function with new workflow."""
    # Initialize Garmin client and login
    client = ... # existing initialization code
    
    # Get user selections
    workout_type = get_workout_type()
    workout_count = get_workout_count()
    
    # Create workouts directory if it doesn't exist
    os.makedirs("workouts", exist_ok=True)
    
    # Get activities filtered by type
    activities = client.get_activities(0, workout_count)
    filtered_activities = [
        activity for activity in activities 
        if activity["activityType"]["typeKey"].lower() == workout_type.lower()
    ]
    
    # Download filtered activities
    for activity in filtered_activities[:workout_count]:
        activity_id = activity["activityId"]
        filename = f"workouts/{workout_type}_{activity_id}.fit"
        client.download_activity(activity_id, filename)
        print(f"Downloaded {workout_type} activity {activity_id}")
```

## Error Handling

### Input Validation
- Workout Type Selection:
  - Must be integer between 1-3
  - Invalid input prompts re-entry
  - Non-numeric input handled gracefully

- Workout Count Selection:
  - Must be integer between 1-20
  - Invalid input prompts re-entry
  - Non-numeric input handled gracefully

### File Operations
- Create workouts directory if not exists
- Handle file write permissions
- Handle download failures

## Implementation Notes

1. **Directory Structure**
   ```
   /workouts/
   ├── Run_[activity_id].fit
   ├── Cycling_[activity_id].fit
   └── Swim_[activity_id].fit
   ```

2. **Activity Type Mapping**
   - Ensure Garmin Connect activity types match our simplified categories
   - Map various Garmin activity subtypes to main categories

3. **File Naming Convention**
   - Format: `[workout_type]_[activity_id].fit`
   - Example: `Run_12345678.fit`

## Testing Recommendations

1. **Input Validation Testing**
   - Test boundary values (0, 1, 20, 21)
   - Test non-numeric inputs
   - Test special characters

2. **Workout Type Testing**
   - Test each workout type selection
   - Verify correct filtering
   - Test case sensitivity

3. **File Operation Testing**
   - Test with existing directory
   - Test with write permissions
   - Test with network interruptions

## Future Enhancements

1. **Additional Features**
   - Add more workout types
   - Add date range selection
   - Add format selection (FIT, TCX, GPX)

2. **User Experience**
   - Add progress bar for downloads
   - Add summary report
   - Add retry mechanism for failed downloads

## Dependencies
- garminconnect
- os
- sys
- datetime

# Function Modification Document: decode_fit.py

## Overview
Modify decode_fit.py to automatically process all .FIT files in the /workouts directory and save decoded data as CSV files in a /workouts/CSV subdirectory.

## Current vs. New Functionality

### Current Functionality
- Decodes individual .FIT files
- Requires manual file specification
- Outputs to current directory

### New Functionality
- Batch processes all .FIT files in /workouts directory
- Automatically creates /workouts/CSV directory if not exists
- Organizes decoded CSV files in dedicated subdirectory
- Maintains workout type categorization in CSV filenames

## Detailed Modifications

### 1. Add Directory Management
```python
def ensure_output_directory():
    """Create CSV output directory if it doesn't exist."""
    csv_dir = os.path.join("workouts", "CSV")
    if not os.path.exists(csv_dir):
        os.makedirs(csv_dir)
    return csv_dir

def get_fit_files():
    """Get list of all .FIT files in workouts directory."""
    workouts_dir = "workouts"
    if not os.path.exists(workouts_dir):
        logger.error(f"Workouts directory '{workouts_dir}' not found")
        return []
    
    return [f for f in os.listdir(workouts_dir) 
            if f.lower().endswith('.fit') and os.path.isfile(os.path.join(workouts_dir, f))]
```

### 2. Modify Main Processing Function
```python
def process_fit_files():
    """Process all FIT files in workouts directory."""
    # Ensure output directory exists
    csv_dir = ensure_output_directory()
    
    # Get list of FIT files
    fit_files = get_fit_files()
    if not fit_files:
        logger.info("No .FIT files found in workouts directory")
        return
    
    logger.info(f"Found {len(fit_files)} .FIT files to process")
    
    # Process each file
    for fit_file in fit_files:
        input_path = os.path.join("workouts", fit_file)
        output_file = fit_file.replace('.fit', '.csv')
        output_path = os.path.join(csv_dir, output_file)
        
        try:
            decode_fit_file(input_path, output_path)
            logger.info(f"Successfully decoded {fit_file} to {output_file}")
        except Exception as e:
            logger.error(f"Error processing {fit_file}: {e}")
```

### 3. Update File Naming Convention
- Input: `workouts/[workout_type]_[activity_id].fit`
- Output: `workouts/CSV/[workout_type]_[activity_id].csv`

### 4. Error Handling
- Directory creation errors
- File read/write permissions
- Invalid .FIT file format
- CSV conversion errors

## Implementation Notes

1. **Directory Structure**
   ```
   /workouts/
   ├── running_12345678.fit
   ├── cycling_87654321.fit
   ├── swimming_11223344.fit
   └── CSV/
       ├── running_12345678.csv
       ├── cycling_87654321.csv
       └── swimming_11223344.csv
   ```

2. **File Processing**
   - Preserve original file names (just change extension)
   - Skip already processed files (optional)
   - Handle large files efficiently

3. **CSV Format**
   - Maintain all relevant workout data
   - Include headers for data columns
   - Use consistent date/time formats

## Testing Recommendations

1. **Directory Testing**
   - Test with missing /workouts directory
   - Test with missing /workouts/CSV directory
   - Test with write permission issues

2. **File Processing Testing**
   - Test with various .FIT file types
   - Test with corrupted .FIT files
   - Test with empty .FIT files
   - Test with large .FIT files

3. **Output Validation**
   - Verify CSV format correctness
   - Verify data accuracy
   - Verify file naming consistency

## Future Enhancements

1. **Processing Options**
   - Add command line arguments for:
     - Custom input/output directories
     - File overwrite options
     - Specific file selection
     - CSV format options

2. **Data Analysis**
   - Add basic statistics generation
   - Add data visualization options
   - Add workout summary reports

3. **Performance**
   - Add parallel processing for multiple files
   - Add progress bar for batch processing
   - Add memory usage optimization

## Dependencies
- fitparse
- pandas
- os
- logging
- sys 