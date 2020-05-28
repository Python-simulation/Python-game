import os
import pygame as pg
from .interface_functions import NeededFunctions
from .background import BackGround
from .cell import Cell
from .findpath import cell_size as cell_sizes

nf = NeededFunctions()


class House(BackGround):
    """Create a house on the map"""

    def __init__(self, Game, background, topleft, cells, borders=dict()):
        BackGround.__init__(self)  # call Sprite intializer
        self.Game = Game

        name = os.path.join(Game.data_dir, 'house.png')
        self.image, self.rect = nf.load_image(name, -1)

        self.rect.topleft = topleft

        self.background = background
        background.image.blit(self.image, self.rect)  # TODO: if want to have
        # the character to "vanish" being a building, must change this line

        self.forbidden_cells = [
            [8, 3],  # generalized using object dimensions on ground
            [8, 4],
            [8, 5],
            [8, 6],
            [8, 7],
            [9, 3],
            [9, 4],
            [9, 5],
            [9, 6],
            [9, 7],
            [10, 3],
            [10, 4],
            [10, 5],
            [10, 6],
            [10, 7],
            [11, 3],
            [11, 4],
            [11, 5],
            [11, 6],
            [11, 7],
            [12, 3],
            [12, 4],
            # [12, 5],  #╚ generalized using special_cell
            [12, 6],
            [12, 7],
            ]

        self.special_cell = [
            [12, 5],
            # [13, 5],  # TODO: must redirected to cell 12,5
            ]

        for cell in self.forbidden_cells:  # WARNING: operations on cell change
            # the cell value in the forbidden_cells
            cell = self.add_init_pos(cell)
            # print("remove", cell)
            # print(cell)
            cells.pop(cell, None)
            borders.pop(cell, None)  # warning, if house del border where char
            # came from, can't go back and can't move : stuck for ever
            # must del border in adjacent map to avoid it

        for cell in self.special_cell:
            cell = self.add_init_pos(cell)
            cells[cell].function = self.tp_house

        self.tp_cell_in = self.special_cell[0]
        self.tp_cell_out = self.add_init_pos([13, 5])

        self.create_inside()

    def add_init_pos(self, cell):
        iso = (self.rect.topleft[0] - 7.5*cell_sizes[0],
               self.rect.topleft[1] + 7.5*cell_sizes[1])
        cart = (iso[0]/2 + iso[1],
                -iso[0]/2 + iso[1])
        row = (2*cart[0]/cell_sizes[0],
               2*cart[1]/cell_sizes[0])
        init_pos = (int(row[0]), int(row[1]))

        cell[0] += init_pos[0]
        cell[1] += init_pos[1]

        unit_pos = (int(cell[0]), int(cell[1]))
        return unit_pos

    def tp_house(self, *args):
        new_map_pos = self.inside

        cart_x = self.tp_cell_in[0] * cell_sizes[0]/2
        cart_y = self.tp_cell_in[1] * cell_sizes[0]/2  # x not a mistake
        iso_x = (cart_x - cart_y)
        iso_y = (cart_x + cart_y)/2

        new_char_pos = (iso_x + 7.5*cell_sizes[0],
                        iso_y - 7.5*cell_sizes[1])

        return self.Game.teleportation(new_map_pos, new_char_pos, *args)

    def tp_outside(self, *args):
        new_map_pos = self.outside
        cart_x = self.tp_cell_out[0] * cell_sizes[0]/2
        cart_y = self.tp_cell_out[1] * cell_sizes[0]/2  # x not a mistake
        iso_x = (cart_x - cart_y)
        iso_y = (cart_x + cart_y)/2

        new_char_pos = (iso_x + 7.5*cell_sizes[0],
                        iso_y - 7.5*cell_sizes[1])
        return self.Game.teleportation(new_map_pos, new_char_pos, *args)

    def create_inside(self):
        # TODO: see if add black background to erase outside
        # or keep outside without sprites
        background = BackGround()
        background.image = self.background.image.copy()
        background.rect = background.image.get_rect()

        name = os.path.join(self.Game.data_dir, 'house_inside.png')
        image, rect = nf.load_image(name, -1)
        rect.topleft = self.rect.topleft

        background.image.blit(image, rect)

        inside_cells = self.add_cell(self.forbidden_cells)
        door = self.add_cell(self.special_cell)
        inside_cells.update(door)

        for cell in self.special_cell:
            cell = (int(cell[0]), int(cell[1]))
            inside_cells[cell].function = self.tp_outside

        table = [
            [9, 4],
            [9, 5],
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
            cart_x = cell[0] * cell_sizes[0]/2
            cart_y = cell[1] * cell_sizes[0]/2  # x not a mistake
            iso_x = (cart_x - cart_y)
            iso_y = (cart_x + cart_y)/2

            new_pos = (iso_x + 7.5*cell_sizes[0],
                       iso_y - 7.5*cell_sizes[1])

            current_cell = Cell(
                self.Game,
                size=(cell_sizes[0], cell_sizes[1]),
                position=(new_pos[0],
                          new_pos[1]),
                function=self.Game.character.dest
            )

            cells_dict[(x, y)] = current_cell

        return cells_dict
