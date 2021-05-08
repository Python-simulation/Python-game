import os
import pygame as pg
from .display import Display
from .interface_functions import NeededFunctions
from .findpath import FindPath

nf = NeededFunctions()
fp = FindPath()
cell_sizes = fp.cell_sizes


class Cell(pg.sprite.Sprite):
    """simple cell to target movement"""

    def __init__(self, Game, size, position, function=None):
        self.Game = Game
        pg.sprite.Sprite.__init__(self)
        # self.image = pg.Surface(size)

        name = os.path.join(Game.data_dir, 'hover.png')
        self.image, self.rect = nf.load_image(name, -1)
        self.rect = self.image.get_rect()
        self.rect.center = position
        self.cell_pos = fp.pos_to_cell(position)

        # text = "Display path"
        # txt_position = self.Game.mouse.rect.topleft
        # self.message = Display(self.Game, text, txt_position)

        self.reset()
        self.function = function
        # Note that a normal cell will have a self.Game.character.dest function

    def reset(self):
        self.function = None
        # color = (50, 50, 50)
        self.alpha_off = 0  # error if != 0 and change map
        self.alpha_on = 200
        # self.alpha_off = 10 # good
        # self.alpha_on = 50
        # self.image.fill(color)
        self.image.set_alpha(self.alpha_off)
        self.state = False
        self.active = True
        self.road = list()
        self.show_path = True
        # self.message.text("reset")
        self.Game.allsprites.remove(self)  # BUG: if want to see, can be proble

    def check_real_pos(self, redirection):

        other_cell = False

        mouse_pos = self.Game.mouse.rect.topleft

        if mouse_pos[1] < self.rect.centery:
            if mouse_pos[0] > self.rect.centerx:
                y2 = self.rect.midtop[1] + (mouse_pos[0]-self.rect.midtop[0])/2
                if mouse_pos[1] < y2:
                    shift = (0, -1)
                    # print("upright")
                    other_cell = True
                pass
            else:
                y2 = self.rect.midtop[1] + (self.rect.midtop[0]-mouse_pos[0])/2
                if mouse_pos[1] < y2:
                    shift = (-1, 0)
                    # print("upleft")
                    other_cell = True
                pass

        else:
            if mouse_pos[0] > self.rect.centerx:
                y2 = self.rect.center[1] + (self.rect.right - mouse_pos[0])/2
                if mouse_pos[1] > y2:
                    shift = (1, 0)
                    # print("bottomright")
                    other_cell = True
                pass
            else:
                y2 = self.rect.center[1] + (mouse_pos[0] - self.rect.left)/2
                if mouse_pos[1] > y2:
                    shift = (0, 1)
                    # print("bottomleft")
                    other_cell = True
                pass

        if other_cell:
            real_cell = (self.cell_pos[0] + shift[0],
                         self.cell_pos[1] + shift[1])

            if redirection == "hovered":
                try:
                    self.Game.all_cells[real_cell].hovered()
                except KeyError:
                    other_cell = False
                    pass
            elif redirection == "clicked":
                try:
                    self.Game.all_cells[real_cell].clicked()
                except KeyError:
                    other_cell = False
                    pass

        return other_cell

    def update(self, dt):
        """by default, if function returns nothing, consider the cell has done
        its purpuse and set state to False. If function exist, check every dt
        if the function return True."""
        if self.function is not None and self.state:
            output = self.function(self.rect.center)

            if output in (True, None):
                self.state = False

    def hovered(self):  # OPTIMIZE: temporary for development
        # return
        if not self.show_path:
            return True

        if not self.check_real_pos("hovered"):
            self.image.set_alpha(self.alpha_on)
            char_pos = self.Game.character.rect.midbottom
            begin_pos = (char_pos[0],
                          char_pos[1] - cell_sizes[1]/2)
            self.road = fp.find_path(self.Game.all_cells,
                                     begin_pos, self.rect.center,
                                     cardinal=self.Game.character.cardinal)

            for next_cell in self.road:
                unit_pos = fp.pos_to_cell(next_cell)

                try:
                    self.Game.allsprites.add(self.Game.cells[unit_pos], layer=0)
                    # self.message.text(str(unit_pos))
                except KeyError:
                    # self.message.text("")
                    pass

            # self.message.activated()

        pg.mouse.set_cursor(*pg.cursors.diamond)
        return True

    def unhovered(self):
        if not self.show_path:
            return

        self.image.set_alpha(self.alpha_off)

        for next_cell in self.road:
            unit_pos = fp.pos_to_cell(next_cell)

            try:
                self.Game.allsprites.remove(self.Game.cells[unit_pos])
                # rect = self.Game.cells[unit_pos].rect
                # self.Game.game_screen.image.blit(
                #     self.Game.background_screen.image,
                #     rect, rect)
            except KeyError:
                pass
        self.road = list()
        # self.message.desactivated()

    def clicked(self):
        for cell in self.Game.all_cells.values():
            cell.state = False

        if not self.check_real_pos("clicked") and self.active:
            self.state = True

        return True

    def unclicked(self):
        # print("cell unclicked")
        pass
        # self.state = False

    def _overwrite_clicked(self):
        self.state = True
