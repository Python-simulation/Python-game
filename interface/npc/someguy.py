import os
from .npc import Npc
from ..quests.first_quest import Quest


class SomeGuy(Npc):
    def __init__(self, Game):
        self.Game = Game
        image_name = os.path.join(Game.data_dir, "npc.png")
        super().__init__(Game, image_name)

        self.allowed_mvt(1, 1)
        self.speed = 2
        self.npc_time = 3

        self.name = "Character with quest"

        self.quest = Quest(self)  #  TODO: need to create quest outside
        # (if several character involved and over differente maps)

    def update(self, dt):
        super().update(dt)
        self.quest.update(dt)
        pass

    def hovered(self):
        super().hovered()
        if not self.quest.menu.active:
            self.message.text("I'm a special npc! I can talk!")
            self.message.activated()
        return True

    def unhovered(self):
        self.message.desactivated()
        pass

    def clicked(self):
        self.quest.clicked()
        return True

    def unclicked(self):
        # self.quest.unclicked()
        pass
