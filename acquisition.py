#!/usr/bin/python

# Author: Fabian Nunes
# Acquisition script to get the private folder application folder from and Android application in a rooted device or
# emulator, script based on the work of @mfrade and is bash implementation
# Example: python acquisition.py com.example.app -d

import sys
import os
import subprocess
from datetime import datetime

USER = 0

# total number of arguments
n = len(sys.argv)

# The number of arguments should be 3 (including the script name, package name and type of acquisition)
if n == 3:
    APP = sys.argv[1]
    DEVICE = sys.argv[2]
else:
    print("Usage: python3 acquisition.py <package name> [-d | -e]")
    print("Device types: e- (emulator), d - usb")
    print("Example: python3 acquisition.py com.garmin.android.apps.connectmobile e-")
    sys.exit()

# Type of acquisition either "-e" for emulator or "-d" for usb device
if DEVICE == "-e":
    print("[Info ] Acquiring from device: emulator")
    CMD = "su 0"
    END = ""
    DEVNAME = "emu"
elif DEVICE == "-d":
    print("[Info ] Acquiring from device: USB")
    CMD = "su -c '"
    END = "'"
    DEVNAME = "usb"
else:
    print("[ERROR] Unknown device " + DEVICE)
    print("Device types: e- (emulator), d - usb")
    sys.exit()

if os.name == 'nt':
    print("[Info ] Host OS: Windows")
    ADB = subprocess.run("where adb", shell=True, capture_output=True)
    ADB = ADB.stdout.decode("utf-8").strip()

    # ADB = os.popen('where adb').read().strip()
    print("[Info ] Does " + APP + " exist?")
    IsDir = subprocess.run(ADB + " " + DEVICE + " shell pm list packages | findstr " + APP, stdout=subprocess.PIPE, shell=True)

    if IsDir.returncode == 0:
        print("[Info ] Yes!")
    else:
        print("[ERROR] " + APP + " does not exist!")
        sys.exit()

    print("[Info ] Getting Info...")

    VERSION = subprocess.run(ADB + " " + DEVICE + " shell pm dump " + APP + " | findstr versionName", shell=True, capture_output=True)


else:
    print("[Info ] You are running this script on Linux machine")
    ADB = subprocess.run("which adb", shell=True, capture_output=True)
    ADB = ADB.stdout.decode("utf-8").strip()

    print("[Info ] Does " + APP + " exist?")
    IsDir = subprocess.run(ADB + " " + DEVICE + " shell pm list packages | grep " + APP, stdout=subprocess.PIPE, shell=True)

    if IsDir.returncode == 0:
        print("[Info ] Yes!")
    else:
        print("[ERROR] " + APP + " does not exist!")
        sys.exit()

    VERSION = subprocess.run(ADB + " " + DEVICE + " shell pm dump " + APP + " | grep versionName", shell=True, capture_output=True)


VERSION = VERSION.stdout.decode("utf-8").strip()
VERSION = VERSION.split("=")[1]

ANDROID = subprocess.run(ADB + " " + DEVICE + " shell getprop ro.build.version.release", shell=True, capture_output=True)
ANDROID = ANDROID.stdout.decode("utf-8").strip()

FILENAME = APP + "-v" + str(VERSION) + "--" + DEVNAME + str(ANDROID) + "-u" + str(USER) + "--" + datetime.now().strftime("%Y%m%d-%H%M%S") + ".tar"

print("[Info ] " + APP + " version: " + str(VERSION))
print("[Info ] Android version: " + str(ANDROID))

print("[Info ] Copying data from " + APP + " version " + VERSION + " ...")

#subprocess.run(ADB + " " + DEVICE + " shell " + CMD + " tar -cvzf /sdcard/Download/" + FILENAME + " /data/data/" + APP + END, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, shell=True)

# Not working need to check why
# Check for filename with spaces
# print(ADB + " " + DEVICE + " shell " + CMD + " find /data/user_de/" + str(USER) + "/" + APP + " -print0 > /sdcard/Download/" + FILENAME + ".1.txt " + END)
os.system(ADB + " " + DEVICE + " shell " + CMD + " find /data/user_de/" + str(USER) + "/" + APP + " -print0 > /sdcard/Download/" + FILENAME + ".1.txt " + END)
os.system(ADB + " " + DEVICE + " shell " + CMD + " find /data/user/" + str(USER) + "/" + APP + " -print0 > /sdcard/Download/" + FILENAME + ".2.txt " + END)
os.system(ADB + " " + DEVICE + " shell " + CMD + " tar -cvzf /sdcard/Download/" + FILENAME + " -T /sdcard/Download/" + FILENAME + ".1.txt " + "-T /sdcard/Download/" + FILENAME + ".2.txt " + END)

print("[Info ] Copy Terminated.")

print("[Info ] Compressing " + FILENAME + " ...")
subprocess.run(ADB + " " + DEVICE + " shell gzip /sdcard/Download/" + FILENAME, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, shell=True)
print("[Info] Compressing Terminated.")

print("[Info ] Copying to local storage ...")
subprocess.run(ADB + " " + DEVICE + " pull /sdcard/Download/" + FILENAME+".gz", stdout=subprocess.DEVNULL, shell=True)
print("[Info ] Copy Terminated.")

print("[Info ] Cleaning acquisition files from phone...")
subprocess.run(ADB + " " + DEVICE + " shell rm /sdcard/Download/" + FILENAME + ".gz", stdout=subprocess.DEVNULL, shell=True)
# os.system(ADB + " " + DEVICE + " shell rm /sdcard/Download/" + FILENAME + ".?.txt")
print("[Info ] Clean Terminated.")
