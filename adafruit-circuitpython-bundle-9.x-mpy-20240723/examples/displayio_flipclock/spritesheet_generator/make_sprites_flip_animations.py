# SPDX-FileCopyrightText: Copyright (c) 2022 Tim Cocks for Adafruit Industries
#
# SPDX-License-Identifier: MIT
"""
Command line script to generate flip clock spritesheet Bitmap image files.


"""

import math

from typing import Tuple, List, Optional
import numpy
from PIL import Image, ImageDraw, ImageFont
from PIL.Image import Palette, Resampling, Transform
import typer

DEFAULT_FONT = "LeagueSpartan-Regular.ttf"
DEFAULT_FONT_SIZE = 44
TILE_WIDTH, TILE_HEIGHT = (48, 100)
TILE_COLOR = (90, 90, 90)
FONT_COLOR = (255, 255, 255)
PADDING_SIZE = 8
TRANSPARENCY_COLOR = (0, 255, 0)
CENTER_LINE_HEIGHT = 1  # px


# pylint: disable=too-many-arguments, too-many-locals


def find_coeffs(pa: Tuple, pb: Tuple) -> numpy.ndarray:
    """
    Find the set of coefficients that can be used to apply a perspective transform
    from the shape of one given plane to the shape of another given plane.

    :param tuple pa: the 4 points that make up the first plane
    :param tuple pb: the 4 points that make up the second plane

    """
    matrix = []
    for p1, p2 in zip(pa, pb):
        matrix.append([p1[0], p1[1], 1, 0, 0, 0, -p2[0] * p1[0], -p2[0] * p1[1]])
        matrix.append([0, 0, 0, p1[0], p1[1], 1, -p2[1] * p1[0], -p2[1] * p1[1]])

    A = numpy.matrix(matrix, dtype=float)
    B = numpy.array(pb).reshape(8)

    res = numpy.dot(numpy.linalg.inv(A.T * A) * A.T, B)
    return numpy.array(res).reshape(8)


def find_top_half_coeffs_inputs_for_angle(img: Image.Image, angle: int) -> Tuple[List]:
    """
    Find the coefficient inputs for the top half of the image for a given angle.

    :param PIL.Image img: The image object representing the top half of the digit
    :param int angle: The angle in degrees (0-90) to generate the coefficients for

    :returns Tuple of Lists of input points that can be passed to the
     find_coefficient() function.
    """
    x_val = (angle * PADDING_SIZE) / 90
    y_val = min((angle * (img.height)) / 90, img.height - 1)

    first_list = [
        (-(x_val + 1), y_val),
        (img.width + x_val, y_val),
        (img.width, img.height),
        (0, img.height),
    ]
    second_list = [(0, 0), (img.width, 0), (img.width, img.height), (0, img.height)]
    return first_list, second_list


def find_bottom_half_coeffs_inputs_for_angle(
    img: Image.Image, angle: int
) -> Tuple[List]:
    """
    Find the coefficient inputs for the bottom half of the image for a given angle.

    :param PIL.Image img: The image object representing the top half of the digit
    :param int angle: The angle in degrees (0-90) to generate the coefficients for.
    """
    x_val = ((90 - angle) * PADDING_SIZE) / 90
    y_val = min((angle * (img.height)) / 90, img.height - 1)
    # print(f"(x: {x_val}, y: {y_val})")
    first_list = [
        (0, 0),
        (img.width, 0),
        (img.width + x_val, y_val),
        (-(x_val + 1), y_val),
    ]
    second_list = [(0, 0), (img.width, 0), (img.width, img.height), (0, img.height)]
    return first_list, second_list


def get_top_half(img: Image.Image) -> Image.Image:
    """
    Return an Image object representing the top half of the input image

    :param Image img: input image

    :returns Image: PIL Image object containing the top half of the input image
    """
    top_half = img.crop((0, 0, img.width, img.height // 2))
    return top_half


def get_bottom_half(img: Image.Image) -> Image.Image:
    """
    Return an Image object representing the bottom half of the input image

    :param Image img: input image

    :returns Image: PIL Image object containing the bottom half of the input image
    """
    bottom_half = img.crop((0, img.height // 2, img.width, img.height))
    return bottom_half


def make_sprite(
    character: str,
    font_size: int = 44,
    font: str = DEFAULT_FONT,
    padding: int = PADDING_SIZE,
    width: int = TILE_WIDTH,
    height: int = TILE_HEIGHT,
    text_color: Tuple[int, int, int] = FONT_COLOR,
    tile_color: Tuple[int, int, int] = TILE_COLOR,
    transparency_color: Tuple[int, int, int] = TRANSPARENCY_COLOR,
    text_y_offset: int = 0,
    center_line_color: Optional[Tuple[int, int, int]] = None,
) -> Image.Image:
    """
    Make a PIL Image object representing a single static digit (or character).
    These get packed into the static sprite sheet, and are used as the basis
    for the angled animation sprites.

    :param str character: A single digit or character to put on this static sprite
    :param int font_size: The size to render the font on the the sprite
    :param str font: The filename of the font to render the character in.
      Filetype must be otf, ttf, or other font formats supported by PIL.
    :param int width: The width in pixels of each tile
    :param int height: The height in pixels of each tile
    :param int padding: The number of pixels padding around all sides. This will be filled with
      the transparent color so displayio won't show it if initialized properly. The padding space
      is used in the perspective animation frames to "poke out" into for the
      visual effect of appearing bigger / closer.
    :param tuple text_color: The color of the digit text in each tile.
      Tuple containing RGB color values 0-255 for each color.
    :param tuple tile_color: The color of the tile the digit is on.
      Tuple containing RGB color values 0-255 for each color.
    :param tuple transparency_color: The color to use for transparency. displayio.Palette
      must call make_transparent() with the indexes represented by this color.
      Tuple containing RGB color values 0-255 for each color.
    :param tuple center_line_color: The color to draw the center horizontal line.
      None for no line.


    :returns Image: The PIL Image object containing a single static character sprite.
    """
    border_rect_size = (width - padding, height - padding)
    inner_image_size = (width, height)
    border_shape = ((padding, padding), border_rect_size)
    center_line_shape = (
        (padding, height // 2 - CENTER_LINE_HEIGHT // 2),
        (border_rect_size[0], height // 2 + CENTER_LINE_HEIGHT // 2),
    )

    fnt = ImageFont.truetype(font, font_size)
    img = Image.new("RGBA", (width, height), color=transparency_color)

    inner_img = Image.new("RGBA", inner_image_size, color=transparency_color)

    inner_draw = ImageDraw.Draw(inner_img)

    inner_draw.rectangle(border_shape, outline=tile_color, fill=tile_color)

    # w, h = inner_draw.textsize(character, font=fnt)
    # print(f"w: {w}, h: {h}")
    bbox = inner_draw.textbbox((0, 0), character, font=fnt)
    w, h = bbox[2], bbox[3]
    # print(bbox)
    inner_draw.text(
        (
            ((inner_image_size[0] - w) // 2) + 1,
            ((inner_image_size[1] - h) // 2) + 1 + text_y_offset,
        ),
        character,
        fill=text_color,
        font=fnt,
    )
    if center_line_color and not center_line_color == (None, None, None):
        inner_draw.rectangle(
            center_line_shape, outline=center_line_color, fill=center_line_color
        )

    img.paste(inner_img, (padding // 2, padding // 2))

    # inner_img.save("test_inner.png")

    return inner_img


def make_angles_sprite_set(
    img: Image.Image, count: int = 10, bottom_skew: bool = False
) -> List[Image.Image]:
    """
    Generate angled sprites from a static sprite image.

    :param Image img: input static image
    :param int count: number of animation frames to generate (default 10)
    :param bool bottom_skew: Whether to render the bottom angle or top angled sprites

    :returns List[Image]: A List of Image objects containing the angled sprites.
    """
    angled_sprites = []
    # test_sheet = Image.new('RGBA', (img.width * 5, img.height * 2), color=(0, 255, 0))
    # test_sheet.save("before_anything.png")

    angle_count_by = (90 // count) + 1
    for _, _angle in enumerate(range(0, 91, angle_count_by)):
        # print(f"angle: {_angle}")
        if bottom_skew:
            coeffs = find_coeffs(
                *find_bottom_half_coeffs_inputs_for_angle(img, _angle + 1)
            )
        else:  # top skew:
            coeffs = find_coeffs(
                *find_top_half_coeffs_inputs_for_angle(img, _angle + 1)
            )

        this_angle_img = img.transform(
            (img.width, img.height), Transform.PERSPECTIVE, coeffs, Resampling.BICUBIC
        )

        # this_angle_img.save(f"test_out/top_half_inner_{_angle + 1}.png")

        # coords = (((_ % 5) * img.width), ((_ // 5) * img.height))
        # print(coords)

        angled_sprites.append(this_angle_img)

    return angled_sprites


def make_static_sheet(
    font_size: int = DEFAULT_FONT_SIZE,
    font: str = DEFAULT_FONT,
    padding: int = PADDING_SIZE,
    width: int = TILE_WIDTH,
    height: int = TILE_HEIGHT,
    text_color: Tuple[int, int, int] = FONT_COLOR,
    tile_color: Tuple[int, int, int] = TILE_COLOR,
    transparency_color: Tuple[int, int, int] = TRANSPARENCY_COLOR,
    text_y_offset: int = 0,
    center_line_color: Optional[Tuple[int, int, int]] = None,
) -> None:
    """
    Generate the spritesheet of static digit images. Outputs static sprite sheet
    file as "static_sheet.bmp"

    :param int font_size: the font size to render the text on the sprites at
    :param str font: the filename of the font to render the text in.
      Must be otf, ttf, or other format supported by PIL.
    :param int width: The width in pixels of each tile
    :param int height: The height in pixels of each tile
    :param int padding: The number of pixels padding around all sides. This will be filled with
      the transparent color so displayio won't show it if initialized properly. The padding space
      is used in the perspective animation frames to "poke out" into for the
      visual effect of appearing bigger / closer.
    :param tuple text_color: The color of the digit text in each tile.
      Tuple containing RGB color values 0-255 for each color.
    :param tuple tile_color: The color of the tile the digit is on.
      Tuple containing RGB color values 0-255 for each color.
    :param tuple transparency_color: The color to use for transparency. displayio.Palette
      must call make_transparent() with the indexes represented by this color.
      Tuple containing RGB color values 0-255 for each color.
    :param int text_y_offset: Amount to shift the text placement verticaly.
      Positive numbers move it down, negative move it up.

    """
    full_sheet_img = Image.new(
        "RGBA", (width * 3, height * 4), color=transparency_color
    )

    for i in range(10):
        img = make_sprite(
            f"{i}",
            font_size=font_size,
            font=font,
            padding=padding,
            width=width,
            height=height,
            text_color=text_color,
            tile_color=tile_color,
            text_y_offset=text_y_offset,
            center_line_color=center_line_color,
        )
        # img.save(f'char_sprites/pil_text_{i}.png')
        coords = (((i % 3) * width), ((i // 3) * height))
        # print(coords)
        full_sheet_img.paste(img, coords)

    # img = make_sprite(":", font_size=font_size)
    # coords = (((10 % 3) * TILE_WIDTH), ((10 // 3) * TILE_HEIGHT))
    # full_sheet_img.paste(img, coords)

    full_sheet_img = full_sheet_img.convert(mode="P", palette=Palette.WEB)
    full_sheet_img.save("static_sheet.bmp")


def pack_images_to_sheet(
    images: List[Image.Image],
    width: int,
    transparency_color=TRANSPARENCY_COLOR,
    tile_width: int = TILE_WIDTH,
) -> Image.Image:
    """
    Pack a list of PIL Image objects into a sprite sheet within
    another PIL Image object.

    :param List[Image] images: A list of Image objects to pack into the sheet
    :param int width: The number of sprites in each row
    :param tuple transparency_color: The color to use for transparency. displayio.Palette
      must call make_transparent() with the indexes represented by this color.
      Tuple containing RGB color values 0-255 for each color.
    :param int tile_width: The width in pixels of each tile that will be in the sheet.

    :returns Image: PIL Image object containing the packed sprite sheet
    """
    row_count = math.ceil(len(images) / width)

    _img_width = images[0].width
    _img_height = images[0].height
    # print(f"len: {len(images)} width:{width} img_w:{_img_width} img_h:{_img_height}")
    _sheet_img = Image.new(
        "RGBA", (_img_width * width, _img_height * row_count), color=transparency_color
    )
    # _sheet_img.save("before_things.bmp")
    for i, image in enumerate(images):
        coords = (((i % width) * tile_width), ((i // width) * image.height))
        # print(coords)
        _sheet_img.paste(image, coords, image)
        # image.save(f"test_out/img_{i}.png")

    return _sheet_img


def make_animations_sheets(
    font_size: int = DEFAULT_FONT_SIZE,
    font: str = DEFAULT_FONT,
    width: int = TILE_WIDTH,
    height: int = TILE_HEIGHT,
    padding: int = PADDING_SIZE,
    text_color: Tuple[int, int, int] = FONT_COLOR,
    tile_color: Tuple[int, int, int] = TILE_COLOR,
    transparency_color: Tuple[int, int, int] = TRANSPARENCY_COLOR,
    animation_frames: int = 10,
    text_y_offset: int = 0,
    center_line_color: Optional[Tuple[int, int, int]] = None,
) -> None:
    """
    Generate and save the top and bottom animation sprite sheets for the digits 0-9.
    Outputs the two spritesheets as "bottom_animation_sheet.bmp" and "top_animation_sheet.bmp"

    :param int font_size: the font size to render the text on the sprites at
    :param str font: the filename of the font to render the text in.
      Must be otf, ttf, or other format supported by PIL.
    :param int width: The width in pixels of each tile
    :param int height: The height in pixels of each tile
    :param int padding: The number of pixels padding around all sides. This will be filled with
      the transparent color so displayio won't show it if initialized properly. The padding space
      is used in the perspective animation frames to "poke out" into for the
      visual effect of appearing bigger / closer.
    :param tuple text_color: The color of the digit text in each tile.
      Tuple containing RGB color values 0-255 for each color.
    :param tuple tile_color: The color of the tile the digit is on.
      Tuple containing RGB color values 0-255 for each color.
    :param tuple transparency_color: The color to use for transparency. displayio.Palette
      must call make_transparent() with the indexes represented by this color.
      Tuple containing RGB color values 0-255 for each color.
    :param animation_frames: The number of frames to use for the flip animations.
    :param int text_y_offset: Amount to shift the text placement verticaly.
      Positive numbers move it down, negative move it up.
    """
    bottom_sprites = []
    top_sprites = []

    for i in range(10):
        img = make_sprite(
            f"{i}",
            font_size=font_size,
            font=font,
            padding=padding,
            width=width,
            height=height,
            text_color=text_color,
            tile_color=tile_color,
            text_y_offset=text_y_offset,
            center_line_color=center_line_color,
        )

        top_half = get_top_half(img)
        bottom_half = get_bottom_half(img)

        bottom_angled_sprites = make_angles_sprite_set(
            bottom_half, animation_frames, bottom_skew=True
        )
        top_angled_sprites = make_angles_sprite_set(
            top_half, animation_frames, bottom_skew=False
        )

        bottom_sprites.extend(bottom_angled_sprites)
        top_sprites.extend(top_angled_sprites)

    bottom_sheet = pack_images_to_sheet(
        images=bottom_sprites,
        width=animation_frames,
        transparency_color=transparency_color,
        tile_width=width,
    )
    # bottom_sheet.save("test_bottom_sheet.png")

    bottom_sheet = bottom_sheet.convert(mode="P", palette=Palette.WEB)
    bottom_sheet.save("bottom_animation_sheet.bmp")

    top_sheet = pack_images_to_sheet(
        images=top_sprites,
        width=animation_frames,
        tile_width=width,
        transparency_color=transparency_color,
    )
    top_sheet = top_sheet.convert(mode="P", palette=Palette.WEB)
    top_sheet.save("top_animation_sheet.bmp")


def main(
    width: int = TILE_WIDTH,
    height: int = TILE_HEIGHT,
    padding: int = PADDING_SIZE,
    text_color: Tuple[int, int, int] = FONT_COLOR,
    tile_color: Tuple[int, int, int] = TILE_COLOR,
    transparent_color: Tuple[int, int, int] = TRANSPARENCY_COLOR,
    font: str = DEFAULT_FONT,
    font_size: int = DEFAULT_FONT_SIZE,
    animation_frames: int = 10,
    text_y_offset: int = 0,
    center_line_color: Optional[Tuple[int, int, int]] = typer.Option(
        (None, None, None)
    ),
) -> None:
    # print(center_line_color)
    make_static_sheet(
        font_size=font_size,
        font=font,
        padding=padding,
        width=width,
        height=height,
        text_color=text_color,
        tile_color=tile_color,
        transparency_color=transparent_color,
        text_y_offset=text_y_offset,
        center_line_color=center_line_color,
    )

    make_animations_sheets(
        font_size=font_size,
        font=font,
        padding=padding,
        width=width,
        height=height,
        text_color=text_color,
        tile_color=tile_color,
        transparency_color=transparent_color,
        animation_frames=animation_frames,
        text_y_offset=text_y_offset,
        center_line_color=center_line_color,
    )


if __name__ == "__main__":
    typer.run(main)
