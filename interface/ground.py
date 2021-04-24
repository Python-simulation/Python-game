import os

from .background import BackGround


def ground(Game):

    ground_dict = {}

    name = os.path.join(Game.data_dir, 'grass.png')
    grass = BackGround(name, -1)
    grass.walkable = True
    ground_dict["grass"] = grass

    name = os.path.join(Game.data_dir, 'ground.png')
    ground = BackGround(name, -1)
    ground.walkable = True
    ground_dict["ground"] = ground

    name = os.path.join(Game.data_dir, 'water.png')
    water = BackGround(name, -1)
    water.walkable = False
    ground_dict["water"] = water

    name = os.path.join(Game.data_dir, 'empty.png')
    empty = BackGround(name, -1)
    empty.walkable = False
    ground_dict["empty"] = empty

    return ground_dict
