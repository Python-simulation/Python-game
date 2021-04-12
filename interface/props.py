import os
import pygame as pg
from .sprite import Sprite

prop_dict = {}


class Prop(Sprite):
    """Prop model"""

    def __init__(self, Map, cell_pos, image, markers=list()):
        """cell_pos =  midbottom - .5*cell_y"""
        self.cell_pos = cell_pos
        self.Map = Map
        self.Game = Map.Game

        super().__init__(image, cell_pos, markers=markers)

        self.forbidden_cells = [cell_pos]

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
        super().__init__(Map, cell_pos, image)


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
        image = os.path.join(self.Game.data_dir, 'wall.png')
        super().__init__(Map, cell_pos, image)


prop_dict["wall"] = Wall


class Table(Prop):  # temp -> will create model for 1x2 1xn
    """Create a 1x2 table on the map"""

    def __init__(self, Map, cell_pos):
        self.Map = Map
        self.Game = Map.Game

        cell_pos = (cell_pos[0] + 0.25,
                    cell_pos[1] - 0.25)
        markers = [
            [3, 2],
            [3, 0],
            ]
        image = os.path.join(self.Game.data_dir, 'table.png')
        super().__init__(Map, cell_pos, image, markers=markers)

        for y in range(0, 2+1):
            self.forbidden_cells.append(self.add_init_pos([3, y]))


prop_dict["table"] = Table


class Wall_left_3(Prop):
    """Create a 1x3 wall on the map"""

    def __init__(self, Map, cell_pos):
        self.Map = Map
        self.Game = Map.Game

        cell_pos = (cell_pos[0] + 0.5,  # left down
                    cell_pos[1] + 1.5)
        markers = [
            [3, 2],
            [3, 0],
            ]
        image = os.path.join(self.Game.data_dir, 'wall_3.png')
        super().__init__(Map, cell_pos, image, markers=markers)

        for y in range(0, 2+1):
            self.forbidden_cells.append(self.add_init_pos([3, y]))


prop_dict["wall_left_3"] = Wall_left_3


class Wall_left_2(Prop):
    """Create a 1x2 wall on the map"""

    def __init__(self, Map, cell_pos):
        self.Map = Map
        self.Game = Map.Game

        cell_pos = (cell_pos[0]+0.25,
                    cell_pos[1]+0.75)
        markers = [
            [3, 2],
            [3, 1],
            ]
        image = os.path.join(self.Game.data_dir, 'wall_2.png')
        super().__init__(Map, cell_pos, image, markers=markers)

        for y in range(1, 2+1):
            self.forbidden_cells.append(self.add_init_pos([3, y]))


prop_dict["wall_left_2"] = Wall_left_2


class Wall_right_3(Prop):
    """Create a 3x1 wall on the map"""

    def __init__(self, Map, cell_pos):
        self.Map = Map
        self.Game = Map.Game

        cell_pos = (cell_pos[0] + 1.5,
                    cell_pos[1] + 0.5)
        markers = [
            [2, 1],
            [4, 1],
            ]
        image = os.path.join(self.Game.data_dir, 'wall_3.png')
        super().__init__(Map, cell_pos, image, markers=markers)

        for x in range(2, 4+1):
            self.forbidden_cells.append(self.add_init_pos([x, 1]))

        self.image = pg.transform.flip(self.image, True, False)


prop_dict["wall_right_3"] = Wall_right_3


class Wall_right_2(Prop):
    """Create a 2x1 wall on the map"""

    def __init__(self, Map, cell_pos):
        self.Map = Map
        self.Game = Map.Game
        cell_pos = (cell_pos[0] + 0.75,
                    cell_pos[1] + 0.25)
        markers = [
            [2, 1],
            [3, 1],
            ]
        image = os.path.join(self.Game.data_dir, 'wall_2.png')
        super().__init__(Map, cell_pos, image, markers=markers)

        for x in range(2, 3+1):
            self.forbidden_cells.append(self.add_init_pos([x, 1]))

        self.image = pg.transform.flip(self.image, True, False)


prop_dict["wall_right_2"] = Wall_right_2
