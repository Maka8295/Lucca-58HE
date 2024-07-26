#LEFT HAND

from kmk.quickpin.RP2040.YD_RP2040 import pinout as pins
#from kmk.quickpin.pro_micro.sparkfun_promicro_rp2040 import pinout as pins
from kmk.kmk_keyboard import KMKKeyboard as _KMKKeyboard
from kmk.scanners import DiodeOrientation
from kmk.modules.split import Split, SplitType, SplitSide
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
        # Split code:
        split = Split(
            split_flip=True,  # If both halves are the same, but flipped, set this True
            split_side=SplitSide.LEFT,  # Sets if this is to SplitSide.LEFT or SplitSide.RIGHT, or use EE hands
            split_type=SplitType.UART,  # Defaults to UART
            uart_interval=1,  # Sets the uarts delay. Lower numbers draw more power
            data_pin=self.rx,  # The primary data pin to talk to the secondary device with
            data_pin2=self.tx,  # Second uart pin to allow 2 way communication
            uart_flip = False,
            use_pio=True,  # Use RP2040 PIO implementation of UART. Required if you want to use other pins than RX/TX
        )
        self.modules.append(split)

    tx = pins[12]

    rx = pins[13]

    read_pin = pins[27] #analog value read here

    ctrl_pins = (pins[10],pins[9],pins[8],pins[7],pins[6]) #pins to control the multiplexers

    mux_in_pins = 32 #number of input pins of the multiplexer

    keys_num = 32  #number of analog keys (per side if its split)

    actuation = [ #choose per key modes and values (positive means threshold negativ means rapid trigger
        [
            1,1,1,1,1,1,                     1,1,1,1,1,1,
            1,1,1,1,1,1,                     1,1,1,1,1,1,
            1,1,1,1,1,1,                     1,1,1,1,1,1,
            1,1,1,1,1,1,                     1,1,1,1,1,1,
            1,1,1,1,1,1,1,1,                 1,1,1,1,1,1,1,1,
        ],
        [
            1,1,1,1,1,1,                     1,1,1,1,1,1,
            1,1,1,1,1,1,                     1,1,1,1,1,1,
            1,1,1,1,1,1,                     1,1,1,1,1,1,
            1,1,1,1,1,1,                     1,1,1,1,1,1,
            1,1,1,1,1,1,1,1,                 1,1,1,1,1,1,1,1,
        ],
    ]



    coord_mapping = [
        20,  4,  24,  8,  16,  0,                   48, 49, 50, 51, 52, 53,
        26,  10,  18,  2, 28, 12,                   54, 55, 56, 57, 58, 59,
        15, 31, 30, 14, 22, 6,                      60, 61, 62, 63, 47, 46,
        3, 19, 11, 27, 7, 23,                       39, 45, 44, 43, 42, 41, 40,
        25, 5, 21, 13, 29,         1, 9, 17,        38, 37, 36, 35,                  32, 33, 34,
    ]
