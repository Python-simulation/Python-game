import os
import pygame as pg
from pygame.compat import geterror
import math
import numpy as np


class NeededFunctions:
    # functions to create our resources

    def load_image(self, name, colorkey=None):
        """Load images to the pygame variables space"""
        fullname = name

        try:
            image = pg.image.load(fullname)

        except pg.error:
            print("Cannot load image:", fullname)
            raise SystemExit(str(geterror()))

        image = image.convert()

        if colorkey is not None:

            if colorkey == -1:
                # (0, 0) ->take the first pixel of the image as reference for alpha
                colorkey = image.get_at((0, 0))

            # RLEACCEL make it faster to display
            image.set_colorkey(colorkey, pg.RLEACCEL)

        return image, image.get_rect()

    def load_sound(self, name):
        """Load sounds to the pygame variables space"""
        class NoneSound:
            def play(self):
                pass

        if not pg.mixer or not pg.mixer.get_init():
            return NoneSound()

        fullname = name

        try:
            sound = pg.mixer.Sound(fullname)

        except pg.error:
            print("Cannot load sound: %s" % fullname)
            raise SystemExit(str(geterror()))

        return sound

    def find_path(self, begin_cell, dest_cell, cell_size,
                  all_cells=None, cardinal=4):
        # print(all_cells)
        if all_cells is None:
            all_cells = range(560)
        road = list()
        previous_cell = begin_cell
        nbr_step = 0

        while previous_cell != dest_cell:

            nbr_step += 1
            if nbr_step > len(all_cells):
                road = list()
    #            print("bad road", road)
                break

            x_length = dest_cell[0] - previous_cell[0]
            y_length = dest_cell[1] - previous_cell[1]
            theta = math.atan2(y_length, x_length)

            if cardinal == 4:
                theta = np.pi/2 * (theta // (np.pi/2))  # allows only cross movement
            elif cardinal == 8:
                theta = np.pi/4 * (theta // (np.pi/4))  # allows cross + diagonal mov
            else:
                raise ValueError("error with alloyed direction, cardinal="
                                 + str(cardinal) + ". Alloyed values: 4 and 8")

            if theta == 0:  # ugly but work
                next_cell = (previous_cell[0]+cell_size,
                             previous_cell[1]+0)
            elif theta == np.pi or theta == -np.pi:
                next_cell = (previous_cell[0]-cell_size,
                             previous_cell[1]+0)
            elif theta == np.pi/2:
                next_cell = (previous_cell[0]+0,
                             previous_cell[1]+cell_size)
            elif theta == -np.pi/2:
                next_cell = (previous_cell[0]+0,
                             previous_cell[1]-cell_size)
            elif theta == np.pi/4:
                next_cell = (previous_cell[0]+cell_size,
                             previous_cell[1]+cell_size)
            elif theta == 3*np.pi/4:
                next_cell = (previous_cell[0]-cell_size,
                             previous_cell[1]+cell_size)
            elif theta == -np.pi/4:
                next_cell = (previous_cell[0]+cell_size,
                             previous_cell[1]-cell_size)
            elif theta == -3*np.pi/4:
                next_cell = (previous_cell[0]-cell_size,
                             previous_cell[1]-cell_size)
            else:
                print("error with angle", theta, theta*180/np.pi)
    #        next_cell = (previous_cell[0]+(math.cos(theta)),  # good looking but
    #                     previous_cell[1]+(math.sin(theta)))  # don't work

            unit_pos = (int((next_cell[0]-cell_size/2)/cell_size),
                        int((next_cell[1]-cell_size/2)/cell_size))
            try:
                all_cells[unit_pos]
            except KeyError:
                # print("can't walk here, stop before it")
                break

            road.append(next_cell)
            previous_cell = next_cell

        return road

    def function_test(self, state):
        print("fct 1 do something with state", state)

    def function_test2(self, state):
        print("fct 2 do something with state", state)
