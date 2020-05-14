import os
import pygame as pg
import numpy as np
from .interface_functions import NeededFunctions
from .display import display_info

nf = NeededFunctions()


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
        self.road = list()
        self.show_path = True

        # text = str("Display path")
        # txt_position = self.Game.mouse.rect.center
        # self.message = display_info(self.Game, text, txt_position)

    def update(self, dt):
        """by default, if function returns nothing, consider
        the cell has done its purpuse and set state to False"""
        if self.function is not None and self.state:
            output = self.function(*self.args, **self.kwargs)

            if output is None:
                self.state = False

    def hovered(self, *args):
        if self.show_path:
            self.image.set_alpha(self.alpha_on)
            self.road = nf.find_path(self.Game.character.rect.midbottom,
                                     self.rect.center, self.rect.w,
                                     all_cells=self.Game.all_cells)
            for next_cell in self.road:
                unit_pos = (int((next_cell[0]-self.rect.w/2)/self.rect.w),
                            int((next_cell[1]-self.rect.w/2)/self.rect.w))
                try:
                    self.Game.allsprites.add(self.Game.cells[unit_pos])
                except KeyError:
                    pass
            # self.message.hovered()
            pass

    def unhovered(self, *args):
        if self.show_path:
            self.image.set_alpha(self.alpha_off)
            for next_cell in self.road:
                unit_pos = (int((next_cell[0]-self.rect.w/2)/self.rect.w),
                            int((next_cell[1]-self.rect.w/2)/self.rect.w))
                try:
                    self.Game.allsprites.remove(self.Game.cells[unit_pos])
                except KeyError:
                    pass
            self.road = list()
            # self.message.unhovered()
            pass

    def clicked(self, *args, **kwargs):
        self.args = args
        self.kwargs = kwargs
        self.state = True

    def unclicked(self):
        self.state = False