# RunningGPT User Guide

## 1. Introduction
RunningGPT is an intelligent running analysis and coaching application that combines Garmin Connect data with OpenAI's GPT to provide personalized training insights and recommendations. The application features a modern, user-friendly interface that guides you through the process of analyzing your workout data and getting AI-powered coaching.

## 2. Getting Started

### 2.1 Installation
```bash
# Clone the repository
git clone https://github.com/Benson0875/RunningGPT.git
cd RunningGPT

# Create and activate virtual environment
# Windows
python -m venv .venv
.\.venv\Scripts\activate

# Linux/Mac
python -m venv .venv
source .venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```

### 2.2 Configuration
Create a `config.ini` file in the project root with your OpenAI API key:
```ini
[OpenAI]
api_key = YOUR_API_KEY

[App]
model = gpt-4o-2024-08-06
max_tokens = 1000
temperature = 0.7
```

## 3. Running the Application

### 3.1 Normal Mode
Start the application in normal mode to go through the complete workflow:
```bash
python gui/main.py
```

### 3.2 Test Mode
If you want to skip the authentication process and directly view results:
```bash
python gui/main.py --test
```

## 4. Using the Application

### 4.1 Step 1: Authentication
1. Enter your Garmin Connect email and password
2. Click "Connect" to authenticate with Garmin Connect
3. If authentication is successful, you'll proceed to the next step

### 4.2 Step 2: Activity Selection
1. Choose the type of activity you want to analyze:
   - Running
   - Cycling
   - Swimming
2. Click "Next" to proceed

### 4.3 Step 3: Workout Selection
1. Use the slider to select how many recent workouts you want to analyze
2. Click "Process Workouts" to begin downloading and analyzing your data

### 4.4 Step 4: Processing
The application will:
1. Download your workout data from Garmin Connect
2. Convert FIT files to CSV format
3. Generate detailed analysis reports
4. Create visualization plots
5. When processing is complete, you'll automatically move to the results page

### 4.5 Step 5: Results and AI Coaching
The results page displays:
1. **Workout Cards**: Each card shows:
   - Date and activity type
   - Distance and duration
   - Pace and elevation gain
   - Heart rate and cadence metrics
   - Visualization plots
   - Link to detailed report

2. **AI Assistant Chat**:
   - Ask questions about your workouts
   - Get personalized training advice
   - Receive recommendations for improvement
   - Discuss your training goals
   - Get periodized training schedules

## 5. AI Assistant Features

### 5.1 Workout Analysis
The AI Assistant can analyze your workout data and provide insights on:
- Performance trends
- Training patterns
- Recovery needs
- Improvement areas

### 5.2 Training Recommendations
Get personalized recommendations for:
- Training intensity
- Recovery periods
- Race preparation
- Injury prevention

### 5.3 Training Plans
Request comprehensive training plans that include:
- Running workouts
- Rest days
- Gym exercises
- Nutrition guidance

### 5.4 Goal Setting
- Discuss your running goals
- Get advice on realistic targets
- Receive guidance on goal achievement

## 6. Output Files

### 6.1 Generated Files
After processing workouts, you'll find:
- FIT files in the `workouts` directory
- CSV files in the `workouts_csv` directory
- Text reports in the `workout_reports` directory
- Plot files in the `workout_plots` directory

### 6.2 Report Format
Example workout report:
```
Workout Report - 2023-05-15 08:30:45
==================================================

Activity Type: Running
Distance: 10.25 km
Duration: 1:05:30
Pace: 6:23 min/km
Elevation Gain: 120 m
Average Heart Rate: 155 bpm
Maximum Heart Rate: 175 bpm
Average Cadence: 172 spm

Detailed Statistics:
--------------------
Total Distance (meters): 10250
Total Time (seconds): 3930
Average Pace (sec/km): 383
Altitude Difference (Enhanced Estimate): 120
Average Heart Rate: 155
Maximum Heart Rate: 175
Average Cadence: 172
```

## 7. Troubleshooting

### 7.1 Common Issues
1. **Authentication Problems**
   - Verify your Garmin Connect credentials
   - Check your internet connection
   - Ensure you have proper permissions

2. **Processing Errors**
   - Check if FIT files were downloaded successfully
   - Verify file permissions
   - Ensure sufficient disk space

3. **AI Assistant Issues**
   - Verify your OpenAI API key in config.ini
   - Check your internet connection
   - Ensure workout reports are available

### 7.2 Error Messages
- "Authentication failed": Check your Garmin Connect credentials
- "No FIT files found": Run the application again and ensure successful download
- "OpenAI API error": Verify your API key and internet connection
- "Missing data": Some workout metrics may be unavailable

## 8. Best Practices

### 8.1 Data Management
- Keep your workout data organized
- Regularly backup your FIT and CSV files
- Clean up old files periodically

### 8.2 AI Assistant Usage
- Be specific in your questions
- Provide context about your goals
- Ask for clarification when needed
- Use the chat for follow-up questions

## 9. Version History
| Version | Date | Description | Author |
|---------|------|-------------|---------|
| 1.0 | 2025-04-04 | Initial release | Lead Developer |
| 1.1 | 2025-04-05 | Added AI Assistant | Lead Developer |
| 1.2 | 2025-04-06 | Improved GUI and test mode | Lead Developer | 