from .cell import Cell

from .findpath import FindPath
from .findpath import cell_sizes

fp = FindPath()


class MapFunctions:

    def __init__(self):

        self.map_data = [
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 1],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
            [0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
            [0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
            [0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
            [0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
            [0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
            [0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
            [0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
            [0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
            [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
            [0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
            [0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
            [0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
            [0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
            [0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
            [0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
            [0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
            [0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 1],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1, 1, 1],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 1, 1],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
        ]

        self.cell_data = [
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, "t", 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, "t", 1, "l", 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, "t", 1, 1, 1, "l", 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, "t", 1, 1, 1, 1, 1, "l", 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, "t", 1, 1, 1, 1, 1, 1, 1, "l", 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, "t", 1, 1, 1, 1, 1, 1, 1, 1, 1, "l", 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, "t", 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, "l", 0],
            [0, 0, 0, 0, 0, 0, 0, 0, "t", 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, "l", 0],
            [0, 0, 0, 0, 0, 0, 0, "t", 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, "l", 0],
            [0, 0, 0, 0, 0, 0, "t", 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, "l", 0],
            [0, 0, 0, 0, 0, "t", 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, "l", 0],
            [0, 0, 0, 0, "t", 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, "l", 0],
            [0, 0, 0, "t", 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, "l", 0],
            [0, 0, "t", 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, "l", 0],
            [0, "r", 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, "l", 0],
            [0, 0, "r", 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, "b", 0],
            [0, 0, 0, "r", 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, "b", 0],
            [0, 0, 0, 0, "r", 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, "b", 0],
            [0, 0, 0, 0, 0, "r", 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, "b", 0],
            [0, 0, 0, 0, 0, 0, "r", 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, "b", 0],
            [0, 0, 0, 0, 0, 0, 0, "r", 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, "b", 0],
            [0, 0, 0, 0, 0, 0, 0, 0, "r", 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, "b", 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, "r", 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, "b", 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, "r", 1, 1, 1, 1, 1, 1, 1, 1, 1, "b", 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, "r", 1, 1, 1, 1, 1, 1, 1, "b", 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, "r", 1, 1, 1, 1, 1, "b", 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, "r", 1, 1, 1, "b", 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, "r", 1, "b", 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, "b", 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        ]

    def create_map(self, Game):
        self.Game = Game

        # map_data = [
        # [left_top],
        # [right_top, left_bottom],
        # [right_bottom],
        cells_dict = dict()
        borders_left = dict()  # BUG: when using only one border, miss one cell
        borders_top = dict()
        borders_right = dict()
        borders_bottom = dict()

        for row_nb, row in enumerate(self.cell_data):
            for col_nb, tile in enumerate(row):

                if tile != 0:
                    position = fp.cell_to_pos((row_nb, col_nb))

                    current_cell = Cell(
                        Game,
                        size=(cell_sizes[0], cell_sizes[1]),
                        position=position,
                        function=None
                    )

                    if tile == 1:
                        current_cell.function = Game.character.dest
                        cells_dict[(row_nb, col_nb)] = current_cell
                        current_cell.alpha_off = 100

                    elif tile == "l":
                        current_cell.function = Game.border_left
                        current_cell.alpha_off = 0
                        borders_left[(row_nb, col_nb)] = current_cell

                    elif tile == "t":
                        current_cell.function = Game.border_top
                        current_cell.alpha_off = 0
                        borders_top[(row_nb, col_nb)] = current_cell

                    elif tile == "r":
                        current_cell.function = Game.border_right
                        current_cell.alpha_off = 0
                        borders_right[(row_nb, col_nb)] = current_cell

                    elif tile == "b":
                        current_cell.function = Game.border_bottom
                        current_cell.alpha_off = 0
                        borders_bottom[(row_nb, col_nb)] = current_cell

        # borders_left[(1, 15)] = self._add_border_cell(Game, (1, 15), "l")
        # borders_top[(15, 1)] = self._add_border_cell(Game, (15, 1), "t")
        # borders_right[(29, 15)] = self._add_border_cell(Game, (29, 15), "r")
        # borders_bottom[(15, 29)] = self._add_border_cell(Game, (15, 29), "b")

        borders = dict()
        borders.update(borders_left)
        borders.update(borders_top)
        borders.update(borders_right)
        borders.update(borders_bottom)

        self._all_cells = [cells_dict, borders_left,
                           borders_top, borders_right,
                           borders_bottom, borders]

    def map_reset_cells(self, **kwargs):
        cell_data = kwargs.get("cell_data", self.cell_data)

        [cells_dict, borders_left, borders_top,
         borders_right, borders_bottom, borders] = self._all_cells

        [cells_dict, borders_left, borders_top,
         borders_right, borders_bottom, borders] = [
             dict(cells_dict), dict(borders_left),
             dict(borders_top), dict(borders_right),
             dict(borders_bottom), dict(borders)
             ]

        for row_nb, row in enumerate(cell_data):
            for col_nb, tile in enumerate(row):

                if tile == 0:
                    current_cell = cells_dict.get((row_nb, col_nb))

                    if current_cell is not None:
                        current_cell.reset()
                        current_cell.active = False

                elif tile == 1:
                    current_cell = cells_dict[(row_nb, col_nb)]
                    current_cell.reset()
                    current_cell.function = self.Game.character.dest
                    current_cell.alpha_off = 100

                elif tile == "l":
                    current_cell = borders_left[(row_nb, col_nb)]
                    current_cell.reset()
                    current_cell.function = self.Game.border_left
                    current_cell.alpha_off = 0

                elif tile == "t":
                    current_cell = borders_top[(row_nb, col_nb)]
                    current_cell.reset()
                    current_cell.function = self.Game.border_top
                    current_cell.alpha_off = 0

                elif tile == "r":
                    current_cell = borders_right[(row_nb, col_nb)]
                    current_cell.reset()
                    current_cell.function = self.Game.border_right
                    current_cell.alpha_off = 0

                elif tile == "b":
                    current_cell = borders_bottom[(row_nb, col_nb)]
                    current_cell.reset()
                    current_cell.function = self.Game.border_bottom
                    current_cell.alpha_off = 0

        borders = dict()
        borders.update(borders_left)
        borders.update(borders_top)
        borders.update(borders_right)
        borders.update(borders_bottom)

        return [cells_dict, borders_left, borders_top,
                borders_right, borders_bottom, borders]

    # def _add_border_cell(self, Game, pos, func=None):
    #     if func == "l":
    #         function = Game.border_left
    #     if func == "t":
    #         function = Game.border_top
    #     if func == "r":
    #         function = Game.border_right
    #     if func == "b":
    #         function = Game.border_bottom

    #     position = fp.cell_to_pos(pos)
    #     cell = Cell(Game, size=(cell_sizes[0], cell_sizes[1]),
    #         position=position, function=function
    #     )
    #     cell.alpha_off = 0

    #     return cell

    def create_maps(self, Game):

        self.all_maps = dict()

        self.create_map(Game)

        from .maps.map_0_0 import Map
        Map(self, Game)

        from .maps.map_0_1 import Map
        Map(self, Game)
    #
        from .maps.map_n1_0 import Map
        Map(self, Game)
    #
        from .maps.map_1_0 import Map
        Map(self, Game)
    #
        from .maps.map_0_n1 import Map
        Map(self, Game)
    #
        from .maps.map_1_1 import Map
        Map(self, Game)

        return self.all_maps
