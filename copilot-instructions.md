# GitHub Copilot Instructions for RFTX Tuning

This document provides context and guidelines for GitHub Copilot coding agent when working on the RFTX Tuning project.

## Project Overview

RFTX Tuning is a BMW ECU flashing and tuning application with:
- **Android app** built with Python/Kivy and Buildozer
- **Desktop app** for Windows, macOS, and Linux
- **Web interface** deployed on Vercel (Next.js/React)

## Technology Stack

### Python Components
- **Framework**: Kivy 2.3.0 for GUI (cross-platform)
- **Serial Communication**: pyserial 3.5 for K+DCAN cable
- **Android Build**: Buildozer 1.5.0, Cython 0.29.33
- **Python Version**: 3.8+

### Web Components
- **Framework**: Next.js 16.0.0 with React 19.2.0
- **UI Library**: Radix UI components with Tailwind CSS
- **Deployment**: Vercel

### Build System
- **Android**: Buildozer (targets Android 5.0+ / API 21+)
- **CI/CD**: GitHub Actions for automated APK builds

## Project Structure

```
.
├── main.py                    # Main Kivy Android application entry point
├── rftx_gui.py               # Desktop GUI application
├── RFTX_FLASHER.py           # Core ECU flashing logic (desktop)
├── rftx_flasher_android.py   # Android-specific flasher implementation
├── tune_matcher.py           # Tune file matching system
├── android_permissions.py    # Android permission handling
├── android_usb_serial.py     # Android USB serial communication
├── requirements.txt          # Python dependencies
├── buildozer.spec           # Android build configuration
├── build_apk.sh             # Automated build script
├── package.json             # Node.js/Web dependencies
└── .github/
    ├── workflows/           # GitHub Actions workflows
    └── agents/             # Custom Copilot agents
```

## Build Commands

### Android APK
```bash
# Automated build (recommended)
./build_apk.sh

# Manual build
buildozer android debug

# GitHub Actions build - automated on push/PR
```

### Desktop Application
```bash
pip install -r requirements.txt
python rftx_gui.py
```

### Web Interface
```bash
npm install
npm run dev      # Development
npm run build    # Production build
npm run lint     # ESLint
```

## Testing Guidelines

### Python Testing
- Test on Ubuntu 20.04+ for Buildozer builds
- Verify Android 5.0+ compatibility
- Test USB serial communication with actual hardware when possible
- Use Kivy Launcher for rapid Android testing without full builds

### Hardware Testing
- **Required**: K+DCAN cable (FTDI, CH340, or compatible)
- **Test ECUs**: MSD80, MSD81, MEVD17.2, MG1/MD1
- **Android**: USB OTG support required
- **Safety**: Always test with backup ECU or in safe environment

## Code Style and Standards

### Python
- Follow PEP 8 style guidelines
- Use logging instead of print statements
- Handle Android platform differences with `platform` checks
- Document complex ECU communication protocols

### JavaScript/TypeScript
- Use ESLint configuration in package.json
- Follow React best practices
- Use TypeScript for type safety

## Common Development Patterns

### Platform Detection
```python
from kivy.utils import platform

if platform == 'android':
    # Android-specific code
else:
    # Desktop code
```

### Android Permissions
```python
from android_permissions import request_permissions_on_start
request_permissions_on_start()
```

### USB Serial Communication
```python
from android_usb_serial import AndroidUSBSerial
# Use for Android USB communication
```

## Important Safety Notes

⚠️ **ECU Flashing Safety**:
- Changes to ECU flashing logic require extensive testing
- Always maintain stable 12V+ power during flashing
- Verify tune file compatibility before flashing
- Test thoroughly before production deployment
- ECU flashing can damage vehicles if done incorrectly

## Documentation Files

- **README.md**: Main project documentation
- **QUICK_START.md**: Quick guide for building APK
- **BUILD_INSTRUCTIONS.md**: Detailed manual build steps
- **README_ANDROID.md**: Android app usage guide
- **APK_BUILD_SUMMARY.md**: Build process summary
- **TROUBLESHOOTING.md**: Common issues and solutions
- **GITHUB_ACTIONS_GUIDE.md**: CI/CD workflow documentation

## Common Tasks

### Adding Dependencies
- **Python**: Add to `requirements.txt`
- **Android**: Update `requirements` in `buildozer.spec`
- **Web**: Use `npm install --save <package>`

### Modifying Build Configuration
- **Android**: Edit `buildozer.spec`
- **GitHub Actions**: Edit `.github/workflows/build-apk.yml`
- **Web**: Edit `package.json` and `vercel.json`

### Adding New ECU Support
1. Update ECU definitions in flasher modules
2. Add tune file matching patterns in `tune_matcher.py`
3. Update documentation with supported ECU list
4. Test thoroughly with actual hardware

## File Handling

### Android Storage
- Use `/sdcard/` paths for Android file access
- Request STORAGE permissions at runtime
- Handle both internal and external storage

### Tune Files
- Binary format (.bin)
- Validate checksums before flashing
- Support automatic tune matching based on ECU type

## Debugging

### Android Logs
```bash
adb logcat | grep python
```

### Build Issues
- Check `.buildozer/android/platform/build-*/` for logs
- Clear cache with `buildozer android clean`
- Verify Java version (11 or 17)

### Common Issues
- USB permissions not granted → Check manifest and runtime requests
- Serial communication fails → Verify cable and USB OTG support
- Build fails → Check TROUBLESHOOTING.md

## Version Control

- Main branch: `main`
- Feature branches: Use descriptive names
- Commits: Write clear, descriptive commit messages
- Pull requests: Include testing notes and screenshots

## Contact and Support

- Email: rftxtuning@gmail.com
- Issues: GitHub issue tracker
- Deployment: Vercel (web interface)

## When Working on Issues

1. **Understand the context**: Review related documentation files
2. **Test locally**: Build and test changes before committing
3. **Maintain compatibility**: Ensure changes work on Android and desktop
4. **Update documentation**: Keep docs in sync with code changes
5. **Safety first**: Be extra careful with ECU flashing logic
6. **Minimal changes**: Make surgical, focused changes
7. **Build verification**: Always verify builds complete successfully

## Custom Agents Available

Custom agents are available in `.github/agents/` for specialized tasks:
- Python/Kivy development
- Android build troubleshooting
- ECU flashing domain expertise

Refer to these agents for specialized guidance in their respective areas.
