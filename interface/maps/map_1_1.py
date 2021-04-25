# -*- coding: utf-8 -*-
import os

from ..npc.npc import Npc
from .map_model import MapDefault


class Map(MapDefault):

    def __init__(self, Maps, Game):
        position = (1, 1)  # position of the map relative to all the maps

        super().__init__(Maps, Game, position,
                         map_data_default="grass",
                         borders="lt")

        self.add_ground("ground", (15, 8))
        self.add_ground("ground", (16, 8))
        self.add_ground("water", (20, 10))

        self.add_ground("ground", (19, 9))
        self.add_ground("ground", (20, 9))
        self.add_ground("ground", (21, 9))

        self.add_ground("ground", (19, 11))
        self.add_ground("ground", (20, 11))
        self.add_ground("ground", (21, 11))

        self.add_ground("ground", (19, 10))
        self.add_ground("ground", (21, 10))

        self.add_ground("empty", (15, 5))
        self.add_ground("empty", (16, 5))
        self.add_ground("empty", (15, 6))
        self.add_ground("empty", (16, 6))

        self.add_prop("tree", (15, 8))
        self.add_prop("tree", (16, 8))
        self.add_prop("tree", (17, 8))

        self.add_ground("water", (21, 17), walkable=False)

        file_name = os.path.join(Game.data_dir, "npc.png")
        npc_1 = Npc(Game, file_name)
        npc_1.allowed_mvt(50, 1)
        npc_1.speed = 5
        npc_1.npc_time = 2

        npc_1.change_position((15, 20))
        self.map_info["npc"].add(npc_1)