import os
import configparser
from pathlib import Path
from typing import Dict, List, Optional
from openai import OpenAI

class AIAssistant:
    def __init__(self):
        self.config = self._load_config()
        self.client = OpenAI(api_key=self.config['OpenAI']['api_key'])
        self.conversation_history = []
        self.first_message = True
        self.workout_reports = {}

    def _load_config(self) -> configparser.ConfigParser:
        """Load configuration from config.ini"""
        config = configparser.ConfigParser()
        config_path = Path(__file__).parent.parent / 'config.ini'
        if not config_path.exists():
            raise FileNotFoundError("config.ini not found. Please create it with your OpenAI API key.")
        config.read(config_path)
        return config

    def _load_workout_reports(self) -> Dict[str, str]:
        """Load all workout reports from the workout_reports directory"""
        reports = {}
        reports_dir = Path(__file__).parent.parent / 'workout_reports'
        if reports_dir.exists():
            for file in reports_dir.glob('*.txt'):
                try:
                    with open(file, 'r', encoding='utf-8') as f:
                        reports[file.name] = f.read()
                except Exception as e:
                    print(f"Error reading {file}: {e}")
        return reports

    def _create_system_prompt(self) -> str:
        """Create the system prompt for the AI"""
        return """You are an experienced running coach and training advisor. Your role is to:
1. Analyze the user's workout data and provide personalized insights
2. Answer questions about their training patterns and performance
3. Provide specific, actionable recommendations for improvement
4. Consider factors like pace, distance, heart rate, and recovery patterns
5. Suggest Periodized training schedule, include the running, rest, gym workout, eating plan
6. Be encouraging while maintaining professional expertise
7. If the user do not provide the goal, suggest the goal based on the user's profile and the workout reports.
Base your analysis and advice on the workout reports provided in the conversation context. 請使用台灣在地繁體中文zh-TW 進行對話"""

    def analyze_message(self, user_message: str) -> Dict[str, str]:
        """Process user message and return AI response"""
        try:
            # Load workout reports on first message
            if self.first_message:
                self.workout_reports = self._load_workout_reports()
                context = "\n\n".join(self.workout_reports.values())
                system_message = self._create_system_prompt()
                
                # Add workout data context to conversation
                self.conversation_history = [
                    {"role": "system", "content": system_message},
                    {"role": "system", "content": f"Here are the user's workout reports:\n\n{context}"},
                ]
                self.first_message = False
            
            # Add user message to conversation history
            self.conversation_history.append({"role": "user", "content": user_message})
            
            # Get response from OpenAI
            response = self.client.chat.completions.create(
                model=self.config['App']['model'],
                messages=self.conversation_history,
                max_tokens=int(self.config['App']['max_tokens']),
                temperature=float(self.config['App']['temperature'])
            )
            
            # Extract and store assistant's response
            assistant_message = response.choices[0].message.content
            self.conversation_history.append({"role": "assistant", "content": assistant_message})
            
            return {
                "success": True,
                "response": assistant_message
            }
            
        except Exception as e:
            return {
                "success": False,
                "message": f"Error processing message: {str(e)}"
            }

    def reset_conversation(self):
        """Reset the conversation history and first message flag"""
        self.conversation_history = []
        self.first_message = True
        self.workout_reports = {} 