# RFTX Tuning - BMW ECU Flasher

*Multi-platform BMW ECU flashing and tuning software*

[![Deployed on Vercel](https://img.shields.io/badge/Deployed%20on-Vercel-black?style=for-the-badge&logo=vercel)](https://vercel.com/mrfortune94s-projects/v0-rftxsoftware-main)
[![Built with v0](https://img.shields.io/badge/Built%20with-v0.app-black?style=for-the-badge)](https://v0.app/chat/eSLKTaFa8i9)

## Overview

RFTX Tuning is a comprehensive BMW ECU flashing and tuning solution available as both an Android app and desktop application. Flash ECUs, read/clear DTCs, backup firmware, and more using K+DCAN cables.

### Features

- 🔧 **ECU Flashing**: Flash custom tunes to BMW ECUs
- 📱 **Android Support**: Native Android app with USB OTG
- 💻 **Desktop Support**: GUI application for Windows, macOS, and Linux
- 🔍 **DTC Management**: Read and clear diagnostic trouble codes
- 💾 **Backup/Restore**: Backup and restore ECU firmware
- 🎯 **Tune Matching**: Automatic tune file matching for your ECU
- 🔌 **USB Serial**: Support for FTDI, CH340, and compatible adapters

### Supported ECUs

- MSD80 (N54 engine)
- MSD81 (N54 engine)
- MEVD17.2 (N55, N20, N26 engines)
- MG1/MD1 (Transmission)
- More coming soon

## Getting Started

### Android App

See **[QUICK_START.md](QUICK_START.md)** for instructions on building the Android APK.

Three ways to build:
1. **GitHub Actions** (Recommended): Automated cloud build
2. **Build Script**: One-command local build with `./build_apk.sh`
3. **Manual Build**: Follow [BUILD_INSTRUCTIONS.md](BUILD_INSTRUCTIONS.md)

### Desktop Application

```bash
# Install dependencies
pip install -r requirements.txt

# Run the GUI application
python rftx_gui.py
```

### Documentation

- **[QUICK_START.md](QUICK_START.md)** - Quick guide to building the Android APK
- **[BUILD_INSTRUCTIONS.md](BUILD_INSTRUCTIONS.md)** - Detailed build instructions
- **[README_ANDROID.md](README_ANDROID.md)** - Android app usage guide

## Requirements

### Hardware
- K+DCAN cable (FTDI, CH340, or compatible)
- BMW vehicle with supported ECU
- Android device with USB OTG (for mobile) OR Windows/Mac/Linux computer

### Software
- Python 3.8+ (for desktop)
- Android 5.0+ (for mobile)

## Installation

### Android
1. Download or build the APK (see [QUICK_START.md](QUICK_START.md))
2. Install on your Android device
3. Grant USB and storage permissions
4. Connect K+DCAN cable and start flashing!

### Desktop
```bash
pip install -r requirements.txt
python rftx_gui.py
```

## Safety Warnings

⚠️ **IMPORTANT**: ECU flashing can damage your vehicle if done incorrectly!

- Always ensure stable 12V+ power during flashing (use battery charger)
- Only use tune files compatible with your ECU type
- Always backup your ECU before flashing
- ECU flashing may void warranties or violate local laws

## Development

Built with:
- **Python 3** - Core application logic
- **Kivy** - Cross-platform GUI framework
- **Buildozer** - Android APK packaging
- **pyserial** - Serial communication
- **pyjnius** - Android Java bindings

## License

Free for personal use. Commercial use requires permission.

## Support

- **Email**: rftxtuning@gmail.com
- **Issues**: Open an issue on GitHub

## Deployment

Web version is live at: **[https://vercel.com/mrfortune94s-projects/v0-rftxsoftware-main](https://vercel.com/mrfortune94s-projects/v0-rftxsoftware-main)**

Continue building on: **[https://v0.app/chat/eSLKTaFa8i9](https://v0.app/chat/eSLKTaFa8i9)**

---

**Disclaimer**: This software is provided as-is without warranty. Use at your own risk. The developers are not responsible for any damage to vehicles or ECUs.