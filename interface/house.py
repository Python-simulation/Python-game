import os
import pygame as pg
from .interface_functions import NeededFunctions
from .background import BackGround
from .cell import Cell
from .findpath import cell_sizes
from .findpath import FindPath

nf = NeededFunctions()
fp = FindPath()


class House(BackGround):
    """Create a house on the map"""

    def __init__(self, Map, topleft):
        BackGround.__init__(self)
        self.Map = Map
        self.Maps = Map.Maps
        self.Game = Map.Game

        self.name = "first_house"

        name = os.path.join(self.Game.data_dir, 'house.png')
        self.image, self.rect = nf.load_image(name, -1)

        self.rect.topleft = topleft

        self.background = self.Map.map_info["background"]
        self.background.image.blit(self.image, self.rect)  # TODO: if want to have
        # the character to "vanish" being a building, must change this line

        self.forbidden_cells = list()

        for cell_x in range(8, 12+1):
            for cell_y in range(3, 7+1):

                cell = self.add_init_pos([cell_x, cell_y])
                self.forbidden_cells.append(cell)

        self.special_cell = [
            self.add_init_pos([12, 5]),
            ]

        for cell in self.special_cell:
            self.forbidden_cells.remove(cell)

        self.refresh()

        self.Maps.all_maps[self.name] = self

        self.create_inside()

    def add_init_pos(self, cell):
        init_pos = fp.pos_to_cell(self.rect.topleft)

        cell[0] += init_pos[0]
        cell[1] += init_pos[1]

        unit_pos = (int(cell[0]), int(cell[1]))
        return unit_pos

    def tp_house(self, *args):
        new_map_pos = self.name

        new_char_pos = fp.cell_to_pos(self.tp_cell_in)

        return self.Game.teleportation(new_map_pos, new_char_pos, *args)

    def tp_outside(self, *args):
        new_map_pos = self.outside

        new_char_pos = fp.cell_to_pos(self.tp_cell_out)

        return self.Game.teleportation(new_map_pos, new_char_pos, *args)

    def create_inside(self):

        self.outside = self.Map.position

        self.map_info = dict()

        background = BackGround()
        background.image = self.background.image.copy()  # change if want black
        background.rect = background.image.get_rect()

        name = os.path.join(self.Game.data_dir, 'house_inside.png')
        image, rect = nf.load_image(name, -1)
        rect.topleft = self.rect.topleft

        background.image.blit(image, rect)

        self.map_info["background"] = background

        sprites = pg.sprite.RenderPlain(())
        self.map_info["sprites"] = sprites

        inside_cells = self.add_cell(self.forbidden_cells)
        door = self.add_cell(self.special_cell)
        inside_cells.update(door)

        for cell in self.special_cell:
            cell = (int(cell[0]), int(cell[1]))
            inside_cells[cell].function = self.tp_outside

        table = [
            [9, 4],
            [9, 5],
            ]
        for cell in table:
            cell = self.add_init_pos(cell)
            inside_cells.pop(cell, None)

        self.map_info["cells"] = inside_cells
        self.map_info["borders"] = dict()

    def add_cell(self, cell_list):
        cells_dict = dict()
        for cell in cell_list:
            x, y = cell
            new_pos = fp.cell_to_pos(cell)

            current_cell = Cell(
                self.Game,
                size=(cell_sizes[0], cell_sizes[1]),
                position=(new_pos[0], new_pos[1]),
                function=self.Game.character.dest
            )

            current_cell.alpha_off = 100
            cells_dict[(x, y)] = current_cell

        return cells_dict

    def refresh(self):
        all_cells = self.Map.map_info["cells"]
        borders = self.Map.map_info["borders"]

        for cell in self.forbidden_cells:
            self.Map.map_info["cells"].pop(
                cell,
                self.Map.map_info["borders"].pop(cell, None))
                # CONSEIL: if house del border where character cam from,
                # can't go back and can't move : stuck for ever.
                # Must del border in adjacent map to avoid it.

        for cell in self.special_cell:
            all_cells[cell].function = self.tp_house

        self.tp_cell_in = self.special_cell[0]
        self.tp_cell_out = self.add_init_pos([13, 5])
