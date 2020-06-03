# -*- coding: utf-8 -*-
"""
Created on Sat May 30 11:15:11 2020

@author: jonathan
"""
import os

import pygame as pg

from ..background import BackGround
from ..character import Character
from ..chimp import Chimp
from ..findpath import cell_sizes


class Map:

    def __init__(self, Maps, Game):
        self.Maps = Maps
        self.Game = Game
        self.position = (0, 0)  # position of the map relative to all the maps

        self.map_info = dict()

        name = os.path.join(Game.data_dir, 'background.png')
        background = BackGround(name)
        background.rect.center = Game.game_screen.rect.center

        self.map_info["background"] = background

        self.bg_sprites = pg.sprite.RenderPlain()

        sprites = pg.sprite.RenderPlain(())
        chimp = Chimp(Game)
        sprites.add(chimp)

        file_name = os.path.join(Game.data_dir, "npc.png")
        npc = Character(Game, file_name)
        npc.rect.midbottom = (5*cell_sizes[0]+cell_sizes[0]/2,
                              5*cell_sizes[1]+cell_sizes[1]/2)
        npc.allowed_mvt(1)
        npc.max_speed = 5
        npc._npc_time = 0.5
        sprites.add(npc)

        # show = BackGround(size=npc.area.size)
        # show.rect.topleft = npc.area.topleft
        # sprites.add(show)

        npc_2 = Character(Game, file_name)
        npc_2.rect.midbottom = (10*cell_sizes[0]+cell_sizes[0]/2,
                                6*cell_sizes[1]+cell_sizes[1]/2)
        npc_2.allowed_mvt(1, 2)
        npc_2._npc_time = 1
        sprites.add(npc_2)

        self.map_info["sprites"] = sprites

        Maps.all_maps[self.position] = self

        self.refresh()

    def refresh(self):
        [cells_dict, borders_left, borders_top,
         borders_right, borders_bottom, borders] = self.Maps.map_reset_cells()

        self.map_info["background_sprites"] = self.bg_sprites
        self.map_info["cells"] = cells_dict
        self.map_info["borders"] = borders
