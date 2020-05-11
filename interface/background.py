import pygame as pg

class BackGround():
    """image of the map"""
    def __init__(self, *args, size=(1, 1)):
        try:
            self.image, self.rect = load_image(*args)
        except Exception:
            self.image = pg.Surface(size)
            self.rect = self.image.get_rect()