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

        map_data_default = kwargs.get("map_data_default", mf.map_data_zero)

        if type(map_data_default) is str:  # BUG: here
            ground = map_data_default
            map_data_default = mf.map_data

            for row_nb, row in enumerate(map_data_default):
                for col_nb, tile in enumerate(row):
                    if map_data_default[row_nb][col_nb] == 1:
                        map_data_default[row_nb][col_nb] = ground

        self.map_data = kwargs.get("map_data", map_data_default)

        for row_nb, row in enumerate(self.map_data):
            for col_nb, tile in enumerate(row):
                if self.map_data[row_nb][col_nb] == 0:
                    self.map_data[row_nb][col_nb] = map_data_default[row_nb][col_nb]

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
        self.map_info["sprites"] = pg.sprite.RenderPlain()  # OPTIMIZE: temporary for dev

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

        self.map_info["npc"] = npc

    def add_npc(self, npc):
        self.map_info["npc"].add(npc)

    def add_ground(self, name, cell, **kwargs):
        ground = self.Game.ground_dict[str(name)]
        ground.rect.center = fp.cell_to_pos(cell)
        self.map_data[cell[0]][cell[1]] = str(name)  # OPTIMIZE: temp for dev

        walkable = kwargs.get("walkable", ground.walkable)
        # BUG: keep in memory previous cell walkable variable when changing map
        if self.cell_data[cell[0]][cell[1]] in (0, 1):
            self.cell_data[cell[0]][cell[1]] = int(walkable)  # OPTIMIZE: had bug here because if "b" -> change to 1 and bug cell
        # TODO: remove borders if water on it (need to acces cell and not just cell_data)
        self.map_info["background"].image.blit(ground.image, ground.rect)

    def add_prop(self, name, cell, *args, **kwargs):
        prop = prop_dict[str(name)]
        self.list_refresh.append(prop(self, cell, *args, **kwargs))

    def refresh(self):
        [cells_dict, borders_left, borders_top, borders_right, borders_bottom,
         borders] = self.Maps.map_reset_cells(cell_data=self.cell_data)

        # for cell in borders_bottom.values():
        #     print("avant", cell.active)
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

        # for cell in borders_bottom.values():
        #     print("apres", cell.active)