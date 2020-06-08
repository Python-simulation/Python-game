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
from ..findpath import FindPath
from ..tree import Tree

fp = FindPath()


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

        self.list_refresh = list()
        self.list_refresh.append(Tree(self, (11, 15)))

        sprites = pg.sprite.RenderPlain(())
        chimp = Chimp(Game)
        sprites.add(chimp)

        file_name = os.path.join(Game.data_dir, "npc.png")
        npc = Character(Game, file_name)
        position = fp.cell_to_pos((10, 20))
        npc.rect.midbottom = (position[0], position[1] + cell_sizes[1]/2)
        # npc.rect.midbottom = (5*cell_sizes[0]+cell_sizes[0]/2,
        #                       5*cell_sizes[1]+cell_sizes[1]/2)
        npc.allowed_mvt(2, 1)
        npc.max_speed = 5
        npc._npc_time = 1
        sprites.add(npc)

        # show = BackGround(size=npc.area.size)
        # show.rect.topleft = npc.area.topleft
        # sprites.add(show)

        npc_2 = Character(Game, file_name)
        position = fp.cell_to_pos((20, 10))
        npc_2.rect.midbottom = (position[0], position[1] + cell_sizes[1]/2)
        npc_2.allowed_mvt(10, 3)
        npc_2._npc_time = 2
        sprites.add(npc_2)

        # show = BackGround(size=npc_2.area.size)
        # show.rect.topleft = npc_2.area.topleft
        # sprites.add(show)

        self.map_info["sprites"] = sprites

        Maps.all_maps[self.position] = self

        self.refresh()

    def refresh(self):
        [cells_dict, borders_left, borders_top,
         borders_right, borders_bottom, borders] = self.Maps.map_reset_cells()

        self.map_info["background_sprites"] = self.bg_sprites
        self.map_info["cells"] = cells_dict
        self.map_info["borders"] = borders

        for sprite in self.list_refresh:
            sprite.refresh()
