# SPDX-FileCopyrightText: 2024 Jeff Epler for Adafruit Industries
#
# SPDX-License-Identifier: Unlicense

"""Effects Demonstration

This will apply a nubmer of effects to a single image.

Press any of the directional buttons to immediately apply a new effect.

Otherwise, effects cycle every DISPLAY_INTERVAL milliseconds (default 2000 = 2 seconds)
"""

import displayio
from jpegio import JpegDecoder
from adafruit_display_text.label import Label
from adafruit_ticks import ticks_less, ticks_ms, ticks_add, ticks_diff
from font_free_mono_bold_24 import FONT
import bitmapfilter

from adafruit_pycamera import imageprocessing
from adafruit_pycamera import PyCameraBase


blend_50_50 = bitmapfilter.blend_precompute(imageprocessing.alphablend_maker(0.5))
screen = bitmapfilter.blend_precompute(imageprocessing.screen_func)
overlay = bitmapfilter.blend_precompute(imageprocessing.overlay_func)
hard_light = bitmapfilter.blend_precompute(imageprocessing.hard_light_func)
soft_light = bitmapfilter.blend_precompute(imageprocessing.soft_light_func)
color_dodge = bitmapfilter.blend_precompute(imageprocessing.color_dodge_func)
# linear_dodge = bitmapfilter.blend_precompute(imageprocessing.linear_dodge_func)
# divide = bitmapfilter.blend_precompute(imageprocessing.divide_func)
multiply = bitmapfilter.blend_precompute(imageprocessing.multiply_func)
# subtract = bitmapfilter.blend_precompute(imageprocessing.subtract_func)
# color_burn = bitmapfilter.blend_precompute(imageprocessing.color_burn_func)
# linear_burn = bitmapfilter.blend_precompute(imageprocessing.linear_burn_func)
# darken_only = bitmapfilter.blend_precompute(min)
# lighten_only = bitmapfilter.blend_precompute(max)


def blender(f):
    def inner(b):
        return bitmapfilter.blend(b, b, testpattern, f)

    return inner


def reverse_blender(f):
    def inner(b):
        return bitmapfilter.blend(b, testpattern, b, f)

    return inner


inverse_greyscale_weights = bitmapfilter.ChannelMixer(
    1 - 0.299,
    1 - 0.587,
    1 - 0.114,
    1 - 0.299,
    1 - 0.587,
    1 - 0.114,
    1 - 0.299,
    1 - 0.587,
    1 - 0.114,
)

blur_more = [
    4,
    15,
    24,
    15,
    4,
    15,
    61,
    97,
    61,
    15,
    24,
    97,
    154,
    97,
    24,
    15,
    61,
    97,
    61,
    15,
    4,
    15,
    24,
    15,
    4,
]


# "Sketch" filter based on
# https://www.freecodecamp.org/news/sketchify-turn-any-image-into-a-pencil-sketch-with-10-lines-of-code-cf67fa4f68ce/
def sketch(b):
    bitmapfilter.mix(b, inverse_greyscale_weights)
    memoryview(auxbuffer)[:] = memoryview(b)
    bitmapfilter.morph(auxbuffer, blur_more)
    bitmapfilter.blend(b, auxbuffer, b, color_dodge)
    bitmapfilter.mix(b, inverse_greyscale_weights)  # get rid of magenta halos
    return b


effects = [
    ("sketch", sketch),
    ("50/50", blender(blend_50_50)),
    ("multiply", blender(multiply)),
    ("soft light", blender(soft_light)),
    ("hard_light", blender(hard_light)),
    ("blue cast", imageprocessing.blue_cast),
    ("blur", imageprocessing.blur),
    ("bright", lambda b: bitmapfilter.mix(b, bitmapfilter.ChannelScale(2.0, 2.0, 2.0))),
    ("emboss", imageprocessing.emboss),
    ("green cast", imageprocessing.green_cast),
    ("greyscale", imageprocessing.greyscale),
    ("ironbow", imageprocessing.ironbow),
    (
        "low contrast",
        lambda b: bitmapfilter.mix(
            b, bitmapfilter.ChannelScaleOffset(0.5, 0.5, 0.5, 0.5, 0.5, 0.5)
        ),
    ),
    ("negative", imageprocessing.negative),
    ("red cast", imageprocessing.red_cast),
    ("sepia", imageprocessing.sepia),
    ("sharpen", imageprocessing.sharpen),
    ("solarize", bitmapfilter.solarize),
    (
        "swap r/b",
        lambda b: bitmapfilter.mix(
            b, bitmapfilter.ChannelMixer(0, 0, 1, 0, 1, 0, 1, 0, 0)
        ),
    ),
]


def cycle(seq):
    while True:
        for s in seq:
            yield s


effects_cycle = iter(cycle(effects))


DISPLAY_INTERVAL = 2000  # milliseconds

decoder = JpegDecoder()

pycam = PyCameraBase()
pycam.init_display()

testpattern = displayio.Bitmap(208, 208, 65535)
auxbuffer = displayio.Bitmap(208, 208, 65535)


def main():
    filename = "/cornell_box_208x208.jpg"

    bitmap = displayio.Bitmap(208, 208, 65535)
    bitmap0 = displayio.Bitmap(208, 208, 65535)
    decoder.open(filename)
    decoder.decode(bitmap0)

    decoder.open("/testpattern_208x208.jpg")
    decoder.decode(testpattern)

    label = Label(font=FONT, x=0, y=8)
    pycam.display.root_group = label
    pycam.display.refresh()

    deadline = ticks_ms()
    while True:
        now = ticks_ms()
        if pycam.up.fell:
            deadline = now

        if pycam.down.fell:
            deadline = now

        if pycam.left.fell:
            deadline = now

        if pycam.right.fell:
            deadline = now

        if ticks_less(deadline, now):
            memoryview(bitmap)[:] = memoryview(bitmap0)
            deadline = ticks_add(deadline, DISPLAY_INTERVAL)

            effect_name, effect = next(effects_cycle)  # random.choice(effects)
            print(effect)
            print(f"applying {effect=}")
            t0 = ticks_ms()
            effect(bitmap)
            t1 = ticks_ms()
            dt = ticks_diff(t1, t0)
            print(f"{dt}ms to apply effect")
            pycam.blit(bitmap, x_offset=16)
            label.text = f"{dt:4}ms: {effect_name}"
            pycam.display.refresh()


main()
