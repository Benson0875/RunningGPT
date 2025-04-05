import webview
import os
import json
from typing import Dict, Any
from pathlib import Path

class RunningGPTAPI:
    def __init__(self):
        self.window = None
        self.state = {
            'authenticated': False,
            'selected_activity': None,
            'workout_count': 1
        }

    def set_window(self, window):
        """Set the webview window instance"""
        self.window = window

    def authenticate(self, email: str, password: str) -> Dict[str, Any]:
        """Authenticate with Garmin Connect"""
        try:
            # TODO: Implement actual Garmin authentication
            # For now, just simulate authentication
            self.state['authenticated'] = True
            return {'success': True, 'message': 'Authentication successful'}
        except Exception as e:
            return {'success': False, 'message': str(e)}

    def select_activity(self, activity_type: str) -> Dict[str, Any]:
        """Set the selected activity type"""
        self.state['selected_activity'] = activity_type
        return {'success': True, 'activity': activity_type}

    def set_workout_count(self, count: int) -> Dict[str, Any]:
        """Set the number of workouts to analyze"""
        self.state['workout_count'] = count
        return {'success': True, 'count': count}

    def process_workouts(self) -> Dict[str, Any]:
        """Process the selected workouts"""
        try:
            # TODO: Implement actual workout processing
            # For now, just return dummy data
            return {
                'success': True,
                'workouts': [
                    {
                        'date': '2024-03-21',
                        'type': 'Running',
                        'distance': 10.0,
                        'duration': '55:30',
                        'pace': '5:33/km'
                    }
                ]
            }
        except Exception as e:
            return {'success': False, 'message': str(e)}

    def analyze_message(self, message: str) -> Dict[str, Any]:
        """Analyze user message and provide AI response"""
        try:
            # TODO: Implement actual AI analysis
            # For now, just return a dummy response
            return {
                'success': True,
                'response': f"Based on your workouts, here's my analysis of: {message}"
            }
        except Exception as e:
            return {'success': False, 'message': str(e)}

def get_html_path() -> str:
    """Get the absolute path to the HTML file"""
    current_dir = Path(__file__).parent
    html_path = current_dir / 'wizard.html'
    return str(html_path)

def main():
    api = RunningGPTAPI()
    
    # Create window with HTML
    window = webview.create_window(
        'Running Analysis Wizard',
        url=get_html_path(),
        js_api=api,
        width=800,
        height=800,
        resizable=True,
        text_select=True
    )
    api.set_window(window)
    
    # Start the application
    webview.start(debug=True)

if __name__ == '__main__':
    main() 