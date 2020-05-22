import pygame as pg


class FlyingMenu(pg.sprite.Sprite):
    """Menu that pop when a npc is clicked"""

    def __init__(self, Game, *args):
        """args being a list of all the buttons that contain the menu.
        Each element can be a button, a background or any class containing
        a Rect and a image subclass"""
        self.Game = Game
        pg.sprite.Sprite.__init__(self)

        self._margin = 3  # (bottom = top = left = right = margin)
        self.buttons = args

    def _update_menu(self):
        width = 2*self._margin
        height = 2*self._margin

        for button in self.buttons:
            width_temp = button.rect.w + 2*self._margin
            height += button.rect.h

            if width_temp >= width:
                width = width_temp

        self.image = pg.Surface((width, height))
        self.rect = self.image.get_rect()
        self.rect.topleft = self.buttons[0].rect.topleft
        color = (185, 122, 87)  # brown
        self.image.fill(color)
        self.image.set_alpha(200)

    def position(self, value):
        self.rect.topleft = value
        height = 0

        for i, button in enumerate(self.buttons):
            button.rect.topleft = (self.rect.topleft[0] + self._margin,
                                   self.rect.topleft[1] + self._margin)
            button.image.set_alpha(200)
            if i != 0:
                height += self.buttons[i-1].rect.h
                button.rect.y += height

    def clicked(self):
        self._update_menu()
        self.position(self.Game.mouse.rect.topleft)
        self.Game.allsprites.add(self)
        self.Game.all_buttons.extend(self.buttons)

    def unclicked(self):
        for button in self.buttons:
            try:
                self.Game.all_buttons.remove(button)
            except ValueError:
                pass
        self.Game.allsprites.remove(self)
