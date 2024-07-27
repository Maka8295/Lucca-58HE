# SPDX-FileCopyrightText: 2022 Jeff Epler, written for Adafruit Industries
#
# SPDX-License-Identifier: MIT
#
# Heavy inspiration from Pimoroni's "PWM Cluster":
# https://github.com/pimoroni/pimoroni-pico/blob/main/drivers/pwm/pwm_cluster.cpp
# https://github.com/pimoroni/pimoroni-pico/blob/main/drivers/pwm/pwm_cluster.pio

import array

import board
import rp2pio
import adafruit_ticks
import ulab.numpy as np
from adafruit_motor import servo


import adafruit_pioasm

_cycle_count = 3
_program = adafruit_pioasm.Program(
    """
.wrap_target
    out pins, 32            ; Immediately set the pins to their new state
    out y, 32               ; Set the counter
count_check:
    jmp y-- delay           ; Check if the counter is 0, and if so wrap around.
                            ; If not decrement the counter and jump to the delay
.wrap

delay:
    jmp count_check [1]     ; Wait a few cycles then jump back to the loop
"""
)


class PulseItem:
    def __init__(self, group, index, phase, maxval):
        self._group = group
        self._index = index
        self._phase = phase
        self._value = 0
        self._maxval = maxval
        self._turn_on = self._turn_off = None
        self._mask = 1 << index

    @property
    def frequency(self):
        return self._group.frequency

    @property
    def duty_cycle(self):
        return self._value

    @duty_cycle.setter
    def duty_cycle(self, value):
        if value < 0 or value > self._maxval:
            raise ValueError(f"value must be in the range(0, {self._maxval+1})")
        self._value = value
        self._recalculate()

    @property
    def phase(self):
        return self._phase

    @phase.setter
    def phase(self, phase):
        if phase < 0 or phase >= self._maxval:
            raise ValueError(f"phase must be in the range(0, {self._maxval})")
        self._phase = phase
        self._recalculate()

    def _recalculate(self):
        self._turn_on = self._get_turn_on()
        self._turn_off = self._get_turn_off()
        self._group._maybe_update()  # pylint: disable=protected-access

    def _get_turn_on(self):
        maxval = self._maxval
        if self._value == 0:
            return None
        if self._value == self._maxval:
            return 0
        return self.phase % maxval

    def _get_turn_off(self):
        maxval = self._maxval
        if self._value == 0:
            return None
        if self._value == self._maxval:
            return None
        return (self._value + self.phase) % maxval

    def __str__(self):
        return f"<PulseItem: {self.duty_cycle=} {self.phase=} {self._turn_on=} {self._turn_off=}>"


class PulseGroup:
    def __init__(
        self,
        first_pin,
        pin_count,
        period=0.02,
        maxval=65535,
        stagger=False,
        auto_update=True,
    ):  # pylint: disable=too-many-arguments
        """Create a pulse group with the given characteristics"""
        self._frequency = round(1 / period)
        pio_frequency = round((1 + maxval) * _cycle_count / period)
        self._sm = rp2pio.StateMachine(
            _program.assembled,
            frequency=pio_frequency,
            first_out_pin=first_pin,
            out_pin_count=pin_count,
            auto_pull=True,
            pull_threshold=32,
            **_program.pio_kwargs,
        )
        self._auto_update = auto_update
        self._items = [
            PulseItem(self, i, round(maxval * i / pin_count) if stagger else 0, maxval)
            for i in range(pin_count)
        ]
        self._maxval = maxval

    @property
    def frequency(self):
        return self._frequency

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        self.deinit()

    def deinit(self):
        self._sm.deinit()
        del self._items[:]

    def __getitem__(self, i):
        """Get an individual pulse generator"""
        return self._items[i]

    def __len__(self):
        return len(self._items)

    def update(self):
        changes = {0: [0, 0]}

        for i in self._items:
            turn_on = i._turn_on  # pylint: disable=protected-access
            turn_off = i._turn_off  # pylint: disable=protected-access
            mask = i._mask  # pylint: disable=protected-access

            if turn_on is not None:
                this_change = changes.get(turn_on)
                if this_change:
                    this_change[0] |= mask
                else:
                    changes[turn_on] = [mask, 0]

                # start the cycle 'on'
                if turn_off is not None and turn_off < turn_on:
                    changes[0][0] |= mask

            if turn_off is not None:
                this_change = changes.get(turn_off)
                if this_change:
                    this_change[1] |= mask
                else:
                    changes[turn_off] = [0, mask]

        def make_sequence():
            sorted_changes = sorted(changes.items())
            # Note that the first change time is always 0! Loop over range(len) is
            # to reduce allocations
            old_time = 0
            value = 0
            for time, (turn_on, turn_off) in sorted_changes:
                if time != 0:  # never occurs on the first iteration
                    yield time - old_time - 1
                old_time = time

                value = (value | turn_on) & ~turn_off
                yield value

            # the final delay value
            yield self._maxval - old_time

        buf = array.array("L", make_sequence())

        self._sm.background_write(loop=buf)

    def _maybe_update(self):
        if self._auto_update:
            self.update()

    @property
    def auto_update(self):
        return self.auto_update

    @auto_update.setter
    def auto_update(self, value):
        self.auto_update = bool(value)

    def __str__(self):
        return f"<PulseGroup({len(self)})>"


class CyclicSignal:
    def __init__(self, data, phase=0):
        self._data = data
        self._phase = 0
        self.phase = phase
        self._scale = len(self._data) - 1

    @property
    def phase(self):
        return self._phase

    @phase.setter
    def phase(self, value):
        self._phase = value % 1

    @property
    def value(self):
        idxf = self._phase * len(self._data)
        idx = int(idxf)
        frac = idxf % 1
        idx1 = (idx + 1) % len(self._data)
        val = self._data[idx]
        val1 = self._data[idx1]
        return val + (val1 - val) * frac

    def advance(self, delta):
        self._phase = (self._phase + delta) % 1


if __name__ == "__main__":
    pulsers = PulseGroup(board.SERVO_1, 18, auto_update=False)
    # Set the phase of each servo so that servo 0 starts at offset 0ms, servo 1
    # at offset 2.5ms, ...
    # For up to 8 servos, this means their duty cycles do not overlap.  Otherwise,
    # servo 9 is also at offset 0ms, etc.
    for j, p in enumerate(pulsers):
        p.phase = 8192 * (j % 8)

    servos = [servo.Servo(p) for p in pulsers]

    sine = np.sin(np.linspace(0, 2 * np.pi, 50, endpoint=False)) * 0.5 + 0.5
    print(sine)

    signals = [CyclicSignal(sine, j / len(servos)) for j in range(len(servos))]

    t0 = adafruit_ticks.ticks_ms()
    while True:
        t1 = adafruit_ticks.ticks_ms()
        for servo, signal in zip(servos, signals):
            signal.advance((t1 - t0) / 8000)
            servo.fraction = signal.value
        pulsers.update()
        print(adafruit_ticks.ticks_diff(t1, t0), "ms")
        t0 = t1
