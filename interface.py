"""
This simple example is used for the line-by-line tutorial
that comes with pygame. It is based on a 'popular' web banner.
Note there are comments here, but for the full explanation,
follow along in the tutorial.
"""


# Import Modules
import os
import time
import pygame as pg
from pygame.compat import geterror
import math
import numpy as np

if not pg.font:
    print("Warning, fonts disabled")
if not pg.mixer:
    print("Warning, sound disabled")

os.environ['SDL_VIDEO_WINDOW_POS'] = "%d,%d" % (50, 50)

main_dir = os.path.split(os.path.abspath(__file__))[0]
data_dir = os.path.join(main_dir, "data")


# functions to create our resources
def load_image(name, colorkey=None):
    """Load images to the pygame variables space"""
    fullname = os.path.join(data_dir, name)

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


def load_sound(name):
    """Load sounds to the pygame variables space"""
    class NoneSound:
        def play(self):
            pass

    if not pg.mixer or not pg.mixer.get_init():
        return NoneSound()

    fullname = os.path.join(data_dir, name)

    try:
        sound = pg.mixer.Sound(fullname)

    except pg.error:
        print("Cannot load sound: %s" % fullname)
        raise SystemExit(str(geterror()))

    return sound


# classes for our game objects
class Mouse(pg.sprite.Sprite):
    """Position and surface of the mouse (can change the mouse image by
    removing the real mouse image and replacing by a defined one)"""

    def __init__(self, Game):
        self.Game = Game
        pg.sprite.Sprite.__init__(self)  # call Sprite initializer
#        self.image, self.rect = load_image("mouse.png")  # , -1)
        self.image = pg.Surface((1, 1))
        self.image.set_colorkey(0)
        self.rect = self.image.get_rect()
        self.state_clicking = False

    def update(self, dt):
        self.position()
#        print(self.rect.center)

    def position(self):
        """move the resized mouse based on the real mouse position"""
        diff_x = (self.Game.resized_screen.rect.w
                  - self.Game.app_screen_rect.w)/2
        diff_y = (self.Game.resized_screen.rect.h
                  - self.Game.app_screen_rect.h)/2

        ratio_x = (self.Game.game_screen.rect.w
                   / self.Game.resized_screen.rect.w)
        ratio_y = (self.Game.game_screen.rect.h
                   / self.Game.resized_screen.rect.h)

        pos = pg.mouse.get_pos()

        real_pos_x = (diff_x + pos[0]) * ratio_x
        real_pos_y = (diff_y + pos[1]) * ratio_y
        real_pos = real_pos_x, real_pos_y

        self.rect.center = real_pos

#        if self.state_clicking:
#            self.rect.move_ip(5, 10)  # good for button

    def hovering(self, target):
        hitbox = self.rect
        return hitbox.colliderect(target.rect)

    def clicking(self, target):
        """returns true if the mouse collides with the target"""
        if self.hovering(target):
            self.state_clicking = True
            return True
        else:
            pass

    def unclicked(self):
        """called to pull the mouse back"""
        self.state_clicking = False
        self.Game.unclick()


class Chimp(pg.sprite.Sprite):
    """moves a monkey critter across the screen. it can spin the
       monkey when it is clicked."""

    def __init__(self, Game):
        self.Game = Game  # add real-time variable change from the Game class
        pg.sprite.Sprite.__init__(self)  # call Sprite intializer
        self.area = self.Game.game_screen.rect.copy()  # walkable space
        self.area.h -= self.Game.lower_tool_bar.rect.h - 19

        self.image, self.rect = load_image("chimp.png", -1)
#        self.image = pg.transform.scale(self.image, (200, 100))
#        self.rect = self.image.get_rect()
        self.rect.topleft = 0, 100

        self.speed_x = 5/np.sqrt(2)
        self.speed_y = 5/np.sqrt(2)  # meter per second

        self.dizzy = 0
        self.angular_speed = 360  # degrees per second

    def update(self, dt):  # implicitly called from allsprite update
        """walk or spin, depending on the monkeys state"""
        if self.dizzy:
            self._spin(dt)
        else:
            self._walk(dt)

    def _walk(self, dt):
        """move the monkey across the screen, and turn at the ends"""

#        if not self.area.contains(newpos_x):  # could be useful but not here

        move_x = self.speed_x * self.Game.ratio_pix_meter_x * dt
        move_y = self.speed_y * self.Game.ratio_pix_meter_y * dt

        newpos = self.rect.move((move_x, move_y))

        if newpos.left < self.area.left or newpos.right > self.area.right:
            self.speed_x = -self.speed_x
            self.image = pg.transform.flip(self.image, 1, 0)  # temporaire

        if newpos.top < self.area.top or newpos.bottom > self.area.bottom:
            self.speed_y = -self.speed_y

        move_x = self.speed_x * self.Game.ratio_pix_meter_x * dt
        move_y = self.speed_y * self.Game.ratio_pix_meter_y * dt

        newpos = self.rect.move((move_x, move_y))
        self.rect = newpos

    def _spin(self, dt):
        """spin the monkey image"""
        center = self.rect.center
        self.dizzy = self.dizzy + self.angular_speed*dt
        if self.dizzy >= 360:
            self.dizzy = 0
            self.image = self.original
        else:
            rotate = pg.transform.rotate
            self.image = rotate(self.original, self.dizzy)
        self.rect = self.image.get_rect(center=center)

    def hovered(self):
        pass

    def unhovered(self):
        pass

    def clicked(self):
        """this will cause the monkey to start spinning"""
        if not self.dizzy:
            self.dizzy = 1
            self.original = self.image


class Character(pg.sprite.Sprite):
    """moves a character across the screen."""

    def __init__(self, Game):
        self.Game = Game  # add real-time variable change from the Game class
        pg.sprite.Sprite.__init__(self)  # call Sprite intializer
        self.area = self.Game.game_screen.rect.copy()  # walkable space
        self.area.h -= self.Game.lower_tool_bar.rect.h - 19

        self.image, self.rect = load_image("character.png", -1)
#        self.image = pg.transform.scale(
#            self.image,
#            (self.image.get_rect().w//2, self.image.get_rect().h//2))
        self.rect.midbottom = 60+60/2, 60+60/2

#        self.position = self.rect.midbottom
        self.dest_coord = self.rect.midbottom
        self.moving = False
        self.max_speed = 10  # 2.5

        text = "I'm you !"
        txt_position = self.Game.mouse.rect.center
        self.message = display_info(self.Game, text, txt_position)

    def update(self, dt):  # implicitly called from allsprite update
        """walk depending on the character state"""
#        self.position = self.rect.midbottom
        if self.moving:
            self._walk(dt)
        else:
            pass

    def dest(self, moving_to_pos):
        if (self.area.left < moving_to_pos[0] < self.area.right
                and self.area.top < moving_to_pos[1] < self.area.bottom):
#            print("pos", self.rect.midbottom, "dest", moving_to_pos)
            if self.rect.midbottom != moving_to_pos:
                self.dest_coord = moving_to_pos
#                print("moving to", moving_to_pos)
                self.moving = True
            else:
                pass

    def _walk(self, dt):
        """move the character across the screen"""

        if self.check_pos():
            return

        x_length = self.dest_coord[0] - self.rect.midbottom[0]
        y_length = self.dest_coord[1] - self.rect.midbottom[1]

        theta = math.atan2(y_length, x_length)

#        theta = np.pi/2 * (theta // (np.pi/2))  # allows only cross movement
        theta = np.pi/4 * (theta // (np.pi/4))  # allows cross + diagonal mov

        self.speed_x = self.max_speed * math.cos(theta)
        self.speed_y = self.max_speed * math.sin(theta)  # meter per second

        self.move_x = self.speed_x * self.Game.ratio_pix_meter_x * dt
        self.move_y = self.speed_y * self.Game.ratio_pix_meter_y * dt

        newpos = self.rect.move((self.move_x, self.move_y))
        self.rect = newpos

    def check_pos(self):
        acceptance = 10
        interv_low = (self.dest_coord[0] - acceptance,
                      self.dest_coord[1] - acceptance)
        interv_high = (self.dest_coord[0] + acceptance,
                       self.dest_coord[1] + acceptance)
#        print("position", self.rect.midbottom)
        if (interv_low[0] < self.rect.midbottom[0] < interv_high[0]
                and interv_low[1] < self.rect.midbottom[1] < interv_high[1]):
            self.speed_x = 0
            self.speed_y = 0
            self.rect.midbottom = self.dest_coord
#            print("position new", self.rect.midbottom)
            self.moving = False
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


class Cell(pg.sprite.Sprite):
    """simple cell to target movement"""
    def __init__(self, Game, size, position, function=None):
        self.Game = Game
        self.function = function
        pg.sprite.Sprite.__init__(self)  # call Sprite intializer
        self.image = pg.Surface(size)
        self.rect = self.image.get_rect()
        self.rect.center = position
        color = (50, 50, 50)
        self.alpha_off = 10
        self.alpha_on = 50
        self.image.fill(color)
        self.image.set_alpha(self.alpha_off)
        self.state = False

    def update(self, dt):
        """by default, if no function or if function returns nothing, consider
        the cell has done its purpuse and set state to False"""
        if self.function is not None and self.state:
            output = self.function(*self.args, **self.kwargs)

            if output is None:
                self.state = False

    def hovered(self, *args):
        self.image.set_alpha(self.alpha_on)
        pass

    def unhovered(self, *args):
        self.image.set_alpha(self.alpha_off)
        pass

    def clicked(self, *args, **kwargs):
        self.args = args
        self.kwargs = kwargs
        self.state = True

    def unclicked(self):
        self.state = False


class BackGround():
    """image of the map"""
    def __init__(self, *args, size=(1, 1)):
        try:
            self.image, self.rect = load_image(*args)
        except Exception:
            self.image = pg.Surface(size)
            self.rect = self.image.get_rect()


def function_test(state):
    print("fct 1 do something with state", state)


def function_test2(state):
    print("fct 2 do something with state", state)


class display_info(pg.sprite.Sprite):
    def __init__(self, Game, text, position):
        self.Game = Game
        self.text = text
        pg.sprite.Sprite.__init__(self)  # call Sprite intializer
#        font = pg.font.Font(None, 30)
#        self.image = font.render(self.text, 1, (10, 10, 10))
        self.rect = self.image.get_rect().center = position

    @property
    def text(self):
        return self._text

    @text.setter
    def text(self, value):
        self._text = value
        font = pg.font.Font(None, 30)
        self.image = font.render(self._text, 1, (10, 10, 10))

    def hovered(self):
        self.rect = self.Game.mouse.rect
        self.Game.allsprites.add(self)

    def unhovered(self):
        self.Game.allsprites.remove(self)


class Button():
    """buttons"""
    def __init__(self, Game, function, *args):
        self.Game = Game
        self.function = function

        self.image, self.rect = load_image(*args)

        self.position = self.rect  # same id until clicked occured, then copy
        self.image_original = self.image

        self.state = False
        self.state_clicked = False

        self.highligh = pg.Surface(self.rect.size)
        self.highligh.fill((255, 255, 255))
        self.highligh.set_alpha(10)

    def add_text(self, text, center=None):
        font = pg.font.Font(None, 30)
        msg = font.render(text, 1, (10, 10, 10))

        if center is None:
            textpos = msg.get_rect(centery=self.rect.h/2,
                                   centerx=self.rect.w/2)
        else:
            textpos = msg.get_rect().center = center

        self.image.blit(msg, textpos)
        self.image_original = self.image

    def hovered(self):
        self.image_original = self.image.copy()
        self.image.blit(self.highligh, self.highligh.get_rect())
        pass

    def unhovered(self):
        self.image = self.image_original
#        self.image_original = self.image  # same id from now
        pass

    def clicked(self):
        if self.Game.mouse.state_clicking:
            self.state_clicked = True
            self.position = self.rect.copy()
#            self.image_original = self.image.copy()
#            self.rect.move_ip(1, 1)
            offset = 6
            self.image = pg.transform.scale(
                self.image, (self.rect.w - offset, self.rect.h - offset))
            self.rect.move_ip(offset/2, offset/2)
#            self.state = not self.state  " good for memory button

    def unclicked(self):
        self.state_clicked = False
        self.image = self.image_original
        self.rect = self.position

        self.position = self.rect  # same id from now
        self.image_original = self.image  # same id from now
        if self.Game.mouse.hovering(self):
            self.state = True
            self.function(self.state)
            # TODO: could be nice to have args and kwargs here
        else:
            self.state = False


def all_maps(Game):

    background = BackGround('background.png')
    background.rect.center = Game.game_screen.rect.center
#        for i in range(1, 1920):
#            if 1920 % i == 0 and 1080 % i == 0:
#                print(i)
    # posible pixel size for the cell to have int for 1920 and 1080 :
    # 1, 2, 3, 4, 5, 6, 8, 10, 12, 15, 20, 24, 30, 40, 60, 120
    cell_left = Cell(
            Game, size=(60, Game.game_screen.rect.h),
            position=(Game.game_screen.rect.left + 60/2,
                      Game.game_screen.rect.centery),
            function=Game.border_left)
    cell_left.alpha_off = 0

    cell_right = Cell(
            Game, size=(60, Game.game_screen.rect.h),
            position=(Game.game_screen.rect.right - 60/2,
                      Game.game_screen.rect.centery),
            function=Game.border_right)
    cell_right.alpha_off = 0

    cell_top = Cell(
            Game, size=(Game.game_screen.rect.w, 60),
            position=(Game.game_screen.rect.centerx,
                      Game.game_screen.rect.top + 60/2),
            function=Game.border_top)
    cell_top.alpha_off = 0

    cell_bottom = Cell(
            Game, size=(Game.game_screen.rect.w, 60),
            position=(Game.game_screen.rect.centerx,
                      Game.game_screen.rect.bottom - 60/2
                      - Game.lower_tool_bar.rect.h + 19),
            function=Game.border_bottom)
    cell_bottom.alpha_off = 0

    borders_list = {
        "left": cell_left,
        "right": cell_right,
        "top": cell_top,
        "bottom": cell_bottom,
    }

    size = 60
    cells_dict = dict()
    for x in range(1, 32-1):
        for y in range(1, 18-1-2):  # -2 because not 16/9 :'( damn lowerbar
            cells_dict[(x, y)] = Cell(
                Game,
                size=(size, size),
                position=(x*size+size/2, y*size+size/2),
                function=Game.character.dest,
            )

    cells_visible = [
        Cell(Game, size=(40, 40), position=(500, 100),
             function=Game.character.dest),
        Cell(Game, size=(40, 40), position=(800, 200),
             function=Game.character.dest),
        Cell(Game, size=(40, 40), position=(1000, 300),
             function=Game.character.dest),
        Cell(Game, size=(40, 40), position=(100, 700),
             function=function_test),
        borders_list["left"],
        borders_list["top"],
        borders_list["right"],
        borders_list["bottom"]
        ]

    chimp = Chimp(Game)
    sprites = pg.sprite.RenderPlain((
            chimp,
            ))

    map_0_0 = {"background": background,
               "cells": cells_dict,
               "cells_visible": cells_visible,
               "sprites": sprites}

#
    background2 = BackGround('background2.png')
    background2.rect.center = Game.game_screen.rect.center

    chimp2 = Chimp(Game)
    chimp2.speed_x = 10
    sprites = pg.sprite.RenderPlain((
            chimp2,
            ))

    map_n1_0 = {"background": background2,
                "cells": cells_dict,
                "cells_visible": [borders_list["right"]],
                "sprites": sprites}

#
    sprites = pg.sprite.RenderPlain()

    map_1_0 = {"background": background2,
               "cells": cells_dict,
               "cells_visible": [borders_list["left"]],
               "sprites": sprites}

    map_0_1 = {"background": background2,
               "cells": cells_dict,
               "cells_visible": [borders_list["top"]],
               "sprites": sprites}

    map_0_n1 = {"background": background2,
                "cells": cells_dict,
                "cells_visible": [borders_list["bottom"]],
                "sprites": sprites}

    all_maps = {
            (0, 0): map_0_0,
            (-1, 0): map_n1_0,
            (1, 0): map_1_0,
            (0, 1): map_0_1,
            (0, -1): map_0_n1,
                }
    return all_maps


class Game():
    """this function is called when the program starts.
       it initializes everything it needs, then runs in
       a loop until the function returns."""

    def __init__(self, WINDOW_W=1920, WINDOW_H=1080):
        GAME_SCREEN_W = 1920
        GAME_SCREEN_H = 1080

        self.ratio_pix_meter_x = GAME_SCREEN_W/32  # pixel/meter
        self.ratio_pix_meter_y = GAME_SCREEN_H/16  # pixel/meter

        pg.init()
        self.check_border = None
        self.flags = (
                pg.RESIZABLE |
                pg.DOUBLEBUF
                )

        self.window_stretched = False  # false mean we want fixed ratio defined
        # by the game_screen size (not the app_screen)

        # application window surface
        self.app_screen = pg.display.set_mode((WINDOW_W, WINDOW_H), self.flags)
        self.app_screen_rect = self.app_screen.get_rect()

        # game screen surface (where all the ingame stuff gets blitted on)
        self.game_screen = BackGround(size=(GAME_SCREEN_W, GAME_SCREEN_H))
#        self.game_screen.image = pg.Surface((GAME_SCREEN_W, GAME_SCREEN_H))
#        self.game_screen.rect = self.game_screen.image.get_rect()

        self.resized_screen = BackGround()

        self.clock = pg.time.Clock()

        pg.display.set_caption("Testing")
        pg.mouse.set_visible(1)

        # Create The Backgound that never changes (with fixed toolbar)
#        self.bg_image = pg.Surface(self.game_screen.get_size()).convert()
#        background_color = (200, 200, 200)
#        self.bg_image.fill(background_color)

        self.lower_tool_bar = BackGround('lower_bar.png', -1)
        self.lower_tool_bar.rect.midbottom = self.game_screen.rect.midbottom

#        self.button_1 = Button(self, function_test,
#                               ('button_1.png', -1), (1000,100),
#                               "button 1", (30,0))
        self.button_1 = Button(self, function_test, 'button_1.png')
        self.button_1.add_text("button 1")  # , center = (0,0)
        self.button_1.rect.midbottom = self.lower_tool_bar.rect.midbottom
        self.button_1.rect.y -= 12
        self.button_1.rect.left = 950

        self.button_2 = Button(self, function_test2, 'button_1.png')
        self.button_2.add_text("button 2")  # , center = (0,0)
        self.button_2.rect.midbottom = self.lower_tool_bar.rect.midbottom
        self.button_2.rect.y -= 12
        self.button_2.rect.left = 1072

        self.all_buttons = [
                self.button_1,
                self.button_2,
                ]

        # Prepare Game Objects
        self.clock = pg.time.Clock()
        self.dt_fixed = 1 / 60
        self.dt_accumulator = 0
        self.dt = 0
    #    whiff_sound = load_sound("whiff.wav")
    #    punch_sound = load_sound("punch.wav")

        self.mouse = Mouse(self)
#        self.chimp = Chimp(self)
        self.character = Character(self)

        self.all_maps = all_maps(self)
#        self.current_map_pos = (0, 0)
        self.change_map((0, 0))
#        self.character.rect.midbottom = self.cells[(1,1)].rect.center

    def change_map(self, current_map_pos):
#        self.check_border = None
        self.current_map_pos = current_map_pos
        self.current_map = self.all_maps[current_map_pos]
        self.background_screen = self.current_map["background"]
        self.cells = self.current_map["cells"]
        self.cells_visible = self.current_map["cells_visible"]
        self.sprites = self.current_map["sprites"]

        self.allsprites = pg.sprite.RenderPlain((
                self.sprites,
                self.cells_visible,  # TODO: remove cell from it but keep borders
#                self.cells[(1,1)],
                self.character,
                ))  # character always ontop of sprites : not good

    def unclick(self):
        for button in self.all_buttons:
            button.unclicked()

    def events(self):
        """All clicked regestered"""
        all_keys = pg.key.get_pressed()  # all pressed key at current time
        if (all_keys[pg.K_LCTRL] or all_keys[pg.K_RCTRL]) and all_keys[pg.K_f]:
            self.flags = self.flags ^ pg.FULLSCREEN
            self.reset_app_screen(self.game_screen.rect.size)

        for event in pg.event.get():  # listed key in pressed order

            if event.type == pg.QUIT:  # close windows using red cross
                self.running = False

            elif event.type == pg.KEYDOWN:
                if event.key == pg.K_ESCAPE:  # close windows using escape key
                    self.running = False

            elif event.type == pg.VIDEORESIZE:

                self.reset_app_screen(event.dict['size'])

            elif event.type == pg.MOUSEBUTTONDOWN and event.button == 1:
                # tried with allsprites but keep having errors
                self.check_border = None  # TODO: ugly but necessary for now
                if self.mouse.clicking(self.character):
                    self.character.clicked()
#                    print("clicked character", self.character.rect)
                else:
                    for button in self.all_buttons:
                        if self.mouse.clicking(button):
                            button.clicked()
#                            print("hit button", button)
                            break
                    else:
                        for sprites in self.sprites:
                            if self.mouse.clicking(sprites):
                                sprites.clicked()
#                                print("hit sprite", sprites)
                                break
                        else:
                            for cell_visible in self.cells_visible:
                                if self.mouse.clicking(cell_visible):
                                    for cell_visible_bis in self.cells_visible:
                                        cell_visible_bis.unclicked()
                                    cell_visible.clicked(cell_visible.rect.center)
                                    print("hit cell", cell_visible.rect)
                                    break
                            else:
                                for cell in self.cells.values():
                                    if self.mouse.clicking(cell):
                                        for cell_visible in self.cells_visible:
                                            cell_visible.unclicked()
                                        for cell_bis in self.cells.values():
                                            cell_bis.unclicked()
                                        cell.clicked(cell.rect.center)
    #                                    print("hit cell", cell.rect)
                                        break
#                            else:
#                                if self.mouse.clicking(self.game_screen):
#                                    print("hit no cells")
#                                    self.character.dest(self.mouse.rect.center)
#                                    for cell in self.all_cells:
#                                        cell.unclicked()

            elif event.type == pg.MOUSEBUTTONUP and event.button == 1:
                self.mouse.unclicked()

            else:
                self.character.unhovered()
                for button in self.all_buttons:
                    button.unhovered()
                for sprites in self.sprites:
                    sprites.unhovered()
                for cell_visible in self.cells_visible:
                    cell_visible.unhovered()
                for cell in self.cells.values():
                    cell.unhovered()

                if self.mouse.hovering(self.character):
                    self.character.hovered()
#                    print("hover character", self.character.rect)
                else:
                    for button in self.all_buttons:
                        if button.state_clicked:
                            button.hovered()
#                            print("special hover button", button)
                            break
                    else:
                        for button in self.all_buttons:
                            if self.mouse.hovering(button):
                                button.hovered()
#                                print("hover button", button)
                                break
                        else:
                            for sprites in self.sprites:
                                if self.mouse.hovering(sprites):
                                    sprites.hovered()
#                                    print("hover sprite", sprites)
                                    break
                            else:
                                for cell_visible in self.cells_visible:
                                    if self.mouse.hovering(cell_visible):
                                        cell_visible.hovered()
                                        break
                                else:
                                    for cell in self.cells.values():
                                        if self.mouse.hovering(cell):
                                            cell.hovered()
                                            break

    def update(self, dt):
        self.allsprites.update(dt)  # call update function of each class inside
        for cell in self.cells.values():
            cell.update(dt)
        self.mouse.update(dt)

    def draw(self):
        """Draw Everything"""
        # self.game_screen.blit(self.bg_image, (0, 0))  # blackground
        self.game_screen.image.blit(self.background_screen.image,
                                    self.background_screen.rect)
#        for cell in self.all_cells:  # TODO: temporary just to test and after can remove
#            self.game_screen.image.blit(cell.image, cell.rect)
#        self.allsprites.remove(self.current_map.cells)
        self.allsprites.draw(self.game_screen.image)  # draw moving items
#        self.allsprites.add(self.current_map.cells)

        self.game_screen.image.blit(self.lower_tool_bar.image,
                                    self.lower_tool_bar.rect)

        for button in self.all_buttons:
            self.game_screen.image.blit(button.image,
                                        button.rect)
        # self.allsprites.remove(self.chimp)

        self.game_screen.image.blit(self.mouse.image,
                                    self.mouse.rect)

        self.resize_app_screen()  # resize the game size to the app size

        self.app_screen.blit(self.resized_screen.image,
                             self.resized_screen.rect)

        fps = self.clock.get_fps()
        pg.display.set_caption(f'{round(fps,2)}')

        pg.display.update(self.resized_screen.rect)
        # must be change to have a fixed bg and only change moving objects ?
        # currently change everything

#        pg.display.flip()  # use update instead to only change moving object ?

    def resize_app_screen(self):
        """Scale the game images to fit the app size respecting a
        constant ratio."""
        if self.window_stretched:  # don't want this but keep in code in cell
            # scale the game screen to the window size
            self.resized_screen.image = pg.transform.scale(
                self.game_screen.image, self.app_screen_rect.size)
        else:  # allows to keep ratio
            # compare aspect ratios
            game_ratio = self.game_screen.rect.w / self.game_screen.rect.h
            app_ratio = self.app_screen_rect.w / self.app_screen_rect.h

            if game_ratio < app_ratio:
                width = int(self.app_screen_rect.h / self.game_screen.rect.h
                            * self.game_screen.rect.w)
                height = self.app_screen_rect.h
            else:
                width = self.app_screen_rect.w
                height = int(self.app_screen_rect.w / self.game_screen.rect.w
                             * self.game_screen.rect.h)
            self.resized_screen.image = pg.transform.scale(
                self.game_screen.image, (width, height))
        # get the rect of the resized screen for blitting
        # and center it to the window screen
        self.resized_screen.rect = self.resized_screen.image.get_rect()
        self.resized_screen.rect.center = self.app_screen_rect.center
#        return self.resized_screen.image, self.resized_screen.rect

    def reset_app_screen(self, size):
        self.app_screen = pg.display.set_mode(size, self.flags)
        self.app_screen_rect = self.app_screen.get_rect()
        pg.display.update()

    def border_left(self, *args):

        if args != self.check_border:
            self.character.dest(*args)
            self.check_border = args
#            print("left")

        if self.character.check_pos():
            self.current_map_pos = (self.current_map_pos[0] - 1,
                                    self.current_map_pos[1])
#            print(self.current_map_pos)
            self.change_map(self.current_map_pos)
            self.character.rect.midbottom = (
                self.game_screen.rect.right - 60 - 60/2,
                self.character.rect.midbottom[1]
                )
            self.check_border = None
            return None
        else:
            return False

    def border_right(self, *args):
#        print("arg", args, "previous", self.check_border)
        if args != self.check_border:  # cause problems but could be usefull
#            print("ask dest")
            self.character.dest(*args)
            self.check_border = args
#            print("right")

        if self.character.check_pos():
            self.current_map_pos = (self.current_map_pos[0] + 1,
                                    self.current_map_pos[1])
#            print(self.current_map_pos)
            self.change_map(self.current_map_pos)
            self.character.rect.midbottom = (
                self.game_screen.rect.left + 60 + 60/2,
                self.character.rect.midbottom[1]
                )
            self.check_border = None
            return None
        else:
            return False

    def border_top(self, *args):

        if args != self.check_border:
            self.character.dest(*args)
            self.check_border = args
#            print("top")

        if self.character.check_pos():
            self.current_map_pos = (self.current_map_pos[0],
                                    self.current_map_pos[1] - 1)
#            print(self.current_map_pos)
            self.change_map(self.current_map_pos)
            self.character.rect.midbottom = (
                    self.character.rect.midbottom[0],
                    self.game_screen.rect.bottom - 60 - 60/2 - 127
                )
            self.check_border = None
            return None
        else:
            return False

    def border_bottom(self, *args):

        if args != self.check_border:
            self.character.dest(*args)
            self.check_border = args
#            print("bottom")

        if self.character.check_pos():
            self.current_map_pos = (self.current_map_pos[0],
                                    self.current_map_pos[1] + 1)
#            print(self.current_map_pos)
            self.change_map(self.current_map_pos)
            self.character.rect.midbottom = (
                self.character.rect.midbottom[0],
                self.game_screen.rect.top + 60 + 60/2
                )
            self.check_border = None
            return None
        else:
            return False

    def run(self):
        self.running = True
        while self.running:
            self.dt = self.clock.tick()/1000  # don't delay the game to 60 Hz
            self.events()  # look for commands
            self.dt_accumulator += self.dt
            step = 0
            while self.dt_accumulator >= self.dt_fixed:
                step += 1
                if step > 30:
                    self.dt_fixed *= 2
                self.update(self.dt_fixed)  # update movement
#                time.sleep(0.02)

                self.dt -= self.dt_fixed
                self.dt_accumulator -= self.dt_fixed

#            print(step, self.dt_fixed)

            self.draw()  # draw everything after the movements

        pg.display.quit()
        pg.quit()

# Game Over


if __name__ == "__main__":

    # wanted resolution (knowing that the game will have a different resolution
    # and will resize to match this size)
    WINDOW_W = 500
    WINDOW_H = 400

    game = Game(WINDOW_W=WINDOW_W, WINDOW_H=WINDOW_H)
    game.run()
