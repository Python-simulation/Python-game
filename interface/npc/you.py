import os
from .character import Character
# from ..findpath import FindPath

from ..display import Display

# fp = FindPath()
# cell_sizes = fp.cell_sizes


class You(Character):
    def __init__(self, Game):
        self.Game = Game
        image_name = os.path.join(Game.data_dir, "character.png")
        Character.__init__(self, Game, image_name, cardinal=8)
        self.speed = 20

        text = "I'm you!"
        txt_position = self.Game.mouse.rect.topleft
        self.message = Display(self.Game, text, txt_position)

    def hovered(self):
        # self.message.text("I'm you")
        self.message.hovered()
        pass

    def unhovered(self):
        self.message.unhovered()
        pass
