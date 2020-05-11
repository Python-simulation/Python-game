import os
import time
import pygame as pg
from pygame.compat import geterror
import math
import numpy as np
from interface.interface_functions import NeededFunctions



class Button:
    """buttons"""
    def __init__(self, Game, function, name=""):
        self.Game = Game
        self.function = function
        nf= NeededFunctions()
        name=os.path.join(Game.data_dir, name)
        self.image, self.rect = nf.load_image(name)

        self.position = self.rect  # same id until clicked occured, then copy
        self.image_original = self.image

        self.state = False
        self.state_clicked = False

        self.highligh = pg.Surface(self.rect.size)
        self.highligh.fill((255, 255, 255))
        self.highligh.set_alpha(10)

    def add_text(self, text, center=None):
        font = pg.font.Font(None, 30)
        msg = font.render(text, 1, (10, 10, 10))

        if center is None:
            textpos = msg.get_rect(centery=self.rect.h/2,
                                   centerx=self.rect.w/2)
        else:
            textpos = msg.get_rect().center = center

        self.image.blit(msg, textpos)
        self.image_original = self.image

    def hovered(self):
        self.image_original = self.image.copy()
        self.image.blit(self.highligh, self.highligh.get_rect())
        pass

    def unhovered(self):
        self.image = self.image_original
#        self.image_original = self.image  # same id from now
        pass

    def clicked(self):
        if self.Game.mouse.state_clicking:
            self.state_clicked = True
            self.position = self.rect.copy()
#            self.image_original = self.image.copy()
#            self.rect.move_ip(1, 1)
            offset = 6
            self.image = pg.transform.scale(
                self.image, (self.rect.w - offset, self.rect.h - offset))
            self.rect.move_ip(offset/2, offset/2)
#            self.state = not self.state  " good for memory button

    def unclicked(self):
        self.state_clicked = False
        self.image = self.image_original
        self.rect = self.position

        self.position = self.rect  # same id from now
        self.image_original = self.image  # same id from now
        if self.Game.mouse.hovering(self):
            self.state = True
            self.function(self.state)
            # TODO: could be nice to have args and kwargs here
        else:
            self.state = False