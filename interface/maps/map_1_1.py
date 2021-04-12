# -*- coding: utf-8 -*-
import os

from ..npc.npc import Npc
from .map_model import MapDefault


class Map(MapDefault):

    def __init__(self, Maps, Game):
        position = (1, 1)  # position of the map relative to all the maps

        map_data = Game.mf.map_data.copy()

        map_data[15][8] = 2  # done: add function to add to existing mapdefault__init__
        map_data[16][8] = 2

        map_data[20][10] = 3

        map_data[19][9] = 2
        map_data[20][9] = 2
        map_data[21][9] = 2

        map_data[19][11] = 2
        map_data[20][11] = 2
        map_data[21][11] = 2

        map_data[19][10] = 2
        map_data[21][10] = 2

        map_data[15][5] = 0
        map_data[16][5] = 0
        map_data[15][6] = 0
        map_data[16][6] = 0

        super().__init__(Maps, Game, position,
                         map_data=map_data,
                         borders="lt")

        # BUG: can't have black sprite (no sprite) if use "grass" -> need to create a black sprite or
        # need to create back background using new map_data
        self.add_prop("tree", (15, 8))
        self.add_prop("tree", (16, 8))
        self.add_prop("tree", (17, 8))

        self.cell_data[15][5] = 0
        self.cell_data[16][5] = 0
        self.cell_data[15][6] = 0
        self.cell_data[16][6] = 0

        file_name = os.path.join(Game.data_dir, "npc.png")
        npc_1 = Npc(Game, file_name)
        npc_1.allowed_mvt(50, 1)
        npc_1.speed = 5
        npc_1.npc_time = 2

        npc_1.change_position((15, 20))
        self.map_info["npc"].add(npc_1)