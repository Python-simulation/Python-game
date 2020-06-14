import os
from .npc import Npc
# from ..findpath import FindPath
# from ..findpath import cell_sizes
from ..flying_menu import FlyingMenu
from ..button import Button
from ..text import Text, text_tuple


class SomeGuy(Npc):
    def __init__(self, Game, cell_pos):
        self.Game = Game
        file_name = os.path.join(Game.data_dir, "npc.png")
        Npc.__init__(self, Game, file_name, cell_pos)

        self.authorized_mvt_save = 1
        self.allowed_mvt(2, self.authorized_mvt_save)
        self.max_speed = 5
        self.npc_time = 1

        self.quest_indicator = Text("!", size=(11, 30))

        self.name = "Character Name"

        name = Text(self.name)  #, size=(600, 30)) # must have the higher width
        name.add_highlight()

        gap_1 = Text(size=(name.rect.w, 10))
        gap_1.add_highlight()

        diag_hi = Text("Hello there!", size=(150, 30))

        text = (
            # "1234567890123456789012345678901234567890123456789012F "
            "The quest description could be long. And can be on several lines "
            "and is automatically cut to fit the given width. "
            "You can see that there is no limit in the length. "
            "In fact, it can be bad to have long text. And a better solution "
            "could be to create a new window with button to continue the "
            "text automatically."
        )
        diag_description = text_tuple(text)  #, size=(600, 30))

        rep_hi = Button(self.Game, self.dialog, size=(150, 50))
        rep_hi.add_text("Hi!")

        diag_ask = Text("Do you want to help me ?", size=(400, 30))

        diag_acept = Button(self.Game, self.accept_mission, size=(150, 50))
        diag_acept.add_text("Yes!")

        rep_refuse = Button(self.Game, self.refuse_mission, size=(150, 50))
        rep_refuse.add_text("No!")

        diag_bye_no = Text("Maybe later then!", size=(300, 30))

        diag_bye_yes = Text("Thank you!", size=(300, 30))

        rep_continue = Button(self.Game, self.dialog, size=(250, 50))
        rep_continue.add_text("I'm listening")

        rep_stop = Button(self.Game, self.stop_dialog, size=(150, 50))
        rep_stop.add_text("Good bye!")

        diag_reminder = Text("Don't forget my request!", size=(300, 30))

        rep_reminder = Button(self.Game, self.stop_dialog, size=(150, 50))
        rep_reminder.add_text("I'm still on it!")

        gap_2 = Text(size=(0, 10))

        self.menu = FlyingMenu(self)

        self.start_mission = [
            (gap_1, name, gap_2, diag_hi, rep_hi),
            (gap_1, name, gap_2, *diag_description, rep_continue),
            (gap_1, name, gap_2, diag_ask, diag_acept, rep_refuse),
            (gap_1, name, gap_2, diag_bye_no, rep_stop),
            (gap_1, name, gap_2, diag_bye_yes, rep_stop),
            (gap_1, name, gap_2, diag_reminder, rep_reminder),
            ]

        self.diag_index = 0
        self.mission_accepted = False

    def update(self, dt):
        Npc.update(self, dt)

        if not self.mission_accepted:
            self.quest_indicator.rect
            self.quest_indicator.rect.bottomleft = (self.rect.centerx - 3,
                                                    self.rect.top - 3)
            self.Game.allsprites.add(self.quest_indicator)
        else:
            self.Game.allsprites.remove(self.quest_indicator)
        pass

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
            self.allowed_mvt(self.allowed_cell, 0)
            if not self.mission_accepted:
                self.diag_index = 0 # redondant
                # TODO : add a freeze character function into Npc. Must also set frame to face
                self.menu.items = self.start_mission[self.diag_index]  # replace by 0 ? or not if want memory
                self.menu.activated()
            else:
                self.diag_index = 5 # redondant
                self.menu.items = self.start_mission[self.diag_index]  # replace by 0 ? or not if want memory
                self.menu.activated()
        pass

    def unclicked(self):
        if not self.Game.mouse.clicking(self.menu):
            # print("desac from unclicked")
            self.stop_dialog()  # if keep activated instead of clicked, must never kill a npc without doing desactivated menu
        pass

    def stop_dialog(self, *args):
        # print("desac from buton")
        self.menu.desactivated()
        self.diag_index = 0
        self.allowed_mvt(self.allowed_cell, self.authorized_mvt_save)
        pass

    def dialog(self, *args):
        # self.kill()  # show the bug if npc is kill without closing the dialog
        # print("desac from dialog")
        self.menu.desactivated()
        self.diag_index += 1

        self.menu.items = self.start_mission[self.diag_index]
        self.menu.activated()

    def accept_mission(self, *args):
        # print("desac from buton")
        self.diag_index += 1
        self.mission_accepted = True
        # print("implement adding the mission here")
        self.dialog()
        pass

    def refuse_mission(self, *args):
        # print("desac from buton")
        self.mission_accepted = False
        self.dialog()
        pass
