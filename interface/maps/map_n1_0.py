# -*- coding: utf-8 -*-
"""
Created on Sat May 30 11:15:11 2020

@author: jonathan
"""
import os

import pygame as pg

from ..background import BackGround
from ..findpath import cell_sizes
from ..map_functions import MapFunctions
from ..findpath import FindPath
from ..props import Wall, Wall_right, Wall_left, Tree, Hole
from ..npc.npc import Npc

fp = FindPath()
mf = MapFunctions()

map_data = [
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 1],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
    [0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 8, 1, 1, 1, 1, 1, 1, 1],
    [0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
    [0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 2],
    [0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 2, 2, 2, 2, 2, 1, 1, 1, 1, 1, 1, 1, 1, 1, 2, 1],
    [0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 2, 3, 3, 3, 2, 1, 1, 1, 1, 1, 1, 7, 1, 1, 2, 1, 1],
    [0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 2, 3, 2, 3, 2, 1, 1, 1, 1, 1, 1, 7, 1, 1, 2, 1, 1, 1],
    [0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 2, 3, 3, 3, 2, 1, 1, 1, 1, 1, 1, 1, 1, 1, 2, 1, 1, 1, 1],
    [0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 2, 2, 2, 2, 2, 1, 1, 1, 1, 1, 1, 1, 1, 1, 2, 1, 1, 1, 1, 1],
    [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 2, 1, 1, 1, 1, 1, 1],
    [0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 2, 1, 1, 1, 1, 1],
    [0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 2, 1, 1, 1, 1],
    [0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 7, 7, 7, 1, 1, 1, 1, 1, 1, 2, 1, 1, 1],
    [0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 6, 5, 1, 1, 4, 4, 4, 7, 2, 2, 2, 2, 2, 2, 2, 1, 1],
    [0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 4, 3, 2, 1, 2, 1, 1, 1, 1, 1, 1, 1],
    [0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 4, 2, 2, 1, 2, 1, 1, 1, 1, 1, 1],
    [0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 2, 1, 1, 1, 1, 1],
    [0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 2, 1, 1, 1, 1],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 2, 1, 1, 1],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 2, 1, 1],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 2, 1],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 2],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
        ]


class Map:  # TODO: create a super class with all the needed parameters by default

    def __init__(self, Maps, Game):
        self.Maps = Maps
        self.Game = Game
        self.position = (-1, 0)  # position of the map relative to all the maps

        self.map_info = dict()

        background = BackGround(size=Game.size)

        self.bg_sprites = pg.sprite.RenderPlain()

        self.list_refresh = list()

        name = os.path.join(Game.data_dir, 'grass.png')
        grass = BackGround(name, -1)
        name = os.path.join(Game.data_dir, 'ground.png')
        ground = BackGround(name, -1)
        name = os.path.join(Game.data_dir, 'water.png')
        water = BackGround(name, -1)

        for row_nb, row in enumerate(map_data):
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

        sprites = pg.sprite.RenderPlain()
        npc = pg.sprite.RenderPlain()

        file_name = os.path.join(Game.data_dir, "npc.png")
        npc_1 = Npc(Game, file_name, cell_pos=(15, 20))
        # position = fp.cell_to_pos((15, 20))
        # npc.rect.midbottom = (position[0], position[1] + cell_sizes[1]/2)
        npc_1.allowed_mvt(50, 1)
        npc_1.max_speed = 5
        npc_1.npc_time = 2
        npc.add(npc_1)

        self.map_info["sprites"] = sprites
        self.map_info["npc"] = npc

        position = (1*cell_sizes[0],
                    1*cell_sizes[1])

        Maps.all_maps[self.position] = self

        self.refresh()

    def refresh(self):
        [cells_dict, borders_left, borders_top,
         borders_right, borders_bottom, borders] = self.Maps.map_reset_cells()

        self.map_info["background_sprites"] = self.bg_sprites
        self.map_info["cells"] = cells_dict
        self.map_info["borders"] = borders_right

        for sprite in self.list_refresh:
            sprite.refresh()
