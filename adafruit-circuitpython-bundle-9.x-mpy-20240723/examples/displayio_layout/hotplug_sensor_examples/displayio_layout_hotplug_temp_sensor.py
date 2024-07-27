# SPDX-FileCopyrightText: 2022 PaulskPt
#
# SPDX-License-Identifier: MIT
"""
Notes by @PaulskPt
Script tested on an Adafruit PyPortal Titano
(Product ID 4444. See: https://www.adafruit.com/product/4444)
This script can make use of an I2C Realtime Clock type DS3231
However, when the flag 'use_ntp' is set, the DS3231 will not be used
instead the NTP class from adafruit_ntp.py will be used.
"""
import time
import board
import busio
import displayio
import terminalio
import adafruit_tmp117
from adafruit_ds3231 import DS3231
from digitalio import DigitalInOut
import neopixel
import adafruit_touchscreen
from adafruit_esp32spi import adafruit_esp32spi
from adafruit_ntp import NTP
from adafruit_pyportal import PyPortal
from adafruit_display_text.bitmap_label import Label
from adafruit_display_shapes.rect import Rect
from adafruit_display_shapes.circle import Circle
from adafruit_display_shapes.triangle import Triangle
from adafruit_bitmap_font import bitmap_font
from adafruit_displayio_layout.layouts.tab_layout import TabLayout


# +-------------------------------------------------------+
# | Definition for variables in the past defined as global|
# +-------------------------------------------------------+
# The gVars class is created
# to elminate the need for global variables.


class gVars:
    def __init__(self):
        self.gVarsDict = {
            0: "my_debug",
            1: "rtc",
            2: "temp_sensor",
            3: "lStart",
            4: "o_secs",
            5: "c_secs",
            6: "dt_refresh",
            7: "sDT_old",
            8: "t0",
            9: "t1",
            10: "t2",
            11: "default_dt",
            12: "pge3_lbl_dflt",
            13: "pge4_lbl_dflt",
            14: "online_time_present",
            15: "temp_in_REPL",
            16: "old_temp",
            17: "use_ntp",
            18: "use_txt_in_month",
            19: "use_usa_notation",
            20: "content_sensor_idx",
            21: "ntp_refresh",
            22: "nHH_old",
            23: "next_NTP_sync",
            24: "s_cnt",
            25: "five_min_cnt",
            26: "next_NTP_sync_t1",
            27: "next_NTP_sync_t3",
            28: "temp_in_fahrenheit",
        }

        self.gVars_rDict = {
            "my_debug": 0,
            "rtc": 1,
            "temp_sensor": 2,
            "lStart": 3,
            "o_secs": 4,
            "c_secs": 5,
            "dt_refresh": 6,
            "sDT_old": 7,
            "t0": 8,
            "t1": 9,
            "t2": 10,
            "default_dt": 11,
            "pge3_lbl_dflt": 12,
            "pge4_lbl_dflt": 13,
            "online_time_present": 14,
            "temp_in_REPL": 15,
            "old_temp": 16,
            "use_ntp": 17,
            "use_txt_in_month": 18,
            "use_usa_notation": 19,
            "content_sensor_idx": 20,
            "ntp_refresh": 21,
            "nHH_old": 22,
            "next_NTP_sync": 23,
            "s_cnt": 24,
            "five_min_cnt": 25,
            "next_NTP_sync_t1": 26,
            "next_NTP_sync_t3": 27,
            "temp_in_fahrenheit": 28,
        }

        self.g_vars = {}

        # self.clean()

    def write(self, s, value):
        if isinstance(s, str):
            if s in self.gVars_rDict:
                n = self.gVars_rDict[s]
                # print("myVars.write() \'{:" ">20s}\'found in self.gVars_rDict,
                # key: {}".format(s, n))
                self.g_vars[n] = value
            else:
                raise KeyError(
                    "variable '{:" ">20s}' not found in self.gVars_rDict".format(s)
                )
        else:
            raise TypeError(
                "myVars.write(): param s expected str, {} received".format(type(s))
            )

    def read(self, s):
        RetVal = None
        if isinstance(s, str):
            if s in self.gVars_rDict:
                n = self.gVars_rDict[s]
                if n in self.g_vars:
                    RetVal = self.g_vars[n]
        return RetVal

    def clean(self):
        self.g_vars = {
            0: None,
            1: None,
            2: None,
            3: None,
            4: None,
            5: None,
            6: None,
            7: None,
            8: None,
            9: None,
            10: None,
            11: None,
            12: None,
            13: None,
            14: None,
            15: None,
            16: None,
            17: None,
            18: None,
            19: None,
            20: None,
            21: None,
            22: None,
            23: None,
            24: None,
            25: None,
            26: None,
            27: None,
            28: None,
        }

    def list(self):
        for i in range(0, len(self.g_vars) - 1):
            print(
                "self.g_vars['{:"
                ">20s}'] = {}".format(
                    self.gVarsDict[i], self.g_vars[i] if i in self.g_vars else "None"
                )
            )


# ---------- End of class gVars ------------------------

myVars = gVars()  # create an instance of the gVars class

myVars.write("my_debug", False)

# Adjust here the date and time that you want the RTC to be set at start:
myVars.write("default_dt", time.struct_time((2022, 5, 14, 11, 42, 0, 5, -1, -1)))

# start_time = time.monotonic()

# -------------- Setting myVars elements ----------------------------------
myVars.write("rtc", None)
myVars.write("temp_sensor", None)
myVars.write("lStart", True)
myVars.write("o_secs", 0)  # old seconds
myVars.write("c_secs", 0)  # current seconds
# dt_refresh is used to flag when more or less static elements
# in datetime stamp have to be refreshed
myVars.write("dt_refresh", True)
myVars.write("sDT_old", "")
myVars.write("t0", None)
myVars.write("t1", None)
myVars.write("t2", None)
# default_dt already set above
myVars.write("pge3_lbl_dflt", "The third page is fun!")
myVars.write("pge4_lbl_dflt", "The fourth page is where it's at")
myVars.write("online_time_present", False)
myVars.write("temp_in_REPL", False)
myVars.write("old_temp", 0.00)
myVars.write("use_txt_in_month", True)
myVars.write("use_usa_notation", True)
myVars.write("use_ntp", True)
myVars.write("content_sensor_idx", None)
myVars.write("ntp_refresh", True)
myVars.write("next_NTP_sync", 0)
myVars.write("s_cnt", 0)
myVars.write("five_min_cnt", 0)
myVars.write("next_NTP_sync_t1", "Next NTP sync in ")
myVars.write("next_NTP_sync_t3", " (mm:ss)")
myVars.write("temp_in_fahrenheit", True)
# nHH_old is used to check if the hour has changed.
# If so we have to re-sync from NTP server
# (if not using an external RTC)
myVars.write("nHH_old", -1)

if myVars.read("my_debug"):
    # print list of all variables in myVars
    myVars.list()
# -------------------------------------------------------------------------
# degs_sign = chr(186)  # I preferred the real degrees sign which is: chr(176)

# If you are using a board with pre-defined ESP32 Pins:
esp32_cs = DigitalInOut(board.ESP_CS)
esp32_ready = DigitalInOut(board.ESP_BUSY)
esp32_reset = DigitalInOut(board.ESP_RESET)

spi = busio.SPI(board.SCK, board.MOSI, board.MISO)
esp = adafruit_esp32spi.ESP_SPIcontrol(spi, esp32_cs, esp32_ready, esp32_reset)

# ------------- Screen Setup ------------- #
pyportal = None
timeout_cnt = 0
while pyportal is None:
    try:
        pyportal = PyPortal(
            esp=esp, external_spi=spi, debug=True
        )  # esp=esp, external_spi=spi) # create a PyPortal object
        if pyportal is not None:
            break
    except ValueError:  # Occurred the error: "SCK in use".
        #                 Also occurred the error "SPEAKER_ENABLE in use"
        time.sleep(0.5)
        timeout_cnt += 1
        if timeout_cnt > 10:
            print("Timeout occurred while trying to create a PyPortal object")
            raise

months = {
    0: "Dum",
    1: "Jan",
    2: "Feb",
    3: "Mar",
    4: "Apr",
    5: "May",
    6: "Jun",
    7: "Jul",
    8: "Aug",
    9: "Sep",
    10: "Oct",
    11: "Nov",
    12: "Dec",
}

i2c = board.I2C()

if myVars.read("use_ntp"):
    print(
        "\ntest_page_layout.showing_page_index test with I2C Temperature sensor and NTP \
synchronized local time"
    )
else:
    print("\nTabLayout test with I2C Temperature sensor and I2C Realtime clock")
print("Add your WiFi SSID, WiFi password and Timezone in file: secrets.h\n")

if myVars.read("my_debug"):
    while not i2c.try_lock():
        pass

    try:
        while True:
            print(
                "I2C addresses found:",
                [hex(device_address) for device_address in i2c.scan()],
            )
            time.sleep(2)
            break

    finally:  # unlock the i2c bus when ctrl-c'ing out of the loop
        i2c.unlock()

# -------- Setting up SDCard ---------------------
# Is not needed to be done here: the SPI module is taking care of initializing the SD Card.
# See: https://andyfelong.com/2019/07/pyportal-access-the-micro-sd-card/#:~:text= \
# It%20also%20has%20support%20for%20a%20micro%2DSD%20Card.&text=Software%20support%20 \
# for%20PyPortal%20is, \
# %2Din%20serial%2Dport%20terminal.77
#
# NOTE: there is also the board.SD_CARD_DETECT pin (33)(but I don't know yet how to interface it)
####

# you'll need to pass in an io username and key
# Get wifi details and more from a secrets.py file
try:
    from secrets import secrets
except ImportError:
    print("WiFi secrets are kept in secrets.py, please add them there!")
    raise

if myVars.read("my_debug"):
    if esp.status == adafruit_esp32spi.WL_IDLE_STATUS:
        print("ESP32 found and in idle mode")
    print("Firmware vers.", esp.firmware_version)
    print("MAC addr:", [hex(i) for i in esp.MAC_address])

    for ap in esp.scan_networks():
        print("\t%s\t\tRSSI: %d" % (str(ap["ssid"], "utf-8"), ap["rssi"]))

# Get our username, key and desired timezone
location = secrets.get("timezone", None)

print("\nConnecting to AP...")
while not esp.is_connected:
    try:
        esp.connect_AP(secrets["ssid"], secrets["password"])
    except RuntimeError as e:
        print("could not connect to AP, retrying: ", e)
        continue
print("Connected to", str(esp.ssid, "utf-8"), "\tRSSI:", esp.rssi)
print("Please wait...")
if myVars.read("my_debug"):
    print("My IP address is", esp.pretty_ip(esp.ip_address))
    print(
        "IP lookup adafruit.com: %s"
        % esp.pretty_ip(esp.get_host_by_name("adafruit.com"))
    )
    print("Ping google.com: %d ms" % esp.ping("google.com"))


def refresh_from_NTP():
    # Fetch and set the microcontroller's current UTC time
    # keep retrying until a valid time is returned
    timeout_cnt2 = 0
    while not ntp.valid_time:
        ntp.set_time(tz_offset)
        if myVars.read("my_debug"):
            print("Failed to obtain time, retrying in 5 seconds...")
        timeout_cnt2 += 1
        time.sleep(5)
        if timeout_cnt2 > 10:
            print("Timeout while trying to get ntp datetime to set the internal rtc")
            break

    if myVars.read("my_debug"):
        print("Value ntp.valid_time = ", ntp.valid_time)

    if ntp.valid_time:
        myVars.write("online_time_present", True)
        myVars.write("ntp_refresh", False)
        # Get the current time in seconds since Jan 1, 1970 and correct it for local timezone
        # (defined in secrets.h)
        ntp_current_time = time.time()
        if myVars.read("my_debug"):
            print("Seconds since Jan 1, 1970: {} seconds".format(ntp_current_time))

        # Convert the current time in seconds since Jan 1, 1970 to a struct_time
        myVars.write("default_dt", time.localtime(ntp_current_time))
        if not myVars.read("my_debug"):
            print(
                "Internal clock synchronized from NTP pool, now =",
                myVars.read("default_dt"),
            )


if myVars.read("use_ntp"):
    # Initialize the NTP object
    ntp = NTP(esp)

    location = secrets.get("timezone", location)
    if myVars.read("my_debug"):
        print("location (from secrets.h) = ", location)
    if location == "Europe/Lisbon":
        if myVars.read("my_debug"):
            print("Using timezone Europe/Lisbon")
        tz_offset = 3600
    else:
        tz_offset = 0

    refresh_from_NTP()

pixel = neopixel.NeoPixel(board.NEOPIXEL, 1, brightness=1)
WHITE = 0xFFFFFF
RED = 0xFF0000
YELLOW = 0xFFFF00
GREEN = 0x00FF00
BLUE = 0x0000FF
PURPLE = 0xFF00FF
BLACK = 0x000000

# ---------- Sound Effects ------------- #
soundDemo = "/sounds/sound.wav"
soundBeep = "/sounds/beep.wav"
soundTab = "/sounds/tab.wav"

# ------------ Touchscreen setup --------------- #
# See: https://learn.adafruit.com/making-a-pyportal-user-interface-displayio/display
display = board.DISPLAY  # create the display object
display.rotation = 0
# screen_width = 320
# screen_height = 240
screen_width = display.width
screen_height = display.height
# -------Rotate 0:
# Note @PaulskPt dd 2022-05-13
# After using a touchscreen calibration script, the values are as follows:
# (XL, YU, XR, YD) are: (6935, 10496, 60127, 57631)
ts = adafruit_touchscreen.Touchscreen(
    board.TOUCH_XL,
    board.TOUCH_XR,
    board.TOUCH_YD,
    board.TOUCH_YU,  # #calibration=((5200, 59000), (5800, 57000)),
    calibration=((6815, 60095), (10520, 58007)),
    size=(screen_width, screen_height),
)  # was: screen_width, screen_height
"""
# If Rotate is 90:
# -------Rotate 90:
ts = adafruit_touchscreen.Touchscreen(board.TOUCH_YU, board.TOUCH_YD,
                                      board.TOUCH_XL, board.TOUCH_XR,
                                      calibration=((5200, 59000), (5800, 57000)),
                                      size=(screen_height, screen_width))
# If Rotate 180:
ts = adafruit_touchscreen.Touchscreen(board.TOUCH_XR, board.TOUCH_XL,
                                      board.TOUCH_YU, board.TOUCH_YD,
                                      calibration=((5200, 59000), (5800, 57000)),
                                      size=(screen_width, screen_height))

# If Rotate 270:
ts = adafruit_touchscreen.Touchscreen(board.TOUCH_XL, board.TOUCH_XR,
                                      board.TOUCH_YD, board.TOUCH_YU,
                                      calibration=((5200, 59000), (5800, 57000)),
                                      size=(screen_height, screen_width))
"""
# -----------------------------------

# create and show main_group
main_group = displayio.Group()  # The Main Display Group

display.root_group = main_group

# font = bitmap_font.load_font("fonts/Helvetica-Bold-16.bdf")
font_arial = bitmap_font.load_font("/fonts/Arial-16.bdf")
font_term = terminalio.FONT

# create the page layout
test_page_layout = TabLayout(
    x=0,
    y=0,
    display=board.DISPLAY,
    tab_text_scale=2,
    custom_font=font_term,
    inactive_tab_spritesheet="lib/adafruit_displayio_layout/examples/bmps/inactive_tab_sprite.bmp",
    showing_tab_spritesheet="lib/adafruit_displayio_layout/examples/bmps/active_tab_sprite.bmp",
    showing_tab_text_color=0x00AA59,
    inactive_tab_text_color=0xEEEEEE,
    inactive_tab_transparent_indexes=(0, 1),
    showing_tab_transparent_indexes=(0, 1),
    tab_count=4,
)
# make 4 pages of content
pge1_group = displayio.Group()
pge2_group = displayio.Group()
pge3_group = displayio.Group()
pge4_group = displayio.Group()
# make 1 background group
bg_group = displayio.Group()

"""
   From: https://learn.adafruit.com/making-a-pyportal-user-interface-displayio/the-full-code
"""


# This will handle switching Images and Icons
def set_image(group, filename):
    """Set the image file for a given goup for display.
    This is most useful for Icons or image slideshows.
        :param group: The chosen group
        :param filename: The filename of the chosen image
    """
    print("Set image to ", filename)
    image = None
    image_sprite = None
    if group:
        group.pop()
    if not filename:
        return  # we're done, no icon desired
    # CircuitPython 6 & 7 compatible
    try:
        image = displayio.OnDiskBitmap(filename)
    except OSError as exc:
        if exc.args[0] == 2:  # No such file/directory
            return
    if image is not None:
        image_sprite = displayio.TileGrid(
            image,
            pixel_shader=getattr(image, "pixel_shader", displayio.ColorConverter()),
        )
        if image_sprite is not None:
            main_group.append(image_sprite)


# ------------- Setup for Images ------------- #

bg_group = displayio.Group()
set_image(bg_group, "/images/BGimage4.bmp")
print(
    "Please wait...building-up things..."
)  # 2022-05-08 13h19 (utc+1) It takes 24 seconds from here to start of main() loop
main_group.append(bg_group)

icon_group = displayio.Group()
icon_group.x = 180
icon_group.y = 120
icon_group.scale = 1
pge2_group.append(icon_group)

# labels
pge1_lbl = Label(
    font=font_term,
    scale=2,
    text="This is the first page!",
    anchor_point=(0, 0),
    anchored_position=(10, 10),
)
pge1_lbl2 = Label(
    font=font_term,
    scale=2,
    text="Please wait...",
    anchor_point=(0, 0),
    anchored_position=(10, 150),
)
pge2_lbl = Label(
    font=font_term,
    scale=2,
    text="This page is the second page!",
    anchor_point=(0, 0),
    anchored_position=(10, 10),
)
pge3_lbl = Label(
    font=font_term,
    scale=2,
    text=myVars.read("pge3_lbl_dflt"),  # Will be "Date/time:"
    anchor_point=(0, 0),
    anchored_position=(10, 10),
)
pge3_lbl2 = Label(
    font=font_term,
    scale=2,
    text="",  # pge3_lbl2_dflt,   # Will be DD-MO-YYYY or Month-DD-YYYY
    anchor_point=(0, 0),
    anchored_position=(10, 40),
)
pge3_lbl3 = Label(
    font=font_term,
    scale=2,
    text="",  # pge3_lbl3_dflt,  # Will be HH:MM:SS
    anchor_point=(0, 0),
    anchored_position=(10, 70),
)
pge3_lbl4 = Label(
    font=font_term,
    scale=2,
    text="",  # pge3_lbl3_dflt,  # Will be time until next NTP sync in MM:SS
    anchor_point=(0, 0),
    anchored_position=(10, 200),
)
pge4_lbl = Label(
    font=font_term,
    scale=2,
    text=myVars.read("pge4_lbl_dflt"),
    anchor_point=(0, 0),
    anchored_position=(10, 10),
)
pge4_lbl2 = Label(
    font=font_term,
    scale=2,
    text="",  # Will be "Temperature"
    anchor_point=(0, 0),
    anchored_position=(10, 130),
)
pge4_lbl3 = Label(
    font=font_arial,  # bitmap_font.load_font("/fonts/Arial-16.bdf"),
    scale=2,
    text="",  # Will be  "xx.yy ºC"
    anchor_point=(0, 0),
    anchored_position=(10, 160),
)

# shapes
square = Rect(x=20, y=70, width=40, height=40, fill=0x00DD00)
circle = Circle(50, 100, r=30, fill=0xDD00DD)
triangle = Triangle(50, 0, 100, 50, 0, 50, fill=0xDDDD00)
rectangle = Rect(x=80, y=60, width=100, height=50, fill=0x0000DD)

triangle.x = 80
triangle.y = 70

# add everything to their page groups
pge1_group.append(square)
pge1_group.append(pge1_lbl)
pge1_group.append(pge1_lbl2)
pge2_group.append(pge2_lbl)
pge2_group.append(circle)
pge3_group.append(pge3_lbl)
pge3_group.append(pge3_lbl2)
pge3_group.append(pge3_lbl3)
pge3_group.append(pge3_lbl4)
pge3_group.append(triangle)
pge4_group.append(pge4_lbl)
pge4_group.append(pge4_lbl2)
pge4_group.append(pge4_lbl3)
pge4_group.append(rectangle)

if board.board_id == "pyportal_titano":
    pages = {0: "Dum", 1: "One", 2: "Two", 3: "Three", 4: "Four"}
else:
    pages = {0: "Dum", 1: "One", 2: "Two", 3: "Thr", 4: "For"}

# add the pages to the layout, supply your own page names
test_page_layout.add_content(pge1_group, pages[1])
test_page_layout.add_content(pge2_group, pages[2])
test_page_layout.add_content(pge3_group, pages[3])
test_page_layout.add_content(pge4_group, pages[4])
# test_page_layout.add_content(displayio.Group(), "page_5")
# add it to the group that is showing on the display
main_group.append(test_page_layout)
# test_page_layout.tab_tilegrids_group[3].x += 50
# ---------- Text Boxes ------------- #
# Set the font and preload letters
# font = bitmap_font.load_font("/fonts/Arial-16.bdf")  # was: Helvetica-Bold-16.bdf")
# font.load_glyphs(b"abcdefghjiklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ1234567890- ()")
glyphs = b' "(),-.0123456789:ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz'
font_arial.load_glyphs(glyphs)
font_arial.load_glyphs(("°",))  # a non-ascii character we need
# font=font_term.collect()  # ADDED by @PaulskPt --
# to prevent MemoryError - memory allocation failed,
#               allocating 6444 bytes

pge2_group = 1


"""If the temperature sensor has been disconnected,
  this function will try to reconnect (test if the sensor is present by now)
  If reconnected this function creates the temp_sensor object"""


def connect_temp_sensor():
    t = "temperature sensor found"

    # myVars.write("temp_sensor",None)

    try:
        myVars.write("temp_sensor", adafruit_tmp117.TMP117(i2c))
    except ValueError:  # ValueError occurs if the temperature sensor is not connected
        pass

    print(
        "connect_temp_sensor(): type(temp_sensor) object = ",
        type(myVars.read("temp_sensor")),
    )
    if myVars.read("temp_sensor") is not None:
        print(t)
        print("temperature sensor connected")
        myVars.write("t0", "Temperature")
        if myVars.read("temp_in_fahrenheit"):
            myVars.write("t1", chr(186) + "F")
        else:
            myVars.write("t1", chr(186) + "C")
        myVars.write("t2", 27 * "_")
    else:
        print("no " + t)
        print("failed to connect temperature sensor")
        myVars.write("t0", None)
        myVars.write("t1", None)
        myVars.write("t2", None)


"""  If the external rtc has been disconnected,
  this function will try to reconnect (test if the external rtc is present by now)"""


def connect_rtc():
    t = "RTC found"

    # myVars.write("rtc",None)

    try:
        myVars.write("rtc", DS3231(i2c))  # i2c addres 0x68
        # myVars.write("rtc",rtc)
    except ValueError:
        pass

    print("connect_rtc() type rtc object = ", type(myVars.read("rtc")))
    if myVars.read("rtc") is not None:
        print(t)
        print("RTC connected")
        if myVars.read("lStart"):
            myVars.write("lStart", False)
            myVars.read("rtc").datetime = myVars.read("default_dt")
    else:
        print("no " + t)
        print("Failed to connect RTC")


"""Function gets a value from the external temperature sensor
   It only updates if the value has changed compared to the previous value
   A fixed text is set in pge4_lbl2.text. The variable temperature value is set in pge4_lbl3.text
   If no value obtained (for instance if the sensor is disconnected),
   the function sets the pge4_lbl to a default text and makes empty
   pge4_lbl2.text and pge4_lbl3.text"""


def get_temp():
    my_debug = myVars.read("my_debug")
    showing_page_idx = test_page_layout.showing_page_index
    RetVal = False
    if myVars.read("temp_sensor") is not None:
        try:
            temp = myVars.read("temp_sensor").temperature
            if myVars.read("temp_in_fahrenheit"):
                temp = (temp * 1.8) + 32
            t = "{:5.2f}{} ".format(temp, myVars.read("t1"))
            if my_debug and temp is not None and not myVars.read("temp_in_REPL"):
                myVars.write("temp_in_REPL", True)
                print("get_temp(): {} {}".format(myVars.read("t0"), t))
            if showing_page_idx == 3:  # show temperature on most right Tab page
                if temp is not None:
                    if temp != myVars.read(
                        "old_temp"
                    ):  # Only update if there is a change in temperature
                        myVars.write("old_temp", temp)
                        t = "{:5.2f}{} ".format(temp, myVars.read("t1"))
                        pge4_lbl.text = ""
                        pge4_lbl2.text = myVars.read("t0")
                        pge4_lbl3.text = t
                        # if not my_debug:
                        # print("pge4_lbl.tex.gvars {}".format(pge4_lbl.text))
                        # time.sleep(2)
                        RetVal = True
                else:
                    t = ""
                    pge4_lbl.text = myVars.read("pge4_lbl_dflt")
        except OSError:
            print("Temperature sensor has disconnected")
            t = ""
            myVars.write("temp_sensor", None)
            pge4_lbl.text = myVars.read(
                "pge4_lbl_dflt"
            )  # clean the line  (eventually: t2)
            pge4_lbl2.text = "Sensor disconnected."
            pge4_lbl3.text = "Check wiring."
    return RetVal


# Moved these six definitions outside handle_dt()
# to correct pylint error 'too many variables'
dt_ridxs = {"yy": 0, "mo": 1, "dd": 2, "hh": 3, "mm": 4, "ss": 5}

# print("dict dt_ridxs =", dt_ridxs.keys())


""" Function called by get_dt()
    Created to repair pylint error R0912: Too many branches (13/12)"""


def handle_dt(dt):
    my_debug = myVars.read("my_debug")
    RetVal = False
    s = "Date/time: "
    sYY = str(dt[dt_ridxs["yy"]])  # was: str(dt[yy])
    # print("dt_ridxs["mo"] = ", dt_ridxs["mo"])
    # modified mo because plynt error R0914 'Too many local variables'
    # mo = dt_ridxs["mo"]
    dd = dt_ridxs["dd"]
    hh = dt_ridxs["hh"]
    mm = dt_ridxs["mm"]
    ss = dt_ridxs["ss"]
    if "mo" in dt_ridxs:
        sMO = (
            months[dt[dt_ridxs["mo"]]]  # was: months[dt[mo]]
            if myVars.read("use_txt_in_month")
            else "0" + str(dt[dt_ridxs["mo"]])
            if dt[dt_ridxs["mo"]] < 10
            else str(dt[dt_ridxs["mo"]])
        )
    else:
        raise KeyError("key {} not in dt_ridxs dict".format("mo"))

    dt_dict = {}

    for _ in range(dd, ss + 1):
        dt_dict[_] = "0" + str(dt[_]) if dt[_] < 10 else str(dt[_])

    if my_debug:
        print("dt_dict = ", dt_dict)

    myVars.write("c_secs", dt_dict[ss])
    sDT = (
        sMO + "-" + dt_dict[dd] + "-" + sYY
        if myVars.read("use_usa_notation")
        else sYY + "-" + sMO + "-" + dt_dict[dd]
    )
    if my_debug:
        print("handle_dt(): sDT_old = {}, sDT = {}".format(myVars.read("sDT_old"), sDT))
    if myVars.read("sDT_old") != sDT:
        myVars.write("sDT_old", sDT)
        myVars.write("dt_refresh", True)  # The date has changed, set the refresh flag
    sDT2 = dt_dict[hh] + ":" + dt_dict[mm] + ":" + dt_dict[ss]

    if myVars.read("dt_refresh"):  # only refresh when needed
        myVars.write("dt_refresh", False)
        pge3_lbl.text = s
        pge3_lbl2.text = sDT

    if myVars.read("c_secs") != myVars.read("o_secs"):
        myVars.write("o_secs", myVars.read("c_secs"))
        sDT3 = s + "{} {}".format(sDT, sDT2)
        print(sDT3)

        pge3_lbl3.text = sDT2
        if my_debug:
            print("pge3_lbl.text = {}".format(pge3_lbl.text))
            print("pge3_lbl2.text = {}".format(pge3_lbl2.text))
            print("pge3_lbl3.text = {}".format(pge3_lbl3.text))
        RetVal = True

    # Return from here with a False but don't set the pge3_lbl to default.
    # It is only to say to the loop() that we did't update the datetime
    return RetVal


"""Function gets the date and time:
   a) if an rtc is present from the rtc;
   b) if using online NTP pool server then get the date and time from the function time.localtime
   This time.localtime has before been set with data from the NTP server.
   In both cases the date and time will be set to the pge3_lbl, pge3_lbl12 and pge3_lbl3
   If no (valid) date and time received then a default text will be shown on the pge3_lbl"""


def get_dt():
    dt = None
    RetVal = False

    if myVars.read("rtc") is not None:
        try:
            dt = myVars.read("rtc").datetime
        except OSError as exc:
            if myVars.read("my_debug"):
                print("Error number: ", exc.args[0])
            if exc.args[0] == 5:  # Input/output error
                print("get_dt(): OSError occurred. RTC probably is disconnected")
                pge3_lbl.text = myVars.read("pge3_lbl_dflt")
                myVars.write("sDT_old", "")
                pge3_lbl2.text = ""
                pge3_lbl3.text = ""
                return RetVal
            raise  # Handle other errors

    elif myVars.read("online_time_present") or myVars.read("use_ntp"):
        dt = time.localtime()

    if myVars.read("my_debug"):
        print("get_dt(): dt = ", dt)
    if dt is not None:
        RetVal = handle_dt(dt)
    else:
        pge3_lbl.text = myVars.read("pge3_lbl_dflt")
        pge3_lbl2.text = ""
        pge3_lbl3.text = ""
    return RetVal


"""  hms_to_cnt()
    function returns a integer value representing
    the conversion from the current hours, minutes and seconds
    into seconds"""


def hms_to_cnt():
    dt = time.localtime()  # get the local time as a time_struct
    return (dt.tm_hour * 3600) + (dt.tm_min * 60) + dt.tm_sec


""" Created this function to correct pylint errors:
    'Too many branches' R0912 and
    'Too many statements' R0915"""


def ck_next_NTP_sync():
    s_cnt = myVars.read("s_cnt")
    c_cnt = hms_to_cnt()  # set current count (seconds)
    c_elapsed = c_cnt - s_cnt
    if c_elapsed < 10:  # continue only when c_elapsed >= 10
        return
    TAG = "ck_next_NTP_sync(): "
    my_debug = myVars.read("my_debug")
    t1 = myVars.read("next_NTP_sync_t1")
    t3 = myVars.read("next_NTP_sync_t3")
    five_min = myVars.read("five_min_cnt")
    myVars.write("s_cnt", hms_to_cnt())
    # --- five minutes count down calculations #1 ---
    if my_debug:
        print(
            TAG + "five_min = {}, s_cnt = {}, c_cnt = {}".format(five_min, s_cnt, c_cnt)
        )
        print(TAG + "c_elapsed = ", c_elapsed)

    # --- five minutes count down calculations #2 ---
    myVars.write("s_cnt", c_cnt)  # remember c_cnt
    five_min -= 10
    myVars.write("five_min_cnt", five_min)  # remember count
    mm2 = five_min // 60
    ss2 = five_min - (mm2 * 60)
    t2 = "{:02d}:{:02d}".format(mm2, ss2)
    t0 = t1 + t2 + t3
    print(t0)
    pge3_lbl4.text = t0
    if five_min == 0:  # five minutes passed
        pge3_lbl4.text = ""
        myVars.write("five_min_cnt", 300)  # reset count
        myVars.write("ntp_refresh", True)


def inc_cnt(cnt):
    cnt += 1
    if cnt > 999:
        cnt = 0
    return cnt


def main():
    cnt = 1
    wipe_pge1_lbl2_text = False
    print("Starting loop")
    pge1_lbl2.text = "Ready..."
    myVars.write("five_min_cnt", 300)  # 5 minutes
    myVars.write("s_cnt", hms_to_cnt())  # set start count (seconds)
    use_ntp = myVars.read("use_ntp")
    rtc = myVars.read("rtc")
    otp = myVars.read("online_time_present")
    # print("Starting loop")
    while True:
        touch = ts.touch_point
        try:
            if use_ntp:
                ck_next_NTP_sync()
            ntp_refresh = myVars.read("ntp_refresh")
            # ------------- Handle Tab touch  ------------- #
            # print("main() value touch: ", touch)
            if touch:  # Only do this if the screen is touched
                if not wipe_pge1_lbl2_text:
                    pge1_lbl2.text = ""  # Clear the label
                    wipe_pge1_lbl2_text = True
                test_page_layout.handle_touch_events(touch)
            if rtc is not None or otp:
                if otp and ntp_refresh:
                    refresh_from_NTP()  # first re-synchronize internal clock from NTP server
                if get_dt():
                    print("Loop nr: {:03d}".format(cnt))
            else:
                connect_rtc()
            if myVars.read("temp_sensor") is not None:
                get_temp()
            else:
                connect_temp_sensor()
                touch = (
                    ts.touch_point
                )  # Just to try - it looks like after re-connecting the sensor,
                #    the touch data has lost
            if myVars.read("temp_in_REPL"):
                myVars.write("temp_in_REPL", False)
            cnt = inc_cnt(cnt)
        except KeyboardInterrupt as exc:
            print("Keyboard interrupt...exiting...")
            raise KeyboardInterrupt from exc


if __name__ == "__main__":
    main()
