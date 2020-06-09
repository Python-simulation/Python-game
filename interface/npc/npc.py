import random
import pygame as pg
from ..findpath import FindPath
from ..findpath import cell_sizes
from .character import Character
from ..display import display_info

fp = FindPath()


class Npc(Character):
    """moves a character across the screen."""

    def __init__(self, Game, file_name, cell_pos,
                 cardinal=4, frames=6, anim_time=0.1):
        Character.__init__(self, Game, file_name, cell_pos,
                 cardinal=4, frames=6, anim_time=0.1)

        self._npc_clock = 0
        self._npc_time = 10
        self.allowed_mvt()

        text = "I'm a basic npc!"
        txt_position = self.Game.mouse.rect.topleft
        self.message = display_info(self.Game, text, txt_position)

    def update(self, dt):  # implicitly called from allsprite update
        """walk depending on the character state"""

        if self.moving:
            self.change_order()
            self._walk(dt)

        else:
            self._auto_dest(dt)
            pass

    def _auto_dest(self, dt):
        self._npc_clock += dt
        char_pos = (self.rect.midbottom[0],
                    self.rect.midbottom[1]-cell_sizes[1]/2)

        left_mvt = (char_pos[0]
                    - self.area.left) // (cell_sizes[0]/2)
        right_mvt = (self.area.right
                     - char_pos[0]) // (cell_sizes[0]/2)
        up_mvt = (char_pos[1]
                  - self.area.top) // (cell_sizes[1]/2)
        bottom_mvt = (self.area.bottom
                      - char_pos[1]) // (cell_sizes[1]/2)

        if left_mvt > self._npc_nbr_cell:
            left_mvt = self._npc_nbr_cell
        if right_mvt > self._npc_nbr_cell:
            right_mvt = self._npc_nbr_cell
        if up_mvt > self._npc_nbr_cell:
            up_mvt = self._npc_nbr_cell
        if bottom_mvt > self._npc_nbr_cell:
            bottom_mvt = self._npc_nbr_cell

        cells = (0, 0)

        if self._npc_clock > self._npc_time:
            self._npc_clock = 0

            cells = (random.randint(-left_mvt, right_mvt),
                     random.randint(-up_mvt, bottom_mvt))

            if (abs(cells[0]) + abs(cells[1])) > self._npc_nbr_cell:
                if random.randint(0, 1) == 0:
                    cells = (0, cells[1])
                else:
                    cells = (cells[0], 0)

            position = (self.rect.midbottom[0],
                        self.rect.midbottom[1] - cell_sizes[1]/2)
            cell_pos = fp.pos_to_cell(position)
            new_cell_pos = (cell_pos[0] + cells[0],
                            cell_pos[1] + cells[1])
            moving_to_pos = fp.cell_to_pos(new_cell_pos)

            self.dest(moving_to_pos)

    def allowed_mvt(self, allowed_cell=0, authorized_mvt=1):
        self._npc_nbr_cell = authorized_mvt
        char_pos = (self.rect.midbottom[0],
                    self.rect.midbottom[1]-cell_sizes[1]/2)

        topleft = (char_pos[0] - allowed_cell*cell_sizes[0]/2,  # OPTIMIZE: not defined by char position, but absolute position
                   char_pos[1] - allowed_cell*cell_sizes[1]/2)
        self.area = pg.Rect(topleft,
                            (allowed_cell*cell_sizes[0],
                             allowed_cell*cell_sizes[1]))

    def hovered(self):
        # self.message.text("I'm a basic npc !")
        self.message.hovered()
        pass

    def unhovered(self):
        self.message.unhovered()
        pass