# SPDX-FileCopyrightText: 2022 PaulskPt
#
# SPDX-License-Identifier: MIT
"""
Make a PageLayout and illustrate all of it's features
"""

import time
import displayio
import board
import terminalio
import adafruit_tmp117
from adafruit_ds3231 import DS3231
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
            21: "temp_in_fahrenheit",
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
            "temp_in_fahrenheit": 21,
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
myVars.write("default_dt", time.struct_time((2022, 5, 14, 19, 42, 0, 5, -1, -1)))

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
myVars.write("use_ntp", False)
myVars.write("content_sensor_idx", None)
myVars.write("temp_in_fahrenheit", False)
# -------------------------------------------------------------------------
if myVars.read("my_debug"):
    # print list of all variables in myVars
    myVars.list()

# degs_sign = chr(186)  # I preferred the real degrees sign which is: chr(176)
# -----------------------------------

# built-in display
display = board.DISPLAY
# display.rotation = 90
display.rotation = 0

# create and show main_group
main_group = displayio.Group()
display.root_group = main_group

# fon.gvars bitmap_font.load_font("fonts/Helvetica-Bold-16.bdf")
font_arial = bitmap_font.load_font("/fonts/Arial-16.bdf")
font_term = terminalio.FONT

# create the page layout
test_page_layout = TabLayout(
    x=0,
    y=0,
    display=board.DISPLAY,
    tab_text_scale=2,
    custom_font=font_term,
    inactive_tab_spritesheet="bmps/inactive_tab_sprite.bmp",
    showing_tab_spritesheet="bmps/active_tab_sprite.bmp",
    showing_tab_text_color=0x00AA59,
    inactive_tab_text_color=0xEEEEEE,
    inactive_tab_transparent_indexes=(0, 1),
    showing_tab_transparent_indexes=(0, 1),
    tab_count=4,
)

# make 3 pages of content
pge1_group = displayio.Group()
pge2_group = displayio.Group()
pge3_group = displayio.Group()
pge4_group = displayio.Group()

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
    font=font_arial,
    scale=2,
    text="",  # Will be  "xx.yy C"
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
pge2_group.append(pge2_lbl)
pge2_group.append(circle)
pge3_group.append(pge3_lbl)
pge3_group.append(pge3_lbl2)
pge3_group.append(pge3_lbl3)
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

# change page with function by name
test_page_layout.show_page(page_name=pages[2])
print("showing page index:{}".format(test_page_layout.showing_page_index))
time.sleep(1)

# change page with function by index
test_page_layout.show_page(page_index=0)
print("showing page name: {}".format(test_page_layout.showing_page_name))
time.sleep(1)

# change page by updating the page name property
test_page_layout.showing_page_name = pages[2]
print("showing page index: {}".format(test_page_layout.showing_page_index))
time.sleep(1)

# change page by updating the page index property
test_page_layout.showing_page_index = 1
print("showing page name: {}".format(test_page_layout.showing_page_name))
time.sleep(5)

"""
another_text = Label(terminalio.FONT, text="And another thing!", \
    scale=2, color=0x00ff00, anchor_point=(0, 0), \
    anchored_position=(100, 100))
test_page_layout.showing_page_content.append(another_text)
"""


"""
  If the temperature sensor has been disconnected,
  this function will try to reconnect (test if the sensor is present by now)
  If reconnected this function sets the global variable t_sensor_present
  If failed to reconnect the function clears t_sensor_present
"""


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


"""
  If the external rtc has been disconnected,
  this function will try to reconnect (test if the external rtc is present by now)
"""


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


"""
   Function gets a value from the external temperature sensor
   It only updates if the value has changed compared to the previous value
   A fixed text is set in pge4_lbl2.text. The variable temperature value is set in pge4_lbl3.text
   If no value obtained (for instance if the sensor is disconnected),
   the function sets the pge4_lbl to a default text and makes empty
   pge4_lbl2.text and pge4_lbl3.text
"""


def get_temp():
    showing_page_idx = test_page_layout.showing_page_index
    RetVal = False
    if myVars.read("temp_sensor") is not None:
        try:
            temp = myVars.read("temp_sensor").temperature
            if myVars.read("temp_in_fahrenheit"):
                temp = (temp * 1.8) + 32
            t = "{:5.2f} ".format(temp) + myVars.read("t1")
            if (
                myVars.read("my_debug")
                and temp is not None
                and not myVars.read("temp_in_REPL")
            ):
                myVars.write("temp_in_REPL", True)
                print("get_temp(): {} {}".format(myVars.read("t0"), t))
            if showing_page_idx == 3:  # show temperature on most right Tab page
                if temp is not None:
                    if temp != myVars.read(
                        "old_temp"
                    ):  # Only update if there is a change in temperature
                        myVars.write("old_temp", temp)
                        t = "{:5.2f} ".format(temp) + myVars.read("t1")
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
            pge4_lbl2.text = ""
            pge4_lbl3.text = ""

    return RetVal


"""
    Function called by get_dt()
    Created to repair pylint error R0912: Too many branches (13/12)
"""

yy = 0
mo = 1
dd = 2
hh = 3
mm = 4
ss = 5


def handle_dt(dt):
    RetVal = False
    s = "Date/time: "
    sYY = str(dt[yy])
    sMO = (
        months[dt[mo]]
        if myVars.read("use_txt_in_month")
        else "0" + str(dt[mo])
        if dt[mo] < 10
        else str(dt[mo])
    )

    dt_dict = {}

    for _ in range(dd, ss + 1):
        dt_dict[_] = "0" + str(dt[_]) if dt[_] < 10 else str(dt[_])

    if myVars.read("my_debug"):
        print("dt_dict = ", dt_dict)

    myVars.write("c_secs", dt_dict[ss])
    sDT = (
        sMO + "-" + dt_dict[dd] + "-" + sYY
        if myVars.read("use_usa_notation")
        else sYY + "-" + sMO + "-" + dt_dict[dd]
    )
    if myVars.read("my_debug"):
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
        if myVars.read("my_debug"):
            print("pge3_lbl.text = {}".format(pge3_lbl.text))
            print("pge3_lbl2.text = {}".format(pge3_lbl2.text))
            print("pge3_lbl3.text = {}".format(pge3_lbl3.text))
        RetVal = True

    # Return from here with a False but don't set the pge3_lbl to default.
    # It is only to say to the loop() that we did't update the datetime
    return RetVal


"""
   Function gets the date and time:
   a) if an rtc is present from the rtc;
   b) if using online NTP pool server then get the date and time from the function time.localtime
   This time.localtime has before been set with data from the NTP server.
   In both cases the date and time will be set to the pge3_lbl, pge3_lbl12 and pge3_lbl3
   If no (valid) date and time has been received then a default text will be shown on the pge3_lbl
"""


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


print("starting loop")


def main():
    cnt = 0
    while True:
        try:
            print("Loop nr: {:03d}".format(cnt))
            # print("main(): type(rtc) object = ", type(myVars.read("rtc")))
            if myVars.read("rtc") is not None:
                get_dt()
            else:
                connect_rtc()
            # print("main(): type(temp_sensor) object = ", type(myVars.read("temp_sensor")))
            if myVars.read("temp_sensor") is not None:
                get_temp()
            else:
                connect_temp_sensor()
            cnt += 1
            if cnt > 999:
                cnt = 0
            # change page by next page function. It will loop by default
            time.sleep(2)
            test_page_layout.next_page()
        except KeyboardInterrupt as exc:
            raise KeyboardInterrupt("Keyboard interrupt...exiting...") from exc
            # raise SystemExit


if __name__ == "__main__":
    main()
