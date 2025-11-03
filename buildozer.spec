[app]

# Application title
title = RFTX Tuning

# Package name
package.name = rftxtuning

# Package domain (needed for android/ios packaging)
package.domain = com.rftx

# Source code directory
source.dir = .

# Source files to include
source.include_exts = py,png,jpg,kv,atlas,json

# Application versioning
version = 1.0

# Application requirements
requirements = python3,kivy==2.3.0,pyjnius,android

# Presplash background color
presplash.color = #1C1C1C

# Icon filename
#icon.filename = %(source.dir)s/icon.png

# Supported orientations
orientation = portrait

# Android specific settings
[app:android]

# Android API level to use
android.api = 33

# Minimum API level required
android.minapi = 21

# Android SDK version to use
android.sdk = 33

# Android NDK version to use
android.ndk = 25b

# Android permissions
android.permissions = INTERNET,READ_EXTERNAL_STORAGE,WRITE_EXTERNAL_STORAGE,USB_PERMISSION,ACCESS_FINE_LOCATION

# Android features
android.features = android.hardware.usb.host

# Add USB host support
android.meta_data = android.hardware.usb.host=true

# Android application theme
android.theme = @android:style/Theme.NoTitleBar.Fullscreen

# Android entrypoint
android.entrypoint = org.kivy.android.PythonActivity

# Android app architecture
android.archs = arm64-v8a,armeabi-v7a

# Android logcat filters
android.logcat_filters = *:S python:D

# Copy library dependencies
android.add_src = 

# Gradle dependencies
android.gradle_dependencies = 

# Java classes to add as activities
android.add_activities = 

# Android services
android.services = 

# Wakelock to prevent device from sleeping
android.wakelock = True

# Android manifest XML additions
android.manifest.intent_filters = 

# USB device filter for K+DCAN adapters
android.manifest.intent_filters = usb_device_filter.xml

[buildozer]

# Log level (0 = error only, 1 = info, 2 = debug)
log_level = 2

# Display warning if buildozer is run as root
warn_on_root = 1

# Build directory
build_dir = ./.buildozer

# Binary directory
bin_dir = ./bin
