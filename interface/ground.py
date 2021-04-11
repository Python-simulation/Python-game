import os
import pygame as pg

from .background import BackGround


def ground(Game):

    ground_dict = {}

    name = os.path.join(Game.data_dir, 'grass.png')
    grass = BackGround(name, -1)
    name = os.path.join(Game.data_dir, 'ground.png')
    ground = BackGround(name, -1)
    name = os.path.join(Game.data_dir, 'water.png')
    water = BackGround(name, -1)

    ground_dict["grass"] = grass
    ground_dict["ground"] = ground
    ground_dict["water"] = water

    return ground_dict
