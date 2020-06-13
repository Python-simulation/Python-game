import os
from .interface_functions import NeededFunctions
from .findpath import FindPath
from .sprite import Sprite

nf = NeededFunctions()
fp = FindPath()


class Tree:
    """Create a tree on the map"""

    def __init__(self, Map, cell_pos):
        self.Map = Map
        self.Game = Map.Game

        name = os.path.join(self.Game.data_dir, 'tree.png')
        self.sprite = Sprite(name, cell_pos)
        self.rect = self.sprite.rect

        self.forbidden_cells = [cell_pos]

    def refresh(self):
        self.Map.bg_sprites.add(self.sprite)

        for cell in self.forbidden_cells:
            self.Map.map_info["cells"].pop(
                cell,
                self.Map.map_info["borders"].pop(cell, None)
            )


class Hole:
    """Create a hole on the map"""

    def __init__(self, Map, cell_pos):
        self.Map = Map
        self.Game = Map.Game

        name = os.path.join(self.Game.data_dir, 'hole.png')
        self.sprite = Sprite(name, cell_pos)
        self.rect = self.sprite.rect

        self.forbidden_cells = [cell_pos]

    def refresh(self):
        self.Map.bg_sprites.add(self.sprite)

        for cell in self.forbidden_cells:
            self.Map.map_info["cells"].pop(
                cell,
                self.Map.map_info["borders"].pop(cell, None)
            )


class Wall:
    """Create a wall on the map"""

    def __init__(self, Map, cell_pos):
        self.Map = Map
        self.Game = Map.Game

        name = os.path.join(self.Game.data_dir, 'wall.png')
        self.sprite = Sprite(name, cell_pos)
        self.rect = self.sprite.rect

        self.forbidden_cells = [cell_pos]

    def refresh(self):
        self.Map.bg_sprites.add(self.sprite)

        for cell in self.forbidden_cells:
            self.Map.map_info["cells"].pop(
                cell,
                self.Map.map_info["borders"].pop(cell, None)
            )


class Wall_left:
    """Create a wall on the map"""

    def __init__(self, Map, cell_pos):
        cell_pos = (cell_pos[0]+0.5,
                    cell_pos[1]+0.5)
        self.Map = Map
        self.Game = Map.Game

        markers = [
            [3, 2],
            [3, 0],
            ]
        name = os.path.join(self.Game.data_dir, 'wall_left.png')
        self.sprite = Sprite(name, cell_pos, markers=markers)
        self.rect = self.sprite.rect

        self.forbidden_cells = []

        for y in range(0, 2+1):
            self.forbidden_cells.append(self.sprite.add_init_pos([3, y]))

    def refresh(self):
        self.Map.bg_sprites.add(self.sprite)

        for cell in self.forbidden_cells:
            self.Map.map_info["cells"].pop(
                cell,
                self.Map.map_info["borders"].pop(cell, None)
            )


class Wall_right:
    """Create a wall on the map"""

    def __init__(self, Map, cell_pos):
        cell_pos = (cell_pos[0]+0.5,
                    cell_pos[1]+0.5)
        self.Map = Map
        self.Game = Map.Game

        markers = [
            [2, 1],
            [4, 1],
            ]
        name = os.path.join(self.Game.data_dir, 'wall_right.png')
        self.sprite = Sprite(name, cell_pos, markers=markers)
        self.rect = self.sprite.rect

        self.forbidden_cells = []

        for x in range(2, 4+1):
            self.forbidden_cells.append(self.sprite.add_init_pos([x, 1]))

    def refresh(self):
        self.Map.bg_sprites.add(self.sprite)

        for cell in self.forbidden_cells:
            self.Map.map_info["cells"].pop(
                cell,
                self.Map.map_info["borders"].pop(cell, None)
            )
