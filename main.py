# -*- coding: utf-8 -*-
"""
Pygame game.

Game description.
"""

# Import Modules
import os
import time
import pygame as pg

from interface.mouse import Mouse
from interface.npc.you import You
from interface.interface_functions import NeededFunctions

from interface.background import BackGround
from interface.maps.map_functions import MapFunctions

from interface.lower_bar import LowerBar

from interface.findpath import cell_sizes

from interface.menu import Menu
from interface.display import Display

from interface.ground import ground

# OPTIMIZE: temporary & should be remove in final version
from interface.maps.map_generator import MapGenerator

if not pg.font:
    print("Warning, fonts disabled")
if not pg.mixer:
    print("Warning, sound disabled")

os.environ['SDL_VIDEO_WINDOW_POS'] = "%d,%d" % (50, 50)

main_dir = os.path.split(os.path.abspath(__file__))[0]
data_dir = os.path.join(main_dir, "data")

nf = NeededFunctions()
mf = MapFunctions()


class Game():
    """
    Game class called when the program starts.

    it initializes everything it needs, then runs in
    a loop until the player stop the game.
    """

    def __init__(self, size=(1920, 1080)):
        pg.init()
        self.loader()
        name = os.path.join(self.data_dir, "logo32x32.png")
        logo = pg.image.load(name)
        pg.display.set_icon(logo)

        GAME_SCREEN_W = 1920
        GAME_SCREEN_H = 1080

        self.size = (GAME_SCREEN_W, GAME_SCREEN_H)

        self.ratio_pix_meter_x = GAME_SCREEN_W/32  # pixel/meter
        self.ratio_pix_meter_y = GAME_SCREEN_H/18  # pixel/meter
        assert self.ratio_pix_meter_x == self.ratio_pix_meter_y
        self.ratio_pix_meter = self.ratio_pix_meter_x

        self.flags = (
                pg.RESIZABLE |
                pg.DOUBLEBUF
                )

        # application window surface
        self.app_screen = pg.display.set_mode(size, self.flags)
        self.app_screen_rect = self.app_screen.get_rect()

        # game screen surface (where all the ingame stuff gets blitted on)
        self.game_screen = BackGround(size=(GAME_SCREEN_W, GAME_SCREEN_H))

        self.resized_screen = BackGround()

        pg.display.set_caption("Loading screen")
        pg.mouse.set_visible(1)

        self.allsprites = pg.sprite.LayeredUpdates()  # init -> cell use it befo

        loading_image = BackGround(size=self.game_screen.image.get_size())
        loading_image.image.fill((200, 200, 200))
        load_txt = Display(self, "Loading game",
                           self.game_screen.rect.center, 100)
        loading_image.image.blit(load_txt.image, load_txt.rect)
        self.background_screen = loading_image

        self.allsprites.add(self.background_screen)

        # Prepare Game Objects
        self.clock = pg.time.Clock()
        self.dt_fixed = 1 / 60  # fps fixed for all computations (!= seen fps)
        self.dt_accumulator = 0
        self.dt = 0
        self.time_warning = 0
        # whiff_sound = load_sound("whiff.wav")
        # punch_sound = load_sound("punch.wav")

        self.draw()
        # time.sleep(3)

        self.mouse = Mouse(self)

        self.lower_bar = LowerBar(self)

        cell_pos = (3, 16)  # will be defined in a load file
        self.character = You(self)
        self.character.change_position(cell_pos)

        self.ground_dict = ground(self)  # OPTIMIZE: ugly position in script
        self.all_maps = self.create_maps(self)

        self.map_pos_txt = Display(self)
        self.change_map((0, 0))  # will be defined in a load file

        self.pause = Menu(self)
        self.map_generator = MapGenerator(self)
        # self.menu.run(self.dt)

    def loader(self):
        """used to call those variables in other files from the main game
        class"""
        self.main_dir = main_dir
        self.data_dir = data_dir
        self.mf = mf
        self.create_maps = mf.create_maps
        self.function_test = nf.function_test
        self.function_test2 = nf.function_test2

    def change_map(self, new_map_pos):
        self.current_map_pos = new_map_pos
        map_class = self.all_maps[new_map_pos]
        map_class.refresh()
        self.current_map = map_class
        self.map_info = map_class.map_info
        self.background_screen = self.map_info["background"]
        self.bg_sprites = self.map_info["background_sprites"]
        self.cells = self.map_info["cells"]  # dict
        self.cells_visible = self.map_info["borders"]  # dict
        self.cells.update(self.cells_visible)  # TODO:need to decide what to do
        self.all_cells = dict(self.cells_visible)
        self.all_cells.update(self.cells)
        self.npc = self.map_info["npc"]
        self.map_pos_txt.text(new_map_pos)
        self.map_pos_txt.rect.topleft = (self.map_pos_txt.rect.h/2,
                                         self.map_pos_txt.rect.h/2)

        self.allsprites = pg.sprite.LayeredUpdates()
        self.allsprites.add(self.background_screen, layer=0)
        # self.allsprites.add(self.all_cells.values(), layer=0)
        self.allsprites.add(self.bg_sprites, layer=1)
        self.allsprites.add(self.npc, layer=1)
        self.allsprites.add(self.character, layer=1)
        self.allsprites.add(self.lower_bar, layer=3)
        self.allsprites.add(self.lower_bar.buttons, layer=3)
        self.allsprites.add(self.map_pos_txt, layer=3)
        # self.allsprites.add(self.mouse, layer=4)

        sprites = self.map_info["sprites"]  # OPTIMIZE: temporary for dev
        self.allsprites.add(sprites, layer=2)

        for npc in self.npc:  # avoid bug if npc behing sprite
            npc.change_order()

        self.character.change_order()
        # self.allsprites.add(self.cells.values(), layer=0)

    def click(self):
        for sprite in self.allsprites.sprites()[::-1]:
            # print("tried to clicked on ", sprite)
            if self.mouse.clicking(sprite):
                output = sprite.clicked()
                # print("just clicked on ", sprite, output)
                if output is True:
                    break

        else:
            for cell in self.all_cells.values():
                # print("tried to clicked on ", cell)
                if self.mouse.clicking(cell):
                    # print("just clicked on ", cell)
                    output = cell.clicked()
                    # print("hit cell", cell.rect, cell.active, output)
                    if output is True:
                        break

    def unclick(self):  # could do function clicked, unclicked, hovered,.. ?
        for sprite in self.allsprites:
            sprite.unclicked()

    def hover(self):
        """Try to hover each sprite following the layer order"""

        for sprite in self.allsprites.sprites()[::-1]:
            # print("tried to hover on ", sprite)
            if self.mouse.hovering(sprite):
                output = sprite.hovered()
                # print("just hovered ", sprite, output)
                if output is True:
                    break

        else:
            for cell in self.all_cells.values():
                if self.mouse.hovering(cell):
                    output = cell.hovered()
                    # print("hover cell", cell)
                    if output is True:
                        break
            else:
                pg.mouse.set_cursor(*pg.cursors.arrow)

    def unhover(self):
        for sprite in self.allsprites:
            sprite.unhovered()

    def events(self):
        """All clicked regestered"""
        all_keys = pg.key.get_pressed()  # all pressed key at current time

        if (all_keys[pg.K_LCTRL] or all_keys[pg.K_RCTRL]) and all_keys[pg.K_f]:
            self.flags = self.flags ^ pg.FULLSCREEN
            self.reset_app_screen(self.game_screen.rect.size)

        if ((all_keys[pg.K_LCTRL] or all_keys[pg.K_RCTRL])
                and (all_keys[97] or all_keys[122])):
            # BUG: q or w, value are wrong
            self.running = False

        for event in pg.event.get():  # listed key in pressed order

            if event.type == pg.QUIT:  # close windows using red cross
                self.running = False

            elif event.type == pg.KEYDOWN:
                if event.key == pg.K_ESCAPE:  # pause the game using escape key
                    self.map_generator.run(self.dt)
                    # self.pause.run(self.dt)

            elif event.type == pg.VIDEORESIZE:
                self.reset_app_screen(event.dict['size'])

            elif event.type == pg.MOUSEBUTTONDOWN and event.button == 1:
                self.click()

            elif event.type == pg.MOUSEBUTTONUP and event.button == 1:
                self.mouse.unclicked()

            else:
                self.unhover()
                self.hover()

    def update(self, dt):
        self.allsprites.update(dt)  # call update function of each class inside
        for cell in self.all_cells.values():
            # OPTIMIZE: check if all_cell or cell
            cell.update(dt)
        self.mouse.update(dt)

    # def rect_coverage(self, *args):
    #     """args are rect"""
    #     rect_list = list()

    #     for arg in args:
    #         if isinstance(arg, list):
    #             for sprite in arg:
    #                 rect_list.append(sprite.rect.copy())
    #         elif isinstance(arg, dict):
    #             # print("dict")
    #             for sprite in arg.values():
    #                 rect_list.append(sprite.rect.copy())
    #         elif isinstance(arg, pg.sprite.Group):
    #             for sprite in arg:
    #                 rect_list.append(sprite.rect.copy())
    #         else:
    #             for sprite in arg:
    #                 rect_list.append(sprite.rect.copy())
    #     return rect_list

    def draw(self):
        """Draw Everything"""
        # for rect in self.old_rects:
        #     self.game_screen.image.blit(self.background_screen.image,
        #                                 rect, rect)

        # self.new_rects = self.rect_coverage(
        #     self.allsprites)

        # for rect in self.new_rects:
        #     self.game_screen.image.blit(self.background_screen.image,
        #                                 rect, rect)

        self.allsprites.draw(self.game_screen.image)  # draw moving items

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

    def reset_app_screen(self, size):
        self.app_screen = pg.display.set_mode(size, self.flags)
        self.app_screen_rect = self.app_screen.get_rect()
        pg.display.update()

    def teleportation(self, new_map_pos, new_char_pos, *args):
        new_char_pos = (new_char_pos[0], new_char_pos[1] + cell_sizes[1]/2)

        self.character.dest(*args)

        char_pos = self.character.position
        char_pos = (char_pos[0], char_pos[1] - cell_sizes[1]/2)

        if char_pos == args[0] and self.character.road == list():
            self.character.position = new_char_pos
            self.character.rect.midbottom = new_char_pos  # avoid sprite bug
            self.change_map(new_map_pos)
            return True
        else:
            return False

    def border_left(self, *args):
        new_map_pos = (self.current_map_pos[0] - 1,
                       self.current_map_pos[1])
        right = (self.game_screen.rect.right//cell_sizes[0])*cell_sizes[0]
        new_char_pos = (
            right - cell_sizes[0]/2,
            self.character.rect.midbottom[1] - cell_sizes[1]/2
        )
        return self.teleportation(new_map_pos, new_char_pos, *args)

    def border_right(self, *args):
        new_map_pos = (self.current_map_pos[0] + 1,
                       self.current_map_pos[1])
        new_char_pos = (
            self.game_screen.rect.left + cell_sizes[0]/2,
            self.character.rect.midbottom[1] - cell_sizes[1]/2
        )
        return self.teleportation(new_map_pos, new_char_pos, *args)

    def border_top(self, *args):
        new_map_pos = (self.current_map_pos[0],
                       self.current_map_pos[1] - 1)
        bottom = (self.game_screen.rect.bottom//cell_sizes[1])*cell_sizes[1]
        new_char_pos = (
            self.character.rect.midbottom[0],
            bottom - cell_sizes[1]/2 - cell_sizes[1]  # toolbar size
        )
        return self.teleportation(new_map_pos, new_char_pos, *args)

    def border_bottom(self, *args):
        new_map_pos = (self.current_map_pos[0],
                       self.current_map_pos[1] + 1)
        new_char_pos = (
            self.character.rect.midbottom[0],
            self.game_screen.rect.top + cell_sizes[1]/2
        )
        return self.teleportation(new_map_pos, new_char_pos, *args)

    def run(self):
        self.running = True
        self.dt = self.clock.tick()/1000  # avoid taking init time into account

        while self.running:
            self.dt = self.clock.tick(80)/1000  # time of the last computation
            self.events()  # look for commands
            self.dt_accumulator += self.dt
            step = 0

            # self.old_rects = self.rect_coverage(
            #     self.allsprites)

            while self.dt_accumulator >= self.dt_fixed:
                step += 1
                # if step > 100:
                #     break
#                    self.dt_fixed *= 2
                self.update(self.dt_fixed)  # update movement
                # time.sleep(0.02)

                self.dt -= self.dt_fixed
                self.dt_accumulator -= self.dt_fixed

            if step > 20:
                self.time_warning += 1
            else:
                self.time_warning = 0

            if self.time_warning > 5:
                print("game is broken due to too much lagging")
#                print("saving data to temporary files")
                self.running = False
            # print(step, self.dt_fixed)

            self.draw()  # draw everything after the movements

        pg.display.quit()
        pg.quit()

# Game Over


if __name__ == "__main__":

    # wanted resolution (knowing that the game will have a different resolution
    # and will resize to match this size)
    WINDOW_W = 1024
    WINDOW_H = 768

    game = Game(size=(WINDOW_W, WINDOW_H))
    game.run()
