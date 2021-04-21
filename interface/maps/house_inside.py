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
        position = "first_house"

        super().__init__(Maps, Game, position)

        self.add_prop("house_inside", (9, 18))

        self.add_prop("table", (10, 19))

        self.add_prop("frame", (9, 15), background=True)
        self.add_prop("vase", (9, 18))

        self.add_prop("door_left", (14, 20), (0, 1),
                      new_char_cell=(14, 20), char_orientation="se")
