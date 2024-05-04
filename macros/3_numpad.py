# SPDX-FileCopyrightText: 2021 Emma Humphries for Adafruit Industries
#
# SPDX-License-Identifier: MIT

# MACROPAD Hotkeys example: Universal Numpad

from adafruit_hid.keycode import Keycode # REQUIRED if using Keycode.* values
import colors

app = {                # REQUIRED dict, must be named 'app'
    'name' : 'Numpad', # Application name
    'macros' : [       # List of button macros...
        # COLOR    LABEL    KEY SEQUENCE
        # 1st row ----------
        (colors.YELLOW, '1', ['1']),
        (colors.YELLOW, '2', ['2']),
        (colors.YELLOW, '3', ['3']),
        # 2nd row ----------
        (colors.YELLOW, '4', ['4']),
        (colors.YELLOW, '5', ['5']),
        (colors.YELLOW, '6', ['6']),
        # 3rd row ----------
        (colors.YELLOW, '7', ['7']),
        (colors.YELLOW, '8', ['8']),
        (colors.YELLOW, '9', ['9']),
        # 4th row ----------
        (colors.BLUE, '*', ['*']),
        (colors.YELLOW, '0', ['0']),
        (colors.RED, '#', ['#']),
        # Encoder button ---
        (0x000000, '', [Keycode.BACKSPACE])
    ],
    'type' : 'stateless',
}
