# Python: Garmin Connect

```bash
$ ./example.py
*** Garmin Connect API Demo by cyberjunky ***

Trying to login to Garmin Connect using token data from directory '~/.garminconnect'...

1 -- Get full name
2 -- Get unit system
3 -- Get activity data for '2024-11-10'
4 -- Get activity data for '2024-11-10' (compatible with garminconnect-ha)
5 -- Get body composition data for '2024-11-10' (compatible with garminconnect-ha)
6 -- Get body composition data for from '2024-11-03' to '2024-11-10' (to be compatible with garminconnect-ha)
7 -- Get stats and body composition data for '2024-11-10'
8 -- Get steps data for '2024-11-10'
9 -- Get heart rate data for '2024-11-10'
0 -- Get training readiness data for '2024-11-10'
- -- Get daily step data for '2024-11-03' to '2024-11-10'
/ -- Get body battery data for '2024-11-03' to '2024-11-10'
! -- Get floors data for '2024-11-03'
? -- Get blood pressure data for '2024-11-03' to '2024-11-10'
. -- Get training status data for '2024-11-10'
a -- Get resting heart rate data for '2024-11-10'
b -- Get hydration data for '2024-11-10'
c -- Get sleep data for '2024-11-10'
d -- Get stress data for '2024-11-10'
e -- Get respiration data for '2024-11-10'
f -- Get SpO2 data for '2024-11-10'
g -- Get max metric data (like vo2MaxValue and fitnessAge) for '2024-11-10'
h -- Get personal record for user
i -- Get earned badges for user
j -- Get adhoc challenges data from start '0' and limit '100'
k -- Get available badge challenges data from '1' and limit '100'
l -- Get badge challenges data from '1' and limit '100'
m -- Get non completed badge challenges data from '1' and limit '100'
n -- Get activities data from start '0' and limit '100'
o -- Get last activity
p -- Download activities data by date from '2024-11-03' to '2024-11-10'
r -- Get all kinds of activities data from '0'
s -- Upload activity data from file 'MY_ACTIVITY.fit'
t -- Get all kinds of Garmin device info
u -- Get active goals
v -- Get future goals
w -- Get past goals
y -- Get all Garmin device alarms
x -- Get Heart Rate Variability data (HRV) for '2024-11-10'
z -- Get progress summary from '2024-11-03' to '2024-11-10' for all metrics
A -- Get gear, the defaults, activity types and statistics
B -- Get weight-ins from '2024-11-03' to '2024-11-10'
C -- Get daily weigh-ins for '2024-11-10'
D -- Delete all weigh-ins for '2024-11-10'
E -- Add a weigh-in of 89.6kg on '2024-11-10'
F -- Get virtual challenges/expeditions from '2024-11-03' to '2024-11-10'
G -- Get hill score data from '2024-11-03' to '2024-11-10'
H -- Get endurance score data from '2024-11-03' to '2024-11-10'
I -- Get activities for date '2024-11-10'
J -- Get race predictions
K -- Get all day stress data for '2024-11-10'
L -- Add body composition for '2024-11-10'
M -- Set blood pressure "120,80,80,notes='Testing with example.py'"
N -- Get user profile/settings
O -- Reload epoch data for '2024-11-10'
P -- Get workouts 0-100, get and download last one to .FIT file
R -- Get solar data from your devices
S -- Get pregnancy summary data
T -- Add hydration data
U -- Get Fitness Age data for '2024-11-10'
V -- Get daily wellness events data for '2024-11-03'
W -- Get userprofile settings
Z -- Remove stored login tokens (logout)
q -- Exit
Make your selection: 
```

[![Donate](https://img.shields.io/badge/Donate-PayPal-green.svg)](https://www.paypal.me/cyberjunkynl/)

Python 3 API wrapper for Garmin Connect.

## About

This package allows you to request garmin device, activity and health data from your Garmin Connect account.
See <https://connect.garmin.com/>

## Installation

### Prerequisites

1. **Python Installation**
   - Download and install Python from [python.org](https://www.python.org/downloads/)
   - During installation, make sure to check "Add Python to PATH"
   - Recommended Python version: 3.11 or 3.12 (Python 3.13 may have compatibility issues)

2. **Visual C++ Build Tools** (Required for Windows)
   - Download from [Visual Studio Build Tools](https://visualstudio.microsoft.com/visual-cpp-build-tools/)
   - During installation, select "Desktop development with C++"
   - Required components:
     - MSVC v143 build tools
     - Windows 10/11 SDK
     - C++ CMake tools

### Installation Steps

#### Windows
```powershell
# Create and activate virtual environment
python -m venv .venv
.\.venv\Scripts\activate

# If you get a PowerShell execution policy error, run:
Set-ExecutionPolicy RemoteSigned -Scope CurrentUser

# Install dependencies
# Note: If you encounter errors installing requirements in the virtual environment,
# try installing them in the global Python environment first:
deactivate  # Exit virtual environment
pip install --only-binary :all: lxml  # Install lxml first to avoid compilation issues
pip install -r requirements-dev.txt
pip install -r requirements-test.txt

# Then reactivate the virtual environment and verify installations
.\.venv\Scripts\activate
pip list  # Check if packages are available
```

#### Linux/macOS
```bash
pip3 install garminconnect
```

## Authentication

The library uses the same authentication method as the app using [Garth](https://github.com/matin/garth).
The login credentials generated with Garth are valid for a year to avoid needing to login each time.  
NOTE: We obtain the OAuth tokens using the consumer key and secret as the Connect app does.
`garth.sso.OAUTH_CONSUMER` can be set manually prior to calling api.login() if someone wants to use a custom consumer key and secret.

### Setting Environment Variables

#### Windows (PowerShell)
```powershell
# Temporary (current session only)
$env:EMAIL="your_garmin_email"
$env:PASSWORD="your_garmin_password"
$env:GARMINTOKENS="C:\Users\$env:USERNAME\.garminconnect"

# Permanent (through System Properties)
# 1. Press Windows + R
# 2. Type "sysdm.cpl" and press Enter
# 3. Go to "Advanced" tab
# 4. Click "Environment Variables"
# 5. Under "User variables", click "New"
# 6. Add each variable (EMAIL, PASSWORD, GARMINTOKENS)
```

#### Linux/macOS
```bash
export EMAIL=<your garmin email>
export PASSWORD=<your garmin password>
export GARMINTOKENS=~/.garminconnect
```

## Testing

### Windows
```powershell
# Set environment variable
$env:GARMINTOKENS="C:\Users\$env:USERNAME\.garminconnect"

# Make sure all dependencies are installed
# If you're in a virtual environment, ensure all required packages are installed:
pip install garth>=0.4.45
pip install withings-sync
pip install pytest pytest-vcr pytest-cov coverage

# Run tests
python -m pytest tests/
```

### Linux/macOS
```bash
export GARMINTOKENS=~/.garminconnect
sudo apt install python3-pytest (needed some distros)
make install-test
make test
```

## Development

### Windows
```powershell
# Create virtual environment
python -m venv .venv
.\.venv\Scripts\activate

# Install development tools
pip install pdm ruff pre-commit isort black mypy

# Initialize PDM
pdm init
```

### Linux/macOS
```bash
make .venv
source .venv/bin/activate
pip3 install pdm ruff pre-commit isort black mypy
pdm init
```

## Troubleshooting

### Common Issues and Solutions

1. **PowerShell Execution Policy Error**
   ```powershell
   # Run as Administrator and execute:
   Set-ExecutionPolicy RemoteSigned -Scope CurrentUser
   ```

2. **lxml Installation Error**
   ```powershell
   # If you see compilation errors, use pre-built wheels:
   pip install --only-binary :all: lxml
   ```

   If you see errors about missing libxml2 or libxslt:
   ```powershell
   # First, install the required libraries using conda
   # Install Miniconda from: https://docs.conda.io/en/latest/miniconda.html
   
   # Create a new conda environment
   conda create -n garmin python=3.11
   conda activate garmin
   
   # Install lxml and its dependencies
   conda install lxml
   
   # Then install withings-sync
   pip install withings-sync
   ```

   Alternative approach without conda:
   ```powershell
   # Install the latest version of lxml using pre-built wheels
   pip install --only-binary :all: lxml
   
   # Then install withings-sync without its lxml dependency
   pip install --no-deps withings-sync
   ```

   If you still encounter issues, try installing the Visual C++ Build Tools:
   1. Download [Visual Studio Build Tools](https://visualstudio.microsoft.com/visual-cpp-build-tools/)
   2. Run the installer
   3. Select "Desktop development with C++"
   4. Make sure these components are selected:
      - MSVC v143 build tools
      - Windows 10/11 SDK
      - C++ CMake tools
   5. Install and restart your computer
   6. Try installing lxml again:
      ```powershell
      pip install lxml
      ```

   **Alternative Solution Without Conda (Recommended)**:
   ```powershell
   # 1. Install a pre-built wheel for lxml
   pip install --only-binary :all: lxml
   
   # 2. Install withings-sync without its lxml dependency
   pip install --no-deps withings-sync
   
   # 3. Install the remaining dependencies
   pip install garth>=0.4.45
   pip install readchar
   pip install requests
   pip install mypy
   ```

   If you still have issues with lxml, try this workaround:
   ```powershell
   # 1. Create a modified requirements file without lxml
   (Get-Content requirements-dev.txt) -replace 'lxml==5.2.2', '# lxml==5.2.2' | Set-Content requirements-dev-modified.txt
   
   # 2. Install from the modified requirements file
   pip install -r requirements-dev-modified.txt
   
   # 3. Install withings-sync without dependencies
   pip install --no-deps withings-sync
   ```

3. **Visual C++ Build Tools Error**
   - Make sure you have installed Visual C++ Build Tools
   - Verify installation by running `cl` in PowerShell
   - If not found, repair/reinstall Visual C++ Build Tools

4. **Python Version Compatibility**
   - If you encounter dataclass-related errors, try using Python 3.11 or 3.12
   - Python 3.13 may have compatibility issues with some packages

5. **Environment Variables Not Found**
   - Verify environment variables are set correctly
   - Try setting them temporarily in PowerShell first
   - Check path separators in Windows paths (use backslashes)

6. **Virtual Environment Installation Issues**
   - If you encounter errors installing requirements in the virtual environment:
     ```powershell
     # Exit virtual environment first
     deactivate
     
     # Install requirements globally
     pip install --only-binary :all: lxml
     pip install -r requirements-dev.txt
     pip install -r requirements-test.txt
     
     # Reactivate virtual environment
     .\.venv\Scripts\activate
     ```
   - This is a known issue with some packages that have compilation requirements
   - The packages will still be available to your virtual environment after global installation

   **Specific Issue with lxml in Virtual Environments**:
   - If lxml installs successfully in the global environment but fails in the virtual environment:
     ```powershell
     # 1. Exit the virtual environment
     deactivate
     
     # 2. Install lxml globally with pre-built wheels
     pip install --only-binary :all: lxml
     
     # 3. Create a modified requirements file without lxml
     (Get-Content requirements-dev.txt) -replace 'lxml==5.2.2', '# lxml==5.2.2' | Set-Content requirements-dev-modified.txt
     
     # 4. Install the modified requirements globally
     pip install -r requirements-dev-modified.txt
     
     # 5. Reactivate the virtual environment
     .\.venv\Scripts\activate
     
     # 6. Verify installations
     pip list | findstr lxml
     pip list | findstr withings
     ```
   - This approach installs the packages globally and makes them available to your virtual environment
   - The virtual environment will use the globally installed packages

7. **ModuleNotFoundError: No module named 'garth'**
   - This error occurs when the `garth` package is not installed in your virtual environment
   - Solution:
     ```powershell
     # Make sure you're in your virtual environment
     .\.venv\Scripts\activate
     
     # Install garth directly
     pip install garth>=0.4.45
     
     # Or reinstall all requirements
     pip install -r requirements-dev.txt
     ```
   - If the above doesn't work, try installing globally:
     ```powershell
     deactivate
     pip install garth>=0.4.45
     .\.venv\Scripts\activate
     ```
   - Verify installation:
     ```powershell
     pip list | findstr garth
     ```

8. **ModuleNotFoundError: No module named 'withings_sync'**
   - This error occurs when the `withings_sync` package is not installed in your virtual environment
   - Solution:
     ```powershell
     # Make sure you're in your virtual environment
     .\.venv\Scripts\activate
     
     # First install lxml using pre-built wheels
     pip install --only-binary :all: lxml
     
     # Then install withings_sync without its lxml dependency
     pip install --no-deps withings-sync
     
     # Or reinstall all requirements
     pip install -r requirements-dev.txt
     ```
   - If the above doesn't work, try using conda:
     ```powershell
     # Create and activate conda environment
     conda create -n garmin python=3.11
     conda activate garmin
     
     # Install lxml and withings-sync
     conda install lxml
     pip install withings-sync
     ```
   - Alternative approach without conda:
     ```powershell
     # Create a modified requirements file without lxml
     (Get-Content requirements-dev.txt) -replace 'lxml==5.2.2', '# lxml==5.2.2' | Set-Content requirements-dev-modified.txt
     
     # Install from the modified requirements file
     pip install -r requirements-dev-modified.txt
     
     # Install withings-sync without dependencies
     pip install --no-deps withings-sync
     ```
   - Verify installation:
     ```powershell
     pip list | findstr withings
     ```

## Example

The tests provide examples of how to use the library.  
There is a Jupyter notebook called `reference.ipynb` provided [here](https://github.com/cyberjunky/python-garminconnect/blob/master/reference.ipynb).  
And you can check out the `example.py` code you can find [here](https://raw.githubusercontent.com/cyberjunky/python-garminconnect/master/example.py), you can run it like so:  

### Windows
```powershell
# If you haven't installed requirements yet, do it globally first:
deactivate  # Exit virtual environment if active
pip install --only-binary :all: lxml
pip install -r requirements-dev.txt
pip install -r requirements-test.txt

# Then activate virtual environment and run example
.\.venv\Scripts\activate
python example.py
```

# Alternative approach if you have issues with lxml:
```powershell
# 1. Exit the virtual environment
deactivate

# 2. Install lxml globally with pre-built wheels
pip install --only-binary :all: lxml

# 3. Create a modified requirements file without lxml
(Get-Content requirements-dev.txt) -replace 'lxml==5.2.2', '# lxml==5.2.2' | Set-Content requirements-dev-modified.txt

# 4. Install the modified requirements globally
pip install -r requirements-dev-modified.txt

# 5. Reactivate the virtual environment
.\.venv\Scripts\activate

# 6. Run the example
python example.py
```

## Credits

:heart: Special thanks to all people contributed, either by asking questions, reporting bugs, coming up with great ideas, or even by creating whole Pull Requests to add new features!
This project deserves more attention, but I'm struggling to free up time sometimes, so thank you for your patience too!

## Donations

[![Donate](https://img.shields.io/badge/Donate-PayPal-green.svg)](https://www.paypal.me/cyberjunky/)
