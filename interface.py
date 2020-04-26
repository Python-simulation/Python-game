"""
This simple example is used for the line-by-line tutorial
that comes with pygame. It is based on a 'popular' web banner.
Note there are comments here, but for the full explanation,
follow along in the tutorial.
"""


# Import Modules
import os
import pygame as pg
from pygame.compat import geterror

if not pg.font:
    print("Warning, fonts disabled")
if not pg.mixer:
    print("Warning, sound disabled")

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
        self.image, self.rect = load_image("mouse.png")#, -1)
        self.cliking = 0

    def update(self):
        """move the resized mouse based on the real mouse position"""

        game_ratio = self.Game.game_screen_rect.w / self.Game.game_screen_rect.h
        app_ratio = self.Game.app_screen_rect.w / self.Game.app_screen_rect.h

        if game_ratio < app_ratio:
            width = int(self.Game.app_screen_rect.h / self.Game.game_screen_rect.h
                    * self.Game.game_screen_rect.w)
            height = self.Game.app_screen_rect.h
        else:
            width = self.Game.app_screen_rect.w
            height = int(self.Game.app_screen_rect.w / self.Game.game_screen_rect.w
                     * self.Game.game_screen_rect.h)
        resized_screen = pg.transform.scale(self.Game.game_screen,
                                            (width, height))

        # get the rect of the resized screen for blitting
        # and center it to the window screen
        res_screen_rect = resized_screen.get_rect()
        res_screen_rect.center = self.Game.app_screen_rect.center

        diff_x = (self.Game.app_screen_rect.w - res_screen_rect.w) / 2
        diff_y = (self.Game.app_screen_rect.h - res_screen_rect.h) / 2

        pos = pg.mouse.get_pos()
        real_pos_x = (-diff_x + pos[0]) * self.Game.game_screen_rect.w / res_screen_rect.w
        real_pos_y = (-diff_y + pos[1]) * self.Game.game_screen_rect.h / res_screen_rect.h
        real_pos = real_pos_x, real_pos_y

        self.rect.midtop = real_pos
        if self.cliking:
            self.rect.move_ip(5, 10)

    def cliked(self, target):
        """returns true if the mouse collides with the target"""
        if not self.cliking:
            self.cliking = 1
            hitbox = self.rect.inflate(-5, -5)
            return hitbox.colliderect(target.rect)

    def uncliked(self):
        """called to pull the mouse back"""
        self.cliking = 0


class Chimp(pg.sprite.Sprite):
    """moves a monkey critter across the screen. it can spin the
       monkey when it is punched."""

    def __init__(self, Game):
        pg.sprite.Sprite.__init__(self)  # call Sprite intializer
        self.area = Game.game_screen_rect  # walkable space
        print(self.area)
        self.image, self.rect = load_image("chimp.png", -1)
#        self.image = pg.transform.scale(self.image, (200, 100))
#        self.rect = self.image.get_rect()
        self.rect.topleft = 0, 100
        self.move = -9  # depend on image original orientation (positive move = directed to right)
        self.dizzy = 0

    def update(self):  # implicitly called from allsprite update
        """walk or spin, depending on the monkeys state"""
        if self.dizzy:
            self._spin()
        else:
            self._walk()

    def _walk(self):
        """move the monkey across the screen, and turn at the ends"""
        newpos = self.rect.move((self.move, 0))
#        if not self.area.contains(newpos):  # could be useful but not here

        if self.rect.left < self.area.left or self.rect.right > self.area.right:
            self.move = -self.move
            newpos = self.rect.move((self.move, 0))
            self.image = pg.transform.flip(self.image, 1, 0)
        self.rect = newpos

    def _spin(self):
        """spin the monkey image"""
        center = self.rect.center
        self.dizzy = self.dizzy + 12
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


class BackGround(pg.sprite.Sprite):
    """image of the map"""
    def __init__(self, image_file, center=None, bottomleft=None,
                 midbottom=None):
        pg.sprite.Sprite.__init__(self)  # call Sprite initializer
        self.image, self.rect = load_image(image_file)

        if center is not None:
            self.rect.center = center
        if bottomleft is not None:
            self.rect.bottomleft = bottomleft
        if midbottom is not None:
            self.rect.midbottom = midbottom


class Game():
    """this function is called when the program starts.
       it initializes everything it needs, then runs in
       a loop until the function returns."""

    def __init__(self):
        GAME_SCREEN_W = 1920
        GAME_SCREEN_H = 1080

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
        self.game_screen = pg.Surface((GAME_SCREEN_W, GAME_SCREEN_H))
        self.game_screen_rect = self.game_screen.get_rect()

        self.clock = pg.time.Clock()

        pg.display.set_caption("Testing")
        pg.mouse.set_visible(1)

        # Create The Backgound that never changes (with fixed toolbar)
#        self.bg_image = pg.Surface(self.game_screen.get_size()).convert()
#        background_color = (200, 200, 200)
#        self.bg_image.fill(background_color)

        # create the map on top of the background
        center = self.game_screen_rect.center
        midbottom = self.game_screen_rect.midbottom
        self.lower_tool_bar = BackGround('lower_bar.png', midbottom=midbottom)
        self.background_screen = BackGround('background.png', center=center)

        # Put Text On The Background, Centered
#        if pg.font:
#            font = pg.font.Font(None, 36)
#            text = font.render("Text displayed on not so white background",
#                               1, (10, 10, 10))
#            textpos = text.get_rect(centerx=self.game_screen.get_width() / 2)
#            self.bg_image.blit(text, textpos)

        # Prepare Game Objects
        self.clock = pg.time.Clock()
    #    whiff_sound = load_sound("whiff.wav")
    #    punch_sound = load_sound("punch.wav")
        self.chimp = Chimp(self)
#        self.mouse = Mouse(game)
#        self.allsprites = pg.sprite.RenderPlain((self.mouse, self.chimp))
        self.allsprites = pg.sprite.RenderPlain((self.chimp))

    def events(self):
        """All clicked regestered"""
        for event in pg.event.get():

            if event.type == pg.QUIT:
                self.running = False

            elif event.type == pg.KEYDOWN:
                if event.key == pg.K_ESCAPE:
                    self.running = False
#                elif event.key == pg.K_s:  # if want to toggle respect ratio
#                    self.window_stretched = not self.window_stretched
#                    self.reset_app_screen(self.app_screen_rect.size)
                elif event.key == pg.K_f:
                    # toggle fullscreen
                    self.flags = self.flags ^ pg.FULLSCREEN
                    self.reset_app_screen(self.app_screen_rect.size)
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
                if self.mouse.cliked(self.chimp):
#                    punch_sound.play()  # punch
                    self.chimp.punched()
                else:
#                    whiff_sound.play()  # miss
                    ""
            elif event.type == pg.MOUSEBUTTONUP and event.button == 1:
                self.mouse.uncliked()

    def update(self, dt):
#        print(dt)
        self.mouse.update()
        self.allsprites.update()  # call update function of each class inside

    def draw(self):
        # Draw Everything
#        self.game_screen.blit(self.bg_image, (0, 0))  # blackground
        self.game_screen.blit(self.background_screen.image,
                              self.background_screen.rect)

        self.game_screen.blit(self.lower_tool_bar.image, self.lower_tool_bar.rect)
#        allsprites.remove(chimp)

        self.allsprites.draw(self.game_screen)  # draw moving items

        if self.window_stretched:  # don't want this but keep in code in case
            # scale the game screen to the window size
            resized_screen = pg.transform.scale(self.game_screen,
                                                self.app_screen_rect.size)
        else:  # allows to keep ratio
            # compare aspect ratios
            game_ratio = self.game_screen_rect.w / self.game_screen_rect.h
            app_ratio = self.app_screen_rect.w / self.app_screen_rect.h

            if game_ratio < app_ratio:
                width = int(self.app_screen_rect.h / self.game_screen_rect.h
                        * self.game_screen_rect.w)
                height = self.app_screen_rect.h
            else:
                width = self.app_screen_rect.w
                height = int(self.app_screen_rect.w / self.game_screen_rect.w
                         * self.game_screen_rect.h)
            resized_screen = pg.transform.scale(self.game_screen,
                                                (width, height))

        # get the rect of the resized screen for blitting
        # and center it to the window screen
        res_screen_rect = resized_screen.get_rect()
        res_screen_rect.center = self.app_screen_rect.center

        self.app_screen.blit(resized_screen, res_screen_rect)

        fps = self.clock.get_fps()
        pg.display.set_caption(f'{round(fps,2)}')

        pg.display.update(res_screen_rect)

        pg.display.flip()

    def reset_app_screen(self, size):
        self.app_screen = pg.display.set_mode(size, self.flags)
        self.app_screen_rect = self.app_screen.get_rect()
        pg.display.update()


    def run(self):
        self.running = True
        while self.running:
            self.clock.tick(60)
            delta_time = self.clock.tick() / 1000
            self.events()
            self.update(delta_time)
            self.draw()

        pg.display.quit()
        pg.quit()

# Game Over


if __name__ == "__main__":

    # wanted resolution (knowing that the game will have a different resolution
    # and will resize to match this size)
    WINDOW_W = 300
    WINDOW_H = 200

    game = Game()
    mouse = Mouse(game)
    game.mouse = mouse
    game.allsprites.add(game.mouse)
    game.run()
