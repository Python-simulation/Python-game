# -*- coding: utf-8 -*-
"""
Created on Sat May 30 11:15:11 2020

@author: jonathan
"""
import os

import pygame as pg

from ..background import BackGround
from ..findpath import FindPath
from ..tree import Tree, Wall_left, Wall_right
fp = FindPath()


class Map:

    def __init__(self, Maps, Game):
        self.Maps = Maps
        self.Game = Game
        self.position = (0, -1)  # position of the map relative to all the maps

        self.map_info = dict()

        Maps.all_maps[self.position] = self

        name = os.path.join(Game.data_dir, 'background2.png')
        background = BackGround(name)
        background.rect.center = Game.game_screen.rect.center

        self.map_info["background"] = background

        self.sprites = pg.sprite.RenderPlain()

        self.bg_sprites = pg.sprite.RenderPlain()

        self.list_refresh = list()
        self.list_refresh.append(Tree(self, (11, 15)))
        self.list_refresh.append(Tree(self, (16, 18)))
        self.list_refresh.append(Tree(self, (17, 18)))
        self.list_refresh.append(Tree(self, (18, 18)))
        self.list_refresh.append(Tree(self, (12, 20)))
        self.list_refresh.append(Tree(self, (16, 26)))
        self.list_refresh.append(Tree(self, (16, 28)))
        self.list_refresh.append(Wall_left(self, (16, 20)))
        self.list_refresh.append(Wall_right(self, (17, 22)))

        self.refresh()

    def refresh(self):
        [cells_dict, borders_left, borders_top,
         borders_right, borders_bottom, borders] = self.Maps.map_reset_cells()

        self.map_info["background_sprites"] = self.bg_sprites
        self.map_info["cells"] = cells_dict
        self.map_info["borders"] = borders_bottom
        self.map_info["sprites"] = self.sprites

        for sprite in self.list_refresh:
            sprite.refresh()
