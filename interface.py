"""
This simple example is used for the line-by-line tutorial
that comes with pygame. It is based on a 'popular' web banner.
Note there are comments here, but for the full explanation,
follow along in the tutorial.
"""


# Import Modules
import os
import pygame as pg
#from pg.locals import *
from pygame.compat import geterror
from pygame import RLEACCEL, QUIT, K_ESCAPE, KEYDOWN, MOUSEBUTTONDOWN, MOUSEBUTTONUP, FULLSCREEN

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
            colorkey = image.get_at((0, 0))  # take the first pixel of the image as reference for alpha

        image.set_colorkey(colorkey, RLEACCEL)  # RLEACCEL make it faster to display

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
class Fist(pg.sprite.Sprite):
    """moves a clenched fist on the screen, following the mouse"""

    def __init__(self):
        pg.sprite.Sprite.__init__(self)  # call Sprite initializer
        self.image, self.rect = load_image("fist.png", -1)
        self.punching = 0

    def update(self):
        """move the fist based on the mouse position"""
        pos = pg.mouse.get_pos()
        self.rect.midtop = pos
        if self.punching:
            self.rect.move_ip(5, 10)

    def punch(self, target):
        """returns true if the fist collides with the target"""
        if not self.punching:
            self.punching = 1
            hitbox = self.rect.inflate(-5, -5)
            return hitbox.colliderect(target.rect)

    def unpunch(self):
        """called to pull the fist back"""
        self.punching = 0


class Chimp(pg.sprite.Sprite):
    """moves a monkey critter across the screen. it can spin the
       monkey when it is punched."""

    def __init__(self):
        pg.sprite.Sprite.__init__(self)  # call Sprite intializer
        screen = pg.display.get_surface()
        self.area = screen.get_rect()  # walkable space
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

def main():
    """this function is called when the program starts.
       it initializes everything it needs, then runs in
       a loop until the function returns."""
    # Initialize Everything
    pg.init()
    screen = pg.display.set_mode((640,480), pg.RESIZABLE)
#    screen = pg.display.set_mode((500, 400))
    pg.display.set_caption("Testing")
    pg.mouse.set_visible(0)

    # Create The Backgound
    background = pg.Surface(screen.get_size())
    background = background.convert()
    background_color = (200, 200, 200)
    background.fill(background_color)

    center = screen.get_rect().center
    midbottom = screen.get_rect().midbottom
    background_screen = BackGround('background.png', center=center)
    lower_tool_bar = BackGround('lower_bar.png', midbottom=midbottom)
    # Put Text On The Background, Centered
    if pg.font:
        font = pg.font.Font(None, 36)
        text = font.render("Text displayed on not so white background", 1, (10, 10, 10))
        textpos = text.get_rect(centerx=screen.get_width() / 2)
        background.blit(text, textpos)
#        background_screen.image.blit(text, textpos)

    # Display The Background before the beginning of the game (while everything is loaded)
    screen.blit(background, (0, 0))  # draw background to erase everything
    pg.display.flip()

    # Prepare Game Objects
    clock = pg.time.Clock()
#    whiff_sound = load_sound("whiff.wav")
#    punch_sound = load_sound("punch.wav")
    chimp = Chimp()
    fist = Fist()
    allsprites = pg.sprite.RenderPlain((fist, chimp))

    # Main Loop
    going = True
    while going:
        clock.tick(60)  # 60 Hz lattency (1/60s = 16.6ms (60 frames per seond max))

        # Handle Input Events
        for event in pg.event.get():
#            print(event)

            if event.type == QUIT:
                going = False

            elif event.type == KEYDOWN and event.key == K_ESCAPE:
                going = False

            elif event.type == MOUSEBUTTONDOWN and event.button == 1:

                if fist.punch(chimp):
#                    punch_sound.play()  # punch
                    chimp.punched()

                else:
#                    whiff_sound.play()  # miss
                    ""

            elif event.type == MOUSEBUTTONUP and event.button == 1:
                fist.unpunch()

        allsprites.update()  # call update function of each class inside

        # Draw Everything
        screen.blit(background, (0, 0))  # draw background to erase everything
        screen.blit(background_screen.image, background_screen.rect)
        screen.blit(lower_tool_bar.image, lower_tool_bar.rect)
        allsprites.draw(screen)  # draw moving items
#        allsprites.remove(chimp)
        pg.display.flip()

    " end "
    pg.display.quit()
    pg.quit()

# Game Over


if __name__ == "__main__":
    main()
