import pygame as pg
from .interface_functions import NeededFunctions

nf = NeededFunctions()


def image_animate(*args, frames=1):

    image_full, rect = nf.load_image(*args)
    size = rect.w // frames
    # image_model = pg.Surface((size, rect.h), pg.SRCALPHA, 32)
    images = list()

    for frame in range(frames):
        image = pg.Surface((size, rect.h), pg.SRCALPHA, 32)
        image.blit(image_full, (-frame*size, 0))
        images.append(image.copy())

    return images