

from kmk.quickpin.RP2040.YD_RP2040 import pinout as pins
#from kmk.quickpin.pro_micro.sparkfun_promicro_rp2040 import pinout as pins
from kmk.kmk_keyboard import KMKKeyboard as _KMKKeyboard
from kmk.scanners import DiodeOrientation

from kmk.scanners.keypad import KeysScanner
from kmk.scanners.analogio import AnalogScanner


class KMKKeyboard(_KMKKeyboard):
    def __init__(
        self
    ):
        # create and register the scanner(s)
        self.matrix = [

            AnalogScanner(
                read_pin = self.read_pin,
                ctrl_pins = self.ctrl_pins,
                mux_in_pins = self.mux_in_pins,
                keys_num = self.keys_num,
                actuation = self.actuation
            ),

        ]




    read_pin = pins[27] #analog value read here

    ctrl_pins = (pins[10],pins[9],pins[8],pins[7],pins[6]) #pins to control the multiplexers

    mux_in_pins = 32 #number of input pins of the multiplexer

    keys_num = 32  #number of analog keys (per side if its split)

    actuation = [ #choose per key modes and values (positive means threshold negativ means rapid trigger
        [
            1,1,1,1,1,1,
            1,1,1,1,1,1,
            1,1,1,1,1,1,
            1,1,1,1,1,1,
            1,1,1,1,1,1,1,1,


        ],
    ]



    coord_mapping = [
        20,  4,  24,  8,  16,  0,
        26,  10,  18,  2, 28, 12,
        15, 31, 30, 14, 22, 6,
        3, 19, 11, 27, 7, 23,
        25, 5, 21, 13, 29,         1, 9, 17,
    ]
