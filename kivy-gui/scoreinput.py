#PSEUDOCODE

class selector:
    def __init__():
        alphabet = ["A","B","C","D","E","F","G","H","I","J","K","L","M","N","O","P","Q","R","S","T","U","V","W","X","Y","Z"]
        pos = 0
    def up():
        if (pos = 0):
            pos = 25
        else:
            pos - 1
    def down():
        if (pos = 25):
            pos = 0
        else:
            pos + 1
    def getLetter():
        return alphabet[pos]

'''
Three selectors for name.
TOTAL CONTROLS: 1 joystick, one select button.

Assign IDs to each button, joystick goes between buttons. Select to click button.

Make three selectors, and a done button that getLetters all letters.
'''
