

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
                inPins = self.analogPins,
                outPins = self.outPins,
                multiNum = self.multiplexer,
                numOfKeys = self.numberOfKeys,
                analogAttrib = self.analogKeyAttribut
            ),

            KeysScanner(
                # require argument:
                pins=self.encoderBtnPins,
                # optional arguments with defaults:
                value_when_pressed=False,
                pull=True,
                interval=0.02,  # Debounce time in floating point seconds
                max_events=64
            ),


        ]

        # Split code:
        split = Split(
            split_flip=True,  # If both halves are the same, but flipped, set this True
            split_side=None,  # Sets if this is to SplitSide.LEFT or SplitSide.RIGHT, or use EE hands
            split_type=SplitType.UART,  # Defaults to UART
            uart_interval=1,  # Sets the uarts delay. Lower numbers draw more power
            data_pin=self.rx,  # The primary data pin to talk to the secondary device with
            data_pin2=self.tx,  # Second uart pin to allow 2 way communication
            uart_flip = False,
            use_pio=True,  # Use RP2040 PIO implementation of UART. Required if you want to use other pins than RX/TX
        )
        self.modules.append(split)

        self.setup_rgb()

    analogPins = pins[27]      #analog pins from which values are read

    outPins = (pins[10],pins[9],pins[8],pins[7],pins[6]) #pins to control the multiplexers

    multiplexer = 32 #number of input pins of the multiplexer

    numberOfKeys = 29  #number of analog keys (per side if its split)

    analogKeyAttribut = [ #choose per key modes and values (positive means threshold negativ means rapid trigger
        [
            2,2,2,2,2,2,
            2,2,2,2,2,2,
            2,2,2,2,2,2,
            2,2,2,2,2,2,
              2,2,2,2,2,

            2,2,2,2,2,2,
            2,2,2,2,2,2,
            2,2,2,2,2,2,
            2,2,2,2,2,2,
              2,2,2,2,2,
        ],
        [
            2,2,2,2,2,2,
            2,2,2,2,2,2,
            2,2,2,2,2,2,
            2,2,2,2,2,2,
              2,2,2,2,2,

            2,2,2,2,2,2,
            2,2,2,2,2,2,
            2,2,2,2,2,2,
            2,2,2,2,2,2,
              2,2,2,2,2,
        ],
        [
            2,2,2,2,2,2,
            2,2,2,2,2,2,
            2,2,2,2,2,2,
            2,2,2,2,2,2,
              2,2,2,2,2,

            2,2,2,2,2,2,
            2,2,2,2,2,2,
            2,2,2,2,2,2,
            2,2,2,2,2,2,
              2,2,2,2,2,
        ],
        [
            2,2,2,2,2,2,
            2,2,2,2,2,2,
            2,2,2,2,2,2,
            2,2,2,2,2,2,
              2,2,2,2,2,

            2,2,2,2,2,2,
            2,2,2,2,2,2,
            2,2,2,2,2,2,
            2,2,2,2,2,2,
              2,2,2,2,2,
        ],
    ]



    rx = pins[1]
    tx = pins[0]





   coord_mapping = [
     0,  1,  2,  3,  4,  5,  35, 34, 33, 32, 31, 30,
     6,  7,  8,  9, 10, 11,  41, 40, 39, 38, 37, 36,
    12, 13, 14, 15, 16, 17,  47, 46, 45, 44, 43, 42,
    18, 19, 20, 21, 22, 23,  53, 52, 51, 50, 49, 48,
        25, 26, 27, 28, 29,  59, 58, 57, 56, 55,
    ]
