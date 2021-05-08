import os
import pygame as pg
from .background import BackGround
from .button import Button
from .interface_functions import NeededFunctions


class LowerBar(BackGround):
    """Lower tool bar"""

    def __init__(self, Game):

        self.Game = Game
        nf = NeededFunctions()

        name = os.path.join(self.Game.data_dir, 'lower_bar.png')

        super().__init__(name, -1)
        self.rect.midbottom = self.Game.game_screen.rect.midbottom

        self.button_1 = Button(self.Game, nf.function_test, size=(100, 100))
        self.button_1.add_text("button 1")  # , center = (0,0)
        self.button_1.rect.midbottom = self.rect.midbottom
        self.button_1.rect.y -= 12
        self.button_1.rect.left = 950

        self.button_2 = Button(self.Game, nf.function_test2, size=(100, 100))
        inventory_image = os.path.join(self.Game.data_dir, 'inventory.png')
        self.button_2.add_image(inventory_image, -1)  # , center = (0,0)
        self.button_2.rect.midbottom = self.rect.midbottom
        self.button_2.rect.y -= 12
        self.button_2.rect.left = 1072

        self.buttons = [
                self.button_1,
                self.button_2,
                ]
