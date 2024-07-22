
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

while True:
    for channel in range(32):  # Assuming 32 channels for the multiplexer
        set_multiplexer_channel(channel)
        adc_value = read_adc()
        print(f"Channel {channel}: {adc_value}")
        time.sleep(0.1)  # Adjust delay as necessary
