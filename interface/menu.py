import pygame as pg
from .background import BackGround


class Menu:
    def __init__(self, Game):
        self.Game = Game
        # BackGround.__init__(self)

        text = "Pause"
        font = pg.font.Font(None, 60)
        self.image = font.render(text, 1, (10, 10, 10))
        self.rect = self.image.get_rect()
        self.rect.center = self.Game.game_screen.rect.center

    def events(self):
        """All clicked regestered"""
        all_keys = pg.key.get_pressed()  # all pressed key at current time

        if (all_keys[pg.K_LCTRL] or all_keys[pg.K_RCTRL]) and all_keys[pg.K_f]:
            self.Game.flags = self.Game.flags ^ pg.FULLSCREEN
            self.Game.reset_app_screen(self.Game.game_screen.rect.size)

        if ((all_keys[pg.K_LCTRL] or all_keys[pg.K_RCTRL])
                and (all_keys[97] or all_keys[122])):
            self.Game.running = False
            self.running = False

        for event in pg.event.get():  # listed key in pressed order

            if event.type == pg.QUIT:  # close windows using red cross
                self.Game.running = False
                self.running = False

            elif event.type == pg.KEYDOWN:
                if event.key == pg.K_ESCAPE:  # close windows using escape key
                    self.running = False

            elif event.type == pg.VIDEORESIZE:
                self.Game.reset_app_screen(event.dict['size'])

    def update(self):
        pass

    def draw(self):

        self.Game.game_screen.image.blit(self.image,
                                          self.rect)
        self.Game.resize_app_screen()  # resize the game size to the app size
        self.Game.app_screen.blit(self.Game.resized_screen.image,
                              self.Game.resized_screen.rect)
        fps = self.Game.clock.get_fps()
        pg.display.set_caption(f'{round(fps,2)}')

        pg.display.update(self.Game.resized_screen.rect)
        pass

    def run(self, dt):
        self.running = True

        while self.running:

            self.Game.clock.tick(300)/1000  # avoid taking init time into account
            self.events()  # look for commands

            self.update()  # update movement

            self.draw()  # draw everything after the movements

        self.Game.clock.tick()/1000  # avoid taking init time into account
        self.Game.dt = dt
