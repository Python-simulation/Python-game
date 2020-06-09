import os
from .npc import Npc
from ..findpath import FindPath
from ..findpath import cell_sizes
from ..flying_menu import FlyingMenu
from ..button import Button

fp = FindPath()


class SomeGuy(Npc):
    def __init__(self, Game, cell_pos):
        self.Game = Game
        file_name = os.path.join(Game.data_dir, "npc.png")
        Npc.__init__(self, Game, file_name, cell_pos)

        self.allowed_mvt(2, 1)
        self.max_speed = 5
        self._npc_time = 1

        name = os.path.join(self.Game.data_dir, 'button_2.png')
        talk = Button(self.Game, self.dialog, name)
        talk.add_text("talk")

        self.menu = FlyingMenu(self.Game, talk)

    def hovered(self):
        self.message.text("I'm a special npc! I can talk!")
        self.message.hovered()
        pass

    def unhovered(self):
        self.message.unhovered()
        pass

    def clicked(self):
        self.menu.clicked()
        pass

    def unclicked(self):
        self.menu.unclicked()
        pass

    def dialog(self, *args):
        self.message.text("Well, I can't actualy")
        self.message.hovered()
        pass