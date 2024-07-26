#RIGHT HAND

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
        # Split code:
        split = Split(
            split_flip=True,  # If both halves are the same, but flipped, set this True
            split_side=SplitSide.RIGHT,  # Sets if this is to SplitSide.LEFT or SplitSide.RIGHT, or use EE hands "NONE"
            split_type=SplitType.UART,  # Defaults to UART
            uart_interval=1,  # Sets the uarts delay. Lower numbers draw more power
            data_pin=self.rx,  # The primary data pin to talk to the secondary device with
            data_pin2=self.tx,  # Second uart pin to allow 2 way communication
            uart_flip = False,
            use_pio=True,  # Use RP2040 PIO implementation of UART. Required if you want to use other pins than RX/TX
        )
        self.modules.append(split)

    tx = pins[8]

    rx = pins[9]

    read_pin = pins[27] #analog value read here

    ctrl_pins = (pins[26],pins[15],pins[14],pins[13],pins[12]) #pins to control the multiplexers

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
        [
            1,1,1,1,1,1,
            1,1,1,1,1,1,
            1,1,1,1,1,1,
            1,1,1,1,1,1,
            1,1,1,1,1,1,1,1,
        ],
    ]



    coord_mapping = [
        16,17,18,19,20,21,
        22,23,24,25,26,27,
        28,29,30,31,15,14,
        7,13,12,11,10,9,8,
        6,5,4,3,                  0,1,2,

    ]
