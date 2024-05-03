from adafruit_hid.keycode import Keycode

app = {
    'name' : 'Keypad', 
    'macros' : [
        # COLOR    LABEL    KEY SEQUENCE
        # 1st row ----------
        (0x202000, '<-', [Keycode.BACKSPACE]),
        (0x202000, 'abc', ['2']),
        (0x202000, 'def', ['3']),
        # 2nd row ----------
        (0x202000, 'ghi', ['4']),
        (0x202000, 'jkl', ['5']),
        (0x202000, 'mno', ['6']),
        # 3rd row ----------
        (0x202000, 'pqrs', ['7']),
        (0x202000, 'tuv', ['8']),
        (0x202000, 'wxyz', ['9']),
        # 4th row ----------
        (0x101010, '[ESC]', ['*']), # escape char - moves onto the next letter
        (0x800000, '_', [Keycode.SPACE]),
        (0x101010, '[ENT]', [Keycode.ENTER]),
        # Encoder button ---
        (0x000000, '', [Keycode.BACKSPACE])
    ]
}
