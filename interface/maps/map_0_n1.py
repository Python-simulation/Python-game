# -*- coding: utf-8 -*-
"""
Created on Sat May 30 11:15:11 2020

@author: jonathan
"""
import os

import pygame as pg

from ..background import BackGround
from ..sprite import Sprite
from ..findpath import cell_sizes
from ..findpath import FindPath
fp = FindPath()


class Map:

    def __init__(self, Maps, Game):
        self.Maps = Maps
        self.Game = Game
        self.position = (0, -1)  # position of the map relative to all the maps

        self.map_info = dict()
        self.cells_dict = dict()

        Maps.all_maps[self.position] = self

        name = os.path.join(Game.data_dir, 'background2.png')
        background = BackGround(name)
        background.rect.center = Game.game_screen.rect.center

        self.map_info["background"] = background

        self.sprites = pg.sprite.RenderPlain()

        self.bg_sprites = pg.sprite.RenderPlain()

        name = os.path.join(Game.data_dir, 'tree.png')

        self.bg_sprites.add(Sprite(Game, self, name, (11, 15)))
        self.bg_sprites.add(Sprite(Game, self, name, (16, 18)))
        self.bg_sprites.add(Sprite(Game, self, name, (17, 18)))
        self.bg_sprites.add(Sprite(Game, self, name, (18, 18)))
        self.bg_sprites.add(Sprite(Game, self, name, (12, 20)))
        self.bg_sprites.add(Sprite(Game, self, name, (16, 26)))
        self.bg_sprites.add(Sprite(Game, self, name, (16, 28)))

        self.refresh()

    def refresh(self):
        [cells_dict, borders_left, borders_top,
         borders_right, borders_bottom, borders] = self.Maps.map_reset_cells()

        self.cells_dict = cells_dict
        self.borders = borders_bottom

        for sprite in self.bg_sprites:
            sprite.refresh()

        self.map_info["background_sprites"] = self.bg_sprites
        self.map_info["cells"] = self.cells_dict
        self.map_info["borders"] = self.borders
        self.map_info["sprites"] = self.sprites
