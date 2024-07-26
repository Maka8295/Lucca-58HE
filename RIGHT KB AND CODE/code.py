#RIGHT HAND
from kb import KMKKeyboard
from kmk.keys import KC
from kmk.modules.layers import Layers
from kmk.extensions.media_keys import MediaKeys
from kmk.modules.mouse_keys import MouseKeys

#from kmk.extensions.debug import Debug
#keyboard.extensions.append(debug)

keyboard = KMKKeyboard()

keyboard.modules.append(Layers())
keyboard.modules.append(MouseKeys())
keyboard.extensions.append(MediaKeys())


# Enable debugging: http://kmkfw.io/docs/debugging/
keyboard.debug_enabled = True

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
        KC.S,   KC.A,    KC.LCTL(KC.SPC),    KC.D,    KC.SPC,    KC.T,            KC.H,   KC.J,    KC.K,    KC.L,    KC.SCLN,    KC.QUOT,
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
