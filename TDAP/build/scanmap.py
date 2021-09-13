from subprocess import check_output as system

class transform:
    currentLocation = system('cd', shell = True).decode('utf-8').strip()
    scanmapFile = open(f"{currentLocation}\\tdap\\scanmap.txt", "r")

    scanmapMass = scanmapFile.readlines()
    scanmapDictionary = {}
    scanmapKeys = []

    for row in scanmapMass:
        row.strip()
        if row != '\n':
            keyValue, hexValue = row.split(" - ")
            scanmapDictionary[keyValue] = hexValue
            scanmapKeys.append(keyValue)

    def __init__(self):
        pass

    def getHexValue(self, keyList = []):
        hexCode = "0000000000000000"
        
        if keyList == []:
            print("Print key list. For exit print 'END'\nList of keys: ")

            while True:
                key = input()

                if key == 'END':
                    break
                elif key not in self.scanmapKeys:
                    print('Key error: invalid key name.')
                else:
                    keyList.append(key)
        else:
            for key in keyList:
                if key not in self.scanmapKeys:
                    keyList.remove(key)
            pass
        
        hexCode += str(len(keyList) + 1).zfill(2) + "000000"

        for key in keyList:
            value = self.scanmapDictionary.get(key)

            hexCode += "0000" + str(value).strip()
        
        hexCode += "00000000"
        return hexCode