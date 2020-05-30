import os
import pygame as pg
import numpy as np
from .display import display_info
from .interface_functions import NeededFunctions
from .findpath import FindPath
from .findpath import cell_sizes

nf = NeededFunctions()
fp = FindPath()

import time
class Cell(pg.sprite.Sprite):
    """simple cell to target movement"""

    def __init__(self, Game, size, position, function=None):
        self.Game = Game
        pg.sprite.Sprite.__init__(self)
        # self.image = pg.Surface(size)

        name = os.path.join(Game.data_dir, 'grass.png')
        self.image, self.rect = nf.load_image(name, -1)
        self.rect = self.image.get_rect()
        self.rect.center = position

        # text = "Display path"
        # txt_position = self.Game.mouse.rect.center
        # self.message = display_info(self.Game, text, txt_position)

        self.reset()
        self.function = function

    def reset(self):
        self.function = None
        # color = (50, 50, 50)
        self.alpha_off = 100  # temp
        self.alpha_on = 200
        # self.alpha_off = 10 # good
        # self.alpha_on = 50
        # self.image.fill(color)
        self.image.set_alpha(self.alpha_off)
        self.state = False
        self.road = list()
        self.show_path = True
        # self.message.text("reset")
        self.Game.allsprites.remove(self)  # BUG: if want to see, can be proble

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
            self.road = fp.find_path(self.Game.character.rect.midbottom,
                                     self.rect.center,
                                     all_cells=self.Game.all_cells,
                                     cardinal=self.Game.character.cardinal)

            for next_cell in self.road:
                unit_pos = fp.pos_to_cell(next_cell)

                try:
                    self.Game.allsprites.add(self.Game.cells[unit_pos])
                    # self.message.text(str(unit_pos))
                except KeyError:
                    # self.message.text("")
                    pass

            # self.message.hovered()
            pass

    def unhovered(self, *args):

        if self.show_path:
            self.image.set_alpha(self.alpha_off)

            for next_cell in self.road:
                unit_pos = fp.pos_to_cell(next_cell)

                try:
                    self.Game.allsprites.remove(self.Game.cells[unit_pos])
                    # rect = self.Game.cells[unit_pos].rect
                    # self.Game.game_screen.image.blit(
                    #     self.Game.background_screen.image,
                    #     rect, rect)
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
