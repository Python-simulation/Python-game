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
        position = (1, 0)  # position of the map relative to all the maps

        image = os.path.join(Game.data_dir, 'background2.png')

        super().__init__(Maps, Game, position, image=image,
                            # map_data=map_data,  # cell_data=cell_data,
                            borders="lbt")
