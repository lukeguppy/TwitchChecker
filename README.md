# TwitchChecker

## Overview
TwitchChecker is a simple Python application that monitors specified Twitch channels and notifies the user when they go live. The notification window allows users to open the live stream or dismiss the notification.

![alt text](example.png "Example")

## Prerequisites
- Python 3.7 or higher
- A registered Twitch Developer application to obtain `CLIENT_ID` and `CLIENT_SECRET`

## Setup Instructions

### 1. Obtain Twitch API Credentials
- Visit [Twitch Developer Portal](https://dev.twitch.tv/console/apps) and log in with your Twitch account.
- Create a new application and note the `CLIENT_ID` and `CLIENT_SECRET`.

### 2. Install Required Python Packages

#### For Windows
Run the following command:
```bash
pip install twitchAPI asyncio
```

#### For macOS
Ensure tkinter is installed if it's not already available
```bash
brew install python-tk
```
Install the required Python packages
```bash
pip3 install twitchAPI asyncio
```

### 3. Configure the Application
- Open the `TwitchChecker.py` script.
- Set the `CLIENT_ID` and `CLIENT_SECRET` with your own credentials.
- Add the Twitch channels you want to monitor in the `CHANNELS_TO_MONITOR` list.
- Update the `twitchLogoPath` variable with the path to an icon file for the notification window.

### 4. Running the Script Automatically

#### For Windows:
1. Create a `.bat` file to run the script at startup:
```batch
@echo off
start "" "path\to\pythonw.exe" "path\to\your\TwitchChecker.py"
```
2. Place the `.bat` file in your startup folder (e.g., `%APPDATA%\Microsoft\Windows\Start Menu\Programs\Startup`).

#### For macOS:
1. Create a `.sh` file to run the script at startup:
```bash
#!/bin/bash
/usr/local/bin/python3 /path/to/your/TwitchChecker.py
```
2. Make the file executable:
```bash
chmod +x /path/to/your/startup.sh
```
3. Use **Automator** to add the script to startup:
   - Open Automator and create a new "Application."
   - Add the "Run Shell Script" action and add the following:
   ```bash
   /path/to/your/startup.sh
   ```
   - Save the application and add it to your login items in **System Preferences > Users & Groups > Login Items**.

### 5. Running the Script
To manually run the script, execute the following:
```bash
python TwitchChecker.py
```

### 6. Customisation
- Modify the `CHANNELS_TO_MONITOR` list in the script to include the names of the channels you want to monitor.
- Change the `twitchLogoPath` variable to the path of your custom icon for the notification window.

### Notes:
- Make sure that the image file for the notification window (`twitchLogoPath`) is accessible and correctly set.
- The script checks for live streams every 60 seconds by default. You can adjust this frequency by modifying the `await asyncio.sleep(60)` line in the code.

