from regedit import functions

currentMachine = functions()

currentMachine.disableTaskMananger()
# currentMachine.disableProgram()
# currentMachine.enableProgram()
currentMachine.disableKeys()
# currentMachine.enableKeys()