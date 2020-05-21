import pygame as pg


class FlyingMenu(pg.sprite.Sprite):
    """Menu that pop when a npc is clicked"""

    def __init__(self, Game, *args):
        self.Game = Game
        pg.sprite.Sprite.__init__(self)
        self.buttons = list()

        for button in args:
            self.add_button(button)

    def remove_button(self, target_button):
        try:
            self.buttons.remove(target_button)
            self._update_menu()
        except ValueError:
            pass

    def add_button(self, new_button):
        self.buttons.append(new_button)
        self._update_menu()

    def _update_menu(self):
        self.border = 5
        width = self.border
        height = self.border

        for button in self.buttons:
            width_temp = button.rect.w + self.border
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
            button.rect.topleft = (self.rect.topleft[0] + self.border/2,
                                   self.rect.topleft[1] + self.border/2)
            button.image.set_alpha(200)
            if i != 0:
                height += self.buttons[i-1].rect.h
                button.rect.y += height

    def clicked(self):
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
