import os
import pygame as pg
from .sprite import Sprite

prop_dict = {}


class Prop(Sprite):
    """Prop model"""

    def __init__(self, Map, cell_pos, image, dimensions=(1, 1, 1)):
        """cell_pos =  midbottom - .5*cell_y"""
        self.Map = Map
        self.Game = Map.Game

        x, y, z = dimensions

        if x < y:
            cell_pos = (cell_pos[0] + min(x, y) - 1 + (y-x)*0.25,
                        cell_pos[1] + min(x, y) - 1 + (y-x)*0.75)
        else:
            cell_pos = (cell_pos[0] + min(x, y) - 1 + (x-y)*0.75,
                        cell_pos[1] + min(x, y) - 1 + (x-y)*0.25)

        if y % 2 == 0:
            a = int(y/2 + 2 + z - 1)
        else:
            a = int(y/2 + 1.5 + z - 1)

        b = a + x
        d = a
        c = d - y

        if x == y or x == 1 or y == 1:
            if x == 1 and y == 1:
                markers = list()
            else:
                markers = [
                    [a, d-1],
                    [b-1, c],
                    ]
        else:
            markers = [
                [a, d-1],
                [b-1, d-1],
                [b-1, c],
                ]

        super().__init__(image, cell_pos, markers=markers)

        self.forbidden_cells = []

        for ori_x in range(a, b):
            for ori_y in range(c, d):
                self.forbidden_cells.append(self.add_init_pos([ori_x, ori_y]))

    def refresh(self):
        self.Map.bg_sprites.add(self)

        for cell in self.forbidden_cells:
            self.Map.map_info["cells"].pop(
                cell,
                self.Map.map_info["borders"].pop(cell, None))


class Tree(Prop):
    """Create a tree on the map"""

    def __init__(self, Map, cell_pos):
        self.Map = Map
        self.Game = Map.Game
        image = os.path.join(self.Game.data_dir, 'tree.png')
        super().__init__(Map, cell_pos, image, dimensions=(1, 1, 3))


prop_dict["tree"] = Tree


class Hole(Prop):
    """Create a hole on the map"""

    def __init__(self, Map, cell_pos):
        self.Map = Map
        self.Game = Map.Game
        image = os.path.join(self.Game.data_dir, 'hole.png')
        super().__init__(Map, cell_pos, image)


prop_dict["hole"] = Hole


class Wall(Prop):
    """Create a wall on the map"""

    def __init__(self, Map, cell_pos):
        self.Map = Map
        self.Game = Map.Game
        image = os.path.join(self.Game.data_dir, 'wall_1_1.png')
        super().__init__(Map, cell_pos, image)


prop_dict["wall"] = Wall


class Wall_1_1_2(Prop):
    """Create a wall on the map"""

    def __init__(self, Map, cell_pos):
        self.Map = Map
        self.Game = Map.Game
        image = os.path.join(self.Game.data_dir, 'wall_1_1_2.png')
        super().__init__(Map, cell_pos, image, dimensions=(1, 1, 2))


prop_dict["wall_left_1_1_2"] = Wall_1_1_2


class Wall_1_1_3(Prop):
    """Create a wall on the map"""

    def __init__(self, Map, cell_pos):
        self.Map = Map
        self.Game = Map.Game
        image = os.path.join(self.Game.data_dir, 'wall_1_1_3.png')
        super().__init__(Map, cell_pos, image, dimensions=(1, 1, 3))


prop_dict["wall_left_1_1_3"] = Wall_1_1_3


class Table(Prop):
    """Create a 1x2 table on the map"""

    def __init__(self, Map, cell_pos):
        self.Map = Map
        self.Game = Map.Game

        image = os.path.join(self.Game.data_dir, 'table.png')
        super().__init__(Map, cell_pos, image, dimensions=(1, 2, 1))


prop_dict["table"] = Table


class Wall_left_3(Prop):
    """Create a 1x3 wall on the map"""

    def __init__(self, Map, cell_pos):
        self.Map = Map
        self.Game = Map.Game

        image = os.path.join(self.Game.data_dir, 'wall_1_3.png')
        super().__init__(Map, cell_pos, image, dimensions=(1, 3, 1))


prop_dict["wall_left_3"] = Wall_left_3


class Wall_left_2(Prop):
    """Create a 1x2 wall on the map"""

    def __init__(self, Map, cell_pos):
        self.Map = Map
        self.Game = Map.Game

        image = os.path.join(self.Game.data_dir, 'wall_1_2.png')
        super().__init__(Map, cell_pos, image, dimensions=(1, 2, 1))


prop_dict["wall_left_2"] = Wall_left_2


class Wall_left_2_2(Prop):
    """Create a 2x2 wall on the map"""

    def __init__(self, Map, cell_pos):
        self.Map = Map
        self.Game = Map.Game

        image = os.path.join(self.Game.data_dir, 'wall_2_2.png')
        super().__init__(Map, cell_pos, image,
                         dimensions=(2, 2, 1))


prop_dict["wall_left_2_2"] = Wall_left_2_2


class Wall_left_2_2_2(Prop):
    """Create a 2x2x2 wall on the map"""

    def __init__(self, Map, cell_pos):
        self.Map = Map
        self.Game = Map.Game

        image = os.path.join(self.Game.data_dir, 'wall_2_2_2.png')
        super().__init__(Map, cell_pos, image, dimensions=(2, 2, 2))


prop_dict["wall_left_2_2_2"] = Wall_left_2_2_2


class Wall_left_2_3(Prop):
    """Create a 2x3 wall on the map"""

    def __init__(self, Map, cell_pos):
        self.Map = Map
        self.Game = Map.Game

        image = os.path.join(self.Game.data_dir, 'wall_2_3.png')
        super().__init__(Map, cell_pos, image, dimensions=(2, 3, 1))


prop_dict["wall_left_2_3"] = Wall_left_2_3


class Wall_left_2_3_2(Prop):
    """Create a 2x3x2 wall on the map"""

    def __init__(self, Map, cell_pos):
        self.Map = Map
        self.Game = Map.Game

        image = os.path.join(self.Game.data_dir, 'wall_2_3_2.png')
        super().__init__(Map, cell_pos, image, dimensions=(2, 3, 2))


prop_dict["wall_left_2_3_2"] = Wall_left_2_3_2


class Wall_left_2_3_4(Prop):
    """Create a 2x3x4 wall on the map"""

    def __init__(self, Map, cell_pos):
        self.Map = Map
        self.Game = Map.Game

        image = os.path.join(self.Game.data_dir, 'wall_2_3_4.png')
        super().__init__(Map, cell_pos, image, dimensions=(2, 3, 4))


prop_dict["wall_left_2_3_4"] = Wall_left_2_3_4


class Wall_left_3_3_4(Prop):
    """Create a 3x3x4 wall on the map"""

    def __init__(self, Map, cell_pos):
        self.Map = Map
        self.Game = Map.Game

        image = os.path.join(self.Game.data_dir, 'wall_3_3_4.png')
        super().__init__(Map, cell_pos, image, dimensions=(3, 3, 4))


prop_dict["wall_left_3_3_4"] = Wall_left_3_3_4


class Wall_left_3_3_4_spec(Prop):
    """Create a 3x3x4 wall with cut right on the map"""

    def __init__(self, Map, cell_pos):
        self.Map = Map
        self.Game = Map.Game

        image = os.path.join(self.Game.data_dir, 'wall_3_3_4_spec.png')
        super().__init__(Map, cell_pos, image, dimensions=(3, 3, 4))
        self.forbidden_cells = self.forbidden_cells[:-3]


prop_dict["wall_left_3_3_4_spec"] = Wall_left_3_3_4_spec


class Wall_right_3(Prop):
    """Create a 3x1 wall on the map"""

    def __init__(self, Map, cell_pos):
        self.Map = Map
        self.Game = Map.Game

        image = os.path.join(self.Game.data_dir, 'wall_1_3.png')
        super().__init__(Map, cell_pos, image, dimensions=(3, 1, 1))

        self.image = pg.transform.flip(self.image, True, False)


prop_dict["wall_right_3"] = Wall_right_3


class Wall_right_2(Prop):
    """Create a 2x1 wall on the map"""

    def __init__(self, Map, cell_pos):
        self.Map = Map
        self.Game = Map.Game

        image = os.path.join(self.Game.data_dir, 'wall_1_2.png')
        super().__init__(Map, cell_pos, image, dimensions=(2, 1, 1))

        self.image = pg.transform.flip(self.image, True, False)


prop_dict["wall_right_2"] = Wall_right_2
