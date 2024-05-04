class App:
    """ Class representing a host-side application, for which we have a set
        of macro sequences. Project code was originally more complex and
        this was helpful, but maybe it's excessive now?"""
    def __init__(self, appdata, macropad, rect):
        self.name = appdata['name']
        self.macros = appdata['macros']
        self.dict = appdata['dict']
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

    def doSomething(self):
        print('something')