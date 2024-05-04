from adafruit_hid.keycode import Keycode
import colors

app = {
    'name' : 'Cursor', 
    'macros' : [
        # COLOR    LABEL    KEY SEQUENCE
        # 1st row ----------
        (colors.CYAN, '[BACKSP]', [Keycode.BACKSPACE]),
        (colors.BLUE, '^', [Keycode.UP_ARROW]),
        (colors.PINK, '', ['']),
        # 2nd row ----------
        (colors.BLUE, '<-', [Keycode.LEFT_ARROW ]),
        (colors.BLUE, 'v', [Keycode.DOWN_ARROW]),
        (colors.BLUE, '->', [Keycode.RIGHT_ARROW]),
        # 3rd row ----------
        (colors.PINK, '', ['']),
        (colors.PINK, '', ['']),
        (colors.PINK, '', ['']),
        # 4th row ----------
        (colors.PINK, '[ESC]', ['*']), # escape char - moves onto the next letter
        (colors.RED, '_', [Keycode.SPACE]),
        (colors.GREEN, '[ENT]', [Keycode.ENTER]),
        # Encoder button ---
        (0x000000, '', [Keycode.BACKSPACE])
    ],
    'type' : 'stateless',
}
