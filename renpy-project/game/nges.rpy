
init python in nges:

    from store import config

    # Reduce the sound buffer, to drop latency.
    config.sound_buffer_size = 512

    import ctypes
    import os

    def load_libnges():
        """
        Loads the libnges library, and sets libnges to point to it.
        Raises an error if it can't be loaded for the platform.
        """

        global libnges

        libnges = None

        for i in renpy.list_files(""):

            if not i.startswith("libnges/libnges-"):
                continue

            try:
                libnges = ctypes.cdll[os.path.join(config.gamedir, i)]
                libnges.load_rom
                break
            except Exception as e:
                libnges = None

        if libnges is None:
            raise Exception("Could not load libnges.")

        renpy.audio.renpysound.set_generate_audio_c_function(libnges.audio);

        libnges.load_rom.argtypes = [ctypes.c_char_p, ctypes.c_int]
        libnges.load_rom.restype = ctypes.c_int

        libnges.step.argtypes = [ ]
        libnges.step.restype = None

        libnges.get_framebuffer.argtypes = [ ]
        libnges.get_framebuffer.restype = ctypes.POINTER(ctypes.c_ubyte)

        libnges.set_button.argtypes = [ctypes.c_int, ctypes.c_int, ctypes.c_int]
        libnges.set_button.restype = None

        libnges.init()

    load_libnges()

    class NGES(renpy.Displayable):

        def __init__(self, rom, **properties):
            renpy.Displayable.__init__(self, **properties)

            self.rom = rom

            self.make_event_map()

        def make_event_map(self):

            # The NES buttons.

            A      = 0x01
            B      = 0x02
            Select = 0x04
            Start  = 0x08
            Up     = 0x10
            Down   = 0x20
            Left   = 0x40
            Right  = 0x80

            # A map from Ren'Py event to NES event.
            self.event_map = { }

            # Keyboard events.
            def add(key, nes_key):
                self.event_map["keydown_" + key] = [ (nes_key, True) ]
                self.event_map["keyup_" + key] = [ (nes_key, False) ]

            add("K_z", A)
            add("K_x", B)
            add("K_RETURN", Start)
            add("K_RSHIFT", Select)
            add("K_UP", Up)
            add("K_DOWN", Down)
            add("K_LEFT", Left)
            add("K_RIGHT", Right)

            # Gamepad button events.
            def pad(key, nes_key):
                self.event_map["pad_" + key + "_press"] = [ (nes_key, True) ]
                self.event_map["pad_" + key + "_release"] = [ (nes_key, False) ]

            pad("a", A)
            pad("b", B)
            pad("start", Start)
            pad("select", Select)
            pad("dpup", Up)
            pad("dpdown", Down)
            pad("dpleft", Left)
            pad("dpright", Right)

            # Gamepad axis events.
            def axis(key, neg_key, pos_key):
                self.event_map["pad_" + key + "_neg"] = [ (neg_key, True), (pos_key, False) ]
                self.event_map["pad_" + key + "_zero"] = [ (neg_key, False), (pos_key, False) ]
                self.event_map["pad_" + key + "_pos"] = [ (neg_key, False), (pos_key, True) ]

            axis("leftx", Left, Right)
            axis("lefty", Up, Down)
            axis("rightx", Left, Right)
            axis("righty", Up, Down)

        # The filename of the current rom.
        current_rom = None

        def load_rom(self):
            """
            Loads the given rom.
            """

            if NGES.current_rom == self.rom:
                return

            NGES.current_rom = self.rom

            print("Loading rom", self.rom)

            with renpy.open_file(self.rom) as f:
                rom = f.read()
                if libnges.load_rom(rom, len(rom)):
                    raise Exception("Could not load rom.")

        def render(self, width, height, st, at):

            self.load_rom()

            # Step the emulator.
            libnges.step()

            # Get the framebuffer.
            rgba = ctypes.string_at(libnges.get_framebuffer(), 256 * 240 * 4)
            tex = renpy.load_rgba(rgba, (256, 240))

            # Render the framebuffer.
            rv = renpy.display.render.Render(256, 240)
            rv.blit(tex, (0, 0))

            # Redraw.
            renpy.redraw(self, 0)

            return rv

        def event(self, ev, x, y, st):

            matched = False

            for k, v in self.event_map.items():
                if renpy.map_event(ev, k):

                    for button, state in v:
                        libnges.set_button(1, button, state)

                    matched = True

            if matched:
                raise renpy.IgnoreEvent()
