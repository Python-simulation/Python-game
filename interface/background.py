import pygame as pg
from .interface_functions import NeededFunctions

nf = NeededFunctions()


class BackGround():
    """image of the map"""
    def __init__(self, *args, size=(1, 1)):
        try:
            self.image, self.rect = nf.load_image(*args)
        except Exception:
            self.image = pg.Surface(size)
            self.rect = self.image.get_rect()