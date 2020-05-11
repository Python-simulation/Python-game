import os
import time
import pygame as pg
from pygame.compat import geterror
import math
import numpy as np
from .interface_functions import NeededFunctions


class Chimp(pg.sprite.Sprite):
    """moves a monkey critter across the screen. it can spin the
       monkey when it is clicked."""

    def __init__(self, Game):
        self.nf=NeededFunctions()
        self.Game = Game  # add real-time variable change from the Game class
        pg.sprite.Sprite.__init__(self)  # call Sprite intializer
        self.area = self.Game.game_screen.rect.copy()  # walkable space
        self.area.h -= self.Game.lower_tool_bar.rect.h - 19
        name=os.path.join(Game.data_dir,"chimp.png")
        self.image, self.rect = self.nf.load_image(name, colorkey=-1)
#        self.image = pg.transform.scale(self.image, (200, 100))
#        self.rect = self.image.get_rect()
        self.rect.topleft = 0, 100

        self.speed_x = 5/np.sqrt(2)
        self.speed_y = 5/np.sqrt(2)  # meter per second

        self.dizzy = 0
        self.angular_speed = 360  # degrees per second

    def update(self, dt):  # implicitly called from allsprite update
        """walk or spin, depending on the monkeys state"""
        if self.dizzy:
            self._spin(dt)
        else:
            self._walk(dt)

    def _walk(self, dt):
        """move the monkey across the screen, and turn at the ends"""

#        if not self.area.contains(newpos_x):  # could be useful but not here

        move_x = self.speed_x * self.Game.ratio_pix_meter_x * dt
        move_y = self.speed_y * self.Game.ratio_pix_meter_y * dt

        newpos = self.rect.move((move_x, move_y))

        if newpos.left < self.area.left or newpos.right > self.area.right:
            self.speed_x = -self.speed_x
            self.image = pg.transform.flip(self.image, 1, 0)  # temporaire

        if newpos.top < self.area.top or newpos.bottom > self.area.bottom:
            self.speed_y = -self.speed_y

        move_x = self.speed_x * self.Game.ratio_pix_meter_x * dt
        move_y = self.speed_y * self.Game.ratio_pix_meter_y * dt

        newpos = self.rect.move((move_x, move_y))
        self.rect = newpos

    def _spin(self, dt):
        """spin the monkey image"""
        center = self.rect.center
        self.dizzy = self.dizzy + self.angular_speed*dt
        if self.dizzy >= 360:
            self.dizzy = 0
            self.image = self.original
        else:
            rotate = pg.transform.rotate
            self.image = rotate(self.original, self.dizzy)
        self.rect = self.image.get_rect(center=center)

    def hovered(self):
        pass

    def unhovered(self):
        pass

    def clicked(self):
        """this will cause the monkey to start spinning"""
        if not self.dizzy:
            self.dizzy = 1
            self.original = self.image


#def speed_for_int_move(ratio_pix_meter_x, dt_fixed, max_speed):
#    """
#    self.max_speed_x = speed_for_int_move(
#        self.Game.ratio_pix_meter_x, self.Game.dt_fixed, self.max_speed)
#    """
#    allowed_speed = list()
#
#    for i in range(1, int(60/(ratio_pix_meter_x*dt_fixed))):
#        if 60 % i == 0:  # 60 from the cell size
#            allowed_speed.append(i/(ratio_pix_meter_x*dt_fixed))
#
#    allowed_speed = np.array(allowed_speed)
#    ind = abs(allowed_speed - max_speed).argmin()
#    print("all_speed", allowed_speed)
#
#    return allowed_speed[ind]