
import time
import board
import digitalio
import analogio

# Define the control pins
control_pins = [
    digitalio.DigitalInOut(board.GP6),
    digitalio.DigitalInOut(board.GP7),
    digitalio.DigitalInOut(board.GP8),
    digitalio.DigitalInOut(board.GP9),
    digitalio.DigitalInOut(board.GP10)
]

# Set control pins as outputs
for pin in control_pins:
    pin.direction = digitalio.Direction.OUTPUT

# Define the ADC pin
adc = analogio.AnalogIn(board.GP27)  # ADC1 on GP27

def read_adc():
    return adc.value

def set_multiplexer_channel(channel):
    # Convert the channel number to binary and set the control pins accordingly
    for i in range(5):
        control_pins[i].value = (channel >> i) & 0x01

# Set the multiplexer to channel 3
set_multiplexer_channel(3)

while True:
    adc_value = read_adc()
    print(f"Channel 3: {adc_value}")
    time.sleep(0.1)  #0.001 High refresh rate (1 ms delay)
