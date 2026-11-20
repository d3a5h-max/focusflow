# Android build notes

Buildozer is best run on a supported Linux environment. On Windows, use WSL2 with Ubuntu rather than running Buildozer directly in native PowerShell.

## WSL2 outline

1. Install WSL2 and Ubuntu.
2. Install the system packages required by the current Buildozer documentation.
3. Install Python and create a virtual environment.
4. Install Buildozer and Cython in that environment.
5. From the project directory, run:

```bash
buildozer android debug
```

The first build downloads Android SDK/NDK components and can take a while.

## Permissions

The starter intentionally requests no special Android permissions. Do not add Accessibility, Usage Access, notification, overlay, VPN, or device-admin permissions without first documenting the user benefit, platform policy, consent flow, and safer alternatives.

Background timers and reliable alarms need dedicated Android design and device testing. A normal Python/Kivy clock is not guaranteed to continue when Android suspends or kills the app.

Always verify a successful build in GitHub Actions and install/test the resulting APK on a physical device before describing it as release-ready.
