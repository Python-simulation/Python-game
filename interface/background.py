import pygame as pg
from .interface_functions import NeededFunctions

nf = NeededFunctions()


class BackGround(pg.sprite.Sprite):  # OPTIMIZE: don' like the try except ->
    # because if bad name in image name, will not return error but a 0x0 image
    """image of the map"""

    def __init__(self, *args, size=(0, 0), **kwargs):

        super().__init__()  # call Sprite intializer

        try:
            self.image, self.rect = nf.load_image(*args, **kwargs)
        except Exception:
            self.image = pg.Surface(size)
            self.image.convert()
            # self.image.set_colorkey(0)
            self.rect = self.image.get_rect()

    def hovered(self):
        pass

    def unhovered(self):
        pass

    def clicked(self):
        pass

    def unclicked(self):
        pass