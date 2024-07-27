#RIGHT HAND
import board
from kb import KMKKeyboard
from kmk.keys import KC
from kmk.modules.layers import Layers
from kmk.extensions.media_keys import MediaKeys
from kmk.modules.mouse_keys import MouseKeys
from kmk.extensions.RGB import RGB
from kmk.extensions.rgb import AnimationModes
#from kmk.extensions.debug import Debug
#keyboard.extensions.append(debug)

keyboard = KMKKeyboard()

keyboard.modules.append(Layers())
keyboard.modules.append(MouseKeys())
keyboard.extensions.append(MediaKeys())


# Enable debugging: http://kmkfw.io/docs/debugging/
keyboard.debug_enabled = True


under_rgb = RGB(pixel_pin=board.GP7,
    num_pixels=10,
    val_limit=100,
    hue_default=0,
    sat_default=100,
    rgb_order=(1, 0, 2),  # GRB WS2812
    val_default=100,
    hue_step=5,
    sat_step=5,
    val_step=5,
    animation_speed=1,
    breathe_center=1,  # 1.0-2.7
    knight_effect_length=3,
    animation_mode=AnimationModes.STATIC,
    reverse_animation=False,
    refresh_rate=60,
    )
rgb = RGB(pixel_pin=board.GP3,
    num_pixels=29,
    val_limit=100,
    hue_default=0,
    sat_default=100,
    rgb_order=(1, 0, 2),  # GRB WS2812
    val_default=100,
    hue_step=5,
    sat_step=5,
    val_step=5,
    animation_speed=1,
    breathe_center=1,  # 1.0-2.7
    knight_effect_length=3,
    animation_mode=AnimationModes.STATIC,
    reverse_animation=False,
    refresh_rate=60,
    )
keyboard.extensions.append(under_rgb)
keyboard.extensions.append(rgb)

# Key aliases
_______ = KC.TRNS
XXXXXXX = KC.NO

LOWER = KC.MO(1)
RAISE = KC.MO(2)
ADJUST = KC.LT(3, KC.SPC)

# Keymap
# fmt: off bvb
keyboard.keymap = [
    [  #Layer 0
        KC.LALT,   KC.N1,   KC.LSFT,   KC.E,   XXXXXXX,   KC.N5,         KC.N6,   KC.N7,   KC.N8,   KC.N9,   KC.N0,   KC.DEL,
        KC.X,    KC.Q,    XXXXXXX,    KC.N3,    KC.V,    KC.G,              KC.Y,    KC.U,    KC.I,    KC.O,    KC.P,    KC.EQL,
        KC.S,   KC.A,    KC.RSFT,    KC.D,    KC.SPC,    KC.T,            KC.H,   KC.J,    KC.K,    KC.L,    KC.SCLN,    KC.QUOT,
        KC.N2,   KC.LCTL,    KC.TAB,    KC.C,    KC.R,    KC.MO(1),             KC.KANA,  KC.N,  KC.M,  KC.COMM,  KC.DOT, KC.SLSH, KC.MINS,
        KC.Z,   KC.ESC,  KC.LGUI, KC.F, KC.B, KC.N4, KC.W, XXXXXXX,            KC.ENT,   KC.BSPC,  KC.LBRC, KC.RBRC, XXXXXXX, XXXXXXX, XXXXXXX,
    ],
    [  #Layer 1
        XXXXXXX,   KC.F1,   XXXXXXX,   XXXXXXX,   XXXXXXX,   KC.F5,             KC.F6,   KC.F7,   KC.F8,   KC.F9,   KC.F10,   KC.F11,
        XXXXXXX,    XXXXXXX,    XXXXXXX,    KC.F3,    KC.MPRV,    KC.VOLU,           XXXXXXX,    XXXXXXX,    KC.UP,    XXXXXXX,    XXXXXXX,    KC.F12,
        XXXXXXX,   XXXXXXX,    XXXXXXX,    XXXXXXX,    KC.MPLY,    XXXXXXX,          KC.H,   KC.LEFT,    KC.DOWN,    KC.RIGHT,    XXXXXXX,    KC.PSCR,
        KC.F2,   XXXXXXX,    XXXXXXX,    XXXXXXX,    XXXXXXX,    KC.MO(1),         KC.MPLY,  KC.TILD,  KC.BSLS,  KC.PIPE,  XXXXXXX, KC.VOLD, KC.VOLU,
        XXXXXXX,   XXXXXXX,  KC.MUTE, KC.VOLD, KC.MNXT, KC.F4, XXXXXXX, XXXXXXX,         KC.LCAP,   KC.MUTE,  KC.MPRV, KC.MNXT, XXXXXXX, XXXXXXX, XXXXXXX,
    ],
]
# fmt: on

if __name__ == "__main__":
    keyboard.go()
