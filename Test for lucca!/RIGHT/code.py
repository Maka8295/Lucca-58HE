
import time
import board
import digitalio
import analogio

# Define the control pins
control_pins = [
    digitalio.DigitalInOut(board.GP12),
    digitalio.DigitalInOut(board.GP13),
    digitalio.DigitalInOut(board.GP14),
    digitalio.DigitalInOut(board.GP15),
    digitalio.DigitalInOut(board.GP26)
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
    adc_values = []  # List to store ADC values for all channels
    for channel in range(32):  # Assuming 32 channels for the multiplexer
        set_multiplexer_channel(channel)
        adc_value = read_adc()
        adc_values.append(f"Channel {channel}: {adc_value}")
    # Print all channels on new lines
    print("\n".join(adc_values))
    print("\n" + "-"*40)  # Separator line for readability
    time.sleep(1)  # Adjust delay as necessary
