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
        self.image, self.rect = load_image("mouse.png")  # , -1)
        self.clicking = False

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

        if self.clicking:
            self.rect.move_ip(5, 10)  # good for button

    def clicked(self, target):
        """returns true if the mouse collides with the target"""
#        if not self.clicking:  # clicked only once and wait to unpress clicking
        self.clicking = True
#        self.position()
        hitbox = self.rect  # .inflate(-5, -5) # change the size - = reduce
#        print(hitbox, target.rect)
        return hitbox.colliderect(target.rect)

    def unclicked(self):
        """called to pull the mouse back"""
        self.clicking = False
        self.Game.unclick()


class Chimp(pg.sprite.Sprite):
    """moves a monkey critter across the screen. it can spin the
       monkey when it is punched."""

    def __init__(self, Game):
        self.Game = Game  # add real-time variable change from the Game class
        pg.sprite.Sprite.__init__(self)  # call Sprite intializer
        self.area = self.Game.game_screen.rect  # walkable space (updated)

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

    def punched(self):
        """this will cause the monkey to start spinning"""
        if not self.dizzy:
            self.dizzy = 1
            self.original = self.image


class Character(pg.sprite.Sprite):
    """moves a character across the screen."""

    def __init__(self, Game):
        self.Game = Game  # add real-time variable change from the Game class
        pg.sprite.Sprite.__init__(self)  # call Sprite intializer
        self.area = self.Game.game_screen.rect  # walkable space (updated)

        self.image, self.rect = load_image("character.png", -1)
        self.rect.topleft = 0, 100

        self.position = self.rect.midbottom
        self.dest_coord = self.position
        self.moving = False
        self.max_speed = 5

    def update(self, dt):  # implicitly called from allsprite update
        """walk depending on the character state"""
        if self.moving:
            self._walk(dt)
        else:
            pass

    def destination(self, real_pos):

        if (self.area.left < real_pos[0] < self.area.right
                and self.area.top < real_pos[1] < self.area.bottom):
            self.dest_coord = real_pos
            self.moving = True

    def _walk(self, dt):
        """move the character across the screen"""
        self.position = self.rect.midbottom
        acceptance = 20
        interv_low = (self.dest_coord[0] - acceptance,
                      self.dest_coord[1] - acceptance)
        interv_high = (self.dest_coord[0] + acceptance,
                       self.dest_coord[1] + acceptance)

        if (interv_low[0] < self.position[0] < interv_high[0]
                and interv_low[1] < self.position[1] < interv_high[1]):
            # if self.position == self.dest_coord:  # not stable
            self.speed_x = 0  # can remove self
            self.speed_y = 0
            self.position = self.dest_coord
            self.rect.midbottom = self.position
            self.moving = False
            pass

        x_length = self.dest_coord[0] - self.position[0]
        y_length = self.dest_coord[1] - self.position[1]

        theta = math.atan2(y_length, x_length)

#        theta = np.pi/2 * (theta // (np.pi/2))  # allows only cross movement
        theta = np.pi/4 * (theta // (np.pi/4))  # allows cross + diagonal mov

        self.speed_x = self.max_speed * math.cos(theta)
        self.speed_y = self.max_speed * math.sin(theta)  # meter per second

        self.move_x = self.speed_x * self.Game.ratio_pix_meter_x * dt
        self.move_y = self.speed_y * self.Game.ratio_pix_meter_y * dt

        newpos = self.rect.move((self.move_x, self.move_y))
        self.rect = newpos


class Cell(pg.sprite.Sprite):
    """simple cell to target movement"""
    def __init__(self, size, position):
        pg.sprite.Sprite.__init__(self)  # call Sprite intializer
        self.image = pg.Surface(size)
        self.rect = self.image.get_rect()
        self.rect.center = position
        color = (200, 100, 50)
        self.image.fill(color)


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


class Button():
    """buttons"""
    def __init__(self, Game, function, *args):
        self.Game = Game
        self.function = function

        self.image, self.rect = load_image(*args)

        self.position = self.rect  # same id until clicked occured, then copy
        self.state = False

    def add_text(self, text, center=None):
        font = pg.font.Font(None, 36)
        msg = font.render(text, 1, (10, 10, 10))

        if center is None:
            textpos = msg.get_rect(centery=self.rect.h/2)
        else:
            textpos = msg.get_rect().center = center

        self.image.blit(msg, textpos)

    def clicked(self):
        if self.Game.mouse.clicking:
            # open if closed or close if openned
            self.position = self.rect.copy()
            self.rect.move_ip(1, 1)
            self.state = not self.state
            self.function(self.state)  # TODO: could be nice to have args and kwargs here
#            print("here", self.position, "state", self.state)

    def unclicked(self):
        self.rect = self.position
        self.position = self.rect  # same id from now


class Game():
    """this function is called when the program starts.
       it initializes everything it needs, then runs in
       a loop until the function returns."""

    def __init__(self, WINDOW_W=1920, WINDOW_H=1080):
        GAME_SCREEN_W = 1920
        GAME_SCREEN_H = 1080

        self.ratio_pix_meter_x = GAME_SCREEN_W/16  # pixel/meter
        self.ratio_pix_meter_y = GAME_SCREEN_H/9  # pixel/meter

        pg.init()

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

        # create the background, then the interface, then the object
        self.background_screen = BackGround('background.png')
        self.background_screen.rect.center = self.game_screen.rect.center

        self.lower_tool_bar = BackGround('lower_bar.png')
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

        self.all_buttons = [self.button_1, self.button_2,
                ]

        # Prepare Game Objects
        self.clock = pg.time.Clock()
        self.dt_fixed = 1 / 60
        self.dt_accumulator = 0
        self.dt = 0
    #    whiff_sound = load_sound("whiff.wav")
    #    punch_sound = load_sound("punch.wav")
        self.mouse = Mouse(self)
        self.chimp = Chimp(self)
        self.character = Character(self)

        self.all_cells = [Cell(size=(40, 40), position=(500, 100)),
                          Cell(size=(40, 40), position=(800, 200)),
                          Cell(size=(40, 40), position=(1000, 300)),
                          Cell(size=(40, 40), position=(100, 700)),
                          ]
#        self.mouse = Mouse(game)
        self.allsprites = pg.sprite.RenderPlain((self.mouse, self.chimp,
                                                 self.character))
#        self.allsprites = pg.sprite.RenderPlain((self.chimp))
#        self.allsprites.add(self.mouse)

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
#                elif event.key == pg.K_s:  # if want to toggle respect ratio
#                    self.window_stretched = not self.window_stretched
#                    self.reset_app_screen(self.app_screen_rect.size)
#                elif event.key == pg.K_f:
#                    # toggle fullscreen  # TODO: for now because mouse is
#                    # not adapted to it and change speed if
#                    # game_size != real screen (fullscreen=zoom)
#                    self.flags = self.flags ^ pg.FULLSCREEN
#                    self.reset_app_screen(self.game_screen.rect.size)
#                elif event.key == pg.K_r:  # if want to toggle resizability
#                    # toggle fullscreen
#                    self.flags = self.flags ^ pg.RESIZABLE
#                    self.reset_app_screen(self.app_screen_rect.size)

            elif event.type == pg.VIDEORESIZE:
                # if the user resizes the window (drag the bottom right corner)
                # get the new size from the event dict and reset the
                # window screen surface
                self.reset_app_screen(event.dict['size'])

            elif event.type == pg.MOUSEBUTTONDOWN and event.button == 1:
                if self.mouse.clicked(self.chimp):
                    print("hit chimp")
                    # punch_sound.play()  # punch
                    self.chimp.punched()
                else:
                    for button in self.all_buttons:
                        if self.mouse.clicked(button):
                            button.clicked()
                            break
                    else:
                        for cell in self.all_cells:
                            if self.mouse.clicked(cell):
                                print("hit cell", cell.rect)
                                self.character.destination(cell.rect.center)
                                break
                        else:
                            if self.mouse.clicked(self.game_screen):
                                print("hit no cells, moving to destination")
                                self.character.destination(self.mouse.rect.center)

                    # whiff_sound.play()  # miss
                    ""
            elif event.type == pg.MOUSEBUTTONUP and event.button == 1:
                self.mouse.unclicked()

    def update(self, dt):
        self.allsprites.update(dt)  # call update function of each class inside

    def draw(self):
        """Draw Everything"""
        # self.game_screen.blit(self.bg_image, (0, 0))  # blackground
        self.game_screen.image.blit(self.background_screen.image,
                                    self.background_screen.rect)
        for cell in self.all_cells:  # TODO: temporary just to test and after can remove
            self.game_screen.image.blit(cell.image, cell.rect)

        self.game_screen.image.blit(self.lower_tool_bar.image,
                                    self.lower_tool_bar.rect)

        for button in self.all_buttons:
            self.game_screen.image.blit(button.image,
                                        button.rect)
        # self.allsprites.remove(self.chimp)

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

    def run(self):
        self.running = True
        while self.running:
            self.dt = self.clock.tick()/1000  # delay the game to 60 Hz
            self.events()  # look for commands
            self.dt_accumulator += self.dt
#            step = 0
#            print(self.dt)
            while self.dt_accumulator >= self.dt_fixed:
#                step += 1
                self.update(self.dt_fixed)  # update movement
#                time.sleep(0.02)

                self.dt -= self.dt_fixed
                self.dt_accumulator -= self.dt_fixed

#            print(step)

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
