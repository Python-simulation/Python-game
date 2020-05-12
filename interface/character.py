import os
import pygame as pg
import math
import numpy as np
from .interface_functions import NeededFunctions
from .display import display_info
nf = NeededFunctions()


class Character(pg.sprite.Sprite):
    """moves a character across the screen."""

    def __init__(self, Game):
        self.Game = Game  # add real-time variable change from the Game class
        pg.sprite.Sprite.__init__(self)  # call Sprite intializer
        self.area = self.Game.game_screen.rect.copy()  # walkable space
        self.area.h -= self.Game.lower_tool_bar.rect.h - 19
        name=os.path.join(Game.data_dir, "character.png")
        self.image, self.rect = nf.load_image(name, colorkey=-1)
#        self.image = pg.transform.scale(
#            self.image,
#            (self.image.get_rect().w//2, self.image.get_rect().h//2))
        self.rect.midbottom = 60+60/2, 60+60/2

#        self.position = self.rect.midbottom
        self.dest_coord = self.rect.midbottom
        self.road = list()
        self.moving = False
        self.max_speed = 10  # 2.5  # can't go higher than 60 (cell size)
        self.previous_theta = None

        text = "I'm you !"
        txt_position = self.Game.mouse.rect.center
        self.message = display_info(self.Game, text, txt_position)

    def update(self, dt):  # implicitly called from allsprite update
        """walk depending on the character state"""
        if self.moving:
            self._walk(dt)
        else:
            pass

    def dest(self, moving_to_pos):

        if (self.area.left < moving_to_pos[0] < self.area.right
                and self.area.top < moving_to_pos[1] < self.area.bottom
                and moving_to_pos != self.rect.midbottom):

            if self.road == list():
                self.road = nf.find_path(self.rect.midbottom,
                                         moving_to_pos, 60
                                         )  # , all_cells=np.zeros(570))
            else:
                new_road = nf.find_path(self.road[0], moving_to_pos, 60)
                self.road = [self.road[0]]
                self.road.extend(new_road)

            if self.road != list():
                self.dest_coord = self.road[0]
                print("moving to", self.road[-1])
#                print("road", self.road)
                self.moving = True

    def _walk(self, dt):
        """move the character across the screen"""
        x_length = self.dest_coord[0] - self.rect.midbottom[0]
        y_length = self.dest_coord[1] - self.rect.midbottom[1]

        theta = math.atan2(y_length, x_length)
#        theta = np.pi/2 * (theta // (np.pi/2))  # allows only cross movement
        theta = np.pi/4 * (theta // (np.pi/4))  # allows cross + diagonal mov
        # Warning, need to change also theta in the find_path

        self.speed_x = self.max_speed * math.cos(theta)
        self.speed_y = self.max_speed * math.sin(theta)  # meter per second

        self.move_x = self.speed_x * self.Game.ratio_pix_meter_x * dt
        self.move_y = self.speed_y * self.Game.ratio_pix_meter_y * dt
        # TODO: could add a memory for the movement left to add up to the
        # next frame ? like the time has a accumulator.
        # I tried but rise a issues with the number of cases than the character
        # can go in advance. To be continue... (reminder: if go further,
        # keep position, if same angle with while loop for each cases ?, if not
        # teleport to case as it is)

        newpos = self.rect.move((self.move_x, self.move_y))
        self.rect = newpos

#        print(theta, self.previous_theta)
        if theta != self.previous_theta and self.previous_theta is not None:
            self.rect.midbottom = self.dest_coord

        if self._check_pos():
            try:
#                print("choose next")
                self.road.pop(0)
                self.dest_coord = self.road[0]
                self.moving = True
                return
            except IndexError:
                return

        self.previous_theta = theta

    def _check_pos(self):
        acceptance = 0  # Obsolete when added self.previous_theta
        interv_low = (self.dest_coord[0] - acceptance,
                      self.dest_coord[1] - acceptance)
        interv_high = (self.dest_coord[0] + acceptance,
                       self.dest_coord[1] + acceptance)

        if (interv_low[0] <= self.rect.midbottom[0] <= interv_high[0]
                and interv_low[1] <= self.rect.midbottom[1] <= interv_high[1]):
            self.speed_x = 0
            self.speed_y = 0
            self.rect.midbottom = self.dest_coord
            self.moving = False
            self.previous_theta = None
            return True
        else:
            return False

    def hovered(self):
        self.message.text = "I'm you !"
        self.message.hovered()
        pass

    def unhovered(self):
        self.message.unhovered()
        pass

    def clicked(self):
        self.message.text = "You just clicked on me !"
        pass

    def unclicked(self):
        pass


# def speed_for_int_move(ratio_pix_meter_x, dt_fixed, max_speed):
#    """
#    self.max_speed_x = speed_for_int_move(
#        self.Game.ratio_pix_meter_x, self.Game.dt_fixed, self.max_speed)
#    """
#    allowed_speed = list()
#
#    for i in range(1, int(60/(ratio_pix_meter_x*dt_fixed))):
#        if 60 % i == 0:  # 60 from the cell size
#            allowed_speed.append(i/(ratio_pix_meter_x*dt_fixed))
#
#    allowed_speed = np.array(allowed_speed)
#    ind = abs(allowed_speed - max_speed).argmin()
#    print("all_speed", allowed_speed)
#
#    return allowed_speed[ind]
