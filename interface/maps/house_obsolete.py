import os
import pygame as pg
from ..interface_functions import NeededFunctions
from ..background import BackGround
from ..cell import Cell
from ..findpath import FindPath
from ..sprite import Sprite

nf = NeededFunctions()
fp = FindPath()
cell_sizes = fp.cell_sizes


class House():
    """Create a house on the map"""

    def __init__(self, Map, cell_pos):
        self.Map = Map
        self.Maps = Map.Maps
        self.Game = Map.Game

        markers = [[8, 7], [12, 3]]
        name = os.path.join(self.Game.data_dir, 'house.png')
        self.sprite = Sprite(name, cell_pos, markers=markers)
        self.rect = self.sprite.rect

        self.forbidden_cells = list()

        for cell_x in range(8, 12+1):  # OPTIMIZE: function for sprite
            for cell_y in range(3, 7+1):

                cell = self.add_init_pos([cell_x, cell_y])
                self.forbidden_cells.append(cell)

        self.special_cell = [
            self.add_init_pos([12, 5]),  # currently can walk on tp
            # cell without tp if try to change map but stopped by the house
            ]

        for cell in self.special_cell:
            self.forbidden_cells.remove(cell)

        self.tp_cell_in = self.special_cell[0]

        # self.create_inside()

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
        self.Game.character.change_orientation("se")

        return self.Game.teleportation(new_map_pos, new_char_pos, *args)

    def create_inside(self):  # TODO: move it to an other file
        self.name = "first_house"
        self.Maps.all_maps[self.name] = self

        self.outside = self.Map.position

        self.tp_cell_out = self.add_init_pos([13, 5])

        self.map_info = dict()

        background = BackGround(size=self.Game.size)  # TODO: search example for colors -> can't read map pos
        # background.image = self.Map.map_info["background"].image.copy()
        # background.rect = background.image.get_rect()

        name = os.path.join(self.Game.data_dir, 'house_inside.png')
        image, rect = nf.load_image(name, -1)
        rect.topleft = self.rect.topleft

        background.image.blit(image, rect)

        self.map_info["background"] = background

        self.bg_sprites = pg.sprite.RenderPlain()
        self.map_info["background_sprites"] = self.bg_sprites

        sprites = pg.sprite.RenderPlain(())
        npc = pg.sprite.RenderPlain(())
        self.map_info["sprites"] = sprites
        self.map_info["npc"] = npc

        inside_cells = self.add_cell(self.forbidden_cells)
        door = self.add_cell(self.special_cell)
        inside_cells.update(door)

        for cell in self.special_cell:
            cell = (int(cell[0]), int(cell[1]))
            inside_cells[cell].function = self.tp_outside

        # table = [
        #     [9, 4],
        #     [9, 5],

        # # self.list_refresh.append(Table(self, (9, 4)))
        # for cell in table:
        #     cell = self.add_init_pos(cell)
        #     inside_cells.pop(cell, None)

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
        print("temp do nothing")
        return
        self.Map.bg_sprites.add(self.sprite)

        # for sprite in self.bg_sprites:
        #     sprite.refresh()

        all_cells = self.Map.map_info["cells"]

        for cell in self.forbidden_cells:
            self.Map.map_info["cells"].pop(
                cell,
                self.Map.map_info["borders"].pop(cell, None)
            )
            # ADVICE: if house del border where character cam from,
            # can't go back and can't move : stuck for ever.
            # Must del border in adjacent map to avoid it.

        for cell in self.special_cell:
            all_cells[cell].function = self.tp_house
