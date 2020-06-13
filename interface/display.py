import pygame as pg


class display_info(pg.sprite.Sprite):

    def __init__(self, Game, text, position):
        self.Game = Game
        pg.sprite.Sprite.__init__(self)  # call Sprite intializer
#        font = pg.font.Font(None, 30)
#        self.image = font.render(self.text, 1, (10, 10, 10))
        self.text(text)
        self.rect = self.image.get_rect().center = position

    def text(self, value):
        font = pg.font.Font(None, 30)
        self.image = font.render(value, 1, (10, 10, 10))

    def hovered(self):
        self.rect = self.Game.mouse.rect
        self.Game.allsprites.add(self)

    def unhovered(self):
        self.Game.allsprites.remove(self)

    def clicked(self):
        pass

    def unclicked(self):
        pass
