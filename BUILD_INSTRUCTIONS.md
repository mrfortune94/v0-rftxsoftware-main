# Building RFTX Tuning Android APK

> **Quick Start**: For easier build methods, see [QUICK_START.md](QUICK_START.md)  
> **Troubleshooting**: Having issues? Check [TROUBLESHOOTING.md](TROUBLESHOOTING.md)

This document provides detailed manual build instructions. For most users, we recommend using:
- **GitHub Actions** (automated cloud build) - see [QUICK_START.md](QUICK_START.md)
- **Build Script** (`./build_apk.sh`) - one-command local build

## Prerequisites

1. **Linux System** (Ubuntu 20.04+ recommended)
   - Buildozer works best on Linux
   - For Windows/Mac, use WSL2 or a Linux VM, or use GitHub Actions

2. **Install Dependencies**
   \`\`\`bash
   sudo apt update
   sudo apt install -y git zip unzip openjdk-17-jdk python3-pip autoconf libtool pkg-config zlib1g-dev libncurses-dev cmake libffi-dev libssl-dev
   \`\`\`
   Note: `libtinfo5` may not be available on Ubuntu 24.04, but it's optional

3. **Install Buildozer**
   \`\`\`bash
   pip3 install --user buildozer cython
   # Add to PATH if needed
   export PATH=$PATH:~/.local/bin
   \`\`\`

4. **Install Android SDK/NDK**
   - Buildozer will automatically download these on first build
   - Or manually install Android Studio and set paths

## Building the APK

1. **Navigate to project directory**
   \`\`\`bash
   cd /path/to/RFTXSOFTWARE
   \`\`\`

2. **Initialize Buildozer** (first time only)
   \`\`\`bash
   buildozer init
   \`\`\`
   - This creates buildozer.spec (already provided)

3. **Build Debug APK**
   \`\`\`bash
   buildozer android debug
   \`\`\`
   - First build takes 30-60 minutes (downloads SDK/NDK)
   - Subsequent builds are much faster

4. **Build Release APK** (for distribution)
   \`\`\`bash
   buildozer android release
   \`\`\`
   - You'll need to sign the APK with a keystore

5. **Deploy to Connected Device**
   \`\`\`bash
   buildozer android debug deploy run
   \`\`\`
   - Requires USB debugging enabled on Android device

## Output

- Debug APK: `bin/rftxtuning-1.0-debug.apk`
- Release APK: `bin/rftxtuning-1.0-release-unsigned.apk`

## Signing Release APK

1. **Create Keystore** (first time only)
   \`\`\`bash
   keytool -genkey -v -keystore rftx-release-key.keystore -alias rftx -keyalg RSA -keysize 2048 -validity 10000
   \`\`\`

2. **Sign APK**
   \`\`\`bash
   jarsigner -verbose -sigalg SHA1withRSA -digestalg SHA1 -keystore rftx-release-key.keystore bin/rftxtuning-1.0-release-unsigned.apk rftx
   \`\`\`

3. **Align APK**
   \`\`\`bash
   zipalign -v 4 bin/rftxtuning-1.0-release-unsigned.apk bin/rftxtuning-1.0-release.apk
   \`\`\`

## Troubleshooting

### Build Fails
- Check Java version: `java -version` (should be 11 or 17)
- Clear build cache: `buildozer android clean`
- Check logs in `.buildozer/android/platform/build-*/`

### USB Not Working
- Ensure USB OTG cable is used
- Check Android device supports USB Host mode
- Grant USB permissions when prompted

### App Crashes
- Check logcat: `adb logcat | grep python`
- Verify all Python dependencies are in requirements
- Test on different Android versions

## Testing Without Building

For quick testing, use Kivy Launcher:
1. Install Kivy Launcher from Play Store
2. Copy project to `/sdcard/kivy/`
3. Launch from Kivy Launcher app

## Requirements

- Android 5.0+ (API 21+)
- USB OTG support
- K+DCAN cable (FTDI, CH340, or compatible)
- 50MB free storage

## Notes

- First build downloads ~2GB of SDK/NDK
- Build requires 4GB+ RAM
- USB permissions must be granted at runtime
- Some devices may require root for USB serial access
