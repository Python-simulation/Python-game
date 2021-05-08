import math
from math import pi

import pygame as pg
from ..interface_functions import NeededFunctions
from ..findpath import FindPath
from ..animation import image_animate

nf = NeededFunctions()
fp = FindPath()
cell_sizes = fp.cell_sizes
authorized_angle = fp.authorized_angle


class Character(pg.sprite.Sprite):
    """moves a character across the screen."""

    def __init__(self, Game, image_name,
                 cardinal=4, frames=6, anim_time=0.1):
        self.Game = Game
        pg.sprite.Sprite.__init__(self)
        self.area = self.Game.game_screen.rect.copy()  # walkable space
        self.area.h -= self.Game.lower_bar.rect.h - 19
        # self.image, self.rect = nf.load_image(name, colorkey=-1)
        self.cardinal = cardinal  # alloyed mvt (8 -> cros+diag, 4 -> diag)
        self.frames = frames  # number of frame for an animation
        self.animation = image_animate(image_name, -1,
                                       frames=self.cardinal*self.frames)
        self._anim_time = anim_time
        self.image = self.animation[0]
        self.rect = self.image.get_rect()

        center = (self.Game.size[0]/2, self.Game.size[1]/2)
        pos = fp.pos_to_cell(center)
        self.change_position(pos)

        self.road = list()
        self.moving = False
        self.speed = 5  # m/s
        # best to have multiple of 64 (cell size)
        # INFO: Dofus goes at 8.3 m/s (30km/h)
        self.angle = None

        self._anim_time_elapsed = 0
        self.step = 0

    def update(self, dt):  # implicitly called from allsprite update
        """walk depending on the character state"""
        self.rect.midbottom = self.position

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

        for i, sprite in enumerate(group):  # all bg_sprites & npc

            if self.rect.colliderect(sprite.rect):  # if player collid with

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

        if self.road != list():
            if self.road[-1] == moving_to_pos:
                return

        if (self.area.left <= moving_to_pos[0] <= self.area.right
                and self.area.top <= moving_to_pos[1] <= self.area.bottom
                and moving_to_pos != self.rect.midbottom):

            if self.road == list():
                begin_cell = (self.rect.midbottom[0],
                              self.rect.midbottom[1] - cell_sizes[1]/2)
                self.road = fp.find_path(self.Game.all_cells,
                                         begin_cell, moving_to_pos,
                                         cardinal=self.cardinal)
                # print(self.road)
            else:
                new_road = fp.find_path(self.Game.all_cells,
                                        self.road[0], moving_to_pos,
                                        cardinal=self.cardinal)
                self.road = [self.road[0]]
                self.road.extend(new_road)

            if self.road != list():
                dest_coord = self.road[0]
                self.dest_coord = (dest_coord[0],
                                   dest_coord[1] + cell_sizes[1]/2)

                # print("you are moving to", self.road[-1])
                # print("road", self.road)
                self.moving = True

    def _walk(self, dt):
        """move the character across the screen"""
        position_x, position_y = self.position

        dest_x, dest_y = self.dest_coord

        length_x = dest_x - position_x
        length_y = dest_y - position_y
        length = math.sqrt(length_x**2 + length_y**2)

        move = self.speed * self.Game.ratio_pix_meter * dt

        while move >= length:
            move -= length
            self.position = self.dest_coord

            try:
                self.road.pop(0)

                dest_coord = self.road[0]
                self.dest_coord = (dest_coord[0],
                                   dest_coord[1] + cell_sizes[1]/2)

                position_x, position_y = self.position

                dest_x, dest_y = self.dest_coord

                length_x = dest_x - position_x
                length_y = dest_y - position_y
                length = math.sqrt(length_x**2 + length_y**2)
            except IndexError:
                self.moving = False
                angle = math.atan2(length_y, length_x)
                angle = fp.theta_cardinal(angle, self.cardinal)
                self._move_animation(angle, self._anim_time, self.frames, 0)
                self.rect.midbottom = self.position

                self.change_order()  # fixed rendering order issue
                return  # without need to set move=0 dt=0

        angle = math.atan2(length_y, length_x)
        angle = fp.theta_cardinal(angle, self.cardinal)

        move_x = move * math.cos(angle)  # pix
        move_y = move * math.sin(angle)

        self.position = (self.position[0] + move_x,
                         self.position[1] + move_y)
        self.rect.midbottom = self.position

        self._move_animation(angle, self._anim_time, self.frames, dt)

    def _move_animation(self, angle, anim_time, frames, dt):
        self.angle = angle
        time_frame = anim_time / frames

        if dt == 0:  # reset
            self._anim_time_elapsed = 0
            self.step = 0
        else:
            self._anim_time_elapsed += dt
            while self._anim_time_elapsed > self.step*time_frame:
                self.step += 1
                if self.step >= frames:
                    self.step = 1
                    self._anim_time_elapsed = 0

        if angle == pi/2:
            self.image = self.animation[4*frames+self.step]
        elif angle == 0:
            self.image = self.animation[5*frames+self.step]
        elif angle == -pi/2:
            self.image = self.animation[6*frames+self.step]
        elif angle == pi or angle == -pi:
            self.image = self.animation[7*frames+self.step]

        elif angle == authorized_angle:
            self.image = self.animation[self.step]
        elif angle == -authorized_angle:
            self.image = self.animation[1*frames+self.step]
        elif angle == -pi + authorized_angle:
            self.image = self.animation[2*frames+self.step]
        elif angle == pi - authorized_angle:
            self.image = self.animation[3*frames+self.step]

    def change_orientation(self, angle):
        if type(angle) is str:
            if angle == "s":
                angle = pi/2
            elif angle == "e":
                angle = 0
            elif angle == "n":
                angle = -pi/2
            elif angle == "w":
                angle = pi
            elif angle == "se":
                angle = authorized_angle
            elif angle == "ne":
                angle = -authorized_angle
            elif angle == "nw":
                angle = -pi + authorized_angle
            elif angle == "sw":
                angle = pi - authorized_angle
            else:
                raise ValueError("bad angle value or name for", angle)
        self._move_animation(angle, self._anim_time, self.frames, 0)

    def change_position(self, cell_pos):
        position = fp.cell_to_pos(cell_pos)
        self.rect.midbottom = (position[0], position[1] + cell_sizes[1]/2)
        self.dest_coord = self.rect.midbottom
        self.position = self.rect.midbottom

    def hovered(self):
        pg.mouse.set_cursor(*pg.cursors.ball)
        return True

    def unhovered(self):
        pass

    def clicked(self):
        return True

    def unclicked(self):
        pass
