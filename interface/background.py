import pygame as pg
from .interface_functions import NeededFunctions

nf = NeededFunctions()


class BackGround(pg.sprite.Sprite):
    """image of the map"""
    def __init__(self, *args, size=(1, 1)):
        pg.sprite.Sprite.__init__(self)  # call Sprite intializer
        try:
            self.image, self.rect = nf.load_image(*args)
        except Exception:
            self.image = pg.Surface(size)
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