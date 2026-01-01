[app]
title = WordMaster
package.name = wordmaster
package.domain = com.wordmaster.app
source.dir = .
source.include_exts = py,png,jpg,kv,atlas,wav,mp3,json,txt,md,pkl,db,pyc,pyo
version = 1.0.0
requirements = python3,kivy>=2.0.0,sqlite3,requests,plyer,pydub,SpeechRecognition,Pillow,pygame
orientation = portrait
fullscreen = 0
display.softinput_mode = pan

[buildozer]
log_level = 2
warn_on_root = 1

[android]
api = 31
android.permissions = android.permission.RECORD_AUDIO,android.permission.INTERNET,android.permission.ACCESS_NETWORK_STATE,android.permission.WRITE_EXTERNAL_STORAGE,android.permission.READ_EXTERNAL_STORAGE
android.archs = arm64-v8a,armeabi-v7a

[android.api]
minapi = 21

[android.permissions]
allow = True

[android.gradle_dependencies]
compile 'com.google.android.gms:play-services-basement:18.1.0'

[ios]
launch_screen = default
deployment_target = 13.0