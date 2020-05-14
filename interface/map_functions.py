import os
from interface.cell import Cell
import pygame as pg
from interface.chimp import Chimp
from .background import BackGround
from .interface_functions import NeededFunctions

nf = NeededFunctions()


class MapFunctions:
    def all_maps(self, Game):

        name = os.path.join(Game.data_dir, 'background.png')
        background = BackGround(name)
        background.rect.center = Game.game_screen.rect.center
    #        for i in range(1, 1920):
    #            if 1920 % i == 0 and 1080 % i == 0:
    #                print(i)
        # posible pixel size for the cell to have int for 1920 and 1080 :
        # 1, 2, 3, 4, 5, 6, 8, 10, 12, 15, 20, 24, 30, 40, 60, 120

        size = 60
        cells_dict = dict()
        for x in range(1, 32-1):
            for y in range(1, 18-1-2):  # -2 because not 16/9 :'( damn lowerbar
                current_cell = Cell(
                    Game,
                    size=(size, size),
                    position=(x*size+size/2, y*size+size/2),
                    function=Game.character.dest
                )
    #            current_cell.position_label = (x, y)  # useless
    #            text = str((x, y))
    #            txt_position = Game.mouse.rect.center
    #            current_cell.message = display_info(Game, text, txt_position)
                cells_dict[(x, y)] = current_cell

        borders_left = dict()
        x = 0
        for y in range(1-1, 18-2-1+1):  # -2 because not 16/9 :'( damn lowerbar
            current_cell = Cell(
                Game,
                size=(size, size),
                position=(x*size+size/2, y*size+size/2),
                function=Game.border_left
            )
            current_cell.alpha_off = 0
            borders_left[(x, y)] = current_cell
            # borders_left.append(current_cell)

        borders_top = dict()
        y = 0  # -2 because not 16/9 :'( damn lowerbar
        for x in range(1, 32-1):
            current_cell = Cell(
                Game,
                size=(size, size),
                position=(x*size+size/2, y*size+size/2),
                function=Game.border_top
            )
            current_cell.alpha_off = 0
            borders_top[(x, y)] = current_cell
            # borders_top.append(current_cell)

        borders_right = dict()
        x = 32-1
        for y in range(1-1, 18-2-1+1):  # -2 because not 16/9 :'( damn lowerbar
            current_cell = Cell(
                Game,
                size=(size, size),
                position=(x*size+size/2, y*size+size/2),
                function=Game.border_right
            )
            current_cell.alpha_off = 0
            borders_right[(x, y)] = current_cell
            # borders_right.append(current_cell)

        borders_bottom = dict()
        y = 18-2-1  # -2 because not 16/9 :'( damn lowerbar
        for x in range(1, 32-1):
            current_cell = Cell(
                Game,
                size=(size, size),
                position=(x*size+size/2, y*size+size/2),
                function=Game.border_bottom
            )
            current_cell.alpha_off = 0
            borders_bottom[(x, y)] = current_cell
            # borders_bottom.append(current_cell)

        borders = dict()
        # Cell(Game, size=(40, 40), position=(500, 100),
        #      function=Game.character.dest),
        # Cell(Game, size=(40, 40), position=(800, 200),
        #      function=Game.character.dest),
        # Cell(Game, size=(40, 40), position=(1000, 300),
        #      function=Game.character.dest),
        # Cell(Game, size=(40, 40), position=(100, 700),
        #      function=nf.function_test),
        # ]
        borders.update(borders_left)
        borders.update(borders_top)
        borders.update(borders_right)
        borders.update(borders_bottom)

        chimp = Chimp(Game)
        sprites = pg.sprite.RenderPlain((
                chimp,
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

        map_0_1 = {"background": background2,
                   "cells": cells_dict,
                   "borders": borders_top,
                   "sprites": sprites}

        cells_dict2 = dict(cells_dict)
        cells_dict2.pop((5, 5))
        name = os.path.join(Game.data_dir, 'tree.png')
        tree = BackGround(name, -1)
        tree.rect.midbottom = (5*size+size/2, 5*size+size/2)
        # borders_bottom.update({(5, 5):[tree]})
        sprites = pg.sprite.RenderPlain()
        sprites.add(tree)
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
                    }
        return all_maps
