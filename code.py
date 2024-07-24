
print("start")
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
print("testing123!")

# Key aliases
_______ = KC.TRNS
XXXXXXX = KC.NO

LOWER = KC.MO(1)
RAISE = KC.MO(2)
ADJUST = KC.LT(3, KC.SPC)

# Keymap
# fmt: off bvb
keyboard.keymap = [
    [  #QWERTY
        KC.LGUI,   KC.N1,   KC.LSFT,   KC.E,   XXXXXXX,   KC.N5,
        KC.X,    KC.Q,    XXXXXXX,    KC.N3,    KC.V,    KC.G,
        KC.S,   KC.A,    KC.KANA,    KC.D,    KC.SPC,    KC.T,
        KC.N2,   KC.LCTL,    KC.X,    KC.C,    KC.R,    KC.SPC,
        KC.Z,   KC.ESC,  KC.LALT, KC.F, KC.B, KC.N4, KC.W, XXXXXXX,

    ],
]
# fmt: on

if __name__ == "__main__":
    keyboard.go()
