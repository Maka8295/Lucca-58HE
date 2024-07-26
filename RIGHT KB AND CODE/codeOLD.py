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
        KC.N6,   KC.N7,   KC.N8,   KC.N9,   KC.N0,   KC.DEL,
        KC.Y,    KC.U,    KC.I,    KC.O,    KC.P,    KC.EQL,
        KC.H,   KC.J,    KC.K,    KC.L,    KC.SCLN,    KC.QUOT,
        KC.KANA,  KC.N,  KC.M,  KC.COMM,  KC.DOT, KC.SLSH, KC.MINS,
        KC.ENT,   KC.BSPC,  KC.LBRC, KC.RBRC, XXXXXXX, XXXXXXX, XXXXXXX,
    ],
    [  #Layer 1
        KC.F6,   KC.F7,   KC.F8,   KC.F9,   KC.F10,   KC.F11,
        XXXXXXX,    XXXXXXX,    KC.UP,    XXXXXXX,    XXXXXXX,    KC.F12,
        KC.H,   KC.LEFT,    KC.DOWN,    KC.RIGHT,    XXXXXXX,    KC.PSCR,
        KC.MPLY,  KC.TILD,  KC.BSLS,  KC.PIPE,  XXXXXXX, KC.VOLD, KC.VOLU,
        KC.LCAP,   KC.MUTE,  KC.MPRV, KC.MNXT, XXXXXXX, XXXXXXX, XXXXXXX,
    ],
]
# fmt: on

if __name__ == "__main__":
    keyboard.go()
