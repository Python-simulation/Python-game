from ..flying_menu import FlyingMenu
from ..button import Button
from ..text import Text, text_tuple


class Quest:
    def __init__(self, Owner):
        self.Owner = Owner
        self.Game = self.Owner.Game

        self.authorized_mvt_save = self.Owner.authorized_mvt

        self.char_sign = Text("!", size=(11, 30))

        name = Text(self.Owner.name, size=(600, 30)) # must have the higher width
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
        diag_description = text_tuple(text, size=(600, 30))

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

        self.menu = FlyingMenu(self.Owner)

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
        if not self.mission_accepted:
            self.char_sign.rect
            self.char_sign.rect.bottomleft = (self.Owner.rect.centerx-3,
                                              self.Owner.rect.top-3)
            self.Game.allsprites.add(self.char_sign)
        else:
            self.Game.allsprites.remove(self.char_sign)

    def clicked(self):
        if self.menu.active:
            return

        self.Owner.authorized_mvt = 0

        if not self.mission_accepted:
            self.diag_index = 0
            self.menu.items = self.start_mission[self.diag_index]
        else:
            self.diag_index = 5
            self.menu.items = self.start_mission[self.diag_index]

        self.menu.activated()

    def unclicked(self):
        if not self.Game.mouse.clicking(self.menu):
            # print("desac from unclicked")
            self.stop_dialog()
            # if keep activated instead of clicked, must never kill a npc
            # without doing desactivated menu

    def stop_dialog(self, *args):
        # print("desac from buton")
        self.menu.desactivated()
        self.diag_index = 0
        self.Owner.authorized_mvt = self.authorized_mvt_save
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
