# RunningGPT Deployment and Operations Guide

## 1. System Requirements

### 1.1 Hardware Requirements
- CPU: 2.0 GHz dual-core processor or better
- RAM: 8GB minimum
- Storage: 1GB free space
- Network: Broadband internet connection
- Display: 1280x720 resolution minimum

### 1.2 Software Requirements
- Python 3.11 or 3.12
- Git version control
- Virtual environment tool (venv)
- Web browser (for GUI interface)

## 2. Installation

### 2.1 Python Environment Setup
```bash
# Clone the repository
git clone https://github.com/Benson0875/RunningGPT.git
cd RunningGPT

# Create virtual environment
python -m venv .venv

# Activate virtual environment
# Windows
.\.venv\Scripts\activate
# Unix/MacOS
source .venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```

### 2.2 Configuration
Create a `config.ini` file in the project root:
```ini
[OpenAI]
api_key = YOUR_API_KEY

[App]
model = gpt-4o-2024-08-06
max_tokens = 1000
temperature = 0.7
```

## 3. Deployment

### 3.1 Directory Structure
```
RunningGPT/
├── gui/
│   ├── main.py
│   ├── wizard.html
│   └── ai_assistant.py
├── workouts/
├── workouts_csv/
├── workout_plots/
├── workout_reports/
├── config.ini
├── requirements.txt
└── .venv/
```

### 3.2 Environment Variables
```bash
# Windows PowerShell
$env:GARMINTOKENS="C:\Users\$env:USERNAME\.garminconnect"

# Linux/macOS
export GARMINTOKENS=~/.garminconnect
```

## 4. Operations

### 4.1 Starting the Application
```bash
# Normal mode
python gui/main.py

# Test mode (skips authentication)
python gui/main.py --test

# Debug mode
python gui/main.py --debug
```

### 4.2 Monitoring
The application logs to `running_gpt.log` in the project root:
```python
# Logging configuration in main.py
logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler(log_file, mode='w'),
        logging.StreamHandler()
    ]
)
```

## 5. Maintenance

### 5.1 Backup Procedures
```bash
# Backup data directories
tar -czf backup_$(date +%Y%m%d).tar.gz workouts/ workouts_csv/ workout_plots/ workout_reports/

# Backup configuration
cp config.ini config.ini.backup
```

### 5.2 Log Rotation
```python
# Log rotation is handled by the application
# Logs are written to running_gpt.log
```

## 6. Troubleshooting

### 6.1 Common Issues
| Issue | Cause | Solution |
|-------|-------|----------|
| Import Error | Missing dependencies | Run `pip install -r requirements.txt` |
| Authentication Error | Invalid Garmin credentials | Check your email and password |
| OpenAI API Error | Invalid API key | Verify your OpenAI API key in config.ini |
| GUI Not Loading | Missing HTML file | Check if wizard.html exists in gui directory |
| Test Mode Not Working | Missing workout data | Ensure workout_reports and workout_plots directories contain data |

### 6.2 Debug Mode
```bash
# Enable debug mode
python gui/main.py --debug
```

## 7. Security

### 7.1 File Permissions
```bash
# Set secure permissions
chmod 600 config.ini
chmod 644 *.py
chmod 755 gui/
```

### 7.2 API Security
- Store OpenAI API key securely in config.ini
- Never commit config.ini to version control
- Regularly rotate API keys
- Use environment variables for sensitive data

## 8. Scaling

### 8.1 Performance Optimization
- Process workouts in batches
- Implement caching for AI responses
- Optimize plot generation for large datasets

### 8.2 Resource Management
- Monitor memory usage during workout processing
- Implement caching for AI Assistant responses
- Optimize file I/O for large workout datasets

## 9. Disaster Recovery

### 9.1 Backup Strategy
- Daily data backups
- Configuration backups
- Log archives

### 9.2 Recovery Procedures
1. Restore from backup
2. Verify data integrity
3. Test functionality
4. Resume operations

## 10. Version History
| Version | Date | Description | Author |
|---------|------|-------------|---------|
| 1.0 | 2025-04-04 | Initial deployment guide | DevOps Engineer |
| 1.1 | 2025-04-05 | Added GUI deployment instructions | DevOps Engineer |
| 1.2 | 2025-04-06 | Updated for AI Assistant and test mode | DevOps Engineer | 