# SPDX-FileCopyrightText: 2023 Tim Cocks
#
# SPDX-License-Identifier: Unlicense

import time
import alarm
import board
from adafruit_magtag.magtag import MagTag

IDLE_TIMEOUT = 10  # seconds idle, then sleep

magtag = MagTag()

magtag.add_text(
    text_position=(
        50,
        (magtag.graphics.display.height // 2) - 1,
    ),
    text_scale=3,
)

magtag.set_text("Awake")

button_colors = ((255, 0, 0), (255, 150, 0), (0, 255, 255), (180, 0, 255))
button_tones = (1047, 1318, 1568, 2093)

now = time.monotonic()
last_action_time = now
while True:
    now = time.monotonic()
    if now - last_action_time >= 10.0:
        magtag.set_text("Sleeping")
        magtag.peripherals.deinit()
        time.sleep(2)
        # go to sleep
        pin_alarm = alarm.pin.PinAlarm(pin=board.D11, value=False, pull=True)

        # Exit the program, and then deep sleep until the alarm wakes us.
        alarm.exit_and_deep_sleep_until_alarms(pin_alarm)

    for i, b in enumerate(magtag.peripherals.buttons):
        if not b.value:
            print("Button %c pressed" % chr((ord("A") + i)))
            last_action_time = now
            magtag.peripherals.neopixel_disable = False
            magtag.peripherals.neopixels.fill(button_colors[i])
            magtag.peripherals.play_tone(button_tones[i], 0.25)
            break
    else:
        magtag.peripherals.neopixel_disable = True
    time.sleep(0.01)
