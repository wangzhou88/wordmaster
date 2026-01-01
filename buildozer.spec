[app]

# (str) Title of your application
title = WordMaster英语学习助手

# (str) Package name
package.name = wordmaster

# (str) Package domain (needed for android/ios packaging)
package.domain = org.wordmaster

# (str) Source code where the main.py live
source.dir = .

# (list) Source files to include (let empty to include all the files)
source.include_exts = py,png,jpg,kv,atlas,wav,mp3,db

# (list) List of inclusions using pattern matching
source.include_patterns = data/*,models/*,utils/*,*.db

# (list) Source files to exclude (let empty to not exclude anything)
#source.exclude_exts = spec

# (list) List of directory to exclude (let empty to not exclude anything)
source.exclude_dirs = .venv,.git,__pycache__,build,dist

# (list) List of exclusions using pattern matching
# Do not prefix with './'
source.exclude_patterns = *.pyc,*.pyo,.DS_Store

# (str) Application versioning (method 1)
version = 1.0

# (str) Application versioning (method 2)
# version.regex = __version__ = ['"](.*)['"]
# version.filename = %(source.dir)s/main.py

# (list) Application requirements
# comma separated e.g. requirements = sqlite3,kivy
requirements = python3,kivy==2.2.1,kivymd==1.1.1,gtts==2.3.2,pygame==2.5.2,speechrecognition==3.10.1,pydub==0.25.1,matplotlib==3.8.0,numpy==1.26.0,pandas==2.1.1

# (str) Custom source folders for requirements
# Sets custom source for any requirements with recipes
# requirements.source.kivy = ../../kivy

# (str) Presplash of the application
#presplash.filename = %(source.dir)s/data/presplash.png

# (str) Icon of the application
#icon.filename = %(source.dir)s/data/icon.png

# (str) Supported orientation (landscape, sensor_landscape, sensor_portrait, or all)
orientation = portrait

# (bool) Indicate if the application should be fullscreen or not
fullscreen = 0

# (list) Permissions
android.permissions = INTERNET,RECORD_AUDIO,WRITE_EXTERNAL_STORAGE,READ_EXTERNAL_STORAGE

# (int) Target Android API, should be as high as possible.
android.api = 33

# (int) Minimum API your APK will support.
android.minapi = 21

# (str) Android NDK version to use
android.ndk = 25b

# (str) Android SDK version to use
android.sdk = 33

# (bool) Use --private data storage (True) or --dir public storage (False)
android.private_storage = True

# (str) Android app theme, default is ok for Kivy-based app
android.theme = "@android:style/Theme.NoTitleBar"

# (list) Pattern to whitelist for the whole project
android.whitelist = 

# (bool) Enable AndroidX support. Enable when 'android.gradle_dependencies'
# contains an 'androidx' package, or any package from Kotlin source.
# android.enable_androidx requires android.api >= 28
android.enable_androidx = True

# (list) add java compile options
# this can for example be necessary when importing certain java libraries using the 'android.gradle_dependencies' option
# see https://developer.android.com/studio/write/java8-support for further information
android.add_compile_options = "sourceCompatibility = 1.8", "targetCompatibility = 1.8"

# (str) The format used to package the app for release mode (aab or apk).
android.release_artifact = aab

# (bool) Enable AndroidX support. Enable when 'android.gradle_dependencies'
# contains an 'androidx' package, or any package from Kotlin source.
# android.enable_androidx requires android.api >= 28
android.enable_androidx = True

[buildozer]

# (int) Log level (0 = error only, 1 = info, 2 = debug (with command output))
log_level = 2

# (int) Display warning if buildozer is run as root (0 = False, 1 = True)
warn_on_root = 1

# (str) Path to build artifact storage, absolute or relative to spec file
build_dir = ./.buildozer

# (str) Path to build output APK/iOS/app file storage, relative to build_dir
bin_dir = ./bin

[ios]

# (str) Path to a custom kivy-ios folder
#ios.kivy_ios_url = https://github.com/kivy/kivy-ios
# Alternately, specify the URL and branch of a git checkout:
ios.kivy_ios_url = https://github.com/kivy/kivy-ios
ios.kivy_ios_branch = master

# Another platform dependency: ios-deploy
# Uncomment to use a custom checkout
#ios.ios_deploy_url = https://github.com/ios-control/ios-deploy.git
# Alternately, specify the URL and branch of a git checkout:
ios.ios_deploy_url = https://github.com/ios-control/ios-deploy.git
ios.ios_deploy_branch = master

# (str) Name of the certificate to use for signing the debug version
# Get a list of available identities: xcodebuild -list -identities
ios.codesign.debug = "iPhone Developer: <lastname> <hex UUID>"

# (str) The development team to use for signing the debug version
ios.codesign.development_team.debug = <hex UUID>

# (str) Name of the certificate to use for signing the release version
ios.codesign.release = %(ios.codesign.debug)s

ios.development_team.debug = %(ios.codesign.development_team.debug)s

# (str) The bundle id to use for signing the debug version
ios.bundle_id.debug = org.test.wordmaster

# (str) The bundle id to use for signing the release version
ios.bundle_id.release = org.test.wordmaster

# (str) Filename to use as the icon for the iOS home screen
# Icon filename should follow the format Icon-57.png (29x29 pixels), Icon@2x.png (58x58 pixels), etc.
ios.icon.filename = %(source.dir)s/data/icon.png

# (str) Title to display on the iOS home screen
ios.title = WordMaster

# (str) The bundle id for the iOS app
ios.bundle_id = org.test.wordmaster

# (str) The minimum version on iOS version
ios.minimum_os_version = 11.0

# (str) Format string used when naming the resulting iOS app
ios.format = ios

# (str) URL pointing to .ipa file to be installed
#ios.url = 

# (str) Mode of the bundled iOS app
ios.mode = development

# (str) App signing configuration
ios.signature = 

# (bool) Toggle to build for iOS using bitcode
ios.bitcode = False