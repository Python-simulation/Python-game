import pygame as pg


class Display(pg.sprite.Sprite):
    """Text with hovering methods"""
    def __init__(self, Game, text="", position=(0, 0), size=30):
        self.Game = Game
        self.position = position
        self.size = size
        pg.sprite.Sprite.__init__(self)  # call Sprite intializer

        self.text(str(text), size=size)

    def text(self, txt, position="default", size="default"):
        if position == "default":
            position = self.position
        if size == "default":
            size = self.size

        font = pg.font.Font(None, size)
        self.image = font.render(str(txt), True, (10, 10, 10))
        self.rect = self.image.get_rect()
        self.rect.center = position

    def hovered(self):
        self.rect = self.Game.mouse.rect
        self.Game.allsprites.add(self, layer=2)

    def unhovered(self):
        self.Game.allsprites.remove(self)

    def clicked(self):
        pass

    def unclicked(self):
        pass
