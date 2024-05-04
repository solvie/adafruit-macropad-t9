import time
from adafruit_hid.keycode import Keycode
from app import App

class StatefulApp(App):
    def __init__(self, appdata, macropad, rect):
        super().__init__(appdata, macropad, rect)
        self.dict = appdata['dict']
        self.last_letter_key = None
        self.last_letter_index = -1
    
    def switch(self):
        super().switch()
        self.last_letter_key = None
        self.last_letter_index = -1

    def handleKeypress(self, key_number): 
        sequence = self.macros[key_number][2]
        # 'sequence' is an arbitrary-length list, each item is one of:
        # Positive integer (e.g. Keycode.KEYPAD_MINUS): key pressed
        # Negative integer: (absolute value) key released
        # Float (e.g. 0.25): delay in seconds
        # String (e.g. "Foo"): corresponding keys pressed & released
        # List []: one or more Consumer Control codes (can also do float delay)
        if key_number < 12: # No pixel for encoder button
            self.macropad.pixels[key_number] = 0xFFFFFF
            self.macropad.pixels.show()
        for item in sequence:
            if isinstance(item, int):
                if item >= 0:
                    self.macropad.keyboard.press(item)
                    self.last_letter_key = None
                    self.last_letter_index = -1
                else:
                    self.macropad.keyboard.release(-item)
            elif isinstance(item, float):
                time.sleep(item)
            elif isinstance(item, str):
                if item == '*':
                    self.last_letter_key = None
                    self.last_letter_index = -1
                elif self.last_letter_key == None:
                    self.last_letter_key = item
                    self.last_letter_index = 0
                    self.macropad.keyboard_layout.write(self.dict[item][self.last_letter_index])
                else:
                    if item == self.last_letter_key:
                        self.last_letter_index = (self.last_letter_index + 1) % len(self.dict[item])
                        self.macropad.keyboard.press(Keycode.BACKSPACE)
                        self.macropad.keyboard_layout.write(self.dict[item][self.last_letter_index])
                    else:
                        self.last_letter_key = item
                        self.last_letter_index = 0
                        self.macropad.keyboard_layout.write(self.dict[item][self.last_letter_index])
            elif isinstance(item, list):
                for code in item:
                    if isinstance(code, int):
                        self.macropad.consumer_control.release()
                        self.macropad.consumer_control.press(code)
                    if isinstance(code, float):
                        time.sleep(code)