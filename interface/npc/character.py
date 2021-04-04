import math
from math import pi

import pygame as pg
from ..interface_functions import NeededFunctions
from ..findpath import FindPath
from ..animation import image_animate

from ..findpath import cell_sizes
from ..findpath import authorized_angle

nf = NeededFunctions()
fp = FindPath()


class Character(pg.sprite.Sprite):
    """moves a character across the screen."""

    def __init__(self, Game, image_name, cell_pos,
                 cardinal=4, frames=6, anim_time=0.1):
        self.Game = Game
        pg.sprite.Sprite.__init__(self)
        self.area = self.Game.game_screen.rect.copy()  # walkable space
        self.area.h -= self.Game.lower_tool_bar.rect.h - 19
        # self.image, self.rect = nf.load_image(name, colorkey=-1)
        self.cardinal = cardinal  # alloyed mvt (8 -> cros+diag, 4 -> diag)
        self.frames = frames  # number of frame for an animation
        self.animation = image_animate(image_name, -1,
                                       frames=self.cardinal*self.frames)
        self._anim_time = anim_time
        self.image = self.animation[0]
        self.rect = self.image.get_rect()
        position = fp.cell_to_pos(cell_pos)
        self.rect.midbottom = (position[0], position[1] + cell_sizes[1]/2)

        self.dest_coord = self.rect.midbottom
        self.road = list()
        self.moving = False
        self.max_speed = 10  # m/s, can't go higher than 64 (1 frame per cell)
        # and best to have multiple of 64 (cell size)
        # INFO: Dofus goes at 8.3 m/s (30km/h)
        self.previous_theta = None

        self._anim_time_elapsed = 0
        self.step = 0

    def update(self, dt):  # implicitly called from allsprite update
        """walk depending on the character state"""

        if self.moving:
            self.change_order()
            self._walk(dt)

    def check_order(self, target):
        y0 = target[1]
        y1 = self.rect.midbottom[1] - cell_sizes[1]/2
        return True if y0 > y1 else False

    def change_order(self):
        """Change the display order of self if collide with a sprite from layer
        1 (you+npc+bg_sprite)"""
        if self not in self.Game.allsprites:  # don't change if not displayed
            return

        character_pos = (self.rect.midbottom[0],
                         self.rect.midbottom[1] - cell_sizes[1]/2)

        group = self.Game.allsprites.get_sprites_from_layer(1)
        group.remove(self)

        for i, sprite in enumerate(group):

            if self.rect.colliderect(sprite.rect):
                new_list = []
                self.Game.allsprites.remove(self)

                for sprite_bis in self.Game.allsprites:
                    # recreate the list by copying when no conditions met and,
                    # by placing self infront or back the the collided sprite

                    if sprite_bis == sprite:

                        if sprite.check_order(character_pos):
                            # print("above")
                            new_list.append(sprite)
                            new_list.append(self)
                            break
                        else:
                            # print("bellow")
                            new_list.append(self)
                            new_list.append(sprite)
                            break

                    new_list.append(sprite_bis)

                check = False
                # add remaining sprites after sprite
                for sprite_bis in self.Game.allsprites:

                    if check is True:
                        new_list.append(sprite_bis)

                    if sprite_bis == sprite:
                        check = True

                self.Game.allsprites.remove(group)
                self.Game.allsprites.add(new_list, layer=1)

                if not sprite.check_order(character_pos):
                    break  # stay behind the 1st

    def dest(self, moving_to_pos):
        if (self.area.left <= moving_to_pos[0] <= self.area.right
                and self.area.top <= moving_to_pos[1] <= self.area.bottom
                and moving_to_pos != self.rect.midbottom):

            if self.road == list():

                begin_cell = (self.rect.midbottom[0],
                              self.rect.midbottom[1] - cell_sizes[1]/2)
                self.road = fp.find_path(begin_cell,
                                         moving_to_pos,
                                         all_cells=self.Game.all_cells,
                                         cardinal=self.cardinal)
                # print(self.road)
            else:
                new_road = fp.find_path(self.road[0],
                                        moving_to_pos,
                                        all_cells=self.Game.all_cells,
                                        cardinal=self.cardinal)
                self.road = [self.road[0]]
                self.road.extend(new_road)

            if self.road != list():
                self.dest_coord = self.road[0]
                self.dest_coord = (self.dest_coord[0],
                                   self.dest_coord[1] + cell_sizes[1]/2)

                # print("you are moving to", self.road[-1])
                # print("road", self.road)
                self.moving = True

    def _walk(self, dt):
        """move the character across the screen"""
        x_length = self.dest_coord[0] - self.rect.midbottom[0]
        y_length = self.dest_coord[1] - self.rect.midbottom[1]

        theta = math.atan2(y_length, x_length)

        theta = fp.theta_cardinal(theta, self.cardinal)

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

        # frames = cell_size/(self.max_speed*self.Game.ratio_pix_meter_x*dt)
        # time = frames * dt
        self._move_animation(self._anim_time, self.frames, dt)

        old_rect = self.rect.copy()
        self.rect = self.image.get_rect()
        self.rect = old_rect.copy()
        del old_rect

        newpos = self.rect.move((self.move_x, self.move_y))
        self.rect = newpos

#        print(theta, self.previous_theta)
        if theta != self.previous_theta and self.previous_theta is not None:
            self.rect.midbottom = self.dest_coord

        if self._check_pos():
            self.speed_x = 0
            self.speed_y = 0
            self.rect.midbottom = self.dest_coord
            self.moving = False
            previous_theta_buffer = self.previous_theta
            self.previous_theta = None

            try:
                self.road.pop(0)
                self.dest_coord = self.road[0]
                self.dest_coord = (self.dest_coord[0],
                                   self.dest_coord[1] + cell_sizes[1]/2)
                self.moving = True
#                print("choose next")
                return
            except IndexError:
                self.previous_theta = previous_theta_buffer
                self._move_animation(self._anim_time, self.frames, 0)  # reset anim
                self.previous_theta = None
                return

        self.previous_theta = theta

    def _check_pos(self):
        acceptance = 0  # OPTIMZE: Obsolete when added self.previous_theta
        interv_low = (self.dest_coord[0] - acceptance,
                      self.dest_coord[1] - acceptance)
        interv_high = (self.dest_coord[0] + acceptance,
                       self.dest_coord[1] + acceptance)

        if (interv_low[0] <= self.rect.midbottom[0] <= interv_high[0]
                and interv_low[1] <= self.rect.midbottom[1] <= interv_high[1]):
            return True
        else:
            return False

    def _move_animation(self, anim_time, frames, dt):
        time_frame = anim_time / frames

        if dt == 0:
            self._anim_time_elapsed = 0
            self.step = 0
        else:
            self._anim_time_elapsed += dt
            while self._anim_time_elapsed > self.step*time_frame:
                self.step += 1
                if self.step >= frames:
                    self.step = 0
                    self._anim_time_elapsed = 0

        if self.previous_theta == pi/2:
            self.image = self.animation[4*frames+self.step]
        elif self.previous_theta == 0:
            self.image = self.animation[5*frames+self.step]
        elif self.previous_theta == -pi/2:
            self.image = self.animation[6*frames+self.step]
        elif self.previous_theta == pi or self.previous_theta == -pi:
            self.image = self.animation[7*frames+self.step]

        elif self.previous_theta == authorized_angle:
            self.image = self.animation[0*frames+self.step]
        elif self.previous_theta == -authorized_angle:
            self.image = self.animation[1*frames+self.step]
        elif self.previous_theta == -pi + authorized_angle:
            self.image = self.animation[2*frames+self.step]
        elif self.previous_theta == pi - authorized_angle:
            self.image = self.animation[3*frames+self.step]

    def hovered(self):
        pass

    def unhovered(self):
        pass

    def clicked(self):
        pass

    def unclicked(self):
        pass
