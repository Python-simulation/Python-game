import pygame as pg
from .background import BackGround


class Text(BackGround):
    """text"""

    def __init__(self, text="", size=(0, 0)):
        self.size = size
        BackGround.__init__(self, size=size)
        self.add_text(text, size)

    def add_text(self, text, size):
        self.text = text
        font = pg.font.Font(None, 30)

        self.image = font.render(text, True, (10, 10, 10))
        self.rect = self.image.get_rect()
        self.rect.size = self.size

    def add_highlight(self, color=(147, 90, 61)):
        self.highligh = pg.Surface(self.size)
        self.highligh.fill(color)

        self.highligh.blit(self.image, self.image.get_rect())
        self.image = self.highligh


def text_tuple(text, size=(0, 0)):
    nbr_char = int(size[0]/(407/36))
    words = text.split(" ")
    new_text = list()
    new_line = str()

    for word in words:
        if (len(new_line) + 1 + len(word)) <= nbr_char:
            new_line = " ".join((new_line, word))
        else:
            new_text.append(new_line)
            new_line = str(word)

    new_text.append(new_line)
    new_text[0] = new_text[0][1:]  # remove first space

    text_class = list()

    for text in new_text:
        text_class.append(Text(text, size))

    return tuple(text_class)
