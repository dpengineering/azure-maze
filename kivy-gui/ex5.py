"""
Exercise 5 functions
"""

def text_toggle(text):
    print("Text Toggle\n Text is: %s" % text)
    if (text == "Obj-1"):
        return " "
    else:
        return "Obj-1"




def counter_text(text):
    text = int(text)
    print("Counter Pressed\n")
    print("Number entered: %i" % text)
    result = text + 1
    print("Number incremented")
    print("Returning %i" % result)
    return str(result)



def motor_toggle(text):
    print("Motor Pressed Toggle\n")
    if (text == "Motor On"):
        return "Motor Off"
    else:
        return "Motor On"
