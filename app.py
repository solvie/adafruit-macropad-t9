class App:
    """ Class representing a host-side application """
    def __init__(self, appdata, macropad, rect):
        self.name = appdata['name']
        self.macros = appdata['macros']
        self.macropad = macropad
        self.rect = rect

    def switch(self):
        """ Activate application settings; update OLED labels and LED
            colors. """
        group = self.macropad.display.root_group
        group[13].text = self.name   # Application name
        if self.name:
            self.rect.fill = 0xFFFFFF
        else: # empty app name indicates blank screen for which we dimm header
            self.rect.fill = 0x000000
        for i in range(12):
            if i < len(self.macros): # Key in use, set label + LED color
                self.macropad.pixels[i] = self.macros[i][0]
                group[i].text = self.macros[i][1]
            else:  # Key not in use, no label or LED
                self.macropad.pixels[i] = 0
                group[i].text = ''
        self.macropad.keyboard.release_all()
        self.macropad.consumer_control.release()
        self.macropad.mouse.release_all()
        self.macropad.stop_tone()
        self.macropad.pixels.show()
        self.macropad.display.refresh()

    def release(self, key_number):
        # Release any still-pressed keys, consumer codes, mouse buttons
        # Keys and mouse buttons are individually released this way (rather
        # than release_all()) because pad supports multi-key rollover, e.g.
        # could have a meta key or right-mouse held down by one macro and
        # press/release keys/buttons with others. Navigate popups, etc.
        sequence = self.macros[key_number][2]
        for item in sequence:
            if isinstance(item, int):
                if item >= 0:
                    self.macropad.keyboard.release(item)
        self.macropad.consumer_control.release()
        if key_number < 12: # No pixel for encoder button
            self.macropad.pixels[key_number] = self.macros[key_number][0]
            self.macropad.pixels.show()
