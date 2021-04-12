# -*- coding: utf-8 -*-
"""
Created on Sat May 30 11:15:11 2020

@author: jonathan
"""
import os

from .map_model import MapDefault

# from ..background import BackGround
from ..npc.character import Character
from ..npc.someguy import SomeGuy
from ..npc.npc import Npc


class Map(MapDefault):

    def __init__(self, Maps, Game):
        self.Game = Game
        self.Maps = Maps
        position = (0, 0)

        image = os.path.join(Game.data_dir, 'background.png')

        super().__init__(Maps, Game, position, image=image,
                         cell_data="walk",
                         borders="a")

        npc = self.map_info["npc"]
        # sprites = self.map_info["sprites"]

        someguy = SomeGuy(Game)
        someguy.change_position((23, 19))
        npc.add(someguy)

        # show = BackGround(size=someguy.area.size)
        # show.rect.topleft = someguy.area.topleft
        # sprites.add(show)

        file_name = os.path.join(Game.data_dir, "npc.png")
        npc_2 = Npc(Game, file_name)
        npc_2.change_position((20, 10))
        # npc_2.allowed_mvt(10, 3)
        # npc_2.npc_time = 2
        npc.add(npc_2)

        most_basic_npc = Character(Game, file_name)
        most_basic_npc.change_position((15, 13))
        npc.add(most_basic_npc)

        # show = BackGround(size=npc_2.area.size)
        # show.rect.topleft = npc_2.area.topleft
        # sprites.add(show)

        # self.map_info["npc"] = npc

        self.add_prop("tree", (11, 15))
