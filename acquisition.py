#!/usr/bin/python

import sys
import os
from datetime import datetime

USER = 0

# total number of arguments
n = len(sys.argv)

# The number of arguments should be 3 (including the script name, package name and type of acquisition)
if n == 3:
    APP = sys.argv[1]
    DEVICE = sys.argv[2]
    testName = "com.garmin.android.apps.connectmobile"
else:
    print("Please enter only one argument the application package name")
    sys.exit()

# Type of acquisition either "-e" for emulator or "-d" for usb device
if DEVICE == "-e":
    print("Emulator")
    CMD = "su 0"
    END = ""
    DEVNAME = "emu"
elif DEVICE == "-d":
    print("USB Device")
    CMD = "su -c '"
    END = "'"
    DEVNAME = "usb"
else:
    print("Invalid argument")
    sys.exit()

if os.name == 'nt':
    print("You are running this script on Windows machine")
    # ADB = 'C:\\Program Files\\Android\\android-sdk\\platform-tools\\adb.exe'
    ADB = 'C:\\adb\\adb.exe'
    print("Does the application " + APP + " exist?")
    app = os.system(ADB + " " + DEVICE + " shell pm list packages | findstr " + APP)
    if app == 0:
        print("The application " + APP + " exists")
    else:
        print("The application " + APP + " does not exist")
        sys.exit()

    VERSION = os.popen(ADB + " " + DEVICE + " shell pm dump " + APP + " | findstr versionName").read()
    VERSION = VERSION.split("=")[1]

    ANDROID = os.popen(ADB + " " + DEVICE + " shell getprop ro.build.version.release").read()

else:
    print("You are running this script on Linux machine")
    ADB = 'usr/bin/adb'
    print("Does the application " + APP + " exist?")
    app = os.system(ADB + " " + DEVICE + " shell pm list packages | grep " + APP)
    if app == 0:
        print("The application " + APP + " exists")
    else:
        print("The application " + APP + " does not exist")
        sys.exit()

    VERSION = os.popen(ADB + " " + DEVICE + " shell pm dump " + APP + " | grep versionName").read()
    VERSION = VERSION.split("=")[1]

    ANDROID = os.popen(ADB + " " + DEVICE + " shell getprop ro.build.version.release").read()

# FILENAME = APP + "-v" + str(VERSION) + "--" + DEVNAME + str(ANDROID) + "-u" + str(USER) + "--" + datetime.now().strftime("%Y%m%d-%H%M%S") + ".tar"
FILENAME = "dados.tar"


print(APP + " version: " + str(VERSION))
print("Android version: " + str(ANDROID))

print("Copying data from " + APP + " to " + FILENAME)

os.system(ADB + " " + DEVICE + " shell " + CMD + " tar -cvzf /sdcard/" + FILENAME + " /data/data/" + APP + END)

# Not working need to check why
# Check for filename with spaces
# print(ADB + " " + DEVICE + " shell " + CMD + " find /data/user_de/" + str(USER) + "/" + APP + " -print0 > /sdcard/Download/" + FILENAME + ".1.txt " + END)
# os.system(ADB + " " + DEVICE + " shell " + CMD + " find /data/user_de/" + str(USER) + "/" + APP + " -print0 > /sdcard/Download/" + FILENAME + ".1.txt " + END)
# os.system(ADB + " " + DEVICE + " shell " + CMD + " find /data/user/" + str(USER) + "/" + APP + " -print0 > /sdcard/Download/" + FILENAME + ".2.txt " + END)
# os.system(ADB + " " + DEVICE + " shell " + CMD + " tar -cvzf /sdcard/Download/" + FILENAME + " -T /sdcard/Download/" + FILENAME + ".1.txt " + "-T /sdcard/Download/" + FILENAME + ".2.txt " + END)

print("Copy Terminated")

# print("Compressing " + FILENAME)
# os.system(ADB + " " + DEVICE + " shell gzip /sdcard/Download/" + FILENAME)
# print("Compressing Terminated")

print("Copying " + FILENAME + " to the local machine")
os.system(ADB + " " + DEVICE + " pull /sdcard/" + FILENAME)

# os.system(ADB + " " + DEVICE + " pull /sdcard/Download/" + FILENAME + ".gz")
print("Copying Terminated")

print("Removing the application data from the device")
os.system(ADB + " " + DEVICE + " shell rm /sdcard/" + FILENAME)
#os.system(ADB + " " + DEVICE + " shell rm /sdcard/Download/" + FILENAME + ".gz")
#os.system(ADB + " " + DEVICE + " shell rm /sdcard/Download/" + FILENAME + ".?.txt")
print("Removing Terminated")