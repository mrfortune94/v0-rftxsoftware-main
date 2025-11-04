# APK Build Troubleshooting Guide

This guide helps you resolve common issues when building the RFTX Tuning Android APK.

## Common Issues

### 1. Network Timeout Errors

**Symptoms:**
```
TimeoutError: The read operation timed out
ERROR: Exception while downloading packages
```

**Solutions:**
- **Use GitHub Actions**: The automated workflow has better network connectivity
- **Retry the build**: Sometimes temporary network issues resolve themselves
- **Use a VPN**: Some networks block PyPI or GitHub
- **Increase pip timeout**:
  ```bash
  pip install --timeout=300 buildozer cython
  ```
- **Use a mirror**: Configure pip to use a different mirror  
  ⚠️ **Security Note**: Only use trusted mirrors. Alternative mirrors may not have the same security validation as official PyPI. Verify package integrity when possible.
  ```bash
  # Example with an alternative mirror (use trusted sources only)
  pip install -i https://pypi.org/simple buildozer cython
  ```

### 2. Duplicate Option Error

**Symptoms:**
```
configparser.DuplicateOptionError: option 'android.manifest.intent_filters' already exists
```

**Solution:**
This has been fixed in the latest buildozer.spec. If you still see this error:
1. Edit `buildozer.spec`
2. Remove one of the duplicate `android.manifest.intent_filters` lines
3. Keep only one entry: `android.manifest.intent_filters = usb_device_filter.xml`

### 3. NDK Version Mismatch

**Symptoms:**
```
ERROR: Could not find NDK version 25b
```

**Solution:**
The buildozer.spec has been updated to use NDK 26.3.11579264. If you need a different version:
1. Check available NDK versions: `ls $ANDROID_SDK_ROOT/ndk/` (if SDK is installed)
2. Edit buildozer.spec and update the `android.ndk` line
3. Or let buildozer download it automatically (takes longer)

### 4. Java Version Issues

**Symptoms:**
```
ERROR: Java compiler (javac) not found
ERROR: Incompatible Java version
```

**Solutions:**
- **Install Java 11 or 17**:
  ```bash
  sudo apt install openjdk-17-jdk
  ```
- **Set JAVA_HOME**:
  ```bash
  export JAVA_HOME=/usr/lib/jvm/java-17-openjdk-amd64
  ```
- **Verify Java version**:
  ```bash
  java -version
  javac -version
  ```

### 5. Out of Memory

**Symptoms:**
```
ERROR: Out of memory
Process killed
```

**Solutions:**
- Close other applications
- Increase swap space:
  ```bash
  sudo fallocate -l 4G /swapfile
  sudo chmod 600 /swapfile
  sudo mkswap /swapfile
  sudo swapon /swapfile
  ```
- Build on a machine with more RAM (minimum 4GB recommended)

### 6. Disk Space Issues

**Symptoms:**
```
ERROR: No space left on device
```

**Solutions:**
- Free up disk space (need ~5GB free)
- Clean previous builds:
  ```bash
  ./build_apk.sh --clean
  # or
  rm -rf .buildozer bin
  ```
- Move build directory to a drive with more space:
  ```bash
  export BUILDOZER_BUILD_DIR=/path/to/large/drive/.buildozer
  ```

### 7. Permission Denied Errors

**Symptoms:**
```
ERROR: Permission denied
```

**Solutions:**
- **Don't run buildozer as root** (it's not recommended)
- Fix permissions:
  ```bash
  chmod +x build_apk.sh
  chmod -R u+w .buildozer
  ```
- If using system Python packages, use `--user` flag:
  ```bash
  pip3 install --user buildozer cython
  ```

### 8. Python Version Issues

**Symptoms:**
```
ERROR: Python 3.X is not supported
```

**Solutions:**
- Use Python 3.8 or 3.9 (most compatible)
- Install correct Python version:
  ```bash
  sudo apt install python3.9 python3.9-dev
  sudo update-alternatives --install /usr/bin/python3 python3 /usr/bin/python3.9 1
  ```

### 9. Missing System Dependencies

**Symptoms:**
```
ERROR: Could not find libffi
ERROR: zlib.h not found
```

**Solutions:**
Install all required system packages:
```bash
sudo apt update
sudo apt install -y \
  git zip unzip openjdk-17-jdk \
  autoconf libtool pkg-config \
  zlib1g-dev libncurses-dev \
  cmake libffi-dev libssl-dev \
  python3-dev build-essential
```

### 10. Buildozer Not Found

**Symptoms:**
```
buildozer: command not found
```

**Solutions:**
- Add ~/.local/bin to PATH:
  ```bash
  export PATH=$PATH:~/.local/bin
  ```
- Add to ~/.bashrc for permanent fix:
  ```bash
  echo 'export PATH=$PATH:~/.local/bin' >> ~/.bashrc
  source ~/.bashrc
  ```
- Verify installation:
  ```bash
  pip3 show buildozer
  which buildozer
  ```

## Platform-Specific Issues

### Ubuntu 24.04 / Debian

**Issue**: libtinfo5 not available
```
E: Unable to locate package libtinfo5
```

**Solution**: Skip libtinfo5, it's not critical:
```bash
# Install without libtinfo5
sudo apt install -y git zip unzip openjdk-17-jdk autoconf libtool \
  pkg-config zlib1g-dev libncurses-dev cmake libffi-dev libssl-dev
```

### WSL (Windows Subsystem for Linux)

**Issues**:
- USB devices not accessible
- Network issues
- Performance problems

**Solutions**:
- Use GitHub Actions instead (recommended for Windows users)
- Or use a Linux VM with USB passthrough
- For network: Use Windows VPN, not WSL VPN

### macOS

**Issue**: Buildozer not officially supported on macOS

**Solution**:
- Use GitHub Actions (recommended)
- Use Linux VM or Docker
- Or use python-for-android directly (advanced)

## GitHub Actions Issues

### Workflow Not Running

**Solutions**:
1. Ensure the workflow file is in `.github/workflows/`
2. Check GitHub Actions is enabled in repository settings
3. Verify you have push access to the repository
4. Check the Actions tab for error messages

### Workflow Times Out

**Solutions**:
- GitHub Actions has a 6-hour limit
- First build may take 1-2 hours
- Subsequent builds use cache and are faster
- Check logs for stuck processes

### Artifact Not Found

**Solutions**:
- Wait for workflow to complete fully
- Check the workflow logs for build errors
- Artifacts expire after 90 days by default
- Re-run the workflow to generate new artifacts

## Advanced Troubleshooting

### Clean Build

If all else fails, try a completely clean build:
```bash
# Remove all build artifacts
rm -rf .buildozer bin ~/.buildozer

# Clear pip cache
pip3 cache purge

# Reinstall buildozer
pip3 uninstall buildozer cython
pip3 install --user --no-cache-dir buildozer cython

# Try building again
./build_apk.sh
```

### Enable Debug Logging

For more detailed error messages:
```bash
# Edit buildozer.spec
# Change: log_level = 2
# To: log_level = 3 (very verbose)

buildozer -v android debug
```

### Check Logs

Build logs are saved to:
- `.buildozer/android/platform/build-*/` - Detailed build logs
- Standard output during build
- `build.log` if using the build script

### Still Having Issues?

1. Check the [Buildozer GitHub Issues](https://github.com/kivy/buildozer/issues)
2. Check the [Kivy Community](https://kivy.org/#community)
3. Search for your specific error message
4. Ask in the Kivy Discord or forums
5. Open an issue on this repository with:
   - Full error message
   - buildozer.spec contents
   - System information (OS, Python version, etc.)
   - Build log

## Quick Reference

### Minimum Requirements
- Linux (Ubuntu 20.04+)
- Python 3.8 or 3.9
- Java 11 or 17
- 4GB RAM
- 5GB disk space
- Stable internet connection

### Build Commands
```bash
# Option 1: Automated script
./build_apk.sh

# Option 2: Manual
buildozer android debug

# Option 3: Deploy to device
buildozer android debug deploy run
```

### Environment Variables
```bash
export ANDROID_HOME=/path/to/android/sdk
export ANDROID_SDK_ROOT=$ANDROID_HOME
export ANDROID_NDK_ROOT=/path/to/ndk
export JAVA_HOME=/usr/lib/jvm/java-17-openjdk-amd64
export PATH=$PATH:~/.local/bin
```

---

For more information, see:
- [BUILD_INSTRUCTIONS.md](BUILD_INSTRUCTIONS.md)
- [QUICK_START.md](QUICK_START.md)
- [Buildozer Documentation](https://buildozer.readthedocs.io/)
