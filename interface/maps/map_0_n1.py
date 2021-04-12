# -*- coding: utf-8 -*-
"""
Created on Sat May 30 11:15:11 2020

@author: jonathan
"""
import os

from .map_model import MapDefault


class Map(MapDefault):

    def __init__(self, Maps, Game):
        self.Maps = Maps
        self.Game = Game
        position = (0, -1)  # position of the map relative to all the maps

        image = os.path.join(Game.data_dir, 'background2.png')

        super().__init__(Maps, Game, position, image=image,
                         cell_data="walk",
                         borders="br")

        self.add_prop("tree", (11, 15))
        self.add_prop("tree", (11, 15))
        self.add_prop("tree", (16, 18))
        self.add_prop("tree", (17, 18))
        self.add_prop("tree", (18, 18))
        self.add_prop("tree", (12, 20))
        self.add_prop("tree", (16, 26))
        self.add_prop("tree", (16, 28))
        self.add_prop("wall_left_3", (16, 19))
        self.add_prop("wall_right_3", (16, 22))
