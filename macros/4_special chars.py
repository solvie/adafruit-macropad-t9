from adafruit_hid.keycode import Keycode # REQUIRED if using Keycode.* values
import colors

app = {                # REQUIRED dict, must be named 'app'
    'name' : 'Special chars', # Application name
    'macros' : [       # List of button macros...
        # COLOR    LABEL    KEY SEQUENCE
        # 1st row ----------
        (colors.RED, '!', ['1']),
        (colors.GREEN, '@', ['2']),
        (colors.PINK, '#', ['3']),
        # 2nd row ----------
        (colors.CYAN, '$', ['4']),
        (colors.YELLOW, '%', ['5']),
        (colors.BLUE, '^', ['6']),
        # 3rd row ----------
        (colors.WHITE, '&', ['7']),
        (colors.BLUE, '*', ['8']),
        (colors.RED, '(', ['9']),
        # 4th row ----------
        (colors.GREEN, '-', ['*']),
        (colors.PINK, ')', ['0']),
        (colors.YELLOW, '+', ['#']),
        # Encoder button ---
        (0x000000, '', [Keycode.BACKSPACE])
    ],
    'type' : 'stateful',
    'dict' : { # TODO add more special characters
        '1' : ['!'],
        '2' : ['@'],
        '3' : ['#'],
        '4' : ['$'],
        '5' : ['%'],
        '6' : ['^'],
        '7' : ['&'],
        '8' : ['t'],
        '9' : ['('],
        '*' : ['-'],
        '0' : [')'],
        '#' : ['+']
    }}
