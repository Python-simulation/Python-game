# -*- coding: utf-8 -*-
"""
Created on Sat May 30 11:15:11 2020

@author: jonathan
"""
import os

import pygame as pg

from ..background import BackGround
from ..house import House
from ..findpath import FindPath
from ..npc.npc import Npc

fp = FindPath()


class Map:

    def __init__(self, Maps, Game):
        self.Maps = Maps
        self.Game = Game
        self.position = (0, 1)  # position of the map relative to all the maps

        self.map_info = dict()

        name = os.path.join(Game.data_dir, 'background2.png')
        background = BackGround(name)
        background.rect.center = Game.game_screen.rect.center

        self.map_info["background"] = background

        self.bg_sprites = pg.sprite.RenderPlain()

        sprites = pg.sprite.RenderPlain()
        npc = pg.sprite.RenderPlain()

        file_name = os.path.join(Game.data_dir, "npc.png")
        npc_1 = Npc(Game, file_name)
        npc_1.change_position((17, 15))
        npc_1.allowed_mvt(50, 50)
        npc_1.npc_time = 1

        npc.add(npc_1)

        self.map_info["sprites"] = sprites
        self.map_info["npc"] = npc

        house_cell = (13, 22)
        self.house = House(self, house_cell)
        # self.house.create_inside()

        Maps.all_maps[self.position] = self

        self.refresh()

    def refresh(self):
        [cells_dict, borders_left, borders_top,
         borders_right, borders_bottom, borders] = self.Maps.map_reset_cells()

        self.map_info["background_sprites"] = self.bg_sprites
        self.map_info["cells"] = cells_dict
        self.map_info["borders"] = borders_top
        self.map_info["borders"].update(borders_right)

        self.house.refresh()
