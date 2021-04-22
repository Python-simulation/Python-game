import pygame as pg


class NeededFunctions:
    # functions to create our resources

    def load_image(self, name, colorkey=None, **kwargs):
        """Load images to the pygame variables space"""
        fullname = name

        image = pg.image.load(fullname)

        alpha = kwargs.get("alpha", False)

        if alpha:
            image = image.convert_alpha()
        else:
            image = image.convert()

        if colorkey is not None:

            if colorkey == -1:
                # (0, 0) ->take the first pixel of the image and remove all same pix from image
                colorkey = image.get_at((0, 0))
                # print(colorkey)  #  (0, 0, 0, 255) or (255, 255, 255, 255)

            # RLEACCEL make it faster to display
            image.set_colorkey(colorkey, pg.RLEACCEL)

        # image = image.convert_alpha()  # almost work for every sprite used
            # bug for cell but need to investigate benefice
        return image, image.get_rect()

    def load_sound(self, name):
        """Load sounds to the pygame variables space"""
        class NoneSound:
            def play(self):
                pass

        if not pg.mixer or not pg.mixer.get_init():
            return NoneSound()

        fullname = name

        sound = pg.mixer.Sound(fullname)

        return sound

    def function_test(self, state):
        print("fct 1 do something with state", state)

    def function_test2(self, state):
        print("fct 2 do something with state", state)
