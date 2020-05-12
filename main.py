"""
This simple example is used for the line-by-line tutorial
that comes with pygame. It is based on a 'popular' web banner.
Note there are comments here, but for the full explanation,
follow along in the tutorial.
"""

# Import Modules
import os
import pygame as pg

from interface.button import Button
from interface.mouse import Mouse
from interface.character import Character
from interface.interface_functions import NeededFunctions

from interface.background import BackGround
from interface.map_functions import MapFunctions

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
    """this function is called when the program starts.
       it initializes everything it needs, then runs in
       a loop until the function returns."""

    def __init__(self, WINDOW_W=1920, WINDOW_H=1080):
        GAME_SCREEN_W = 1920
        GAME_SCREEN_H = 1080

        self.ratio_pix_meter_x = GAME_SCREEN_W/32  # pixel/meter
        self.ratio_pix_meter_y = GAME_SCREEN_H/18  # pixel/meter

        pg.init()
        self.check_border = None
        self.flags = (
                pg.RESIZABLE |
                pg.DOUBLEBUF
                )

        self.loader()

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

#        self.clock = pg.time.Clock()

        pg.display.set_caption("Testing")
        pg.mouse.set_visible(1)

        # Create The Backgound that never changes (with fixed toolbar)
#        self.bg_image = pg.Surface(self.game_screen.get_size()).convert()
#        background_color = (200, 200, 200)
#        self.bg_image.fill(background_color)

        name = os.path.join(self.data_dir, 'lower_bar.png')
        self.lower_tool_bar = BackGround(name, -1)
        self.lower_tool_bar.rect.midbottom = self.game_screen.rect.midbottom

#        self.button_1 = Button(self, self.function_test,
#                               ('button_1.png', -1), (1000,100),
#                               "button 1", (30,0))

        self.button_1 = Button(self, self.function_test, name='button_1.png')
        self.button_1.add_text("button 1")  # , center = (0,0)
        self.button_1.rect.midbottom = self.lower_tool_bar.rect.midbottom
        self.button_1.rect.y -= 12
        self.button_1.rect.left = 950

        self.button_2 = Button(self, self.function_test2, 'button_1.png')
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
        self.character = Character(self)

        self.all_maps = self.all_maps_fct(self)
#        self.current_map_pos = (0, 0)
        self.change_map((0, 0))

    #    self.chimp = Chimp(self)

#        self.character.rect.midbottom = self.cells[(1,1)].rect.center

    def loader(self):
        self.data_dir = data_dir
        self.all_maps_fct = mp.all_maps
        self.function_test = nf.function_test
        self.function_test2 = nf.function_test2

    def change_map(self, current_map_pos):
        self.current_map_pos = current_map_pos
        self.current_map = self.all_maps[current_map_pos]
        self.background_screen = self.current_map["background"]
        self.cells = self.current_map["cells"]
        self.cells_visible = self.current_map["cells_visible"]
        self.sprites = self.current_map["sprites"]

        self.allsprites = pg.sprite.RenderPlain((
                self.sprites,
                self.cells_visible,
                ))  # character always ontop of sprites : not good
#        for cells in self.cells.values():
#            self.allsprites.add(cells)
        self.allsprites.add(self.character)

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
                        self.check_border = None  # TODO: ugly but necessary for now
                        for sprites in self.sprites:
                            if self.mouse.clicking(sprites):
                                sprites.clicked()
#                                print("hit sprite", sprites)
                                break
                        else:  # TODO: ugly, check if need to unclicked cell
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
#                                    for cell in self.cells_values():
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

    def border_left(self, *args):

        if args != self.check_border:
            self.character.dest(*args)
            self.check_border = args
#            print("left")

        if (self.character.rect.midbottom == args[0]
                and self.character.road == list()):
            self.current_map_pos = (self.current_map_pos[0] - 1,
                                    self.current_map_pos[1])
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
        if args != self.check_border:
            self.character.dest(*args)
            self.check_border = args
#            print("right")

        if (self.character.rect.midbottom == args[0]
                and self.character.road == list()):
            self.current_map_pos = (self.current_map_pos[0] + 1,
                                    self.current_map_pos[1])
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

        if (self.character.rect.midbottom == args[0]
                and self.character.road == list()):
            self.current_map_pos = (self.current_map_pos[0],
                                    self.current_map_pos[1] - 1)
            self.change_map(self.current_map_pos)
            self.character.rect.midbottom = (
                    self.character.rect.midbottom[0],
                    self.game_screen.rect.bottom - 60 - 60/2 - 60*2
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

        if (self.character.rect.midbottom == args[0]
                and self.character.road == list()):
            self.current_map_pos = (self.current_map_pos[0],
                                    self.current_map_pos[1] + 1)
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
        self.dt = self.clock.tick()/1000  # avoid taking init time into account
        while self.running:
            self.dt = self.clock.tick()/1000  # time from the last computation
            self.events()  # look for commands
            self.dt_accumulator += self.dt
            step = 0
            while self.dt_accumulator >= self.dt_fixed:
                step += 1
#                if step > 20:
#                    self.dt_fixed *= 2
                self.update(self.dt_fixed)  # update movement
#                time.sleep(0.02)

                self.dt -= self.dt_fixed
                self.dt_accumulator -= self.dt_fixed

            if step > 50:
                print("game is broken due to too much lagging")
#                print("saving data to temporary files")
                self.running = False
#            if step > 20:
#                print("warning",
#                      "physics can be broken due to too much lagging")
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
