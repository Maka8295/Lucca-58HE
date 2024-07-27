# SPDX-FileCopyrightText: 2021 ladyada for Adafruit Industries
#
# SPDX-License-Identifier: MIT

"""
How to use this test file:

Copy adafruit_debouncer's dependencies to lib/ on your circuitpython device.
Copy adafruit_debouncer.py to / on the device
Copy this tests.py file to /main.py on the device
Connect to the serial terminal (e.g. sudo screen /dev/ttyACM0 115200)
Press Ctrl-D, if needed to start the tests running
"""
import sys
import time
import adafruit_debouncer


def _true():
    return True


def _false():
    return False


def assertEqual(var_a, var_b):  # pylint: disable=invalid-name
    assert var_a == var_b, "Want %r, got %r" % (var_a, var_b)


def test_back_and_forth():
    # Start false
    debouncer = adafruit_debouncer.Debouncer(_false)
    assertEqual(debouncer.value, False)

    # Set the raw state to true, update, and make sure the debounced
    # state has not changed yet:
    debouncer.function = _true
    debouncer.update()
    assertEqual(debouncer.value, False)
    assert not debouncer.last_duration, "There was no previous interval??"

    # Sleep longer than the debounce interval, so state can change:
    time.sleep(0.02)
    debouncer.update()
    assert debouncer.last_duration  # is actually duration between powerup and now
    assertEqual(debouncer.value, True)
    assertEqual(debouncer.rose, True)
    assertEqual(debouncer.fell, False)
    # Duration since last change has only been long enough to run these
    # asserts, which should be well under 1/10 second
    assert debouncer.current_duration < 0.1, (
        "Unit error? %d" % debouncer.current_duration
    )

    # Set raw state back to false, make sure it's not instantly reflected,
    # then wait and make sure it IS reflected after the interval has passed.
    debouncer.function = _false
    debouncer.update()
    assertEqual(debouncer.value, True)
    assertEqual(debouncer.fell, False)
    assertEqual(debouncer.rose, False)
    time.sleep(0.02)
    assert 0.019 < debouncer.current_duration <= 1, (
        "Unit error? sleep .02 -> duration %d" % debouncer.current_duration
    )
    debouncer.update()
    assertEqual(debouncer.value, False)
    assertEqual(debouncer.rose, False)
    assertEqual(debouncer.fell, True)

    assert 0 < debouncer.current_duration <= 0.1, (
        "Unit error? time to run asserts %d" % debouncer.current_duration
    )
    assert 0 < debouncer.last_duration < 0.1, (
        "Unit error? Last dur should be ~.02, is %d" % debouncer.last_duration
    )


def test_interval_is_the_same():
    debouncer = adafruit_debouncer.Debouncer(_false, interval=0.25)
    assertEqual(debouncer.value, False)
    debouncer.update()
    debouncer.function = _true
    debouncer.update()

    time.sleep(0.1)  # longer than default interval
    debouncer.update()
    assertEqual(debouncer.value, False)

    time.sleep(0.2)  # 0.1 + 0.2 > 0.25
    debouncer.update()
    assertEqual(debouncer.value, True)
    assertEqual(debouncer.rose, True)
    assertEqual(debouncer.interval, 0.25)


def test_setting_interval():
    # Check that setting the interval does change the time the debouncer waits
    debouncer = adafruit_debouncer.Debouncer(_false, interval=0.01)
    debouncer.update()

    # set the interval to a longer time, sleep for a time between
    # the two interval settings, and assert that the value hasn't changed.

    debouncer.function = _true
    debouncer.interval = 0.2
    debouncer.update()
    assert debouncer.interval - 0.2 < 0.00001, "interval is not consistent"
    time.sleep(0.11)
    debouncer.update()

    assertEqual(debouncer.value, False)
    assertEqual(debouncer.rose, False)
    assertEqual(debouncer.fell, False)

    # and then once the whole time has passed make sure it did change
    time.sleep(0.11)
    debouncer.update()
    assertEqual(debouncer.value, True)
    assertEqual(debouncer.rose, True)
    assertEqual(debouncer.fell, False)


def run():
    passes = 0
    fails = 0
    for name, test in locals().items():
        if name.startswith("test_") and callable(test):
            try:
                print()
                print(name)
                test()
                print("PASS")
                passes += 1
            except Exception as err:  # pylint: disable=broad-except
                sys.print_exception(err)  # pylint: disable=no-member
                print("FAIL")
                fails += 1

    print(passes, "passed,", fails, "failed")
    if passes and not fails:
        print(
            r"""
 ________
< YATTA! >
 --------
        \   ^__^
         \  (oo)\_______
            (__)\       )\/\
                ||----w |
                ||     ||"""
        )


if __name__ == "__main__":
    run()
