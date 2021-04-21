# -*- coding: utf-8 -*-
"""
Created on Sat May 30 11:15:11 2020

@author: jonathan
"""
import os

import pygame as pg

from .map_functions import MapFunctions
from ..background import BackGround
from ..findpath import FindPath
from ..props import prop_dict

fp = FindPath()


class MapDefault:
    """Map model"""

    def __init__(self, Maps, Game, position, **kwargs):
        mf = MapFunctions()  # only solution to have independent cell_data
        # not corrupted by other maps
        self.Maps = Maps
        self.Game = Game
        self.position = position  # pos of the map relative to all the maps
        Maps.all_maps[position] = self

        # warning: don't use Game.mf because id conflict that change cell
        self.map_data = kwargs.get("map_data", mf.map_data_zero)

        if self.map_data == "grass":
            self.map_data = mf.map_data

        self.cell_data = kwargs.get("cell_data", mf.cell_data_zero)

        if self.cell_data == "walk":
            self.cell_data = mf.cell_data

        self.borders = kwargs.get("borders", dict())
        image = kwargs.get("image", None)

        self.map_info = dict()
        self.list_refresh = list()
        self.bg_sprites = pg.sprite.RenderPlain()
        npc = pg.sprite.RenderPlain()

        if image is not None:
            background = BackGround(image)
            background.rect.center = Game.game_screen.rect.center
        else:
            background = BackGround(size=Game.size)

        self.map_info["background"] = background

        for row_nb, row in enumerate(self.map_data):
            for col_nb, tile in enumerate(row):
                cell = (row_nb, col_nb)

                # TODO: choose if keep number of switch to str
                try:
                    self.add_ground(tile, cell)
                except KeyError:

                    if tile == 1 or tile == "grass":
                        self.add_ground("grass", cell)

                    elif tile == 2 or tile == "ground":
                        self.add_ground("ground", cell)

                    elif tile == 3 or tile == "water":
                        self.add_ground("water", cell)

                # elif tile == 4:
                #     self.add_prop("wall", cell)

                # elif tile == 5:
                #     self.add_prop("wall_right_3", cell)

                # elif tile == 6:
                #     # self.list_refresh.append(Wall_left(self, cell))
                #     self.add_prop("wall_left_3", cell)

                # elif tile == 7:
                #     self.add_prop("tree", cell)

                # elif tile == 8:
                #     self.add_prop("hole", cell)

                # elif tile == 9:
                #     self.add_prop("wall_left_2", cell)

                # elif tile == 10:
                #     self.add_prop("wall_right_2", cell)

        self.map_info["npc"] = npc

    def add_npc(self, npc):
        self.map_info["npc"].add(npc)

    def add_ground(self, name, cell):
        ground = self.Game.ground_dict[str(name)]
        position = fp.cell_to_pos(cell)
        ground.rect.center = position
        self.map_data[cell[0]][cell[1]] = name
        # print(self.cell_data[cell[0]][cell[1]])
        self.cell_data[cell[0]][cell[1]] = 1
        # print(self.cell_data[cell[0]][cell[1]])
        self.map_info["background"].image.blit(ground.image, ground.rect)

    def add_prop(self, name, cell, *args, **kargs):
        prop = prop_dict[str(name)]
        self.list_refresh.append(prop(self, cell, *args, **kargs))

    def refresh(self):
        [cells_dict, borders_left, borders_top, borders_right, borders_bottom,
         borders] = self.Maps.map_reset_cells(cell_data=self.cell_data)

        borders_choice = {"l": borders_left, "r": borders_right,
                          "t": borders_top, "b": borders_bottom,
                          "a": borders}

        borders_choosen = dict()

        for choice in self.borders:
            borders_choosen.update(borders_choice.get(choice))

        self.map_info["background_sprites"] = self.bg_sprites
        self.map_info["cells"] = cells_dict

        self.map_info["borders"] = borders_choosen

        for sprite in self.list_refresh:
            sprite.refresh()
