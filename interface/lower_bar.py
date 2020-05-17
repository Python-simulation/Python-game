import os
import pygame as pg
import numpy as np
from .background import BackGround
from .button import Button
from .interface_functions import NeededFunctions


class LowerBar:
    """Lower tool bar"""

    def __init__(self, Game):
        self.Game = Game
        nf = NeededFunctions()

        name = os.path.join(self.Game.data_dir, 'lower_bar.png')
        self.lower_tool_bar = BackGround(name, -1)
        self.lower_tool_bar.rect.midbottom = self.Game.game_screen.rect.midbottom

        name = os.path.join(self.Game.data_dir, 'button_1.png')
        self.button_1 = Button(self.Game, nf.function_test, name)
        self.button_1.add_text("button 1")  # , center = (0,0)
        self.button_1.rect.midbottom = self.lower_tool_bar.rect.midbottom
        self.button_1.rect.y -= 12
        self.button_1.rect.left = 950

        self.button_2 = Button(self.Game, nf.function_test2, name)
        inventory_image = os.path.join(self.Game.data_dir, 'inventory.png')
        self.button_2.add_image(inventory_image, -1)  # , center = (0,0)
        self.button_2.rect.midbottom = self.lower_tool_bar.rect.midbottom
        self.button_2.rect.y -= 12
        self.button_2.rect.left = 1072

        self.buttons = [
                self.button_1,
                self.button_2,
                ]