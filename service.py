from subprocess import getoutput
from time import sleep
from termcolor import colored
import ipaddress
from os import getcwd
import re

ip_regex = r'\b\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}\b'

try:
    folder = getcwd()

    adb = '"'+ folder + "\\scrcpy\\adb.exe" + '"'
    scrcpy = '"' + folder + "\\scrcpy\\scrcpy.exe" + '"'

    input(colored("PROMPT: Make sure USB debugging is enabled on your device and press ENTER to continue","blue"))
    input(colored("PROMPT: Make sure your device is connected to the same network as your PC and press ENTER to continue","blue"))
    input(colored("PROMPT: Make sure your device is connected to your PC via USB and press ENTER to continue", "blue"))

    print(colored("INFO: Killing adb server", "yellow"))
    output = getoutput(f"{adb} kill-server")
    sleep(3)
    print(output)

    print(colored("INFO: Starting adb server", "yellow"))
    output = getoutput(f"{adb} start-server")
    sleep(3)
    print(output)

    print(colored("INFO: Restarting adb server to port 5555", "yellow"))
    output = getoutput(f"{adb} tcpip 5555")
    sleep(5)
    print(output)

    print(colored("INFO: Getting device IP address", "yellow"))
    output = getoutput(f"{adb} shell ip addr show wlan0")
    sleep(1)
    ip_list = re.findall(ip_regex, output)
    if len(ip_list) == 0:
        print(colored(f"ERROR: Couldn't get device IP address :(", "red"))
        exit()
    ipaddress.ip_address(ip_list[0])
    print(colored(f"SUCCESS: Device IP address = {ip_list[0]}", "green"))
    print(colored("INFO: Connecting to device", "yellow"))
    output = getoutput(f"{adb} connect "+ip_list[0])
    sleep(2)
    print(output)
    
    print(colored("SUCCESS: Device connected successfully", "green"))
    input(colored("PROMPT: Remove USB cable and press ENTER to continue", "blue"))

    print(colored("INFO: Starting scrcpy", "yellow"))
    output = getoutput(f"{scrcpy} --fullscreen -m 5000")
    print(output)

except Exception as e:
    print(colored(f"ERROR: Couldn't get device :(", "red"))

input(colored("PROMPT: Press ENTER to exit", "blue"))