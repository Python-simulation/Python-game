# -*- coding: utf-8 -*-
"""
Created on Sat May 30 11:15:11 2020

@author: jonathan
"""
import os

import pygame as pg

from ..background import BackGround
from ..npc.character import Character
# from ..chimp import Chimp
from ..findpath import cell_sizes
from ..findpath import FindPath
from ..props import Tree
from ..npc.someguy import SomeGuy
from ..npc.npc import Npc

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
        npc = pg.sprite.RenderPlain(())
        # chimp = Chimp(Game)
        # sprites.add(chimp)

        someguy = SomeGuy(Game, (23, 19))#(10, 20))
        npc.add(someguy)

        # show = BackGround(size=npc.area.size)
        # show.rect.topleft = npc.area.topleft
        # sprites.add(show)

        file_name = os.path.join(Game.data_dir, "npc.png")
        npc_2 = Npc(Game, file_name, cell_pos=(20, 10))
        # npc_2.allowed_mvt(10, 3)
        # npc_2.npc_time = 2
        npc.add(npc_2)

        # show = BackGround(size=npc_2.area.size)
        # show.rect.topleft = npc_2.area.topleft
        # sprites.add(show)

        self.map_info["sprites"] = sprites
        self.map_info["npc"] = npc

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
