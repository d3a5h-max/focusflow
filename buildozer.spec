[app]
title = FocusFlow
package.name = focusflow
package.domain = com.focusflow
source.dir = .
source.include_exts = py,kv,png,jpg,atlas,json,md,txt
version = 0.1.0
requirements = python3,kivy==2.3.1
orientation = portrait
fullscreen = 0

# Android configuration. Keep permissions minimal in the starter.
android.api = 35
android.minapi = 23
android.archs = arm64-v8a
android.accept_sdk_license = True

[buildozer]
log_level = 2
warn_on_root = 1
