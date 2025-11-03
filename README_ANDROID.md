# RFTX Tuning - Android Version

BMW ECU Flasher for Android devices with USB OTG support.

## Features

- Connect to BMW ECUs via K+DCAN cable
- Read ECU information (VIN, ECU ID, Software Version)
- Flash ECU with custom tunes (.bin files)
- Backup ECU firmware
- Read and clear Diagnostic Trouble Codes (DTCs)
- Reset ECU
- Support for MSD80, MSD81, MEVD17.2, and other BMW ECUs

## Requirements

### Hardware
- Android device with USB OTG support (Android 5.0+)
- USB OTG cable or adapter
- K+DCAN cable (FTDI, CH340, or compatible USB-to-CAN adapter)
- BMW vehicle with supported ECU
- Stable 12V+ power supply (battery charger recommended during flashing)

### Software
- RFTX Tuning APK (this app)
- Tune files (.bin) stored on device

## Installation

1. **Enable Unknown Sources**
   - Go to Settings > Security
   - Enable "Install from Unknown Sources" or "Install Unknown Apps"

2. **Install APK**
   - Download `rftxtuning-1.0.apk`
   - Tap the APK file to install
   - Grant requested permissions

3. **Grant USB Permissions**
   - Connect K+DCAN cable to Android device
   - App will request USB permission
   - Check "Always allow" and tap OK

## Usage

### 1. Connect to ECU

1. Connect K+DCAN cable to vehicle OBD-II port
2. Connect cable to Android device via USB OTG
3. Turn on vehicle ignition (engine off)
4. Open RFTX Tuning app
5. Select USB device from dropdown
6. Tap "Connect"
7. Wait for ECU information to load

### 2. Flash ECU

1. Ensure vehicle battery is fully charged or connected to charger
2. Go to "Flash" tab
3. Tap "Select File" and choose .bin tune file
4. Review matching tunes (if available)
5. Tap "Flash ECU"
6. Confirm battery warning
7. Wait for flash to complete (10-30 minutes)
8. **DO NOT disconnect cable or power during flashing**

### 3. Backup ECU

1. Connect to ECU
2. Go to "Settings" tab
3. Tap "Backup ECU"
4. Wait for backup to complete
5. Backup saved to Downloads folder

### 4. Read/Clear DTCs

1. Connect to ECU
2. Go to "DTC" tab
3. Tap "Read DTCs" to view codes
4. Tap "Clear DTCs" to remove codes

### 5. Reset ECU

1. Connect to ECU
2. Go to "Settings" tab
3. Tap "Reset ECU"
4. Confirm reset

## Safety Warnings

- **Battery Voltage**: Ensure stable 12V+ power during flashing. Power loss can brick the ECU.
- **Valid Tunes**: Only use .bin files compatible with your ECU type.
- **Legal**: ECU flashing may void warranties or violate local laws. Use responsibly.
- **Backup**: Always backup your ECU before flashing.

## Supported ECU Types

- MSD80 (N54 engine)
- MSD81 (N54 engine)
- MEVD17.2 (N55, N20, N26 engines)
- MG1 (Transmission)
- MD1 (Transmission)

## Troubleshooting

### USB Device Not Found
- Check USB OTG cable connection
- Verify device supports USB Host mode
- Try different USB cable
- Restart app

### Connection Failed
- Check K+DCAN cable is properly connected to OBD-II port
- Ensure vehicle ignition is on
- Try different COM port/device
- Check cable compatibility (FTDI/CH340)

### Flash Failed
- Ensure battery voltage is stable (12V+)
- Check .bin file is valid and not corrupted
- Verify .bin file matches ECU type
- Try backup first to test connection

### App Crashes
- Clear app cache and data
- Reinstall app
- Check Android version (5.0+ required)
- Report issue to rftxtuning@gmail.com

## Permissions

- **USB**: Access K+DCAN cable
- **Storage**: Read/write tune files and backups
- **Internet**: Check for updates (optional)

## File Locations

- **Tune Files**: `/sdcard/Download/` or `/sdcard/tunes/`
- **Backups**: `/sdcard/Download/BACKUP_*.bin`
- **Logs**: App internal storage

## Support

- Email: rftxtuning@gmail.com
- Website: [Coming Soon]

## Version

- Version: 1.0
- Build Date: 2025
- License: Free for personal use

## Credits

Developed by RFTX TUNING team.
Making BMW tuning accessible to everyone.

---

**Disclaimer**: This software is provided as-is without warranty. Use at your own risk. The developers are not responsible for any damage to vehicles or ECUs.
