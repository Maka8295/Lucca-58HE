# SPDX-FileCopyrightText: 2017 Scott Shawcroft, written for Adafruit Industries
# SPDX-FileCopyrightText: Copyright (c) 2021 Melissa LeBlanc-Williams for Adafruit Industries
#
# SPDX-License-Identifier: Unlicense
import board
from digitalio import DigitalInOut, Direction, Pull
from adafruit_funhouse import FunHouse

funhouse = FunHouse(
    default_bg=0x0F0F00,
    scale=2,
)

funhouse.peripherals.set_dotstars(0x800000, 0x808000, 0x008000, 0x000080, 0x800080)

# sensor setup
sensors = []
for p in (board.A0, board.A1, board.A2):
    sensor = DigitalInOut(p)
    sensor.direction = Direction.INPUT
    sensor.pull = Pull.DOWN
    sensors.append(sensor)


def set_label_color(conditional, index, on_color):
    if conditional:
        funhouse.set_text_color(on_color, index)
    else:
        funhouse.set_text_color(0x606060, index)


# Create the labels
funhouse.display.root_group = None
slider_label = funhouse.add_text(
    text="Slider:", text_position=(50, 30), text_color=0x606060
)
capright_label = funhouse.add_text(
    text="Touch", text_position=(85, 10), text_color=0x606060
)
pir_label = funhouse.add_text(text="PIR", text_position=(60, 10), text_color=0x606060)
capleft_label = funhouse.add_text(
    text="Touch", text_position=(25, 10), text_color=0x606060
)
onoff_label = funhouse.add_text(text="OFF", text_position=(10, 25), text_color=0x606060)
up_label = funhouse.add_text(text="UP", text_position=(10, 10), text_color=0x606060)
sel_label = funhouse.add_text(text="SEL", text_position=(10, 60), text_color=0x606060)
down_label = funhouse.add_text(
    text="DOWN", text_position=(10, 100), text_color=0x606060
)
jst1_label = funhouse.add_text(
    text="SENSOR 1", text_position=(40, 80), text_color=0x606060
)
jst2_label = funhouse.add_text(
    text="SENSOR 2", text_position=(40, 95), text_color=0x606060
)
jst3_label = funhouse.add_text(
    text="SENSOR 3", text_position=(40, 110), text_color=0x606060
)
temp_label = funhouse.add_text(
    text="Temp:", text_position=(50, 45), text_color=0xFF00FF
)
pres_label = funhouse.add_text(
    text="Pres:", text_position=(50, 60), text_color=0xFF00FF
)
funhouse.display.root_group = funhouse.splash

while True:
    funhouse.set_text("Temp %0.1F" % funhouse.peripherals.temperature, temp_label)
    funhouse.set_text("Pres %d" % funhouse.peripherals.pressure, pres_label)

    print(funhouse.peripherals.temperature, funhouse.peripherals.relative_humidity)
    set_label_color(funhouse.peripherals.captouch6, onoff_label, 0x00FF00)
    set_label_color(funhouse.peripherals.captouch7, capleft_label, 0x00FF00)
    set_label_color(funhouse.peripherals.captouch8, capright_label, 0x00FF00)

    slider = funhouse.peripherals.slider
    if slider is not None:
        funhouse.peripherals.dotstars.brightness = slider
        funhouse.set_text("Slider: %1.1f" % slider, slider_label)
    set_label_color(slider is not None, slider_label, 0xFFFF00)

    set_label_color(funhouse.peripherals.button_up, up_label, 0xFF0000)
    set_label_color(funhouse.peripherals.button_sel, sel_label, 0xFFFF00)
    set_label_color(funhouse.peripherals.button_down, down_label, 0x00FF00)

    set_label_color(funhouse.peripherals.pir_sensor, pir_label, 0xFF0000)
    set_label_color(sensors[0].value, jst1_label, 0xFFFFFF)
    set_label_color(sensors[1].value, jst2_label, 0xFFFFFF)
    set_label_color(sensors[2].value, jst3_label, 0xFFFFFF)
