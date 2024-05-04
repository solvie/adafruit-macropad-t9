from adafruit_hid.keycode import Keycode
import colors

app = {
    'name' : 'Keypad', 
    'macros' : [
        # COLOR    LABEL    KEY SEQUENCE
        # 1st row ----------
        (colors.CYAN, '<-', [Keycode.BACKSPACE]),
        (colors.BLUE, 'abc', ['2']),
        (colors.BLUE, 'def', ['3']),
        # 2nd row ----------
        (colors.BLUE, 'ghi', ['4']),
        (colors.BLUE, 'jkl', ['5']),
        (colors.BLUE, 'mno', ['6']),
        # 3rd row ----------
        (colors.BLUE, 'pqrs', ['7']),
        (colors.BLUE, 'tuv', ['8']),
        (colors.BLUE, 'wxyz', ['9']),
        # 4th row ----------
        (colors.PINK, '[ESC]', ['*']), # escape char - moves onto the next letter
        (colors.RED, '_', [Keycode.SPACE]),
        (colors.GREEN, '[ENT]', [Keycode.ENTER]),
        # Encoder button ---
        (0x000000, '', [Keycode.BACKSPACE])
    ],
    'dict' : {
        '2' : ['a', 'b', 'c'],
        '3' : ['d', 'e', 'f'],
        '4' : ['g', 'h', 'i'],
        '5' : ['j', 'k', 'l'],
        '6' : ['m', 'n', 'o'],
        '7' : ['p', 'q', 'r', 's'],
        '8' : ['t', 'u', 'v'],
        '9' : ['w', 'x', 'y', 'z'],
    },
    'type' : 'stateful',
}
