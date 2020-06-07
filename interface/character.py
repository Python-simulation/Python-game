import os
import math
from math import pi
import random

import pygame as pg
from .interface_functions import NeededFunctions
from .findpath import FindPath
from .display import display_info
from .animation import image_animate
from .flying_menu import FlyingMenu
from .button import Button
from .background import BackGround

nf = NeededFunctions()
fp = FindPath()

from .findpath import cell_sizes
from .findpath import authorized_angle


class Character(pg.sprite.Sprite):
    """moves a character across the screen."""

    def __init__(self, Game, file_name, cardinal=4, npc=True):
        self.Game = Game
        pg.sprite.Sprite.__init__(self)
        self.area = self.Game.game_screen.rect.copy()  # walkable space
        self.area.h -= self.Game.lower_tool_bar.rect.h - 19
        # self.image, self.rect = nf.load_image(name, colorkey=-1)
        self.cardinal = cardinal  # mvt alloyed (8 means cros+diag, 4 means cross)
        self._npc = npc  # if is a npc or the player
        self.frames = 6  # number of frame for an animation
        self.animation = image_animate(file_name, -1,
                                       frames=self.cardinal*self.frames)
        self.image = self.animation[0]
        self.rect = self.image.get_rect()
#        self.image = pg.transform.scale(
#            self.image,
#            (self.image.get_rect().w//2, self.image.get_rect().h//2))
        position = fp.cell_to_pos((4, 16))
        self.rect.midbottom = (position[0], position[1] + cell_sizes[1]/2)

        self.dest_coord = self.rect.midbottom
        self.road = list()
        self.moving = False
        self.max_speed = 10  # m/s, can't go higher than 64 (1 frame per cell)
        # and best to have multiple of 64 (cell size)
        # INFO: Dofus goes at 8.3 m/s (30km/h)
        self.previous_theta = None

        self.animation_time = 0
        self.step = 0

        self._npc_clock = 0
        self._npc_time = 10

        text = "I'm you !"
        txt_position = self.Game.mouse.rect.topleft
        self.message = display_info(self.Game, text, txt_position)

        name = os.path.join(self.Game.data_dir, 'button_1.png')
        button_1 = Button(self.Game, nf.function_test, name)
        button_1.add_text("carac")

        button_2 = Button(self.Game, nf.function_test2, name)
        inventory_image = os.path.join(self.Game.data_dir, 'inventory.png')
        button_2.add_image(inventory_image, -1)

        # button_blank_1 = BackGround(size=(button_1.rect.size[0], button_1.rect.size[1]-30))
        # button_blank_1.image.set_colorkey(0)

        # button_blank_2 = BackGround(size=(button_1.rect.size[0], button_1.rect.size[1]-30))

        name = os.path.join(self.Game.data_dir, 'button_1.png')
        button_3 = Button(self.Game, nf.function_test, name)
        button_3.add_text("talk")

        self.menu = FlyingMenu(self.Game, button_1, button_2,
                               # button_blank_1, button_blank_2,
                               button_3)
        if npc:
            self.allowed_mvt()

    def update(self, dt):  # implicitly called from allsprite update
        """walk depending on the character state"""

        if self.moving:
            self.change_order()
            self._walk(dt)

        else:
            if self._npc:
                self._auto_dest(dt)
            pass

    def change_order(self):
        player_feet = (self.rect.midbottom[0],
                       self.rect.midbottom[1] - cell_sizes[1]/2)

        self.Game.allsprites.remove(self)  # used to set back player and npc
        self.Game.allsprites.add(self)  # to first plan if no overlap

        for sprite in self.Game.bg_sprites:
            if self.rect.colliderect(sprite.rect):
                # print("overlap", self.rect, sprite.rect)
                new_list = pg.sprite.LayeredUpdates(())
                # self.Game.allsprites.copy()
                # new_list.empty()
                self.Game.allsprites.remove(self)

                for sprite_bis in self.Game.allsprites:
                    # print(sprite_bis)  # BUG: infinit group creation !!
                    if sprite_bis == sprite:
                        if sprite.check_order(player_feet):
                            # print("above")
                            new_list.add(sprite)
                            new_list.add(self)
                            break
                        else:
                            # print("bellow")
                            new_list.add(self)
                            new_list.add(sprite)
                            break

                    new_list.add(sprite_bis)

                check = False

                for sprite_bis in self.Game.allsprites:
                    # print(sprite_bis, check)
                    if check is True:
                        new_list.add(sprite_bis)

                    if sprite_bis == sprite:
                        check = True

                self.Game.allsprites = new_list.copy()
                # new_list.empty()
                if not sprite.check_order(player_feet):  # stay behind the 1st
                    break

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
                # if not self._npc:
                #     print(self.road)
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
                # if self._npc:
                #     print("npc is moving to", self.road[-1])
                # else:
                #     print("you are moving to", self.road[-1])
#                print("road", self.road)
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
        self._move_animation(0.1, self.frames, dt)

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
                self._move_animation(0.1, self.frames, 0)  # reset anim
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
            self.animation_time = 0
            self.step = 0
        else:
            self.animation_time += dt
            while self.animation_time > self.step*time_frame:
                self.step += 1
                if self.step >= frames:
                    self.step = 0
                    self.animation_time = 0

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

    def _auto_dest(self, dt):
        self._npc_clock += dt
        left_mvt = (self.rect.midbottom[0]
                    - self.area.left) // (cell_sizes[0]/2)
        right_mvt = (self.area.right
                     - self.rect.midbottom[0]) // (cell_sizes[0]/2)
        up_mvt = (self.rect.midbottom[1]
                  - self.area.top) // (cell_sizes[1]/2)
        bottom_mvt = (self.area.bottom
                      - self.rect.midbottom[1]) // (cell_sizes[1]/2)

        if left_mvt > self._npc_nbr_cell:
            left_mvt = self._npc_nbr_cell
        if right_mvt > self._npc_nbr_cell:
            right_mvt = self._npc_nbr_cell
        if up_mvt > self._npc_nbr_cell:
            up_mvt = self._npc_nbr_cell
        if bottom_mvt > self._npc_nbr_cell:
            bottom_mvt = self._npc_nbr_cell

        cells = (0, 0)

        if self._npc_clock > self._npc_time:
            self._npc_clock = 0

            cells = (random.randint(-left_mvt, right_mvt),
                     random.randint(-up_mvt, bottom_mvt))

        moving_to_pos = (cells[0]*(cell_sizes[0]/2)+self.rect.midbottom[0],
                         cells[1]*(cell_sizes[1]/2)+self.rect.midbottom[1])
        self.dest(moving_to_pos)

    def allowed_mvt(self, allowed_cell=0, authorized_mvt=1):
        self._npc_nbr_cell = authorized_mvt
        topleft = (self.rect.midbottom[0] - allowed_cell*cell_sizes[0]/2,
                   self.rect.midbottom[1] - allowed_cell*cell_sizes[1]/2)
        self.area = pg.Rect(topleft,
                            (allowed_cell*cell_sizes[0],
                             allowed_cell*cell_sizes[1]))

    def hovered(self):
        if self._npc:
            self.message.text("I'm a npc !")
        else:
            self.message.text("I'm you !")
        self.message.hovered()
        pass

    def unhovered(self):
        self.message.unhovered()
        pass

    def clicked(self):
        self.message.text("You just clicked on me !")
        self.menu.clicked()
        pass

    def unclicked(self):
        self.menu.unclicked()
        pass
