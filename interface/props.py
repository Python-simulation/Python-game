import os
import pygame as pg
from .sprite import Sprite
from .findpath import FindPath

fp = FindPath()

prop_dict = {}


"""Model class"""


class Object(Sprite):
    """Object model for all displayed item that don't affect the cells"""

    def __init__(self, Map, image, cell_pos, dimensions=(1, 1, 1), **kwargs):
        """cell_pos =  midbottom - .5*cell_y"""
        self.Map = Map
        self.Game = Map.Game

        self.background = kwargs.get("background", False)

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

        self._abcd = a, b, c, d

        super().__init__(image, cell_pos, markers=markers, **kwargs)

    def refresh(self):
        if self.background:  # if behind everything
            self.Map.map_info["background"].image.blit(self.image, self.rect)
        else:  # if can move around
            self.Map.bg_sprites.add(self)


class Prop(Object):
    """Prop model for item that change the walkable cells"""

    def __init__(self, Map, image, cell_pos, dimensions=(1, 1, 1), **kwargs):
        """cell_pos =  midbottom - .5*cell_y"""
        self.Map = Map
        self.Game = Map.Game

        super().__init__(Map, image, cell_pos, dimensions=dimensions, **kwargs)

        self.additive = kwargs.get("additive", False)

        self.forbidden_cells = []

        a, b, c, d = self._abcd

        for ori_x in range(a, b):
            for ori_y in range(c, d):
                self.forbidden_cells.append(self.add_init_pos([ori_x, ori_y]))

    def refresh(self):
        super().refresh()

        for cell in self.forbidden_cells:
            try:
                current_cell = self.Map.map_info["cells"][cell]
                if self.additive:
                    self.Game.mf.fct_tile_1(current_cell)

                current_cell.active = self.additive
            except KeyError:
                try:
                    # no sure yet because if don't exist, do nothing
                    current_cell = self.Map.map_info["borders"][cell]
                    if self.additive:
                        self.Game.mf.fct_tile_1(current_cell)

                    current_cell.active = self.additive
                except KeyError:
                    pass  # outside map


class PropTP(Prop):
    """Prop model with teleportation function"""

    def __init__(self, Map, image, cell_pos, new_map_pos,
                 dimensions=(1, 1, 1), **kwargs):
        self.Map = Map
        self.Game = Map.Game

        assert dimensions[0] == 1 and dimensions[1] == 1  # only for 1x1xz cell

        super().__init__(Map, image, cell_pos, dimensions=dimensions, **kwargs)

        self.special_cell = [
            fp.pos_to_cell(self.markers[0]),
            # self.add_init_pos([2, 1]),  # currently can walk on tp
            # cell without tp if try to change map but stopped by the house
            ]

        for cell in self.special_cell:
            self.forbidden_cells.remove(cell)

        tp_cell_in = self.special_cell[0]

        self.char_orientation = kwargs.get("char_orientation", None)
        new_char_cell = kwargs.get("new_char_cell", tp_cell_in)

        self.new_char_pos = fp.cell_to_pos(new_char_cell)

        self.new_map_pos = new_map_pos

    def teleport(self, *args):
        if self.char_orientation is not None:
            self.Game.character.change_orientation(self.char_orientation)
        return self.Game.teleportation(self.new_map_pos,
                                       self.new_char_pos, *args)

    def refresh(self):
        super().refresh()

        all_cells = self.Map.map_info["cells"]

        for cell in self.special_cell:
            all_cells[cell].active = True
            all_cells[cell].function = self.teleport


def _fct_none(*args, **kwargs):
    pass


class PropClickable(Prop):
    """ Class model for Prop with clicked and hovered functions"""

    def __init__(self, Map, image, cell_pos, dimensions=(1, 1, 1), **kwargs):
        self.Map = Map
        self.Game = Map.Game

        super().__init__(Map, image, cell_pos, dimensions=dimensions, **kwargs)

        self.function = kwargs.get("function", _fct_none)
        self.arguments = kwargs.get("arguments", None)

        self.position = self.rect  # same id until clicked occured, then copy
        self.image_original = self.image

        self.state = False
        self.state_clicked = False
        self.is_hovered = False

        self.highligh = pg.Surface(self.rect.size).convert_alpha()
        self.highligh.fill((240, 240, 240))

    def hovered(self):
        self.is_hovered = True
        self.image_original = self.image.copy()

        self.image.blit(self.highligh, (0, 0),
                        special_flags=pg.BLEND_RGBA_MULT)

        return True

    def unhovered(self):
        self.is_hovered = False
        self.set_back_size()

    def clicked(self):
        # the not state alloyed to avoid clicking twice and add infinit offset
        if self.Game.mouse.state_clicking and not self.state_clicked:
            self.state_clicked = True

        return True

    def unclicked(self):
        was_clicked = True if self.state_clicked else False
        self.state_clicked = False
        self.set_back_size()

        if was_clicked and self.Game.mouse.hovering(self):
            self.hovered()
            self.state = True

            if self.arguments is not None:
                self.function(self.arguments)
            else:
                self.function()

        else:
            self.state = False

    def set_back_size(self):
        self.image = self.image_original
        self.rect = self.position

        self.position = self.rect  # same id from now
        self.image_original = self.image  # same id from now


"""Classes made from Object model"""


class Frame(Object):
    """Create a frame on the map"""

    def __init__(self, Map, cell_pos, **kwargs):
        self.Map = Map
        self.Game = Map.Game
        image = os.path.join(self.Game.data_dir, 'frame.png')
        kwargs["alpha"] = True
        super().__init__(Map, image, cell_pos, dimensions=(1, 0, 1), **kwargs)


prop_dict["frame"] = Frame


class Vase(Object):
    """Create a vase on the map"""

    def __init__(self, Map, cell_pos, **kwargs):
        self.Map = Map
        self.Game = Map.Game
        image = os.path.join(self.Game.data_dir, 'vase.png')
        super().__init__(Map, image, cell_pos, **kwargs)


prop_dict["vase"] = Vase


"""Classes made from Prop model"""


class Tree(Prop):
    """Create a tree on the map"""

    def __init__(self, Map, cell_pos):
        self.Map = Map
        self.Game = Map.Game
        image = os.path.join(self.Game.data_dir, 'tree.png')
        super().__init__(Map, image, cell_pos, dimensions=(1, 1, 3))


prop_dict["tree"] = Tree


class Hole(Prop):
    """Create a hole on the map"""

    def __init__(self, Map, cell_pos):
        self.Map = Map
        self.Game = Map.Game
        image = os.path.join(self.Game.data_dir, 'hole.png')
        super().__init__(Map, image, cell_pos)


prop_dict["hole"] = Hole


class Wall(Prop):
    """Create a wall on the map"""

    def __init__(self, Map, cell_pos):
        self.Map = Map
        self.Game = Map.Game
        image = os.path.join(self.Game.data_dir, 'wall_1_1.png')
        super().__init__(Map, image, cell_pos)


prop_dict["wall"] = Wall


class Wall_1_1_2(Prop):
    """Create a wall 1x1x2 on the map"""

    def __init__(self, Map, cell_pos):
        self.Map = Map
        self.Game = Map.Game
        image = os.path.join(self.Game.data_dir, 'wall_1_1_2.png')
        super().__init__(Map, image, cell_pos, dimensions=(1, 1, 2))


prop_dict["wall_left_1_1_2"] = Wall_1_1_2


class Wall_1_1_3(Prop):
    """Create a wall 1x1x3 on the map"""

    def __init__(self, Map, cell_pos):
        self.Map = Map
        self.Game = Map.Game
        image = os.path.join(self.Game.data_dir, 'wall_1_1_3.png')
        super().__init__(Map, image, cell_pos, dimensions=(1, 1, 3))


prop_dict["wall_left_1_1_3"] = Wall_1_1_3


class Table(Prop):
    """Create a 1x2 table on the map"""

    def __init__(self, Map, cell_pos):
        self.Map = Map
        self.Game = Map.Game

        image = os.path.join(self.Game.data_dir, 'table.png')
        super().__init__(Map, image, cell_pos, dimensions=(1, 2, 1))


prop_dict["table"] = Table


class Wall_left_3(Prop):
    """Create a 1x3 wall on the map"""

    def __init__(self, Map, cell_pos):
        self.Map = Map
        self.Game = Map.Game

        image = os.path.join(self.Game.data_dir, 'wall_1_3.png')
        super().__init__(Map, image, cell_pos, dimensions=(1, 3, 1))


prop_dict["wall_left_3"] = Wall_left_3


class Wall_left_2(Prop):
    """Create a 1x2 wall on the map"""

    def __init__(self, Map, cell_pos):
        self.Map = Map
        self.Game = Map.Game

        image = os.path.join(self.Game.data_dir, 'wall_1_2.png')
        super().__init__(Map, image, cell_pos, dimensions=(1, 2, 1))


prop_dict["wall_left_2"] = Wall_left_2


class Wall_left_2_2(Prop):
    """Create a 2x2 wall on the map"""

    def __init__(self, Map, cell_pos):
        self.Map = Map
        self.Game = Map.Game

        image = os.path.join(self.Game.data_dir, 'wall_2_2.png')
        super().__init__(Map, image, cell_pos,
                         dimensions=(2, 2, 1))


prop_dict["wall_left_2_2"] = Wall_left_2_2


class Wall_left_2_2_2(Prop):
    """Create a 2x2x2 wall on the map"""

    def __init__(self, Map, cell_pos):
        self.Map = Map
        self.Game = Map.Game

        image = os.path.join(self.Game.data_dir, 'wall_2_2_2.png')
        super().__init__(Map, image, cell_pos, dimensions=(2, 2, 2))


prop_dict["wall_left_2_2_2"] = Wall_left_2_2_2


class Wall_left_2_3(Prop):
    """Create a 2x3 wall on the map"""

    def __init__(self, Map, cell_pos):
        self.Map = Map
        self.Game = Map.Game

        image = os.path.join(self.Game.data_dir, 'wall_2_3.png')
        super().__init__(Map, image, cell_pos, dimensions=(2, 3, 1))


prop_dict["wall_left_2_3"] = Wall_left_2_3


class Wall_left_2_3_2(Prop):
    """Create a 2x3x2 wall on the map"""

    def __init__(self, Map, cell_pos):
        self.Map = Map
        self.Game = Map.Game

        image = os.path.join(self.Game.data_dir, 'wall_2_3_2.png')
        super().__init__(Map, image, cell_pos, dimensions=(2, 3, 2))


prop_dict["wall_left_2_3_2"] = Wall_left_2_3_2


class Wall_left_2_3_4(Prop):
    """Create a 2x3x4 wall on the map"""

    def __init__(self, Map, cell_pos):
        self.Map = Map
        self.Game = Map.Game

        image = os.path.join(self.Game.data_dir, 'wall_2_3_4.png')
        super().__init__(Map, image, cell_pos, dimensions=(2, 3, 4))


prop_dict["wall_left_2_3_4"] = Wall_left_2_3_4


class Wall_left_3_3_4(Prop):
    """Create a 3x3x4 wall on the map"""

    def __init__(self, Map, cell_pos):
        self.Map = Map
        self.Game = Map.Game

        image = os.path.join(self.Game.data_dir, 'wall_3_3_4.png')
        super().__init__(Map, image, cell_pos, dimensions=(3, 3, 4))


prop_dict["wall_left_3_3_4"] = Wall_left_3_3_4


class Wall_left_3_3_4_spec(Prop):
    """Create a 3x3x4 wall with cut right on the map"""

    def __init__(self, Map, cell_pos):
        self.Map = Map
        self.Game = Map.Game

        image = os.path.join(self.Game.data_dir, 'wall_3_3_4_spec.png')
        super().__init__(Map, image, cell_pos, dimensions=(3, 3, 4))
        self.forbidden_cells = self.forbidden_cells[:-3]


prop_dict["wall_left_3_3_4_spec"] = Wall_left_3_3_4_spec


class Wall_right_3(Prop):
    """Create a 3x1 wall on the map"""

    def __init__(self, Map, cell_pos):
        self.Map = Map
        self.Game = Map.Game

        image = os.path.join(self.Game.data_dir, 'wall_1_3.png')
        super().__init__(Map, image, cell_pos, dimensions=(3, 1, 1))

        self.image = pg.transform.flip(self.image, True, False)


prop_dict["wall_right_3"] = Wall_right_3


class Wall_right_2(Prop):
    """Create a 2x1 wall on the map"""

    def __init__(self, Map, cell_pos):
        self.Map = Map
        self.Game = Map.Game

        image = os.path.join(self.Game.data_dir, 'wall_1_2.png')
        super().__init__(Map, image, cell_pos, dimensions=(2, 1, 1))

        self.image = pg.transform.flip(self.image, True, False)


prop_dict["wall_right_2"] = Wall_right_2


class House(Prop):
    """Create a house 5x5x5 on the map"""

    def __init__(self, Map, cell_pos):
        self.Map = Map
        self.Game = Map.Game

        image = os.path.join(self.Game.data_dir, 'house.png')
        super().__init__(Map, image, cell_pos, dimensions=(5, 5, 5))


prop_dict["house"] = House


class House_inside(Prop):
    """Create the inside of a house 5x5x5 on the map and make the inside cell
    walkable"""

    def __init__(self, Map, cell_pos):
        self.Map = Map
        self.Game = Map.Game

        image = os.path.join(self.Game.data_dir, 'house_inside.png')
        super().__init__(Map, image, cell_pos, dimensions=(5, 5, 5),
                         background=True, additive=True)


prop_dict["house_inside"] = House_inside


"""Classes made from PropTP model"""


class TPCell(PropTP):
    """Create a visible on the map with tp function"""

    def __init__(self, Map, cell_pos, new_map_pos, **kwargs):
        self.Map = Map
        self.Game = Map.Game

        image = os.path.join(self.Game.data_dir, 'tp_cell.png')

        super().__init__(Map, image, cell_pos, new_map_pos, **kwargs)


prop_dict["tp_cell"] = TPCell


class TPCellInvisble(PropTP):
    """Create a invisible cell on the map with tp function"""

    def __init__(self, Map, cell_pos, new_map_pos, **kwargs):
        self.Map = Map
        self.Game = Map.Game

        image = os.path.join(self.Game.data_dir, '128x128.png')

        super().__init__(Map, image, cell_pos, new_map_pos, **kwargs)


prop_dict["tp_cell_invisible"] = TPCellInvisble


"""Classes made from PropClickable model"""


class Door(PropClickable):
    """Create a door on the map with tp function"""

    def __init__(self, Map, cell_pos, target_cell, **kwargs):
        self.Map = Map
        self.Game = Map.Game

        image = os.path.join(self.Game.data_dir, 'door.png')
        kwargs["alpha"] = True
        super().__init__(Map, image, cell_pos,
                         dimensions=(0, 1, 2), **kwargs)

        self.target_cell = target_cell

    def refresh(self):
        super().refresh()

        cell = self.Map.map_info["cells"][self.target_cell]
        self.function = cell._overwrite_clicked


prop_dict["door"] = Door


class Door_right(PropClickable):
    """Create a door on the map with tp function"""

    def __init__(self, Map, cell_pos, target_cell, **kwargs):
        self.Map = Map
        self.Game = Map.Game

        image = os.path.join(self.Game.data_dir, 'door.png')
        kwargs["alpha"] = True
        super().__init__(Map, image, cell_pos,
                         dimensions=(1, 0, 2), **kwargs)

        self.target_cell = target_cell

        self.image = pg.transform.flip(self.image, True, False)
        self.image_original = pg.transform.flip(self.image_original,
                                                True, False)

    def refresh(self):
        super().refresh()

        cell = self.Map.map_info["cells"][self.target_cell]
        self.function = cell._overwrite_clicked


prop_dict["door_right"] = Door_right
