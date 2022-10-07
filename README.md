# Android App Acquisition Script
Python script to acquire data form Android apps

## Description
Script to acquire the private folder of an Android app (`/data/data/<app-name>`) as a `tar.gz` file, and adds the app version and a timestamp to the compressed filename. 

> **Note**
>
> This scripts supports files and folder names with spaces on them (which happens on the `zoom` app).


### Requirements

This script requires:
- `adb`
- `Python 3`
- `tar`
- `gzip`

This script was developed and tested on Windows 11 and MacOS 12 and Android 11.


### Examples

Acquire data with the wrong app name:
```
user@linux:~$ python3 acquisition.py com.garmin.android.apps.connectmobile -d
[Info ] Does "com.garmin.android.apps.connectmobile" exist?
[ERROR] "com.garmin.android.apps.connectmobile" does not exist!
```

Acquire data with the correct app name:
```
user@linux:~$ python3 acquisition.py com.garmin.android.apps.connectmobile -d
[Info ] Acquiring from device: USB
[Info ] Host OS: Windows
[Info ] Does com.garmin.android.apps.connectmobile exist?
[Info ] Yes!
[Info ] Getting Info...
[Info ] com.garmin.android.apps.connectmobile version: 4.59
[Info ] Android version: 11
[Info ] Copying data from com.garmin.android.apps.connectmobile version 4.59 ...
[Info ] Copy Terminated.
[Info ] Compressing com.garmin.android.apps.connectmobile-v4.59--usb11-u0--20221007-191307.tar ...
[Info] Compressing Terminated.
[Info ] Copying to local storage ...
[Info ] Copy Terminated.
[Info ] Cleaning acquisition files from phone...
[Info ] Clean Terminated.
```

Uncompress the acquired file (on UNIX):
```
user@linux:~$ gunzip us.zoom.videomeetings-v5.9.6.4756--usb10--u0--2022.03.14T17.01.42.tar.gz
user@linux:~$ tar -xvf us.zoom.videomeetings-v5.9.6.4756--usb10--u0--2022.03.14T17.01.42.tar
data/user_de/0/us.zoom.videomeetings/
data/user_de/0/us.zoom.videomeetings/code_cache/
data/user_de/0/us.zoom.videomeetings/code_cache/com.android.skia.shaders_cache
data/user_de/0/us.zoom.videomeetings/code_cache/com.android.opengl.shaders_cache
data/user_de/0/us.zoom.videomeetings/cache/
data/user/0/us.zoom.videomeetings/
data/user/0/us.zoom.videomeetings/data/
...
```
For windows, use `7zip`  to uncompress the file.

The folder structure should be similar to this:
```
user@linux:~$ tree -d -L 4 data/
data/
├── user
│   └── 0
│       └── us.zoom.videomeetings
│           ├── cache
│           ├── code_cache
│           ├── data
│           ├── files
│           ├── no_backup
│           └── shared_prefs
└── user_de
    └── 0
        └── us.zoom.videomeetings
            ├── cache
            └── code_cache

14 directories
```
