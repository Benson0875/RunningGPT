# Deployment and Operations Guide

## 1. System Requirements

### 1.1 Hardware Requirements
- CPU: 2.0 GHz dual-core processor or better
- RAM: 8GB minimum
- Storage: 1GB free space
- Network: Broadband internet connection

### 1.2 Software Requirements
- Python 3.8 or higher
- Git version control
- Virtual environment tool (venv/conda)

## 2. Installation

### 2.1 Python Environment Setup
```bash
# Create virtual environment
python -m venv venv

# Activate virtual environment
# Windows
venv\Scripts\activate
# Unix/MacOS
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```

### 2.2 Configuration
```python
# config.py
CONFIG = {
    'data_dir': 'workouts/CSV',
    'output_dir': 'workouts/analysis',
    'log_level': 'INFO',
    'api_timeout': 30
}
```

## 3. Deployment

### 3.1 Directory Structure
```
project_root/
├── workouts/
│   ├── CSV/
│   └── analysis/
├── logs/
├── config/
└── venv/
```

### 3.2 Environment Variables
```bash
# .env file
GARMIN_USERNAME=your_username
GARMIN_PASSWORD=your_password
LOG_LEVEL=INFO
DATA_DIR=/path/to/data
```

## 4. Operations

### 4.1 Starting the Application
```bash
# Run the main analysis
python analysis_running_CSV.py

# Run with specific file
python analysis_running_CSV.py --file workout.csv
```

### 4.2 Monitoring
```python
import logging

logging.config.dictConfig({
    'version': 1,
    'handlers': {
        'file': {
            'class': 'logging.FileHandler',
            'filename': 'app.log',
            'formatter': 'detailed'
        }
    }
})
```

## 5. Maintenance

### 5.1 Backup Procedures
```bash
# Backup data directory
tar -czf backup_$(date +%Y%m%d).tar.gz workouts/

# Backup configuration
cp config.py config.py.backup
```

### 5.2 Log Rotation
```python
from logging.handlers import RotatingFileHandler

handler = RotatingFileHandler(
    'app.log',
    maxBytes=1024*1024,  # 1MB
    backupCount=5
)
```

## 6. Troubleshooting

### 6.1 Common Issues
| Issue | Cause | Solution |
|-------|-------|----------|
| Import Error | Missing dependencies | Run `pip install -r requirements.txt` |
| File Not Found | Incorrect path | Check config DATA_DIR setting |
| API Error | Authentication failed | Verify Garmin credentials |

### 6.2 Debug Mode
```python
# Enable debug logging
import logging
logging.basicConfig(level=logging.DEBUG)
```

## 7. Security

### 7.1 File Permissions
```bash
# Set secure permissions
chmod 600 .env
chmod 644 *.py
chmod 755 scripts/
```

### 7.2 API Security
```python
def secure_api_connection():
    """Establish secure API connection"""
    verify_ssl_cert()
    check_api_tokens()
    validate_connection()
```

## 8. Scaling

### 8.1 Performance Optimization
```python
# Batch processing for multiple files
def process_batch(files, batch_size=10):
    """Process files in batches"""
    for i in range(0, len(files), batch_size):
        batch = files[i:i + batch_size]
        process_files(batch)
```

### 8.2 Resource Management
- Monitor memory usage
- Implement caching
- Optimize file I/O

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
| 1.0 | 2024-03-20 | Initial deployment guide | DevOps Engineer | 