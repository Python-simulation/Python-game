import os
from .npc import Npc
# from ..findpath import FindPath
# from ..findpath import cell_sizes
from ..flying_menu import FlyingMenu
from ..button import Button

# from ..background import BackGround
# fp = FindPath()


class SomeGuy(Npc):
    def __init__(self, Game, cell_pos):
        self.Game = Game
        file_name = os.path.join(Game.data_dir, "npc.png")
        Npc.__init__(self, Game, file_name, cell_pos)

        self.allowed_mvt(2, 1)
        self.max_speed = 5
        self._npc_time = 1

        # talk = Button(self.Game, self.dialog, size=(100, 50))
        # talk.add_background((100, 100))
        # talk.add_text("talk")

        # test = BackGround(size=(100, 100))

        self.menu = FlyingMenu(self)##, talk)
        self.menu.name = "first"
        # self.menu_dialog = FlyingMenu(self.menu, diag, diag_stop)
        # self.menu_dialog.name = "second"

    def hovered(self):
        if not self.menu.active:
            self.message.text("I'm a special npc! I can talk!")
            self.message.hovered()
        pass

    def unhovered(self):
        self.message.unhovered()
        pass

    def clicked(self):
        # TODO but not for dialog?: make a menu like the pause one to prevent any mvt or anything that could be hard to solve (like closing the menu)
        if not self.menu.active:
            talk = Button(self.Game, self.dialog, size=(100, 50))
            # talk.add_background((100, 100))
            talk.add_text("talk")

            self.menu.items = (talk, )
            self.menu.activated()
        pass

    def unclicked(self):
        # use directly self.rect.hitbox.colliderect(target.rect) ?
        if not self.Game.mouse.clicking(self.menu):
            # print("desac from unclicked")
            # print(self.menu.rect)
            self.menu.desactivated()  # if keep activated instead of clicked, must never kill a npc without doing desactivated menu
        pass

    def dialog(self, *args):
        # self.kill()  # show the possible bug if npc is kill without closing the dialog
        # print("desac from dialog")
        self.menu.desactivated()
        diag = Button(self.Game, size=(600, 100))
        diag.add_text("Temporary button, need to be replace by pure text")
        diag_continue = Button(self.Game, size=(100, 50))
        diag_continue.add_text("Continue")

        diag_stop = Button(self.Game, self.stop_dialog, size=(150, 50))
        diag_stop.add_text("Stop talking")

        self.menu.items = (diag, diag_stop)
        self.menu.activated()

    def stop_dialog(self, *args):
        # print("desac from buton")
        self.menu.desactivated()
        pass
