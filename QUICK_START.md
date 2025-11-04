# Quick Start Guide for Building APK

## Option 1: Using GitHub Actions (Recommended - Automated)

The repository now includes a GitHub Actions workflow that automatically builds the APK.

### Steps:
1. Push your code to GitHub (main or master branch)
2. Go to your repository's "Actions" tab
3. Select "Build Android APK" workflow
4. Click "Run workflow" button
5. Wait for the build to complete (30-60 minutes)
6. Download the APK from the "Artifacts" section

The APK will be available as `rftxtuning-debug-apk` in the workflow artifacts.

## Option 2: Using the Build Script (Local Machine)

For building on your local Linux machine:

### Prerequisites:
- Linux system (Ubuntu 20.04+ recommended)
- 4GB+ RAM
- 5GB+ free disk space
- Stable internet connection

### Steps:
```bash
# Make the script executable
chmod +x build_apk.sh

# Run the build script
./build_apk.sh

# For clean build (removes previous build cache)
./build_apk.sh --clean
```

The script will:
1. Install all required system dependencies
2. Install Python packages (buildozer, cython)
3. Build the APK using buildozer
4. Save the APK to `bin/rftxtuning-1.0-debug.apk`

## Option 3: Manual Build (Advanced)

Follow the instructions in `BUILD_INSTRUCTIONS.md` for manual building.

## Installation on Android Device

Once you have the APK file:

### Method 1: Using ADB (Android Debug Bridge)
```bash
# Install ADB if not already installed
sudo apt install android-tools-adb

# Connect your Android device via USB with USB debugging enabled
# Install the APK
adb install -r bin/rftxtuning-1.0-debug.apk
```

### Method 2: Direct Install
1. Copy the APK file to your Android device
2. Open the APK file on your device
3. Enable "Install from Unknown Sources" if prompted
4. Tap "Install"

## Troubleshooting

### Build fails with network timeout
- Ensure you have a stable internet connection
- Try building on a different network
- Use a VPN if your network blocks certain domains
- Use GitHub Actions (Option 1) which has better network connectivity

### Build fails with "Out of memory"
- Ensure you have at least 4GB RAM
- Close other applications
- Increase swap space

### Build fails with missing dependencies
- Re-run the build script
- Manually install dependencies as shown in BUILD_INSTRUCTIONS.md

## What's Included

The APK includes:
- RFTX Tuning app with full UI
- USB serial support for K+DCAN cables
- ECU flashing capabilities
- DTC reading/clearing
- ECU backup and reset functions

## Support

For issues or questions:
- Check BUILD_INSTRUCTIONS.md for detailed build information
- Check README_ANDROID.md for app usage information
- Report issues to rftxtuning@gmail.com

## File Sizes

- Final APK size: ~20-30 MB
- Build cache size: ~2-3 GB (first build)
- Total disk space needed: ~5 GB

## Build Time

- First build: 30-60 minutes (downloads SDK/NDK)
- Subsequent builds: 5-10 minutes (uses cache)
