# GitHub Copilot Instructions for RFTX Tuning

## Project Overview

RFTX Tuning is a multi-platform BMW ECU flashing and tuning software solution. The project includes:
- **Android App**: Built with Python/Kivy using Buildozer
- **Desktop Application**: Python GUI application using Kivy
- **Web Interface**: Next.js application deployed on Vercel

This is safety-critical automotive software that interfaces with vehicle ECUs. Code quality, reliability, and safety are paramount.

## Tech Stack

### Python Components (Desktop & Android)
- **Python 3.8+**: Core application logic
- **Kivy 2.3.0**: Cross-platform GUI framework
- **pyserial 3.5**: Serial communication with K+DCAN cables
- **Buildozer 1.5.0**: Android APK packaging
- **pyjnius**: Android Java bindings for USB permissions

### Web Components
- **Next.js 16.0.0**: React framework
- **TypeScript**: Type-safe JavaScript
- **Tailwind CSS**: Styling
- **Radix UI**: UI components
- **React 19.2.0**: UI library

## Build Commands

### Python/Desktop Application
```bash
# Install dependencies
pip install -r requirements.txt

# Run desktop GUI
python rftx_gui.py

# Run main flasher
python RFTX_FLASHER.py
```

### Android APK Build
```bash
# Quick build using script (Linux only)
./build_apk.sh

# Clean build
./build_apk.sh --clean

# Manual build with buildozer
buildozer android debug

# Deploy to connected device
buildozer android debug deploy run
```

### Web Application
```bash
# Install dependencies
npm install
# or
pnpm install

# Development server
npm run dev

# Production build
npm run build

# Start production server
npm start

# Lint code
npm run lint
```

## Testing

### Python Testing
- Test serial communication with mock devices
- Validate ECU communication protocols
- Test file I/O for tune files and backups
- Test GUI interactions in Kivy

### Web Testing
- Test Next.js pages render correctly
- Validate API endpoints if any
- Test responsive design

### Android Testing
```bash
# View logs from device
adb logcat | grep python

# Install and test APK
adb install -r bin/rftxtuning-1.0-debug.apk
```

## Code Guidelines

### Safety-Critical Considerations
⚠️ This software controls vehicle ECUs - bugs can cause physical damage or safety issues!

- **Always validate input parameters** for ECU commands
- **Implement proper error handling** for all serial communication
- **Add timeout mechanisms** to prevent infinite waits
- **Validate tune file compatibility** before flashing
- **Confirm destructive operations** with user warnings
- **Test voltage levels** before starting flash operations
- **Backup before modifications** to ECU

### Python Code Style
- Follow PEP 8 conventions
- Use type hints where possible
- Add docstrings for classes and functions
- Keep functions focused and single-purpose
- Use meaningful variable names (avoid single letters except for loops)
- Handle exceptions explicitly, avoid bare `except:`
- Log important operations and errors

### TypeScript/JavaScript Style
- Use TypeScript for all new code
- Follow ESLint rules configured in the project
- Use functional components with hooks
- Prefer async/await over promises
- Use proper typing, avoid `any`
- Follow Next.js best practices (Server/Client Components)

### File Organization
- Python modules in root directory
- Web components follow Next.js structure
- Documentation in markdown files at root
- Build scripts in root with `.sh` extension
- Android-specific code in files with `_android` suffix

## Key Files

### Python Application Files
- `RFTX_FLASHER.py`: Core ECU flashing logic
- `rftx_gui.py`: Desktop GUI application
- `rftx_flasher_android.py`: Android-specific implementation
- `main.py`: Kivy app entry point for Android
- `tune_matcher.py`: Automatic tune file matching
- `android_usb_serial.py`: USB serial communication for Android
- `android_permissions.py`: Android runtime permissions

### Build Configuration
- `buildozer.spec`: Android build configuration
- `requirements.txt`: Python dependencies
- `package.json`: Node.js dependencies and scripts
- `build_apk.sh`: Automated build script

### Documentation
- `README.md`: Main project documentation
- `BUILD_INSTRUCTIONS.md`: Detailed build guide
- `QUICK_START.md`: Quick start guide
- `README_ANDROID.md`: Android app usage
- `TROUBLESHOOTING.md`: Common issues and solutions
- `APK_BUILD_SUMMARY.md`: APK build summary

## Common Tasks

### Adding New ECU Support
1. Update supported ECU list in documentation
2. Add ECU-specific communication protocols
3. Test with actual hardware or simulators
4. Update tune matching logic
5. Add validation for new ECU types

### Modifying GUI
- Kivy files use `.kv` language for layouts
- Update both desktop (`rftx_gui.py`) and Android (`rftx_flasher_android.py`) if needed
- Test on multiple screen sizes
- Ensure touch targets are appropriate size for mobile

### Updating Dependencies
- **Python**: Update `requirements.txt`, test desktop and Android builds
- **Node.js**: Update `package.json`, run `npm install` or `pnpm install`
- Always test after dependency updates
- Check for breaking changes in changelogs

### Working with Serial Communication
- Always implement timeouts
- Handle device disconnection gracefully
- Validate data before sending to ECU
- Log all communication for debugging
- Test with different cable types (FTDI, CH340)

## Development Environment

### Python Development
- Python 3.8+ required
- Virtual environment recommended: `python -m venv venv`
- Linux required for Android builds (or use WSL2/VM on Windows/Mac)
- 4GB+ RAM for Android builds
- 5GB+ disk space for SDK/NDK

### Web Development
- Node.js 18+ recommended
- pnpm preferred over npm
- TypeScript enabled by default

### Android Development
- Android device with USB OTG support for testing
- USB debugging enabled
- `adb` installed for deployment
- K+DCAN cable for actual ECU testing

## Deployment

### Web Deployment
- Automatically deployed to Vercel on push to main branch
- Environment variables managed in Vercel dashboard
- Preview deployments for pull requests

### Android Deployment
- GitHub Actions workflow available (`.github/workflows/build-apk.yml`)
- Manual builds using `./build_apk.sh`
- APK output in `bin/` directory
- Sign APK for release builds

### Desktop Distribution
- Users install Python and dependencies manually
- Consider PyInstaller for standalone executables
- Test on Windows, macOS, and Linux

## Security Considerations

- Never commit API keys or secrets
- Validate all user input
- Sanitize file paths to prevent directory traversal
- Use secure serial communication
- Don't store sensitive ECU data in logs
- Follow OWASP security guidelines

## License & Legal

- Free for personal use
- Commercial use requires permission
- ECU flashing may void warranties
- May violate local laws in some jurisdictions
- Users assume all risk

## Support & Contact

- Email: rftxtuning@gmail.com
- Issues: GitHub Issues
- Web: Deployed on Vercel
- Development: Built with v0.app

## Additional Notes

- First Android build takes 30-60 minutes (downloads SDK/NDK)
- USB permissions must be granted at runtime on Android
- Some devices may require root for USB serial access
- Always ensure stable 12V+ power during ECU flashing
- Always backup ECU before flashing custom tunes
