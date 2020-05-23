import os
import pygame as pg
from .interface_functions import NeededFunctions
from .background import BackGround
from .cell import Cell

class House(BackGround):
    """Create a house on the map"""

    def __init__(self, Game, background, topleft, cells, borders=dict()):
        BackGround.__init__(self)  # call Sprite intializer
        self.Game = Game
        self.nf = NeededFunctions()

        name = os.path.join(Game.data_dir, 'house.png')
        self.image, self.rect = self.nf.load_image(name, -1)

        self.rect.topleft = topleft

        self.background = background
        background.image.blit(self.image, self.rect)  # TODO: if want to have
        # the character to "vanish" being a building, must change this line

        self.forbidden_cells = [
            [4, 9],
            [5, 9],
            [2, 8],
            [3, 8],
            [4, 8],
            [5, 8],
            [6, 8],
            [0, 7],
            [1, 7],
            [2, 7],
            [3, 7],
            [4, 7],
            [5, 7],
            [6, 7],
            [8, 7],
            [9, 7],
            [2, 6],
            [3, 6],
            [4, 6],
            [5, 6],
            [6, 6],
            [7, 6],
            [4, 5],
            [5, 5],

            [7, 7],  # special one
            ]

        self.special_cell = [
            [7, 8],
            # [7, 7],  # TODO: must redirected to cell 7,8
            ]

        self.cell_size = 0

        for cell in cells.values():
            self.cell_size = cell.rect.w
            break

        for cell in self.forbidden_cells:  # WARNING: operations on cell change
            # the cell value in the forbidden_cells
            cell = self.add_init_pos(cell)
            # print(cell)
            cells.pop(cell, None)
            borders.pop(cell, None)  # warning, if house del border where char
            # came from, can't go back and can't move : stuck for ever
            # must del border in adjacent map to avoid it

        for cell in self.special_cell:
            cell = self.add_init_pos(cell)
            cells[cell].function = self.tp_house

        self.tp_cell_in = self.add_init_pos([7, 8])
        self.tp_cell_out = self.add_init_pos([7, 8])

        self.create_inside()

    def add_init_pos(self, cell):
        cell[0] += self.rect.topleft[0]/self.cell_size
        cell[1] += self.rect.topleft[1]/self.cell_size
        return (int(cell[0]), int(cell[1]))

    def tp_house(self, *args):
        new_map_pos = self.inside
        new_char_pos = (self.tp_cell_in[0]*self.cell_size + self.cell_size/2,
                        self.tp_cell_in[1]*self.cell_size + self.cell_size/2,)
        return self.Game.teleportation(new_map_pos, new_char_pos, *args)

    def tp_outside(self, *args):
        new_map_pos = self.outside
        new_char_pos = (self.tp_cell_out[0]*self.cell_size + self.cell_size/2,
                        self.tp_cell_out[1]*self.cell_size + self.cell_size/2,)
        return self.Game.teleportation(new_map_pos, new_char_pos, *args)

    def create_inside(self):
        # TODO: see if add black background to erase outside
        # or keep outside without sprites
        background = BackGround()
        background.image = self.background.image.copy()
        background.rect = background.image.get_rect()

        name = os.path.join(self.Game.data_dir, 'house_inside.png')
        image, rect = self.nf.load_image(name, -1)
        rect.topleft = self.rect.topleft

        background.image.blit(image, rect)

        inside_cells = self.add_cell(self.forbidden_cells)
        door = self.add_cell(self.special_cell)
        inside_cells.update(door)

        for cell in self.special_cell:
            cell = (int(cell[0]), int(cell[1]))
            inside_cells[cell].function = self.tp_outside

        table = [
            [3, 6],
            [4, 6],
            [5, 6],
            [4, 5],
            [5, 5],
            ]
        for cell in table:
            cell = self.add_init_pos(cell)
            # print(cell)
            inside_cells.pop(cell, None)

        self.inside = "first_house"
        self.outside = (0, 1)
        self.map = {"background": background,
                    "cells": inside_cells,
                    "borders": dict(),
                    "sprites": pg.sprite.RenderPlain(())}

    def add_cell(self, cell_list):
        cells_dict = dict()
        for cell in cell_list:
            x, y = cell
            current_cell = Cell(
                self.Game,
                size=(self.cell_size, self.cell_size),
                position=(x*self.cell_size+self.cell_size/2,
                          y*self.cell_size+self.cell_size/2),
                function=self.Game.character.dest
            )

            cells_dict[(x, y)] = current_cell

        return cells_dict
