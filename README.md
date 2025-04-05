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
   
   > **Why are C++ Build Tools Required?**
   > - This project depends on `withings-sync`, which in turn requires `lxml`
   > - `lxml` is a Python library that wraps the C libraries `libxml2` and `libxslt`
   > - When installing `lxml` from source, it needs to compile these C extensions, requiring C++ build tools
   > - If you want to avoid installing C++ build tools, you can use pre-built wheels:
   >   ```powershell
   >   pip install --only-binary :all: lxml
   >   ```
   > - Or follow the alternative installation methods in the Troubleshooting section

### Dependencies

This project has several key dependencies:

1. **Core Dependencies**
   - `garth>=0.4.45`: For Garmin Connect authentication
   - `requests`: For making HTTP requests
   - `readchar`: For command-line interface

2. **Data Processing Dependencies**
   - `withings-sync>=4.2.4`: For data synchronization
     - Requires `lxml` for XML processing
     - `lxml` needs C++ build tools for compilation from source

3. **Development Dependencies**
   - `pytest`: For testing
   - `pytest-vcr`: For recording HTTP interactions
   - `pytest-cov`: For test coverage
   - `coverage`: For code coverage reporting

### Understanding Virtual Environments

If you're new to Python, you might wonder why we use virtual environments. Here's why they're important:

1. **What is a Virtual Environment?**
   - A virtual environment is like a separate, isolated container for your Python project
   - It has its own Python interpreter and package installations
   - It keeps your project's dependencies separate from other projects and your system Python

2. **Why Use Virtual Environments?**
   - **Isolation**: Different projects might need different versions of the same package
     - Project A might need `requests==2.28.0`
     - Project B might need `requests==2.31.0`
     - Without virtual environments, you can only install one version globally
   
   - **Clean Environment**: Prevents conflicts between project dependencies
     - No interference from globally installed packages
     - Easy to recreate the exact same environment on another computer
   
   - **Project Portability**: Makes it easier to share your project
     - All dependencies are listed in requirements files
     - Others can recreate your exact environment
   
   - **System Protection**: Prevents messing up your system Python installation
     - Experiments and tests are contained within the virtual environment
     - Easy to delete and recreate if something goes wrong

3. **When to Use Virtual Environments?**
   - It's recommended to use a virtual environment for EVERY Python project
   - This project specifically requires certain package versions to work correctly
   - Virtual environments ensure these requirements don't conflict with other projects

### Installation Steps

#### Windows

1. **Basic Setup**
```powershell
# Create and activate virtual environment
python -m venv .venv
.\.venv\Scripts\activate

# If you get a PowerShell execution policy error, run:
Set-ExecutionPolicy RemoteSigned -Scope CurrentUser
```

2. **For Traditional Chinese Windows Users (or if you encounter encoding errors)**
```powershell
# Set UTF-8 encoding for pip
$env:PYTHONUTF8=1

# Install lxml first (to avoid compilation issues)
pip install lxml==5.3.1 --only-binary :all:

# Install other dependencies
pip install garth==0.4.46 requests==2.31.0 python-dotenv
pip install withings-sync==4.2.7 --no-deps
pip install readchar>=4.0.0 mypy>=1.8.0
pip install -r requirements-dev.txt
```

3. **For Other Windows Users**
```powershell
# Regular installation
pip install -r requirements-dev.txt
pip install -r requirements-test.txt
```

4. **Verify Installation**
```powershell
# Check if packages are installed correctly
pip list
```

#### Troubleshooting Windows Installation

1. **Encoding Errors**
   - If you see Chinese characters or encoding errors during installation
   - Use the Traditional Chinese Windows installation method above
   - Always set `$env:PYTHONUTF8=1` before running pip commands

2. **lxml Installation Issues**
   - If lxml fails to install:
     - Make sure you have Visual C++ Build Tools installed
     - Or use `pip install lxml --only-binary :all:` to install pre-built wheels
     - For Python 3.13, use lxml 5.3.1 or newer

3. **withings-sync Installation Issues**
   - If withings-sync fails to install:
     - Install its dependencies separately as shown in the Traditional Chinese Windows steps
     - Make sure to install withings-sync with `--no-deps` flag
     - Version conflicts warnings are normal and can be ignored

#### Linux/macOS
```bash
pip3 install garminconnect
```

## Authentication

The library uses the same authentication method as the app using [Garth](https://github.com/matin/garth).
The login credentials generated with Garth are valid for a year to avoid needing to login each time.  
NOTE: We obtain the OAuth tokens using the consumer key and secret as the Connect app does.
`garth.sso.OAUTH_CONSUMER` can be set manually prior to calling api.login() if someone wants to use a custom consumer key and secret.

### Authentication Methods

1. **Environment Variables** (Recommended)
   - Most secure method
   - Credentials are not stored in plain text files
   - See setup instructions below

2. **USERNAMEPASSWORD.txt** (For Development Only)
   - Create a file named `USERNAMEPASSWORD.txt` in your project root directory
   - Add your credentials in this format:
     ```
     email:your_garmin_email
     password:your_garmin_password
     ```
   
   > **⚠️ Security Warning**
   > - This method stores credentials in plain text
   > - NEVER commit this file to version control
   > - NEVER share this file with others
   > - For development/testing only
   > 
   > **How to Protect Your Credentials:**
   > 1. Add `USERNAMEPASSWORD.txt` to your `.gitignore` file
   > 2. Use file system permissions to restrict access:
   >    ```powershell
   >    # Windows (PowerShell)
   >    $acl = Get-Acl "USERNAMEPASSWORD.txt"
   >    $acl.SetAccessRuleProtection($true, $false)
   >    $rule = New-Object System.Security.AccessControl.FileSystemAccessRule("$env:USERNAME","FullControl","Allow")
   >    $acl.AddAccessRule($rule)
   >    Set-Acl "USERNAMEPASSWORD.txt" $acl
   >    ```
   >    ```bash
   >    # Linux/macOS
   >    chmod 600 USERNAMEPASSWORD.txt
   >    ```
   > 3. Consider using environment variables in production

3. **Interactive Login**
   - If no credentials are provided through the above methods
   - The script will prompt you to enter credentials manually

### Setting Environment Variables

#### Windows (PowerShell)
```powershell
# Temporary (current session only)
$env:EMAIL="your_garmin_email"
$env:PASSWORD="your_garmin_password"
$env:GARMINTOKENS="C:\Users\$env:USERNAME\.garminconnect"

# Permanent (through System Properties)
 1. Press Windows + R
 2. Type "sysdm.cpl" and press Enter
 3. Go to "Advanced" tab
 4. Click "Environment Variables"
 5. Under "User variables", click "New"
 6. Add each variable (EMAIL, PASSWORD, GARMINTOKENS)
```

#### Linux/macOS
```bash
export EMAIL=<your garmin email>
export PASSWORD=<your garmin password>
export GARMINTOKENS=~/.garminconnect
```

## Testing

### Prerequisites for Testing
Before running tests, make sure you have:
1. All test dependencies installed:
   ```powershell
   pip install pytest pytest-vcr pytest-cov coverage
   ```
2. The `GARMINTOKENS` environment variable set:
   ```powershell
   # Windows (PowerShell)
   $env:GARMINTOKENS="C:\Users\$env:USERNAME\.garminconnect"
   
   # Linux/macOS
   export GARMINTOKENS=~/.garminconnect
   ```

### Running Tests

#### Windows
```powershell
# Make sure you're in your virtual environment
.\.venv\Scripts\activate

# Set environment variable and run tests in one command
$env:GARMINTOKENS="C:\Users\$env:USERNAME\.garminconnect"; python -m pytest tests/

# Or set environment variable permanently (recommended for development):
# 1. Open System Properties (Windows + R, type sysdm.cpl)
# 2. Go to Advanced tab -> Environment Variables
# 3. Under User variables, add GARMINTOKENS with value C:\Users\YOUR_USERNAME\.garminconnect
```

#### Linux/macOS
```bash
# Set environment variable
export GARMINTOKENS=~/.garminconnect

# Install pytest if needed
sudo apt install python3-pytest  # needed on some distros

# Run tests
make install-test
make test
```

### Troubleshooting Tests

1. **Missing GARMINTOKENS Environment Variable**
   If you see this error:
   ```
   AssertionError: assert 'GARMINTOKENS' in environ(...)
   ```
   Make sure to set the GARMINTOKENS environment variable as shown above.

2. **Test Dependencies**
   If you encounter missing package errors:
   ```powershell
   pip install pytest pytest-vcr pytest-cov coverage
   ```

3. **VCR Cassette Errors**
   If tests fail due to VCR cassette issues:
   - Delete the `tests/cassettes` directory
   - Run the tests again to generate new cassettes

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
