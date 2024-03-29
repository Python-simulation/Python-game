import pygame as pg
from .button import Button
from .background import BackGround


class FlyingMenu(BackGround):
    """Menu that pop when a npc is clicked"""

    def __init__(self, Owner, *args, background=False):
        """args being a list of all the elements that contain the menu.
        Each element can be a button, a background or any class containing
        a Rect and a image subclass"""
        self.Game = Owner.Game
        self.Owner = Owner
        BackGround.__init__(self)
        self._margin = 3  # (bottom = top = left = right = margin)
        self.items = args
        self.active = False
        self.background = background
        self.bg = BackGround(size=self.Game.size)
        self.bg.image.set_alpha(0)
        self.bg.clicked = self.clicked  # used to stop mouse if outside menu
        self.bg.hovered = self.hovered  # used to stop mouse if outside menu

    def _update_menu(self):
        extra_width = 2*self._margin
        height = 2*self._margin
        width_max = extra_width

        for item in self.items:
            width_temp = item.rect.w + extra_width
            height += item.rect.h

            if width_temp >= width_max:
                width_max = width_temp

        width = width_max
        self.image = pg.Surface((width, height))
        self.rect = self.image.get_rect()

        color = (185, 122, 87)  # brown
        self.image.fill(color)

        color2 = (147, 90, 61)  # brown
        pg.draw.rect(self.image, color2, self.rect, self._margin)

        self.image.set_alpha(200)

    def position(self, value):

        if value[0] < 0:
            value = (0, value[1])
        elif (value[0] + self.rect.w) > self.Game.size[0]:
            value = (self.Game.size[0]-self.rect.w, value[1])

        if value[1] < 0:
            value = (value[0], 0)
        elif (value[1] + self.rect.h
              + self.Game.lower_bar.rect.h - 19) > self.Game.size[1]:
            value = (value[0], (self.Game.size[1] - self.rect.h
                                - self.Game.lower_bar.rect.h + 19))

        self.rect.topleft = value
        height = 0
        topleft = (self.rect.topleft[0] + self._margin,
                   self.rect.topleft[1] + self._margin)

        for i, item in enumerate(self.items):
            item.rect.topleft = topleft
            # item.image.set_alpha(200)

            if i != 0:
                height += self.items[i-1].rect.h
                item.rect.y += height

    def activated(self):

        self.desactivated()  # reset and put menu on top of display # TODO: OBSOLETE: ?
        self.active = True
        # print("menu clicked", self.name, self)
        self._update_menu()

        topleft = (self.Owner.rect.centerx - self.rect.w/2,
                   self.Owner.rect.top - self.rect.h - 50)
        # topleft = (self.Owner.rect.center[0] - self.rect.w/2,
        #            self.Owner.rect.center[1] - self.rect.h/2)
        self.position(topleft)

        # if self not in self.Game.allsprites:  # could be used but meh
        if self.background:
            self.Game.allsprites.add(self.bg, layer=2)  # display

        self.Game.allsprites.add(self, layer=2)  # display
        self.Game.allsprites.add(self.items, layer=2)
        # reminder: allsprites does unclicked if clicked outside

    def desactivated(self):

        self.active = False
        # print("menu unclicked", self.name, self)
        if self.background:
            self.Game.allsprites.remove(self.bg)  # display

        self.Game.allsprites.remove(self)
        self.Game.allsprites.remove(self.items)

    def clicked(self):
        return True

    def hovered(self):
        return True