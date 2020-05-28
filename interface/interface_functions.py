import pygame as pg
from pygame.compat import geterror


class NeededFunctions:
    # functions to create our resources

    def load_image(self, name, colorkey=None):
        """Load images to the pygame variables space"""
        fullname = name

        try:
            image = pg.image.load(fullname)

        except pg.error:
            print("Cannot load image:", fullname)
            raise SystemExit(str(geterror()))

        image = image.convert()
        # image = image.convert_alpha()

        if colorkey is not None:

            if colorkey == -1:
                # (0, 0) ->take the first pixel of the image as reference for alpha
                colorkey = image.get_at((0, 0))

            # RLEACCEL make it faster to display
            image.set_colorkey(colorkey, pg.RLEACCEL)

        return image, image.get_rect()

    def load_sound(self, name):
        """Load sounds to the pygame variables space"""
        class NoneSound:
            def play(self):
                pass

        if not pg.mixer or not pg.mixer.get_init():
            return NoneSound()

        fullname = name

        try:
            sound = pg.mixer.Sound(fullname)

        except pg.error:
            print("Cannot load sound: %s" % fullname)
            raise SystemExit(str(geterror()))

        return sound

    def function_test(self, state):
        print("fct 1 do something with state", state)

    def function_test2(self, state):
        print("fct 2 do something with state", state)
