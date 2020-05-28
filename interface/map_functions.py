import os
import math
from math import pi
import pygame as pg
from .cell import Cell
from .chimp import Chimp
from .background import BackGround
from .character import Character
from .house import House

from .findpath import cell_size as cell_sizes


class MapFunctions:

    def all_maps(self, Game):

        name = os.path.join(Game.data_dir, 'background.png')
        background = BackGround(name)
        background.rect.center = Game.game_screen.rect.center
    #        for i in range(1, 1920):
    #            if 1920 % i == 0 and 1080 % i == 0:
    #                print(i)
        # posible pixel cell_size for the cell to have int for 1920 and 1080 :
        # 1, 2, 3, 4, 5, 6, 8, 10, 12, 15, 20, 24, 30, 40, 60, 120
        map_data = [
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
        # map_data = [
        # [left_top],
        # [right_top, left_bottom],
        # [right_bottom],
        (cell_size, cell_size_y) = cell_sizes
        cells_dict = dict()
        borders_left = dict() # BUG: when using only one border, miss one cell
        borders_top = dict()
        borders_right = dict()
        borders_bottom = dict()

        for row_nb, row in enumerate(map_data):
            for col_nb, tile in enumerate(row):
                cart_x = row_nb * cell_size/2
                cart_y = col_nb * cell_size/2  #x not a mistake
                iso_x = (cart_x - cart_y)
                iso_y = (cart_x + cart_y)/2

                if tile != 0:
                    current_cell = Cell(
                        Game,
                        size=(cell_size, cell_size_y),
                        position=(iso_x + 7.5*cell_size,
                                  iso_y - 7.5*cell_size_y),
                        function=None
                    )
                    if tile == 1:
                        current_cell.function=Game.character.dest
                        cells_dict[(row_nb, col_nb)] = current_cell
                        # print((row_nb, col_nb),
                              # (iso_x + 7.5*cell_size, iso_y - 7.5*cell_size_y))

                    elif tile == "l":
                        current_cell.function=Game.border_left
                        current_cell.alpha_off = 0
                        borders_left[(row_nb, col_nb)] = current_cell

                    elif tile == "t":
                        current_cell.function=Game.border_top
                        current_cell.alpha_off = 0
                        borders_top[(row_nb, col_nb)] = current_cell

                    elif tile == "r":
                        current_cell.function=Game.border_right
                        current_cell.alpha_off = 0
                        borders_right[(row_nb, col_nb)] = current_cell

                    elif tile == "b":
                        current_cell.function=Game.border_bottom
                        current_cell.alpha_off = 0
                        borders_bottom[(row_nb, col_nb)] = current_cell

        borders = dict()
        borders.update(borders_left)
        borders.update(borders_top)
        borders.update(borders_right)
        borders.update(borders_bottom)

        chimp = Chimp(Game)
        file_name = os.path.join(Game.data_dir, "npc.png")
        npc = Character(Game, file_name)
        npc.rect.midbottom = (5*cell_size+cell_size/2,
                              5*cell_size_y+cell_size_y/2)
        npc.allowed_mvt(1)
        # npc._npc_time = 0.1
        # show = BackGround(size=npc.area.size)
        # show.rect.topleft = npc.area.topleft

        npc_2 = Character(Game, file_name)
        npc_2.rect.midbottom = (10*cell_size+cell_size/2,
                              6*cell_size_y+cell_size_y/2)
        npc_2.allowed_mvt(1)

        sprites = pg.sprite.RenderPlain((
                chimp,
                # show,
                npc,
                npc_2,
                ))

        map_0_0 = {"background": background,
                   "cells": cells_dict,
                   "borders": borders,
                   "sprites": sprites}

    #
        name = os.path.join(Game.data_dir, 'background2.png')
        background2 = BackGround(name)
        background2.rect.center = Game.game_screen.rect.center

        chimp2 = Chimp(Game)
        chimp2.speed_x = 10
        sprites = pg.sprite.RenderPlain((
                chimp2,
                ))

        map_n1_0 = {"background": background2,
                    "cells": cells_dict,
                    "borders": borders_right,
                    "sprites": sprites}

    #
        sprites = pg.sprite.RenderPlain()

        map_1_0 = {"background": background2,
                   "cells": cells_dict,
                   "borders": borders_left,
                   "sprites": sprites}

    #
        name = os.path.join(Game.data_dir, 'background2.png')
        background3 = BackGround(name)
        background3.rect.center = Game.game_screen.rect.center

        position = (1*cell_sizes[0],
                    1*cell_sizes[1])
        cells_dict2 = dict(cells_dict)
        house = House(Game, background3, position, cells_dict2, borders_top)
        sprites = pg.sprite.RenderPlain()

        map_0_1 = {"background": background3,
                   "cells": cells_dict2,
                   "borders": borders_top,
                   "sprites": sprites}

    #
        cells_dict2 = dict(cells_dict)
        cells_dict2.pop((11, 15))
        name = os.path.join(Game.data_dir, 'tree.png')
        tree = BackGround(name, -1)
        tree.rect.midbottom = (5*cell_sizes[0]+cell_sizes[0]/2,
                               5*cell_sizes[1]+cell_sizes[1]/2)
        # borders_bottom.update({(5, 5):[tree]})

        sprites = pg.sprite.RenderPlain(tree)
        map_0_n1 = {"background": background2,
                    "cells": cells_dict2,
                    "borders": borders_bottom,
                    "sprites": sprites}

        all_maps = {
                (0, 0): map_0_0,
                (-1, 0): map_n1_0,
                (1, 0): map_1_0,
                (0, 1): map_0_1,
                (0, -1): map_0_n1,
                house.inside: house.map
                    }
        return all_maps
