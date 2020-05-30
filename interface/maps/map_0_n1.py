# -*- coding: utf-8 -*-
"""
Created on Sat May 30 11:15:11 2020

@author: jonathan
"""
import os

import pygame as pg

from ..background import BackGround
from ..findpath import cell_sizes
from ..findpath import FindPath
fp = FindPath()


class Map:

    def __init__(self, Maps, Game):
        self.Maps = Maps
        self.Game = Game
        self.position = (0, -1)  # position of the map relative to all the maps

        self.map_info = dict()

        self.refresh()

        name = os.path.join(Game.data_dir, 'background2.png')
        background = BackGround(name)
        background.rect.center = Game.game_screen.rect.center

        self.map_info["background"] = background

        sprites = pg.sprite.RenderPlain()

        name = os.path.join(Game.data_dir, 'tree.png')
        tree = BackGround(name, -1)
        self.tree_cell = (11, 15)
        position = fp.cell_to_pos(self.tree_cell)
        tree.rect.midbottom = position
        sprites.add(tree)

        self.map_info["sprites"] = sprites

        Maps.all_maps[self.position] = self

    def refresh(self):
        [cells_dict, borders_left, borders_top,
         borders_right, borders_bottom, borders] = self.Maps.map_reset_cells()
        try:
            cells_dict.pop(self.tree_cell)
        except AttributeError:
            pass

        self.map_info["cells"] = cells_dict
        self.map_info["borders"] = borders_bottom
