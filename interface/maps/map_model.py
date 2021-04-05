# -*- coding: utf-8 -*-
"""
Created on Sat May 30 11:15:11 2020

@author: jonathan
"""
import os

import pygame as pg

from ..background import BackGround
from ..map_functions import MapFunctions
from ..findpath import FindPath
from ..props import Wall, Wall_right, Wall_left, Tree, Hole

fp = FindPath()
mf = MapFunctions()


class MapDefault:
    """Map model"""
    map_data = mf.map_data
    cell_data = mf.cell_data

    def __init__(self, Maps, Game, position, **kwargs):
        self.map_data = kwargs.get("map_data", mf.map_data)
        self.cell_data = kwargs.get("cell_data", mf.cell_data)
        self.borders = kwargs.get("borders", dict())
        # npc_list = kwargs.get("npc", list())

        self.Maps = Maps
        self.Game = Game
        self.position = position  # position of the map relative to all the maps

        self.map_info = dict()

        background = BackGround(size=Game.size)

        self.bg_sprites = pg.sprite.RenderPlain()
        sprites = pg.sprite.RenderPlain()
        npc = pg.sprite.RenderPlain()

        self.list_refresh = list()

        name = os.path.join(Game.data_dir, 'grass.png')
        grass = BackGround(name, -1)
        name = os.path.join(Game.data_dir, 'ground.png')
        ground = BackGround(name, -1)
        name = os.path.join(Game.data_dir, 'water.png')
        water = BackGround(name, -1)

        for row_nb, row in enumerate(self.map_data):
            for col_nb, tile in enumerate(row):

                if tile == 1:
                    position = fp.cell_to_pos((row_nb, col_nb))
                    grass.rect.center = position
                    background.image.blit(grass.image, grass.rect)

                elif tile == 2:
                    position = fp.cell_to_pos((row_nb, col_nb))
                    ground.rect.center = position
                    background.image.blit(ground.image, ground.rect)

                elif tile == 3:
                    position = fp.cell_to_pos((row_nb, col_nb))
                    water.rect.center = position
                    background.image.blit(water.image, water.rect)

                elif tile == 4:
                    self.list_refresh.append(Wall(self, (row_nb, col_nb)))

                elif tile == 5:
                    self.list_refresh.append(Wall_right(self, (row_nb, col_nb)))

                elif tile == 6:
                    self.list_refresh.append(Wall_left(self, (row_nb, col_nb)))

                elif tile == 7:
                    position = fp.cell_to_pos((row_nb, col_nb))
                    grass.rect.center = position
                    background.image.blit(grass.image, grass.rect)
                    self.list_refresh.append(Tree(self, (row_nb, col_nb)))

                elif tile == 8:
                    self.list_refresh.append(Hole(self, (row_nb, col_nb)))

        self.map_info["background"] = background

        self.map_info["sprites"] = sprites
        self.map_info["npc"] = npc

        Maps.all_maps[self.position] = self

        self.refresh()

    def refresh(self):
        [cells_dict, borders_left, borders_top,
         borders_right, borders_bottom, borders] = self.Maps.map_reset_cells(cell_data=self.cell_data)

        borders_choice = {"l":borders_left, "r":borders_right,
                          "t":borders_top, "b":borders_bottom}

        borders_choosen = dict()

        for choice in self.borders:
            borders_choosen.update(borders_choice.get(choice))

        self.map_info["background_sprites"] = self.bg_sprites
        self.map_info["cells"] = cells_dict

        self.map_info["borders"] = borders_choosen

        for sprite in self.list_refresh:
            sprite.refresh()
