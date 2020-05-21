import os
from interface.cell import Cell
import pygame as pg
from interface.chimp import Chimp
from .background import BackGround
from .interface_functions import NeededFunctions
from .character import Character

nf = NeededFunctions()


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

        cell_size = 60
        cells_dict = dict()
        for x in range(1, 32-1):
            for y in range(1, 18-1-2):  # -2 because not 16/9 :'( damn lowerbar
                current_cell = Cell(
                    Game,
                    size=(cell_size, cell_size),
                    position=(x*cell_size+cell_size/2, y*cell_size+cell_size/2),
                    function=Game.character.dest
                )
    #            text = str((x, y))
    #            txt_position = Game.mouse.rect.center
    #            current_cell.message = display_info(Game, text, txt_position)
                cells_dict[(x, y)] = current_cell

        borders_left = dict()
        x = 0
        for y in range(1-1, 18-2-1+1):  # -2 because not 16/9 :'( damn lowerbar
            current_cell = Cell(
                Game,
                size=(cell_size, cell_size),
                position=(x*cell_size+cell_size/2, y*cell_size+cell_size/2),
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
                size=(cell_size, cell_size),
                position=(x*cell_size+cell_size/2, y*cell_size+cell_size/2),
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
                size=(cell_size, cell_size),
                position=(x*cell_size+cell_size/2, y*cell_size+cell_size/2),
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
                size=(cell_size, cell_size),
                position=(x*cell_size+cell_size/2, y*cell_size+cell_size/2),
                function=Game.border_bottom
            )
            current_cell.alpha_off = 0
            borders_bottom[(x, y)] = current_cell
            # borders_bottom.append(current_cell)

        borders = dict()
        borders.update(borders_left)
        borders.update(borders_top)
        borders.update(borders_right)
        borders.update(borders_bottom)

        chimp = Chimp(Game)
        file_name = os.path.join(Game.data_dir, "npc.png")
        npc = Character(Game, file_name)
        npc.rect.midbottom = (10*cell_size+cell_size/2,
                              5*cell_size+cell_size/2)
        npc.area = pg.Rect(npc.rect.topleft,
                           (cell_size*3, cell_size*3))
        # npc._npc_time = 1
        npc_2 = Character(Game, file_name)
        npc_2.rect.midbottom = (16*cell_size+cell_size/2,
                              6*cell_size+cell_size/2)
        npc_2.area = pg.Rect(npc_2.rect.topleft,
                           (cell_size*3, cell_size*3))

        sprites = pg.sprite.RenderPlain((
                chimp,
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

        map_0_1 = {"background": background2,
                   "cells": cells_dict,
                   "borders": borders_top,
                   "sprites": sprites}

        cells_dict2 = dict(cells_dict)
        cells_dict2.pop((5, 5))
        name = os.path.join(Game.data_dir, 'tree.png')
        tree = BackGround(name, -1)
        tree.rect.midbottom = (5*cell_size+cell_size/2, 5*cell_size+cell_size/2)
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
