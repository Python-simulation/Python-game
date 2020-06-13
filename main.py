
"""
Pygame game.

This simple example is used for the line-by-line tutorial
that comes with pygame. It is based on a 'popular' web banner.
Note there are comments here, but for the full explanation,
follow along in the tutorial.
"""

# Import Modules
import os
# import time
import pygame as pg

from interface.mouse import Mouse
from interface.npc.you import You
from interface.interface_functions import NeededFunctions

from interface.background import BackGround
from interface.map_functions import MapFunctions

from interface.lower_bar import LowerBar

from interface.findpath import cell_sizes

from interface.menu import Menu

if not pg.font:
    print("Warning, fonts disabled")
if not pg.mixer:
    print("Warning, sound disabled")

os.environ['SDL_VIDEO_WINDOW_POS'] = "%d,%d" % (50, 50)

main_dir = os.path.split(os.path.abspath(__file__))[0]
data_dir = os.path.join(main_dir, "data")

nf = NeededFunctions()
mp = MapFunctions()


class Game():
    """
    Game class called when the program starts.

    it initializes everything it needs, then runs in
    a loop until the function returns.
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

        self.check_border = None

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

        pg.display.set_caption("Testing")
        pg.mouse.set_visible(1)

        # Create The Backgound that never changes (with fixed toolbar)
        # self.bg_image = pg.Surface(self.game_screen.get_size()).convert()
        # background_color = (200, 200, 200)
        # self.bg_image.fill(background_color)

        self.lower_bar = LowerBar(self)
        self.lower_tool_bar = self.lower_bar.lower_tool_bar

        self.all_buttons = []
        self.all_buttons.extend(self.lower_bar.buttons)

        # Prepare Game Objects
        self.clock = pg.time.Clock()
        self.dt_fixed = 1 / 60  # fps fixed for all computations (!= seen fps)
        self.dt_accumulator = 0
        self.dt = 0
        self.time_warning = 0
        # whiff_sound = load_sound("whiff.wav")
        # punch_sound = load_sound("punch.wav")
        self.mouse = Mouse(self)

        cell_pos = (3, 16)
        self.character = You(self, cell_pos)

        self.allsprites = pg.sprite.RenderPlain(())  # init -> cell use it befo
        self.all_maps = self.all_maps_fct(self)
        self.change_map((0, 0))

        self.game_screen.image.blit(self.background_screen.image,
                                    self.background_screen.rect)

        self.menu = Menu(self)

    def loader(self):
        self.data_dir = data_dir
        self.all_maps_fct = mp.create_maps
        self.function_test = nf.function_test
        self.function_test2 = nf.function_test2

    def change_map(self, new_map_pos):
        self.current_map_pos = new_map_pos
        map_class = self.all_maps[new_map_pos]
        map_class.refresh()
        self.current_map = map_class.map_info
        self.background_screen = self.current_map["background"]
        self.bg_sprites = self.current_map["background_sprites"]
        self.cells = self.current_map["cells"]  # dict
        self.cells_visible = self.current_map["borders"]  # dict
        self.cells.update(self.cells_visible)  # TODO:need to decide what to do
        self.all_cells = dict(self.cells_visible)
        self.all_cells.update(self.cells)
        self.sprites = self.current_map["sprites"]

        self.allsprites = pg.sprite.LayeredUpdates((
            # self.character,
            self.bg_sprites,
            # self.cells_visible.values(),
            self.sprites,
            self.character,
            ))
        # for cells in self.cells.values():
        #     self.allsprites.add(cells)
        # self.allsprites.add(self.mouse)

    def unclick(self):
        for button in self.all_buttons:
            button.unclicked()

    def events(self):
        """All clicked regestered"""
        all_keys = pg.key.get_pressed()  # all pressed key at current time

        if (all_keys[pg.K_LCTRL] or all_keys[pg.K_RCTRL]) and all_keys[pg.K_f]:
            self.flags = self.flags ^ pg.FULLSCREEN
            self.reset_app_screen(self.game_screen.rect.size)

        if ((all_keys[pg.K_LCTRL] or all_keys[pg.K_RCTRL])
                and (all_keys[97] or all_keys[122])):  # BUG: q or w, value are wrong
            self.running = False

        for event in pg.event.get():  # listed key in pressed order

            if event.type == pg.QUIT:  # close windows using red cross
                self.running = False

            elif event.type == pg.KEYDOWN:
                if event.key == pg.K_ESCAPE:  # pause the game using escape key
                    self.menu.run(self.dt)

            elif event.type == pg.VIDEORESIZE:
                self.reset_app_screen(event.dict['size'])

            elif event.type == pg.MOUSEBUTTONDOWN and event.button == 1:
                # tried with allsprites but keep having errors
                if self.mouse.clicking(self.character):
                    # OPTIMIZE: could remove from it by using
                    # list(reversed(sprites)) but Group is not a callable
                    for sprite in self.allsprites:
                        # BUG: ?? set state=False to cells and can't teleport if click on menu
                        sprite.unclicked()
                        # print("unclicking", sprite)

                    self.character.clicked()
                    # print("clicked character", self.character.rect)
                else:
                    for button in self.all_buttons:
                        if self.mouse.clicking(button):
                            # reminder that unclicked occure here before
                            button.clicked()
#                            print("hit button", button)
                            break
                    else:
                        self.check_border = None  # OPTIMIZE: ugly but necessary for now

                        for sprite in self.allsprites:
                                sprite.unclicked()
                                # print("unclicking", sprite)

                        for sprites in self.sprites:
                            # print("tried to clicked on ", sprites)
                            if self.mouse.clicking(sprites):
                                # print("just clicked on ", sprites)
                                sprites.clicked()
#                                print("hit sprite", sprites)
                                break
                        else:
                            for cell in self.all_cells.values():
                                if self.mouse.clicking(cell):
                                    for cell_bis in self.all_cells.values():
                                        cell_bis.unclicked()
                                    cell.clicked()
                                    # print("hit cell", cell.rect)
                                    break
                            # else:
                            #     if self.mouse.clicking(self.game_screen):
                            #         print("hit no cells")
                            #         self.character.dest(self.mouse.rect.topleft)
                            #         for cell in self.all_cells.values():
                            #             cell.unclicked()

            elif event.type == pg.MOUSEBUTTONUP and event.button == 1:
                self.mouse.unclicked()

            else:
                self.character.unhovered()
                for button in self.all_buttons:
                    button.unhovered()
                for sprites in self.sprites:
                    sprites.unhovered()
                for cell in self.all_cells.values():
                    cell.unhovered()
                pg.mouse.set_cursor(*pg.cursors.diamond)
                if self.mouse.hovering(self.character):
                    self.character.hovered()
#                    print("hover character", self.character.rect)
                else:  # OPTIMIZE: tried without succes to do one for loop
                    for button in self.all_buttons:
                        if self.mouse.hovering(button):
                            pg.mouse.set_cursor(*pg.cursors.ball)
                            button.hovered()
                            # print("hover button", button)
                            break
                    else:
                        for sprites in self.sprites:
                            if self.mouse.hovering(sprites):
                                sprites.hovered()
                                pg.mouse.set_cursor(*pg.cursors.ball)
#                                    print("hover sprite", sprites)
                                break
                        else:
                            for cell in self.all_cells.values():
                                if self.mouse.hovering(cell):
                                    cell.hovered()
                                    break
                            else:
                                pg.mouse.set_cursor(*pg.cursors.arrow)

    def update(self, dt):
        self.allsprites.update(dt)  # call update function of each class inside
        for cell in self.cells.values():
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
        self.game_screen.image.blit(self.background_screen.image,
                                    self.background_screen.rect)
        # for rect in self.old_rects:
        #     self.game_screen.image.blit(self.background_screen.image,
        #                                 rect, rect)

        # self.new_rects = self.rect_coverage(
        #     self.allsprites)#, self.all_buttons)

        # for rect in self.new_rects:
        #     self.game_screen.image.blit(self.background_screen.image,
        #                                 rect, rect)

        self.allsprites.draw(self.game_screen.image)  # draw moving items

        self.game_screen.image.blit(self.lower_tool_bar.image,
                                    self.lower_tool_bar.rect)

        for button in self.all_buttons:
            self.game_screen.image.blit(button.image,
                                        button.rect)

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

        if args != self.check_border:
            self.character.dest(*args)
            self.check_border = args

        char_pos = self.character.rect.midbottom
        char_pos = (char_pos[0], char_pos[1] - cell_sizes[1]/2)

        if char_pos == args[0] and self.character.road == list():
            self.change_map(new_map_pos)
            self.character.rect.midbottom = new_char_pos
            self.check_border = None
            return None
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
            #     self.allsprites)#, self.all_buttons)

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
