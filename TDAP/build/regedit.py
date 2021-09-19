from subprocess import check_output as system
from scanmap import transform as tr

class functions:
    disabledPrograms = {}
    disableCount = 0
    transform = tr()

    def __init__(self):
        system("REG ADD HKCU\SOFTWARE\Microsoft\Windows\CurrentVersion\Policies\Explorer /v DisallowRun /t REG_DWORD /d 1 /f")

    def __removeKey__(self, key):
        value = self.disabledPrograms.get(key)
        del self.disabledPrograms[key]
        
        return value

    def __addKey__(self, key):
        self.disableCount += 1
        self.disabledPrograms[key] = self.disableCount

        return self.disableCount

    def disableTaskMananger(self, disableTaskMgr = None):
        if disableTaskMgr == None:
            disableTaskMgr = input('Disable Task Manager (yes/no)? ').lower()

        if disableTaskMgr == 'yes':
            system("REG ADD HKCU\SOFTWARE\Microsoft\Windows\CurrentVersion\Policies\System /v DisableTaskMgr /t REG_DWORD /d 1 /f")
        else:
            system("REG ADD HKCU\SOFTWARE\Microsoft\Windows\CurrentVersion\Policies\System /v DisableTaskMgr /t REG_DWORD /d 0 /f")
    
    def disableProgram(self, prog = None):
        if prog == None:
            prog = input('Program to disable: ').lower() + '.exe'

        try:
            if prog != 'None':
                system(f"REG ADD HKCU\SOFTWARE\Microsoft\Windows\CurrentVersion\Policies\Explorer\DisallowRun /v {self.__addKey__(prog)} /t REG_SZ /d {prog} /f")
        except:
            pass
    
    def enableProgram(self, prog = None):
        if prog == None:
            prog = input('Program to enable: ').lower() + '.exe'
        
        try:
            if prog != 'None':
                system(f"REG DELETE HKCU\SOFTWARE\Microsoft\Windows\CurrentVersion\Policies\Explorer\DisallowRun /v {self.__removeKey__(prog)} /f")
        except:
            pass
    
    def disableKeys(self, keysToDisable = []):
        hexCode = self.transform.getHexValue(keyList = keysToDisable)

        try:
            system('''REG DELETE "HKLM\SYSTEM\CurrentControlSet\Control\Keyboard Layout" /v "Scancode Map" /f''')
        except:
            pass

        system(f'''REG ADD "HKLM\SYSTEM\CurrentControlSet\Control\Keyboard Layout" /v "Scancode Map" /t REG_BINARY /d {hexCode} /f''')
    
    def enableKeys(self):
        try:
            system('''REG DELETE "HKLM\SYSTEM\CurrentControlSet\Control\Keyboard Layout" /v "Scancode Map" /f''')
        except:
            pass