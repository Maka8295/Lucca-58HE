
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

def average_sensor_readings(num_readings=10):
    averages = []
    for channel in range(32):  # Assuming 32 channels for the multiplexer
        total = 0
        for _ in range(num_readings):
            set_multiplexer_channel(channel)
            total += read_adc()
            time.sleep(0.01)  # Adjust delay as necessary for accurate readings
        averages.append(total / num_readings)
    return averages

# Store initial averages
initial_averages = average_sensor_readings()

# Wait for user to press buttons (adjust the sleep time as needed)
print("Press the buttons now...")
time.sleep(10)

# Store new averages after button presses
new_averages = average_sensor_readings()

# Print the initial and new averages
print("Initial Averages:")
for i, avg in enumerate(initial_averages):
    print(f"Channel {i}: {avg}")

print("New Averages:")
for i, avg in enumerate(new_averages):
    print(f"Channel {i}: {avg}")
