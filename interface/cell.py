import os
import pygame as pg
import numpy as np
from .display import display_info
from .findpath import FindPath
from .interface_functions import NeededFunctions
fp = FindPath()
from .findpath import cell_size as cell_sizes

nf = NeededFunctions()


class Cell(pg.sprite.Sprite):
    """simple cell to target movement"""

    def __init__(self, Game, size, position, function=None):
        self.Game = Game
        self.function = function
        pg.sprite.Sprite.__init__(self)
        self.image = pg.Surface(size)

        name = os.path.join(Game.data_dir, 'grass.png')
        self.image, self.rect = nf.load_image(name, -1)
        self.rect = self.image.get_rect()
        self.rect.center = position
        # print(position)
#        self.position_label = None  # useless
        color = (50, 50, 50)
        self.alpha_off = 100 # temp
        self.alpha_on = 200
        # self.alpha_off = 10 # good
        # self.alpha_on = 50
        # self.image.fill(color)
        self.image.set_alpha(self.alpha_off)
        self.state = False
        self.road = list()
        self.show_path = True

        text = str("Display path")
        txt_position = self.Game.mouse.rect.center
        self.message = display_info(self.Game, text, txt_position)

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
                                     cardinal=self.Game.character.cardinal)  # only works for the player
            for next_cell in self.road:
                iso = (next_cell[0] - 7.5*cell_sizes[0],
                       next_cell[1] + 7.5*cell_sizes[1])
                cart = (iso[0]/2 + iso[1],
                        -iso[0]/2 + iso[1])
                row = (2*cart[0]/cell_sizes[0],
                       2*cart[1]/cell_sizes[0])
                unit_pos = (int(row[0]), int(row[1]))
                try:
                    self.Game.allsprites.add(self.Game.cells[unit_pos])
                    self.message.text = str(unit_pos)
                except KeyError:
                    self.message.text = ""
                    pass

            self.message.hovered()
            pass

    def unhovered(self, *args):
        if self.show_path:
            self.image.set_alpha(self.alpha_off)
            for next_cell in self.road:
                iso = (next_cell[0] - 7.5*cell_sizes[0],
                       next_cell[1] + 7.5*cell_sizes[1])
                cart = (iso[0]/2 + iso[1],
                        -iso[0]/2 + iso[1])
                row = (2*cart[0]/cell_sizes[0],
                       2*cart[1]/cell_sizes[0])
                unit_pos = (int(row[0]), int(row[1]))
                try:
                    self.Game.allsprites.remove(self.Game.cells[unit_pos])
                    # rect = self.Game.cells[unit_pos].rect
                    # self.Game.game_screen.image.blit(
                    #     self.Game.background_screen.image,
                    #     rect, rect)
                except KeyError:
                    pass
            self.road = list()
            self.message.unhovered()
            pass

    def clicked(self, *args, **kwargs):
        self.args = args
        self.kwargs = kwargs
        self.state = True

    def unclicked(self):
        self.state = False
