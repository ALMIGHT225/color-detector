[app]
title = Color Detector
package.name = colordetector
package.domain = org.example
source.dir = .
source.include_exts = py,png,jpg,kv,atlas
version = 1.0
requirements = python3,kivy,opencv-python,numpy
orientation = portrait
fullscreen = 0

# Permissions nécessaires
android.permissions = CAMERA, INTERNET

[buildozer]
log_level = 2
warn_on_root = 1
