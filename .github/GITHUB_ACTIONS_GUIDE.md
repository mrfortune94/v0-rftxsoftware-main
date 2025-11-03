# GitHub Actions APK Build Guide

This repository includes an automated GitHub Actions workflow that builds the Android APK automatically.

## How It Works

The workflow (`build-apk.yml`) automatically triggers when you:
- Push code to the `main` or `master` branch
- Create a pull request
- Manually trigger it from the Actions tab

## Setup Steps

1. **Push to GitHub**
   - Click the GitHub logo button in the top right of v0
   - Or manually push this code to a GitHub repository

2. **Wait for Build**
   - Go to your repository on GitHub
   - Click the "Actions" tab
   - Watch the build progress (takes ~20-30 minutes first time)

3. **Download APK**
   - Once complete, click on the workflow run
   - Scroll down to "Artifacts"
   - Download `rftx-tuning-apk.zip`
   - Extract to get your APK file

## Build Time

- **First build**: 20-30 minutes (downloads Android SDK/NDK)
- **Subsequent builds**: 10-15 minutes (uses cache)

## Manual Trigger

You can manually trigger a build:
1. Go to Actions tab
2. Click "Build Android APK" workflow
3. Click "Run workflow" button
4. Select branch and click "Run workflow"

## Creating Releases

To create a release with the APK:
1. Create a git tag: `git tag v1.0.0`
2. Push the tag: `git push origin v1.0.0`
3. The workflow will automatically create a GitHub Release with the APK attached

## Troubleshooting

If the build fails:
- Check the Actions logs for error messages
- Common issues:
  - Buildozer spec configuration errors
  - Missing dependencies in requirements
  - Android SDK/NDK download failures (retry usually fixes)

## Cache

The workflow caches:
- Buildozer global directory (`~/.buildozer`)
- Project buildozer directory (`.buildozer`)

This significantly speeds up subsequent builds.
