# SPDX-FileCopyrightText: 2021 Phillip Burgess for Adafruit Industries
#
# SPDX-License-Identifier: MIT

"""
A macro/hotkey program for Adafruit MACROPAD. Macro setups are stored in the
/macros folder (configurable below), load up just the ones you're likely to
use. Plug into computer's USB port, use dial to select an application macro
set, press MACROPAD keys to send key sequences and other USB protocols.
"""

# pylint: disable=import-error, unused-import, too-few-public-methods

import os
import time
import displayio # type: ignore
import terminalio
from adafruit_display_shapes.rect import Rect
from adafruit_display_text import label
from adafruit_macropad import MacroPad
from adafruit_hid.keycode import Keycode
from app import App

# CONFIGURABLES ------------------------

MACRO_FOLDER = '/macros'

# INITIALIZATION -----------------------

macropad = MacroPad()
macropad.display.auto_refresh = False
macropad.pixels.auto_write = False
last_letter_key = None
last_letter_index = -1


# Set up displayio group with all the labels
group = displayio.Group()
for key_index in range(12):
    x = key_index % 3
    y = key_index // 3
    group.append(label.Label(terminalio.FONT, text='', color=0xFFFFFF,
                             anchored_position=((macropad.display.width - 1) * x / 2,
                                                macropad.display.height - 1 -
                                                (3 - y) * 12),
                             anchor_point=(x / 2, 1.0)))
rect = Rect(0, 0, macropad.display.width, 13, fill=0xFFFFFF)
group.append(rect)
group.append(label.Label(terminalio.FONT, text='', color=0x000000,
                         anchored_position=(macropad.display.width//2, 0),
                         anchor_point=(0.5, 0.0)))
macropad.display.root_group = group

# Load all the macro key setups from .py files in MACRO_FOLDER
apps = []
files = os.listdir(MACRO_FOLDER)
files.sort()
for filename in files:
    if filename.endswith('.py') and not filename.startswith('._'):
        try:
            module = __import__(MACRO_FOLDER + '/' + filename[:-3])
            apps.append(App(module.app, macropad, rect))
        except (SyntaxError, ImportError, AttributeError, KeyError, NameError,
                IndexError, TypeError) as err:
            print("ERROR in", filename)
            import traceback
            traceback.print_exception(err, err, err.__traceback__)

last_position = None
last_encoder_switch = macropad.encoder_switch_debounced.pressed
app_index = 0
apps[app_index].switch()


# MAIN LOOP ----------------------------

while True:
    # Read encoder position. If it's changed, switch apps.
    position = macropad.encoder

    if position != last_position:
        app_index = position % len(apps)
        apps[app_index].switch()
        last_position = position
        last_letter_key = None
        last_letter_index = -1

    # Handle encoder button. If state has changed, and if there's a
    # corresponding macro, set up variables to act on this just like
    # the keypad keys, as if it were a 13th key/macro.
    macropad.encoder_switch_debounced.update()
    encoder_switch = macropad.encoder_switch_debounced.pressed
    if encoder_switch != last_encoder_switch:
        last_encoder_switch = encoder_switch
        if len(apps[app_index].macros) < 13:
            continue    # No 13th macro, just resume main loop
        key_number = 12 # else process below as 13th macro
        pressed = encoder_switch
    else:
        event = macropad.keys.events.get()
        if not event or event.key_number >= len(apps[app_index].macros):
            continue # No key events, or no corresponding macro, resume loop
        key_number = event.key_number
        pressed = event.pressed

    # If code reaches here, a key or the encoder button WAS pressed/released
    # and there IS a corresponding macro available for it...other situations
    # are avoided by 'continue' statements above which resume the loop.

    sequence = apps[app_index].macros[key_number][2]

    keypad_dict = apps[app_index].dict

    if pressed:
        # 'sequence' is an arbitrary-length list, each item is one of:
        # Positive integer (e.g. Keycode.KEYPAD_MINUS): key pressed
        # Negative integer: (absolute value) key released
        # Float (e.g. 0.25): delay in seconds
        # String (e.g. "Foo"): corresponding keys pressed & released
        # List []: one or more Consumer Control codes (can also do float delay)
        # Dict {}: mouse buttons/motion (might extend in future)
        if key_number < 12: # No pixel for encoder button
            macropad.pixels[key_number] = 0xFFFFFF
            macropad.pixels.show()
        for item in sequence:
            if isinstance(item, int):
                if item >= 0:
                    macropad.keyboard.press(item)
                    if apps[app_index].name == 'Keypad':
                        last_letter_key = None
                        last_letter_index = -1
                else:
                    macropad.keyboard.release(-item)
            elif isinstance(item, float):
                time.sleep(item)
            elif isinstance(item, str):
                if apps[app_index].name == 'Keypad':
                    if item == '*':
                        last_letter_key = None
                        last_letter_index = -1
                    elif last_letter_key == None:
                        last_letter_key = item
                        last_letter_index = 0
                        macropad.keyboard_layout.write(keypad_dict[item][last_letter_index])
                    else:
                        if item == last_letter_key:
                            last_letter_index = (last_letter_index + 1) % len(keypad_dict[item])
                            macropad.keyboard.press(Keycode.BACKSPACE)
                            macropad.keyboard_layout.write(keypad_dict[item][last_letter_index])
                        else:
                            last_letter_key = item
                            last_letter_index = 0
                            macropad.keyboard_layout.write(keypad_dict[item][last_letter_index])
                else:
                    macropad.keyboard_layout.write(item)
            elif isinstance(item, list):
                for code in item:
                    if isinstance(code, int):
                        macropad.consumer_control.release()
                        macropad.consumer_control.press(code)
                    if isinstance(code, float):
                        time.sleep(code)
            elif isinstance(item, dict):
                if 'buttons' in item:
                    if item['buttons'] >= 0:
                        macropad.mouse.press(item['buttons'])
                    else:
                        macropad.mouse.release(-item['buttons'])
                macropad.mouse.move(item['x'] if 'x' in item else 0,
                                    item['y'] if 'y' in item else 0,
                                    item['wheel'] if 'wheel' in item else 0)
                if 'tone' in item:
                    if item['tone'] > 0:
                        macropad.stop_tone()
                        macropad.start_tone(item['tone'])
                    else:
                        macropad.stop_tone()
                elif 'play' in item:
                    macropad.play_file(item['play'])
    else:
        # Release any still-pressed keys, consumer codes, mouse buttons
        # Keys and mouse buttons are individually released this way (rather
        # than release_all()) because pad supports multi-key rollover, e.g.
        # could have a meta key or right-mouse held down by one macro and
        # press/release keys/buttons with others. Navigate popups, etc.
        for item in sequence:
            if isinstance(item, int):
                if item >= 0:
                    macropad.keyboard.release(item)
            elif isinstance(item, dict):
                if 'buttons' in item:
                    if item['buttons'] >= 0:
                        macropad.mouse.release(item['buttons'])
                elif 'tone' in item:
                    macropad.stop_tone()
        macropad.consumer_control.release()
        if key_number < 12: # No pixel for encoder button
            macropad.pixels[key_number] = apps[app_index].macros[key_number][0]
            macropad.pixels.show()
