import pygame as pg
from .interface_functions import NeededFunctions


def _fct_none(*args, **kwargs):
    pass


class Button:
    """buttons"""

    def __init__(self, Game, function=None, name=None, size=(1, 1)):
        self.Game = Game
        self.nf = NeededFunctions()

        if function is None:
            self.function = _fct_none
        else:
            self.function = function

        if name is not None:
            self.image, self.rect = self.nf.load_image(name)
        else:
            self.add_background(size)

        self.position = self.rect  # same id until clicked occured, then copy
        self.image_original = self.image

        self.state = False
        self.state_clicked = False
        self.is_hovered = False

        self.highligh = pg.Surface(self.rect.size)
        self.highligh.fill((255, 255, 255))
        self.highligh.set_alpha(10)

        self.text = ""

    def add_background(self, size):
        self._margin = 3
        self.image = pg.Surface(size)
        self.rect = self.image.get_rect()
        color = (185, 122, 87)  # brown
        color2 = (147, 90, 61)  # brown
        self.image.fill(color)
        pg.draw.rect(self.image, color2, self.rect, self._margin)
        self.image_original = self.image
        self.position = self.rect  # same id until clicked occured, then copy

    def add_image(self, *args, center=None):

        image, rect = self.nf.load_image(*args)
        if center is None:
            imagepos = image.get_rect(centery=self.rect.h/2,
                                      centerx=self.rect.w/2)
        else:
            imagepos = image.get_rect().center

        self.image.blit(image, imagepos)
        self.image_original = self.image

    def add_text(self, text, center=None):
        self.text = text
        font = pg.font.Font(None, 30)
        msg = font.render(text, 1, (10, 10, 10))

        if center is None:
            textpos = msg.get_rect(centery=self.rect.h/2,
                                   centerx=self.rect.w/2)
        else:
            textpos = msg.get_rect().center

        self.image.blit(msg, textpos)
        self.image_original = self.image

    def hovered(self):
        self.is_hovered = True
        self.image_original = self.image.copy()
        self.image.blit(self.highligh, self.highligh.get_rect())

        if self.state_clicked:
            self.change_size()

    def unhovered(self):
        self.is_hovered = False
        self.set_back_size()

    def clicked(self):
        # the not state alloyed to avoid clicking twice and add infinit offset
        if self.Game.mouse.state_clicking and not self.state_clicked:
            self.state_clicked = True
            self.change_size()

    def unclicked(self):
        was_clicked = True if self.state_clicked else False
        self.state_clicked = False
        self.set_back_size()

        if was_clicked and self.Game.mouse.hovering(self):
            self.hovered()
            self.state = True
            self.function(self.state)
        else:
            self.state = False

    def change_size(self):
        self.position = self.rect.copy()
        offset = 6
        self.image = pg.transform.scale(
            self.image, (self.rect.w - offset, self.rect.h - offset))
        self.rect.move_ip(offset/2, offset/2)

    def set_back_size(self):
        self.image = self.image_original
        self.rect = self.position

        self.position = self.rect  # same id from now
        self.image_original = self.image  # same id from now
