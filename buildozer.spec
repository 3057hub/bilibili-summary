[app]

# (str) Title of your application
title = BiliSummary

# (str) Package name
package.name = bilisummary

# (str) Package domain (needed for android/ios packaging)
package.domain = com.bilisummary

# (str) Source code where the main.py live
source.dir = .

# (list) Source files to include (let empty to include all the files)
source.include_exts = py,png,jpg,jpeg,html,css,js,md,toml,ttf,svg,icns

# (list) List of inclusions using pattern matching
source.include_patterns = static/*,routes/*,docs/*,config.toml,icon.png

# (list) Source files to exclude (let empty to not exclude anything)
source.exclude_patterns = venv/*,.git/*,__pycache__/*,.agent/*

# (str) Application versioning
version = 1.0.0

# (str) Application versioning (android)
version.code = 1

# (list) Application requirements
# comma separated e.g. requirements = sqlite3,kivy
requirements = python3,kivy,fastapi,uvicorn,anthropic,bilibili-api-python,aiohttp,python-dotenv,toml,pydantic,starlette,anyio,httptools

# (str) Supported orientations
# one of landscape, portrait or all
orientation = portrait

# (bool) Indicate if the application should be fullscreen or not
fullscreen = 0

# (str) Presplash of the application
presplash.filename = icon.png

# (str) Icon of the application
icon.filename = icon.png

# (str) The Android arch to build for, choices: armeabi-v7a, arm64-v8a, x86, x86_64
android.arch = arm64-v8a

# (int) Target Android API
android.api = 31

# (int) Minimum API your APK will support
android.minapi = 26

# (int) Android NDK version to use
android.ndk = 25c

# (str) Python version to use (3.11 is stable, avoid 3.14)
p4a.python_version = 3.11

# (int) Android SDK version to use
android.sdk = 34

# (list) Android permissions
android.permissions = INTERNET

# (bool) Skip the automatic update of Android SDK
android.skip_update = False

# (bool) Accept Android SDK License
android.accept_sdk_license = True

# (bool) Allow the app to be installed on external storage
android.allow_backup = True

# (str) XML to add in the AndroidManifest
android.manifest.application_meta = android:usesCleartextTraffic="true"

# (list) Java classes to add as activities to the manifest
# android.add_activity =

# (list) Java classes or JAR files to include
# android.add_jar =

# (list) Gradle dependencies to add
# android.gradle_dependencies =

# (bool) Use AndroidX
android.use_androidx = True

# (str) android-presplash gradient
android.presplash_color = #0B1220

# (str) Supported Gradle version
# android.gradle_version =

# (str) Custom Gradle build file
# android.gradle_build =

# (str) Entry point for the app
package.executable = main.py

# (bool) Whether the app is a Kivy app
android.kivy_application = True

#
# OSX Specific
#
[buildozer]

# (int) Log level (0 = error only, 1 = info, 2 = debug (with command output))
log_level = 2

# (int) Display warning if buildozer is run as root (0 = False, 1 = True)
warn_on_root = 1

# (str) Path to build artifact storage, absolute or relative to spec file
# build_dir = ./.buildozer

# (str) Path to build output (i.e. .apk, .aab) storage
# bin_dir = ./bin
