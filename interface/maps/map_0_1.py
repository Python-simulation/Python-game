# -*- coding: utf-8 -*-
"""
Created on Sat May 30 11:15:11 2020

@author: jonathan
"""
import os

from .map_model import MapDefault

from ..npc.npc import Npc


class Map(MapDefault):

    def __init__(self, Maps, Game):
        self.Maps = Maps
        self.Game = Game
        position = (0, 1)  # position of the map relative to all the maps

        super().__init__(Maps, Game, position,
                         map_data="grass", borders="tr")

        file_name = os.path.join(Game.data_dir, "npc.png")
        npc_1 = Npc(Game, file_name)
        npc_1.change_position((17, 15))
        npc_1.allowed_mvt(50, 50)
        npc_1.npc_time = 1

        self.map_info["npc"].add(npc_1)

        self.add_prop("house", (9, 18))
        self.add_prop("door", (14, 20), (14, 20))
        self.add_prop("tp_cell_invisible", (14, 20), "first_house",
                      new_char_cell=(13, 20), char_orientation="nw")

        self.add_prop("tp_cell", (20, 17), (1, -1), new_char_cell=(14, 15))

    def refresh(self):
        super().refresh()
        # try:  # error if refresh before house creation
        # self.house.refresh()
        # except AttributeError:
        #     print("not created yet")
