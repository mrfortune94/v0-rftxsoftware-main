#!/bin/bash
# build_apk.sh - Script to build the RFTX Tuning Android APK

set -e

echo "================================================"
echo "RFTX Tuning - Android APK Build Script"
echo "================================================"
echo ""

# Check if running on Linux
if [ "$(uname)" != "Linux" ]; then
    echo "ERROR: This script must run on Linux (Ubuntu 20.04+ recommended)"
    echo "For Windows/Mac, please use WSL2 or a Linux VM"
    exit 1
fi

# Check Python version
echo "Checking Python version..."
PYTHON_VERSION=$(python3 --version 2>&1 | awk '{print $2}')
echo "Python version: $PYTHON_VERSION"

# Check Java version
echo "Checking Java version..."
if command -v java &> /dev/null; then
    JAVA_VERSION=$(java -version 2>&1 | head -n 1)
    echo "Java version: $JAVA_VERSION"
else
    echo "ERROR: Java not found. Please install OpenJDK 11 or 17"
    exit 1
fi

# Install system dependencies
echo ""
echo "Installing system dependencies..."
if ! sudo apt update; then
    echo "Warning: apt update failed, continuing anyway..."
fi

# Install core dependencies
if ! sudo apt install -y git zip unzip openjdk-17-jdk autoconf libtool \
    pkg-config zlib1g-dev libncurses-dev cmake libffi-dev libssl-dev; then
    echo "ERROR: Failed to install required system dependencies"
    echo "Please install manually and try again"
    exit 1
fi

# Install Python packages
echo ""
echo "Installing Buildozer and Cython..."
pip3 install --user --upgrade pip
pip3 install --user -r requirements.txt

# Add local bin to PATH
export PATH=$PATH:~/.local/bin

# Verify installations
echo ""
echo "Verifying installations..."
if ! command -v buildozer &> /dev/null; then
    echo "ERROR: Buildozer not found in PATH"
    echo "Please add ~/.local/bin to your PATH"
    exit 1
fi

echo "Buildozer version: $(buildozer --version)"

# Clean previous builds (optional)
if [ "$1" == "--clean" ]; then
    echo ""
    echo "Cleaning previous build..."
    rm -rf .buildozer bin
fi

# Build the APK
echo ""
echo "================================================"
echo "Building Android APK (this may take 30-60 minutes on first build)"
echo "================================================"
echo ""

buildozer android debug

# Check if build succeeded
if ls bin/*.apk 1> /dev/null 2>&1; then
    echo ""
    echo "================================================"
    echo "BUILD SUCCESSFUL!"
    echo "================================================"
    echo ""
    echo "APK file(s):"
    ls -lh bin/*.apk
    echo ""
    echo "To install on your Android device:"
    echo "  adb install -r bin/rftxtuning-1.0-debug.apk"
    echo ""
    echo "Or deploy directly:"
    echo "  buildozer android deploy run"
    echo ""
else
    echo ""
    echo "================================================"
    echo "BUILD FAILED!"
    echo "================================================"
    echo ""
    echo "Please check the log above for errors."
    echo "Common issues:"
    echo "  - Network timeouts: Try again or use a VPN"
    echo "  - Low disk space: Requires ~5GB free space"
    echo "  - Missing dependencies: Re-run dependency installation"
    echo ""
    exit 1
fi
