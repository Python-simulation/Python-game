import os
import time
import pygame as pg
from pygame.compat import geterror
import math
import numpy as np


class Cell(pg.sprite.Sprite):
    """simple cell to target movement"""
    def __init__(self, Game, size, position, function=None):
        self.Game = Game
        self.function = function
        pg.sprite.Sprite.__init__(self)
        self.image = pg.Surface(size)
        self.rect = self.image.get_rect()
        self.rect.center = position
#        self.position_label = None  # useless
        color = (50, 50, 50)
        self.alpha_off = 10
        self.alpha_on = 50
        self.image.fill(color)
        self.image.set_alpha(self.alpha_off)
        self.state = False

#        text = str("test")
#        txt_position = self.Game.mouse.rect.center
#        self.message = display_info(self.Game, text, txt_position)

    def update(self, dt):
        """by default, if function returns nothing, consider
        the cell has done its purpuse and set state to False"""
        if self.function is not None and self.state:
            output = self.function(*self.args, **self.kwargs)

            if output is None:
                self.state = False

    def hovered(self, *args):
#        self.message.hovered()
        self.image.set_alpha(self.alpha_on)
        pass

    def unhovered(self, *args):
#        self.message.unhovered()
        self.image.set_alpha(self.alpha_off)
        pass

    def clicked(self, *args, **kwargs):
        self.args = args
        self.kwargs = kwargs
        self.state = True

    def unclicked(self):
        self.state = False