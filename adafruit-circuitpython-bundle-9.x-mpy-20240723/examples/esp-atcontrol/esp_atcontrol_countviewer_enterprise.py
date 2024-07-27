# SPDX-FileCopyrightText: 2021 ladyada for Adafruit Industries
# SPDX-License-Identifier: MIT

"""
This example will access an API, grab a number like hackaday skulls, github
stars, price of bitcoin, twitter followers... if you can find something that
spits out JSON data, we can display it!
"""
import gc
import time
import board
import busio
from digitalio import DigitalInOut
from digitalio import Direction
import neopixel
import adafruit_connection_manager
import adafruit_requests
import adafruit_espatcontrol.adafruit_espatcontrol_socket as pool
from adafruit_espatcontrol import adafruit_espatcontrol

try:
    from adafruit_ht16k33 import segments
except ImportError:
    pass


# Get wifi details and more from a secrets.py file
try:
    from secrets import secrets
except ImportError:
    print("WiFi secrets are kept in secrets.py, please add them there!")
    raise

#              CONFIGURATION
PLAY_SOUND_ON_CHANGE = False
NEOPIXELS_ON_CHANGE = True
DISPLAY_ATTACHED = False
TIME_BETWEEN_QUERY = 60  # in seconds

# Some data sources and JSON locations to try out

# Bitcoin value in USD
# DATA_SOURCE = "http://api.coindesk.com/v1/bpi/currentprice.json"
# DATA_LOCATION = ["bpi", "USD", "rate_float"]

# Github stars! You can query 1ce a minute without an API key token
# DATA_SOURCE = "https://api.github.com/repos/adafruit/circuitpython"
# if 'github_token' in secrets:
#    DATA_SOURCE += "?access_token="+secrets['github_token']
# DATA_LOCATION = ["stargazers_count"]

# Youtube stats
# CHANNEL_ID = "UCpOlOeQjj7EsVnDh3zuCgsA" # this isn't a secret but you have to look it up
# DATA_SOURCE = "https://www.googleapis.com/youtube/v3/channels/?part=statistics&id=" \
#              + CHANNEL_ID +"&key="+secrets['youtube_token']
# #try also 'viewCount' or 'videoCount
# DATA_LOCATION = ["items", 0, "statistics", "subscriberCount"]


# # Subreddit subscribers
# DATA_SOURCE = "https://www.reddit.com/r/circuitpython/about.json"
# DATA_LOCATION = ["data", "subscribers"]

# Hackaday Skulls (likes), requires an API key
# DATA_SOURCE = "https://api.hackaday.io/v1/projects/1340?api_key="+secrets['hackaday_token']
# DATA_LOCATION = ["skulls"]

# Twitter followers
DATA_SOURCE = (
    "http://cdn.syndication.twimg.com/widgets/followbutton/info.json?"
    + "screen_names=adafruit"
)
DATA_LOCATION = [0, "followers_count"]

# Debug Level
# Change the Debug Flag if you have issues with AT commands
debugflag = True

if board.board_id == "challenger_rp2040_wifi":
    RX = board.ESP_RX
    TX = board.ESP_TX
    resetpin = DigitalInOut(board.WIFI_RESET)
    rtspin = False
    uart = busio.UART(TX, RX, baudrate=11520, receiver_buffer_size=2048)
    esp_boot = DigitalInOut(board.WIFI_MODE)
    esp_boot.direction = Direction.OUTPUT
    esp_boot.value = True
    status_light = None
    pixel_pin = board.NEOPIXEL
    num_pixels = 1
    pixel_type = "RGBW/GRBW"
else:
    RX = board.TX
    TX = board.RX
    resetpin = DigitalInOut(board.D4)
    rtspin = DigitalInOut(board.D5)
    uart = busio.UART(
        board.TX, board.RX, baudrate=11520, timeout=0.1, receiver_buffer_size=512
    )
    esp_boot = DigitalInOut(board.D9)
    esp_boot.direction = Direction.OUTPUT
    esp_boot.value = True
    status_light = None
    pixel_pin = board.A1
    num_pixels = 16
    pixel_type = "RGB/GRB"

# Create the connection to the co-processor and reset
esp = adafruit_espatcontrol.ESP_ATcontrol(
    uart, 115200, reset_pin=resetpin, rts_pin=rtspin, debug=debugflag
)
esp.soft_reset()
esp.disconnect()

ssl_context = adafruit_connection_manager.create_fake_ssl_context(pool, esp)
requests = adafruit_requests.Session(pool, ssl_context)

# display
if DISPLAY_ATTACHED:
    # Create the I2C interface.
    i2c = busio.I2C(board.SCL, board.SDA)
    # Attach a 7 segment display and display -'s so we know its not live yet
    display = segments.Seg7x4(i2c)
    display.print("----")

# neopixels
if NEOPIXELS_ON_CHANGE:
    pixels = neopixel.NeoPixel(
        pixel_pin, num_pixels, brightness=0.4, pixel_order=(1, 0, 2, 3)
    )
    pixels.fill(20)

# music!
if PLAY_SOUND_ON_CHANGE:
    import audioio

    wave_file = open("coin.wav", "rb")  # pylint: disable=consider-using-with
    wave = audioio.WaveFile(wave_file)

# we'll save the value in question
last_value = value = None
the_time = None
times = 0


def chime_light():
    """Light up LEDs and play a tune"""
    if NEOPIXELS_ON_CHANGE:
        for i in range(0, 100, 10):
            if pixel_type == "RGB/GRB":
                pixels.fill((i, i, i))
            elif pixel_type == "RGBW/GRBW":
                pixels.fill((i, i, i, i))
            pixels.show()
            time.sleep(1)
    if PLAY_SOUND_ON_CHANGE:
        with audioio.AudioOut(board.A0) as audio:
            audio.play(wave)
            while audio.playing:
                pass
    if NEOPIXELS_ON_CHANGE:
        for i in range(100, 0, -10):
            if pixel_type == "RGB/GRB":
                pixels.fill((i, i, i))
            elif pixel_type == "RGBW/GRBW":
                pixels.fill((i, i, i, i))
            pixels.show()
            time.sleep(1)
        pixels.fill(0)


while True:
    try:
        while not esp.is_connected:
            # secrets dictionary must contain 'ssid' and 'password' at a minimum
            esp.connect_enterprise(secrets)

        the_time = esp.sntp_time

        # great, lets get the data
        print("Retrieving data source...", end="")
        r = requests.get(DATA_SOURCE)
        print("Reply is OK!")
    except (ValueError, RuntimeError, adafruit_espatcontrol.OKError) as e:
        print("Failed to get data, retrying\n", e)
        continue
    # print('-'*40,)
    # print("Headers: ", r.headers)
    # print("Text:", r.text)
    # print('-'*40)

    value = r.json()
    for x in DATA_LOCATION:
        value = value[x]
    if not value:
        continue
    print("Times:{0}. The Time:{1}. Value: {2}".format(times, the_time, value))
    if DISPLAY_ATTACHED:
        display.print(int(value))
    else:
        print("INT Value:{0}".format(int(value)))

    if last_value != value:
        chime_light()  # animate the neopixels
        last_value = value
    times += 1

    # normally we wouldn't have to do this, but we get bad fragments
    r = value = None
    gc.collect()
    print("GC MEM:{0}".format(gc.mem_free()))  # pylint: disable=no-member
    print("Sleeping for: {0} Seconds".format(TIME_BETWEEN_QUERY))
    time.sleep(TIME_BETWEEN_QUERY)
