import os
import time
import pygame as pg
from pygame.compat import geterror
import math
import numpy as np

class display_info(pg.sprite.Sprite):
    
    def __init__(self, Game, text, position):
        self.Game = Game
        self.text = text
        pg.sprite.Sprite.__init__(self)  # call Sprite intializer
#        font = pg.font.Font(None, 30)
#        self.image = font.render(self.text, 1, (10, 10, 10))
        self.rect = self.image.get_rect().center = position

    @property
    def text(self):
        return self._text

    @text.setter
    def text(self, value):
        self._text = value
        font = pg.font.Font(None, 30)
        self.image = font.render(self._text, 1, (10, 10, 10))

    def hovered(self):
        self.rect = self.Game.mouse.rect
        self.Game.allsprites.add(self)

    def unhovered(self):
        self.Game.allsprites.remove(self)