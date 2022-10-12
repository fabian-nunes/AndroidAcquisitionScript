#!/usr/bin/python

# Author: Fabian Nunes
# Acquisition script to get the private folder application folder from and Android application in a rooted device or
# emulator, script based on the work of @mfrade and is bash implementation
# Example: python acquisition.py com.example.app -d
# Attention: In Windows, it is best to run the script in the PowerShell, additionaly use 7zip to extract the .tar.gz file, winrar does not work

import sys
import os
import subprocess
from datetime import datetime


class Bcolors:
    OKBLUE = '\033[94m'
    OKGREEN = '\033[92m'
    FAIL = '\033[91m'


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
    print(Bcolors.OKBLUE + "[Info ] Acquiring from device: emulator")
    CMD = "su 0"
    END = ""
    DEVNAME = "emu"
elif DEVICE == "-d":
    print(Bcolors.OKBLUE + "[Info ] Acquiring from device: USB")
    CMD = "su -c '"
    END = "'"
    DEVNAME = "usb"
else:
    print(Bcolors.FAIL + "[ERROR] Unknown device " + DEVICE)
    print("Device types: e- (emulator), d - usb")
    sys.exit()

if os.name == 'nt':
    print(Bcolors.OKBLUE + "[Info ] Host OS: Windows")
    SHELL = False
    ADB = subprocess.run("where adb", shell=True, capture_output=True)
    ADB = ADB.stdout.decode("utf-8").strip()

    # ADB = os.popen('where adb').read().strip()
    print(Bcolors.OKBLUE + "[Info ] Does " + APP + " exist?")
    IsDir = subprocess.run(ADB + " " + DEVICE + " shell pm list packages | findstr " + APP, stdout=subprocess.PIPE, shell=True)

    if IsDir.returncode == 0:
        print(Bcolors.OKBLUE + "[Info ] Yes!")
    else:
        print(Bcolors.FAIL + "[ERROR] " + APP + " does not exist!")
        sys.exit()

    print(Bcolors.OKBLUE + "[Info ] Getting Info...")

    VERSION = subprocess.run(ADB + " " + DEVICE + " shell pm dump " + APP + " | findstr versionName", shell=True, capture_output=True)


else:
    print(Bcolors.OKBLUE + "[Info ] Host OS: Linux")
    SHELL = True
    ADB = subprocess.run("which adb", shell=True, capture_output=True)
    ADB = ADB.stdout.decode("utf-8").strip()

    print(Bcolors.OKBLUE + "[Info ] Does " + APP + " exist?")
    IsDir = subprocess.run(ADB + " " + DEVICE + " shell pm list packages | grep " + APP, stdout=subprocess.PIPE, shell=True)

    if IsDir.returncode == 0:
        print(Bcolors.OKBLUE + "[Info ] Yes!")
    else:
        print(Bcolors.FAIL + "[ERROR] " + APP + " does not exist!")
        sys.exit()

    VERSION = subprocess.run(ADB + " " + DEVICE + " shell pm dump " + APP + " | grep versionName", shell=True, capture_output=True)


VERSION = VERSION.stdout.decode("utf-8").strip()
VERSION = VERSION.split("=")[1]

ANDROID = subprocess.run(ADB + " " + DEVICE + " shell getprop ro.build.version.release", shell=True, capture_output=True)
ANDROID = ANDROID.stdout.decode("utf-8").strip()

FILENAME = APP + "-v" + str(VERSION) + "--" + DEVNAME + str(ANDROID) + "-u" + str(USER) + "--" + datetime.now().strftime("%Y%m%d-%H%M%S") + ".tar"

print(Bcolors.OKBLUE + "[Info ] " + APP + " version: " + str(VERSION))
print(Bcolors.OKBLUE + "[Info ] Android version: " + str(ANDROID))

print(Bcolors.OKBLUE + "[Info ] Copying data from " + APP + " version " + VERSION + " ...")

# Primary method used to copy the data from the application
# subprocess.run(ADB + " " + DEVICE + " shell " + CMD + " tar -cvzf /sdcard/Download/" + FILENAME + " /data/data/" + APP + END, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, shell=True)

# Method used in the bash script to copy the data from the application
# Check for filename with spaces
subprocess.run(ADB + " " + DEVICE + " shell " + CMD + " find /data/user_de/" + str(USER) + "/" + APP + " -print0 | tee /sdcard/Download/" + FILENAME + ".1.txt " + END, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, shell=SHELL)
subprocess.run(ADB + " " + DEVICE + " shell " + CMD + " find /data/user/" + str(USER) + "/" + APP + " -print0 | tee /sdcard/Download/" + FILENAME + ".2.txt " + END, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, shell=SHELL)
subprocess.run(ADB + " " + DEVICE + " shell " + CMD + " tar -cvzf /sdcard/Download/" + FILENAME + " -T /sdcard/Download/" + FILENAME + ".1.txt " + "-T /sdcard/Download/" + FILENAME + ".2.txt " + END, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, shell=True)

print(Bcolors.OKBLUE + "[Info ] Copy Terminated.")

print(Bcolors.OKBLUE + "[Info ] Compressing " + FILENAME + " ...")
subprocess.run(ADB + " " + DEVICE + " shell gzip /sdcard/Download/" + FILENAME, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, shell=True)
print(Bcolors.OKBLUE + "[Info] Compressing Terminated.")

print(Bcolors.OKBLUE + "[Info ] Copying to local storage ...")
subprocess.run(ADB + " " + DEVICE + " pull /sdcard/Download/" + FILENAME+".gz", stdout=subprocess.DEVNULL, shell=True)
print(Bcolors.OKBLUE + "[Info ] Copy Terminated.")

print(Bcolors.OKBLUE + "[Info ] Cleaning acquisition files from phone...")
subprocess.run(ADB + " " + DEVICE + " shell rm /sdcard/Download/" + FILENAME + ".gz", stdout=subprocess.DEVNULL, shell=True)
os.system(ADB + " " + DEVICE + " shell rm /sdcard/Download/" + FILENAME + ".?.txt")
print(Bcolors.OKBLUE + "[Info ] Clean Terminated.")
print(Bcolors.OKGREEN + "[Done ] Operation Completed with success, generated file: " + FILENAME + ".gz")
