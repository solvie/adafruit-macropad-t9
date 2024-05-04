import time
from app import App

class StatelessApp(App):
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
                else:
                    self.macropad.keyboard.release(-item)
            elif isinstance(item, float):
                time.sleep(item)
            elif isinstance(item, str):
                self.macropad.keyboard_layout.write(item)
            elif isinstance(item, list):
                for code in item:
                    if isinstance(code, int):
                        self.macropad.consumer_control.release()
                        self.macropad.consumer_control.press(code)
                    if isinstance(code, float):
                        time.sleep(code)