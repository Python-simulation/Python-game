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
        self.cell_pos = fp.pos_to_cell(position)

        # text = "Display path"
        # txt_position = self.Game.mouse.rect.topleft
        # self.message = display_info(self.Game, text, txt_position)

        self.reset()
        self.function = function

    def reset(self):
        self.function = None
        # color = (50, 50, 50)
        self.alpha_off = 0  # error if != 0 and change map
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

    def check_real_pos(self, redirection, *args, **kwargs):

        other_cell = False

        # if not self.Game._anti_recursion:
        #     self.Game._anti_recursion = True

        mouse_pos = self.Game.mouse.rect.topleft

        if mouse_pos[1] < self.rect.centery:
            if mouse_pos[0] > self.rect.centerx:
                (x1, y1) = (self.rect.midtop[0], self.rect.midtop[1])
                # print((x1, y1))
                y2 = y1 + (mouse_pos[0] - x1)/2
                # print(mouse_pos, y2)
                if mouse_pos[1] < y2:
                    shift = (0, -1)
                    # print("upright")
                    other_cell = True
                pass
            else:
                (x1, y1) = (self.rect.midtop[0], self.rect.midtop[1])
                # print((x1, y1))
                y2 = y1 + (x1 - mouse_pos[0])/2
                # print(mouse_pos[1], y2)
                if mouse_pos[1] < y2:
                    shift = (-1, 0)
                    # print("upleft")
                    other_cell = True
                pass

        else:
            if mouse_pos[0] > self.rect.centerx:
                (x1, y1) = (self.rect.right, self.rect.center[1])
                # print((x1, y1))
                y2 = y1 + (x1 - mouse_pos[0])/2
                # print(mouse_pos, y2)
                if mouse_pos[1] > y2:
                    shift = (1, 0)
                    # print("bottomright")
                    other_cell = True
                pass
            else:
                (x1, y1) = (self.rect.left, self.rect.center[1])
                # print((x1, y1))
                y2 = y1 + (mouse_pos[0] - x1)/2
                # print(mouse_pos[1], y2)
                if mouse_pos[1] > y2:
                    shift = (0, 1)
                    # print("bottomleft")
                    other_cell = True
                pass

        if other_cell:
            # print("yes", shift)
            real_cell = (self.cell_pos[0] + shift[0],
                         self.cell_pos[1] + shift[1])

            if redirection == "hovered":
                try:
                    # print(self.rect.center, self.Game.all_cells[real_cell].rect.center)
                    self.Game.all_cells[real_cell].hovered(*args)
                except KeyError:
                    pass
            elif redirection == "clicked":
                try:
                    self.Game.all_cells[real_cell].clicked(*args, **kwargs)
                except KeyError:
                    pass

            # self.Game._anti_recursion = False

        return other_cell

    def update(self, dt):
        """by default, if function returns nothing, consider
        the cell has done its purpuse and set state to False"""
        if self.function is not None and self.state:
            output = self.function(*self.args, **self.kwargs)

            if output is None:
                self.state = False

    def hovered(self, *args):

        if not self.check_real_pos("hovered", *args) and self.show_path:
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
        if not self.check_real_pos("clicked", *args, **kwargs):
            self.args = args
            self.kwargs = kwargs
            self.state = True

    def unclicked(self):
        self.state = False
