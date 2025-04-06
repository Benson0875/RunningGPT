import os
import json
import logging
from datetime import datetime
from pathlib import Path
from typing import Dict, Any, List, Optional

import webview
import pandas as pd
import matplotlib.pyplot as plt

# Add the project root to Python path for imports
import sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from gui.ai_assistant import AIAssistant

# Get the absolute path to the log file
log_file = Path(__file__).parent.parent / 'running_gpt.log'
log_file = str(log_file.absolute())

# Configure logging
logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler(log_file, mode='w'),  # Use absolute path and overwrite existing file
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

# Import existing functionality
from garminconnect import (
    Garmin,
    GarminConnectAuthenticationError,
    GarminConnectConnectionError,
    GarminConnectTooManyRequestsError
)
from decode_fit import decode_fit_file
from Get_workouts_data import init_api, download_workouts
from analysis_running_CSV import analyze_csv_file

# Global state
state = {
    'authenticated': False,
    'selected_activity': None,
    'workout_count': 1,
    'client': None,
    'workouts_data': None,
    'ai_assistant': None
}

def authenticate(email: str, password: str) -> Dict[str, Any]:
    """Authenticate with Garmin Connect using provided credentials"""
    try:
        logger.info("Starting authentication process with provided credentials")
        
        # Initialize API client with provided credentials
        logger.debug("Initializing Garmin API client...")
        state['client'] = init_api(email, password)
        
        logger.info("Authentication successful - API client initialized")
        state['authenticated'] = True
        return {'success': True, 'message': 'Authentication successful'}
    except GarminConnectAuthenticationError as e:
        logger.error(f"Authentication failed - Invalid credentials: {str(e)}")
        return {'success': False, 'message': 'Invalid email or password'}
    except GarminConnectConnectionError as e:
        logger.error(f"Authentication failed - Connection error: {str(e)}")
        return {'success': False, 'message': 'Connection failed. Please check your internet connection.'}
    except GarminConnectTooManyRequestsError as e:
        logger.error(f"Authentication failed - Too many requests: {str(e)}")
        return {'success': False, 'message': 'Too many login attempts. Please try again later.'}
    except Exception as e:
        logger.error(f"Authentication failed - Unexpected error: {str(e)}", exc_info=True)
        return {'success': False, 'message': f'Authentication failed: {str(e)}'}

def select_activity(activity_type: str) -> Dict[str, Any]:
    """Set the selected activity type"""
    try:
        if not state['authenticated']:
            return {'success': False, 'message': 'Please authenticate first'}
        
        # Convert activity type to match Garmin Connect's format
        activity_map = {
            'Running': 'running',
            'Cycling': 'cycling',
            'Swimming': 'swimming'
        }
        activity_type = activity_map.get(activity_type, activity_type.lower())
        state['selected_activity'] = activity_type
        return {'success': True, 'activity': activity_type}
    except Exception as e:
        return {'success': False, 'message': str(e)}

def set_workout_count(count: int) -> Dict[str, Any]:
    """Set the number of workouts to analyze"""
    try:
        state['workout_count'] = count
        return {'success': True, 'count': count}
    except Exception as e:
        return {'success': False, 'message': str(e)}

def process_workouts() -> Dict[str, Any]:
    """Process the selected workouts"""
    try:
        if not state['authenticated']:
            return {'success': False, 'message': 'Please authenticate first'}

        if not state['selected_activity']:
            return {'success': False, 'message': 'Please select an activity type'}

        # Download workouts using existing functionality
        download_workouts(
            state['client'],
            state['selected_activity'],
            state['workout_count']
        )

        # Process downloaded workouts
        processed_workouts = []
        workouts_dir = "workouts"
        output_dir = "workouts_csv"
        plots_dir = "workout_plots"
        reports_dir = "workout_reports"
        
        # Create output directories if they don't exist
        for directory in [output_dir, plots_dir, reports_dir]:
            os.makedirs(directory, exist_ok=True)
        
        # Get list of downloaded workout files
        workout_files = [
            f for f in os.listdir(workouts_dir)
            if f.startswith(f"{state['selected_activity']}_") and f.endswith('.fit')
        ]
        
        # Sort by most recent first (based on filename timestamp)
        workout_files.sort(reverse=True)
        
        # Process each workout file
        for fit_file in workout_files[:state['workout_count']]:
            fit_path = os.path.join(workouts_dir, fit_file)
            csv_path = os.path.join(output_dir, fit_file.replace('.fit', '.csv'))
            plot_path = os.path.join(plots_dir, fit_file.replace('.fit', '.png'))
            report_path = os.path.join(reports_dir, fit_file.replace('.fit', '.txt'))
            
            # Decode FIT file to CSV
            try:
                logger.info(f"Decoding FIT file: {fit_file}")
                decode_fit_file(fit_path, csv_path)
                
                # Analyze the workout data
                stats, df = analyze_csv_file(csv_path)
                
                # Extract activity ID and get activity details
                activity_id = fit_file.split('_')[1].split('.')[0]
                activity_details = state['client'].get_activity_details(activity_id)
                
                if stats and not df.empty:
                    # Get start time from FIT file if not available in activity details
                    start_time = None
                    if 'startTimeLocal' in activity_details:
                        start_time = datetime.fromisoformat(activity_details['startTimeLocal'].replace('Z', '+00:00'))
                    elif 'timestamp' in df.columns:
                        start_time = pd.to_datetime(df['timestamp'].iloc[0])
                    
                    if start_time:
                        # Get correct distance and duration from stats
                        total_distance = float(stats.get('Total Distance (meters)', 0)) / 1000  # Convert to km
                        total_duration = float(stats.get('Total Time (seconds)', 0))
                        
                        # Format duration for display (convert to minutes)
                        duration_minutes = total_duration / 60
                        hours = int(duration_minutes // 60)
                        minutes = int(duration_minutes % 60)
                        seconds = int((duration_minutes * 60) % 60)
                        
                        if hours > 0:
                            duration_display = f"{hours}:{minutes:02d}:{seconds:02d}"
                        else:
                            duration_display = f"{minutes}:{seconds:02d}"
                        
                        # Generate workout report
                        with open(report_path, 'w') as f:
                            f.write(f"Workout Report - {start_time.strftime('%Y-%m-%d %H:%M:%S')}\n")
                            f.write("=" * 50 + "\n\n")
                            f.write(f"Activity Type: {state['selected_activity'].capitalize()}\n")
                            f.write(f"Distance: {total_distance:.2f} km\n")
                            f.write(f"Duration: {duration_display}\n")
                            f.write(f"Pace: {stats.get('Average Pace (sec/km)', 'N/A')}\n")
                            f.write(f"Elevation Gain: {stats.get('Altitude Difference (Enhanced Estimate)', 0)} m\n")
                            f.write(f"Average Heart Rate: {stats.get('Average Heart Rate', 0)} bpm\n")
                            f.write(f"Maximum Heart Rate: {stats.get('Maximum Heart Rate', 0)} bpm\n")
                            f.write(f"Average Cadence: {stats.get('Average Cadence', 0)} spm\n\n")
                            f.write("Detailed Statistics:\n")
                            f.write("-" * 20 + "\n")
                            for key, value in stats.items():
                                f.write(f"{key}: {value}\n")
                        
                        # Generate plots
                        plt.figure(figsize=(15, 10))
                        
                        # Plot 1: Heart Rate over Distance
                        plt.subplot(2, 2, 1)
                        plt.plot(df['distance'] / 1000, df['heart_rate'], 'r-')
                        plt.title('Heart Rate vs Distance')
                        plt.xlabel('Distance (km)')
                        plt.ylabel('Heart Rate (bpm)')
                        plt.grid(True)
                        
                        # Plot 2: Pace over Distance
                        plt.subplot(2, 2, 2)
                        pace = 1000 / (df['enhanced_speed'] * 3.6)  # Convert speed to min/km
                        plt.plot(df['distance'] / 1000, pace, 'b-')
                        plt.title('Pace vs Distance')
                        plt.xlabel('Distance (km)')
                        plt.ylabel('Pace (min/km)')
                        plt.grid(True)
                        
                        # Plot 3: Elevation Profile
                        plt.subplot(2, 2, 3)
                        plt.plot(df['distance'] / 1000, df['enhanced_altitude'], 'g-')
                        plt.title('Elevation Profile')
                        plt.xlabel('Distance (km)')
                        plt.ylabel('Elevation (m)')
                        plt.grid(True)
                        
                        # Plot 4: Cadence over Distance
                        plt.subplot(2, 2, 4)
                        plt.plot(df['distance'] / 1000, df['cadence'], 'm-')
                        plt.title('Cadence vs Distance')
                        plt.xlabel('Distance (km)')
                        plt.ylabel('Cadence (spm)')
                        plt.grid(True)
                        
                        plt.tight_layout()
                        plt.savefig(plot_path)
                        plt.close()
                        
                        processed_workouts.append({
                            'date': start_time.strftime('%Y-%m-%d'),
                            'type': state['selected_activity'].capitalize(),
                            'distance': total_distance,
                            'duration': duration_display,
                            'pace': stats.get('Average Pace (sec/km)', 'N/A').split('(')[1].strip(')'),
                            'elevation_gain': float(stats.get('Altitude Difference (Enhanced Estimate)', 0)),
                            'average_hr': float(stats.get('Average Heart Rate', 0)),
                            'max_hr': float(stats.get('Maximum Heart Rate', 0)),
                            'cadence': float(stats.get('Average Cadence', 0)),
                            'plot_path': plot_path,
                            'report_path': report_path
                        })
                        logger.info(f"Successfully processed workout: {fit_file}")
                    else:
                        logger.warning(f"No start time available for workout: {fit_file}")
                else:
                    logger.warning(f"No stats available for workout: {fit_file}")
            except Exception as e:
                logger.error(f"Error processing workout {fit_file}: {str(e)}", exc_info=True)
                continue

        state['workouts_data'] = processed_workouts
        return {'success': True, 'workouts': processed_workouts}
    except Exception as e:
        logger.error(f"Error in process_workouts: {str(e)}", exc_info=True)
        return {'success': False, 'message': str(e)}

def analyze_message(message: str) -> Dict[str, Any]:
    """Analyze user message and provide AI response"""
    try:
        logger.info(f"=== Analyzing message: {message} ===")
        
        if not state.get('workouts_data'):
            logger.error("No workout data available in state")
            return {'success': False, 'message': 'No workout data available for analysis'}

        # Initialize AI Assistant if not already done
        if state.get('ai_assistant') is None:
            logger.info("Initializing AI Assistant for the first time")
            try:
                state['ai_assistant'] = AIAssistant()
                logger.info("AI Assistant initialized successfully")
            except Exception as e:
                logger.error(f"Failed to initialize AI Assistant: {str(e)}", exc_info=True)
                return {'success': False, 'message': f"Failed to initialize AI Assistant: {str(e)}"}

        # Process message and get response
        logger.info("Sending message to AI Assistant")
        try:
            result = state['ai_assistant'].analyze_message(message)
            if result['success']:
                logger.info("Successfully got response from AI Assistant")
                logger.debug(f"Response: {result['response']}")
            else:
                logger.error(f"AI Assistant error: {result.get('message', 'Unknown error')}")
            return result
        except Exception as e:
            logger.error(f"Error in AI Assistant analyze_message: {str(e)}", exc_info=True)
            return {'success': False, 'message': f"Error in AI analysis: {str(e)}"}

    except Exception as e:
        logger.error(f"Error in analyze_message: {str(e)}", exc_info=True)
        return {'success': False, 'message': str(e)}

def get_html_path() -> str:
    """Get the absolute path to the HTML file"""
    current_dir = Path(__file__).parent
    html_path = current_dir / 'wizard.html'
    return str(html_path)

# Define API class at module level
class API:
    def authenticate(self, email: str, password: str) -> Dict[str, Any]:
        return authenticate(email, password)
    
    def select_activity(self, activity_type: str) -> Dict[str, Any]:
        return select_activity(activity_type)
    
    def set_workout_count(self, count: int) -> Dict[str, Any]:
        return set_workout_count(count)
    
    def process_workouts(self) -> Dict[str, Any]:
        return process_workouts()
    
    def analyze_message(self, message: str) -> Dict[str, Any]:
        return analyze_message(message)

    def read_report_file(self, filename: str) -> Dict[str, Any]:
        """Read the contents of a report file"""
        try:
            report_path = os.path.join('workout_reports', filename)
            if not os.path.exists(report_path):
                return {'success': False, 'message': f'Report file not found: {filename}'}
            
            with open(report_path, 'r', encoding='utf-8') as f:
                content = f.read()
            return {'success': True, 'content': content}
        except Exception as e:
            logger.error(f"Error reading report file: {str(e)}")
            return {'success': False, 'message': str(e)}

    def read_plot_file(self, filename: str) -> Dict[str, Any]:
        """Read a plot file and return it as base64 encoded data"""
        try:
            plot_path = os.path.join('workout_plots', filename)
            if not os.path.exists(plot_path):
                return {'success': False, 'message': f'Plot file not found: {filename}'}
            
            with open(plot_path, 'rb') as f:
                import base64
                plot_data = base64.b64encode(f.read()).decode('utf-8')
            return {'success': True, 'data': plot_data}
        except Exception as e:
            logger.error(f"Error reading plot file: {str(e)}")
            return {'success': False, 'message': str(e)}

    def get_processed_workouts(self) -> Dict[str, Any]:
        """Get already processed workout data"""
        try:
            processed_workouts = []
            # 从 workout_reports 目录读取所有报告
            reports_dir = Path('workout_reports')
            for report_file in reports_dir.glob('*.txt'):
                try:
                    # 获取对应的 plot 文件
                    plot_file = Path('workout_plots') / f"{report_file.stem}.png"
                    
                    # 从报告文件中提取数据
                    with open(report_file, 'r', encoding='utf-8') as f:
                        content = f.read()
                        
                    # 解析报告内容
                    lines = content.split('\n')
                    date = lines[0].split(' - ')[1].split()[0]
                    activity_type = lines[3].split(': ')[1]
                    distance = float(lines[4].split(': ')[1].replace('km', ''))
                    duration = lines[5].split(': ')[1]
                    pace = lines[6].split(': ')[1].split('(')[1].strip(')')
                    elevation_gain = float(lines[7].split(': ')[1].replace('m', ''))
                    avg_hr = float(lines[8].split(': ')[1].replace('bpm', ''))
                    max_hr = float(lines[9].split(': ')[1].replace('bpm', ''))
                    cadence = float(lines[10].split(': ')[1].replace('spm', ''))
                    
                    processed_workouts.append({
                        'date': date,
                        'type': activity_type,
                        'distance': distance,
                        'duration': duration,
                        'pace': pace,
                        'elevation_gain': elevation_gain,
                        'average_hr': avg_hr,
                        'max_hr': max_hr,
                        'cadence': cadence,
                        'plot_path': str(plot_file),
                        'report_path': str(report_file)
                    })
                except Exception as e:
                    logger.error(f"Error processing report {report_file}: {e}")
                    continue
                
            return {
                'success': True,
                'workouts': processed_workouts
            }
        except Exception as e:
            logger.error(f"Error getting processed workouts: {e}")
            return {
                'success': False,
                'message': str(e)
            }

def main():
    """Main entry point for the GUI application"""
    try:
        # Create output directories if they don't exist
        for directory in ['workouts', 'workouts_csv', 'workout_plots', 'workout_reports']:
            os.makedirs(directory, exist_ok=True)

        # Create API instance
        api = API()

        # Configure webview window
        debug = '--debug' in sys.argv
        test_mode = '--test' in sys.argv  # 添加测试模式标志
        html_path = os.path.join(os.path.dirname(__file__), 'wizard.html')
        
        if not os.path.exists(html_path):
            raise FileNotFoundError(f"HTML file not found at {html_path}")
            
        logger.info(f"Starting webview with HTML file: {html_path}")
        
        window = webview.create_window(
            'RunningGPT',
            html_path,
            js_api=api,
            width=800,
            height=900,
            min_size=(800, 600),
            text_select=True,
            confirm_close=True,
            frameless=False
        )
            
        if test_mode:
            def init_test_mode():
                logger.info("=== Initializing test mode state ===")
                try:
                    # 获取训练数据
                    logger.info("Loading workout data")
                    result = api.get_processed_workouts()
                    if result['success']:
                        state['workouts_data'] = result['workouts']
                        logger.info(f"Successfully loaded {len(result['workouts'])} workouts")
                        
                        # 预初始化 AI Assistant
                        logger.info("Pre-initializing AI Assistant")
                        try:
                            state['ai_assistant'] = AIAssistant()
                            logger.info("AI Assistant pre-initialized successfully")
                        except Exception as e:
                            logger.error(f"Failed to pre-initialize AI Assistant: {str(e)}", exc_info=True)
                    else:
                        logger.error(f"Failed to load workouts: {result.get('message', 'Unknown error')}")
                except Exception as e:
                    logger.error(f"Error in init_test_mode: {str(e)}", exc_info=True)

            # 在窗口加载完成后执行 JavaScript
            def on_loaded():
                logger.info("=== Test mode: Window loaded ===")
                # 初始化状态
                init_test_mode()
                
                logger.info("Executing JavaScript")
                js_code = """
                    console.log('Test mode JavaScript executing');
                    
                    // Hide all steps
                    document.querySelectorAll('.step-content > div').forEach(div => {
                        div.style.display = 'none';
                        console.log('Hidden div:', div.className);
                    });
                    
                    // Show results
                    const resultsDiv = document.querySelector('.results');
                    if (resultsDiv) {
                        console.log('Showing results div');
                        resultsDiv.style.display = 'block';
                    } else {
                        console.error('Results div not found');
                    }
                    
                    // Update progress dots
                    document.querySelectorAll('.step').forEach((dot, index) => {
                        if (index === 4) {
                            dot.classList.add('active');
                            console.log('Activated step 5 dot');
                        } else {
                            dot.classList.remove('active');
                        }
                    });

                    // Load workout data
                    console.log('Fetching workout data...');
                    window.pywebview.api.get_processed_workouts().then(result => {
                        console.log('get_processed_workouts result:', result);
                        if (result.success) {
                            console.log(`Found ${result.workouts.length} workouts`);
                            updateWorkoutCards(result.workouts);
                        } else {
                            console.error('Failed to get workouts:', result.message);
                        }
                    }).catch(error => {
                        console.error('Error fetching workouts:', error);
                    });
                """
                window.evaluate_js(js_code)
                logger.info("Test mode: JavaScript executed")
            
            window.events.loaded += on_loaded
            logger.info("Test mode: Added loaded event handler")
        
        webview.start(debug=debug)
        
    except Exception as e:
        logger.error(f"Error in main: {str(e)}", exc_info=True)

if __name__ == '__main__':
    main() 