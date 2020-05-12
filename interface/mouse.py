import os
import time
import pygame as pg
from pygame.compat import geterror
import math
import numpy as np

class Mouse(pg.sprite.Sprite):
    """Position and surface of the mouse (can change the mouse image by
    removing the real mouse image and replacing by a defined one)"""

    def __init__(self, Game):
        self.Game = Game
        pg.sprite.Sprite.__init__(self)  # call Sprite initializer
#        self.image, self.rect = load_image("mouse.png")  # , -1)
        self.image = pg.Surface((1, 1))
        self.image.set_colorkey(0)
        self.rect = self.image.get_rect()
        self.state_clicking = False

    def update(self, dt):
        self.position()

    def position(self):
        """move the resized mouse based on the real mouse position"""
        diff_x = (self.Game.resized_screen.rect.w
                  - self.Game.app_screen_rect.w)/2
        diff_y = (self.Game.resized_screen.rect.h
                  - self.Game.app_screen_rect.h)/2

        ratio_x = (self.Game.game_screen.rect.w
                   / self.Game.resized_screen.rect.w)
        ratio_y = (self.Game.game_screen.rect.h
                   / self.Game.resized_screen.rect.h)

        pos = pg.mouse.get_pos()

        real_pos_x = (diff_x + pos[0]) * ratio_x
        real_pos_y = (diff_y + pos[1]) * ratio_y
        real_pos = real_pos_x, real_pos_y

        self.rect.center = real_pos

    def hovering(self, target):
        hitbox = self.rect
        return hitbox.colliderect(target.rect)

    def clicking(self, target):
        """returns true if the mouse collides with the target"""
        if self.hovering(target):
            self.state_clicking = True
            return True
        else:
            pass

    def unclicked(self):
        """called to pull the mouse back"""
        self.state_clicking = False
        self.Game.unclick()
