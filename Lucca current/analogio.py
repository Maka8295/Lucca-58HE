import analogio
import digitalio
import time
import math

import keypad

from kmk.scanners import Scanner
from kmk.modules import Module
from kmk.kmk_keyboard import KMKKeyboard
from kmk.keys import KC
#from hallCali import input_range, output_range
input_range = [7800,1120]
output_range = (0,4)
keyboard = KMKKeyboard()


a=-16.1941
b=0.81885
c=1.66367
d=-16.0382

def remap_range(value, input_range, output_range):
    input_min, input_max = input_range
    output_min, output_max = output_range

    # Avoid division by zero
    if input_max - input_min == 0:
        return output_min

    # Perform the linear mapping
    mv = (value - input_min) / (input_max - input_min) * (output_max - output_min) + output_min

    #a\left(1-e^{\left(-b\left(x_{1}+c\right)\right)}\right)-d
    lut_val = a * (1 - math.exp(-b * (mv + c))) - d

    # Clip the result to make sure it falls within the output range
    mapped_value = max(min(lut_val, output_max), output_min)

    return mapped_value

class AnalogScanner(Scanner):

    def __init__(self,inPins,outPins,multiNum,numOfKeys,analogAttrib):

        self.inPins = [analogio.AnalogIn(pin) for pin in inPins] #setup pins where analog signals are read

        self.outPins = [digitalio.DigitalInOut(pin) for pin in outPins] #setup pins to controll multiplexers
        for pin in self.outPins:
            pin.direction = digitalio.Direction.OUTPUT

        self.multiNum = multiNum

        self.aVal = [4]*self.multiNum*len(inPins) #array to store current value
        self.aValold = [4]*self.multiNum*len(inPins) #array to store last value
        self.que = [] #que to store keys which have to be pressed
        #print(self.aVal)
        self.pressed = [False]*self.multiNum*len(inPins) #array to store state of keys
        self.numOfKeys = numOfKeys #number of keys

        self.analogAttrib = analogAttrib #per key info about threshold/press type



    @property
    def key_count(self):
        return self.numOfKeys

    def scan_for_changes(self):
        '''
        Poll the analog pins for changes and return either None (if nothing updated)
        or a KeyEvent object if the pin value exceeds the threshold.
        '''

        #print(self.offset)
        if len(self.que) == 0: #if no key is in que
            for i in range(self.multiNum): #cycles through multiplexer
                self.outPins[0].value = (i & 0b00001) != 0
                self.outPins[1].value = (i & 0b00010) != 0
                self.outPins[2].value = (i & 0b00100) != 0
                self.outPins[3].value = (i & 0b01000) != 0
                self.outPins[4].value = (i & 0b10000) != 0
                for index, j in enumerate(self.inPins):    #read and stored analog values
                    self.aVal[i + self.multiNum * index] = j.value

            for i in range(self.numOfKeys):
                self.aVal[i] = remap_range(self.aVal[i], input_range[i+self.offset], output_range)

            for i in range(self.numOfKeys): #checks if values have changed

                #
                if self.analogAttrib[keyboard.active_layers[0]][i + self.offset] > 0:
                    if self.aVal[i] < self.analogAttrib[keyboard.active_layers[0]][i + self.offset] and self.pressed[i] == False:
                        self.pressed[i] = True
                        self.que.append(i)
                    elif self.aVal[i] > self.analogAttrib[keyboard.active_layers[0]][i + self.offset] and self.pressed[i] == True:
                        self.pressed[i] = False
                        self.que.append(i)
                #rapid trigger mode
                elif self.analogAttrib[keyboard.active_layers[0]][i + self.offset] < 0:
                    if self.aVal[i] < self.aValold[i] - abs(self.analogAttrib[keyboard.active_layers[0]][i + self.offset]):
                        self.aValold[i] = self.aVal[i]
                        if not self.pressed[i]:
                            self.pressed[i] = True
                            self.que.append(i)
                    elif self.aVal[i] > self.aValold[i] + abs(self.analogAttrib[keyboard.active_layers[0]][i + self.offset]):
                        self.aValold[i] = self.aVal[i]
                        if self.pressed[i]:
                            self.pressed[i] = False
                            self.que.append(i)
                    elif self.pressed[i] and self.aVal[i]>3.9: #edge case if key gets stuck
                        self.aValold[i] = self.aVal[i]
                        self.pressed[i] = False
                        self.que.append(i)

        elif len(self.que) > 0: #if keys in que: remove one from que and send return
            temp = self.que.pop(0)
            #print(temp, self.pressed[temp])
            return keypad.Event(temp+self.offset, self.pressed[temp])
