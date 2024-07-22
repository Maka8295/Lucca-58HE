
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
        KC.ESC,   KC.N1,   KC.N2,   KC.N3,   KC.N4,   KC.N5,
        KC.TAB,    KC.Q,    KC.W,    KC.E,    KC.R,    KC.T,
        KC.LCTL,   KC.A,    KC.S,    KC.D,    KC.F,    KC.G,
        KC.LSFT,   KC.Z,    KC.X,    KC.C,    KC.V,    KC.B,
                                KC.LCTL,   KC.LGUI,  KC.LALT, KC.SPC,
    ],
]
# fmt: on

if __name__ == "__main__":
    keyboard.go()
