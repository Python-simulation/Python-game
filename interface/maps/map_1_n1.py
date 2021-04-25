# -*- coding: utf-8 -*-
import os

from .map_model import MapDefault


class Map(MapDefault):

    def __init__(self, Maps, Game):
        self.Maps = Maps
        position = (1, -1)

        map_data = [[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 'ground', 'ground', 'ground'],
                    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 'ground', 'ground', 'ground', 'ground'],
                    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 'ground', 'ground', 'ground', 'ground','ground'],
                    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 'grass', 'grass', 'grass', 'grass', 0, 0, 0, 0, 0, 'ground', 0, 0, 'ground', 'ground', 'ground'],
                    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 'grass', 0, 0, 'ground', 0, 0, 0, 0, 0, 'ground', 0, 0, 0, 'grass', 'ground', 'ground'],
                    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 'grass', 0, 'grass', 'ground', 'grass', 'grass', 'ground', 'ground', 'ground', 'ground', 0, 0, 0, 'grass', 'grass', 'ground', 'ground'],
					[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 'grass', 'grass', 'grass', 'ground', 'grass', 'grass', 'grass', 0, 0, 0, 0, 0, 0, 'grass', 'grass', 'grass', 'ground', 'ground'],
					[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 'ground', 'ground', 'ground', 'grass', 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
					[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 'ground', 'ground', 'ground', 'grass', 0, 0, 0, 0, 0, 0, 0, 0, 0],
					[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 'grass', 0, 0, 0, 0, 0, 0, 0, 0],
					[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 'grass', 0, 0, 0, 0, 0, 0, 0],
					[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 'grass', 0, 0, 0, 0, 0, 0],
					[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 'grass', 'grass', 'grass', 'grass', 'grass', 'grass'],
					[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 'grass', 'grass', 'grass', 'grass', 'grass'],
					[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 'grass', 'grass', 'grass', 'grass'],
					[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 'grass', 'grass'],  # TODO: can't change the last cell because normaly not accessable ingame -> need to overwrite this feature in generator
					[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
					[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
					[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
					[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
					[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]]

        super().__init__(Maps, Game, position,
                         map_data_default="water",
                         map_data=map_data,
                         borders="lb")

        self.add_ground("grass", (14, 7))
        self.add_ground("grass", (14, 8))
        self.add_ground("grass", (15, 8))
        self.add_ground("grass", (15, 7))
        self.add_prop("tp_cell", (15, 7), (0, 1), new_char_cell=(20, 17))
        self.add_ground("grass", (14, 6))
        self.add_ground("grass", (15, 6))
        self.add_ground("grass", (16, 6))
        self.add_ground("grass", (16, 7))
        self.add_ground("grass", (16, 8))

        self.add_prop("wall", (13, 14))
        self.add_prop("wall", (13, 15))
        self.add_prop("wall", (14, 14))

        self.add_prop("tree", (13, 26))
        self.add_prop("tree", (14, 26))
        self.add_prop("tree", (15, 26))

        self.add_prop("wall_right_3", (18, 18))
        self.add_prop("wall_right_3", (21, 18))
        self.add_prop("wall_left_2", (24, 18))
        self.add_prop("wall_left_2", (25, 19))

        self.add_ground("water", (14, 28))  # BUG should cause issue but don't ? check again after borders will be done
