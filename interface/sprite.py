import pygame as pg
from .interface_functions import NeededFunctions
from .findpath import FindPath
from .findpath import cell_sizes
from .background import BackGround

nf = NeededFunctions()
fp = FindPath()


class Sprite(BackGround):

    def __init__(self, Game, Map, file_name, cell_pos):
        self.Game = Game
        self.Map = Map
        BackGround.__init__(self, file_name, -1)

        self.cell_pos = cell_pos
        position = fp.cell_to_pos(cell_pos)
        position = (position[0],
                    position[1] + cell_sizes[1]/2)
        self.rect.midbottom = position

    def update(self, dt):
        # TODO : add function that look if this sprite overlap with an other
        pass

    def refresh(self):
        self.Map.cells_dict.pop(self.cell_pos,
                                self.Map.borders.pop(self.cell_pos, None))
