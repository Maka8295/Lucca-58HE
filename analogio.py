import analogio
import digitalio
import time
import math
import keypad
from kmk.scanners import Scanner
from kmk.modules import Module
from kmk.kmk_keyboard import KMKKeyboard
from kmk.keys import KC
from callibration import input_range
keyboard = KMKKeyboard()

def mapping(val, input_range):
    input_max, input_min = input_range
    output_min = 0
    output_max = 3.5

    if input_max - input_min == 0:
        return output_min

    mapped_val = (val - input_min) / (input_max - input_min) * (output_max - output_min) + output_min

    return max(min(mapped_val, output_max), output_min)

class AnalogScanner(Scanner):

    def __init__(self, read_pin, ctrl_pins, mux_in_pins, keys_num, actuation): #input is relative to MCU, so pin 27

        self.read_pin = [analogio.AnalogIn(read_pin)] #list of input pins
        self.ctrl_pins = [digitalio.DigitalInOut(pin) for pin in ctrl_pins]
        for pin in self.ctrl_pins:
            pin.direction = digitalio.Direction.OUTPUT

        self.mux_in_pins = mux_in_pins # 32
        self.a_val = [3.5]*self.mux_in_pins
        self.a_val_old = [3.5]*self.mux_in_pins
        self.que = []
        self.pressed = [False]*self.mux_in_pins
        self.keys_num = keys_num
        self.actuation = actuation

    @property
    def key_count(self):
        return self.keys_num

    def scan_for_changes(self):
        if len(self.que) == 0:  # if no key event is waiting to be read
            for i in range(self.mux_in_pins):
                # Set control pins for the current multiplexer channel
                for pin_index, bit_mask in enumerate([0b00001, 0b00010, 0b00100, 0b01000, 0b10000]):
                    self.ctrl_pins[pin_index].value = (i & bit_mask) != 0

                # Read the value from the single analog input pin
                self.a_val[i] = self.read_pin[0].value

            for i in range(self.keys_num):
                self.a_val[i] = mapping(self.a_val[i], input_range[i + self.offset])  #input_range[i + self.offset]

            for i in range(self.keys_num):

                if self.actuation[keyboard.active_layers[0]][i + self.offset] > 0:
                    if self.a_val[i] < self.actuation[keyboard.active_layers[0]][i + self.offset] and self.pressed[i] == False:
                        self.pressed[i] = True
                        self.que.append(i)
                    elif self.a_val[i] > self.actuation[keyboard.active_layers[0]][i + self.offset] and self.pressed[i] == True:
                        self.pressed[i] = False
                        self.que.append(i)
#RAPID TRIGGER HERE
#        elif self.actuation[keyboard.active_layers[0]][i + self.offset] < 0:
#            if self.a_val[i] < self.a_val_old[i] - abs(self.actuation[keyboard.active_layers[0]][i + self.offset]):
#                self.a_val_old[i] = self.a_val[i]
#                if not self.pressed[i]:
#                    self.pressed[i] = True
#                    self.que.append(i)
#            elif self.a_val[i] > self.a_val_old[i] + abs(self.actuation[keyboard.active_layers[0]][i + self.offset]):
#                self.a_val_old[i] = self.a_val[i]
#                if self.pressed[i]:
#                    self.pressed[i] = False
#                    self.que.append(i)
#                elif self.pressed[i] and self.a_val[i]>3.4: #edge case if key gets stuck
#                    self.a_val_old[i] = self.a_val[i]
#                    self.pressed[i] = False
#                    self.que.append(i)
################
        elif len(self.que) > 0:
            temp = self.que.pop(0)
            return keypad.Event(temp + self.offset, self.pressed[temp])
