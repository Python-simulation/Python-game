import pygame as pg
from ..background import BackGround
from ..props import prop_dict

from ..findpath import FindPath

fp = FindPath()


class MapGenerator:
    def __init__(self, Game):
        self.Game = Game

        text = "MapGenerator"
        font = pg.font.Font(None, 60)
        self.image = font.render(text, True, (10, 10, 10))
        self.rect = self.image.get_rect()
        self.rect.center = self.Game.game_screen.rect.center

        self.tile = "grass"
        self.tile_number = 0
        self.tile_list = list(Game.ground_dict.keys())+list(prop_dict.keys())
        self.time_pressed = 0

    def events(self):
        """All clicked regestered"""
        all_keys = pg.key.get_pressed()  # all pressed key at current time

        if (all_keys[pg.K_LCTRL] or all_keys[pg.K_RCTRL]) and all_keys[pg.K_f]:
            self.Game.flags = self.Game.flags ^ pg.FULLSCREEN
            self.Game.reset_app_screen(self.Game.game_screen.rect.size)

        elif ((all_keys[pg.K_LCTRL] or all_keys[pg.K_RCTRL])
                and (all_keys[97] or all_keys[122])):
            self.Game.running = False
            self.running = False

        elif all_keys[pg.K_UP] or all_keys[pg.K_KP_PLUS]:

            if ((self.time_pressed == 0 or self.time_pressed > 1)
                    and self.tile_number+1 < len(self.tile_list)):
                self.tile_number += 1

            self.time_pressed += self.Game.dt

        elif all_keys[pg.K_DOWN] or all_keys[pg.K_KP_MINUS]:

            if ((self.time_pressed == 0 or self.time_pressed > 1)
                    and self.tile_number >= 1):
                self.tile_number -= 1

            self.time_pressed += self.Game.dt

        else:
            self.time_pressed = 0

        self.tile = self.tile_list[self.tile_number]


        for event in pg.event.get():  # listed key in pressed order

            if event.type == pg.QUIT:  # close windows using red cross
                self.Game.running = False
                self.running = False

            elif event.type == pg.KEYDOWN:
                if event.key == pg.K_ESCAPE:  # close windows using escape key
                    self.running = False

            elif event.type == pg.VIDEORESIZE:
                self.Game.reset_app_screen(event.dict['size'])

            elif event.type == pg.MOUSEBUTTONDOWN and event.button == 1:

                for cell in self.Game.all_cells.values():
                    if self.Game.mouse.clicking(cell):
                        try:
                            self.map.add_ground(self.tile, cell.cell_pos)
                            print("self.add_ground(\""+str(self.tile)+"\", "+str(cell.cell_pos)+")")
                        except KeyError:
                            try:
                                self.map.add_prop(self.tile, cell.cell_pos)
                                print("self.add_prop(\""+str(self.tile)+"\", "+str(cell.cell_pos)+")")
                                self.map.refresh()
                            except TypeError:
                                self.map.add_prop(self.tile, cell.cell_pos, cell.cell_pos)
                                print("self.add_prop(\""+str(self.tile)+"\", "+str(cell.cell_pos)+", "+str(cell.cell_pos)+")")
                                self.map.refresh()
                        break

            elif event.type == pg.MOUSEBUTTONUP and event.button == 1:
                self.Game.mouse.unclicked()

            else:
                pg.mouse.set_cursor(*pg.cursors.diamond)

                for cell in self.Game.all_cells.values():
                    if self.Game.mouse.hovering(cell):

                        self.Game.sprites.empty()
                        try:
                            self.show_ground(self.tile, cell.cell_pos)
                        except KeyError:
                            try:
                                self.show_prop(self.tile, cell.cell_pos)
                            except TypeError:
                                self.show_prop(self.tile, cell.cell_pos, cell.cell_pos)
                        break
                else:
                    pg.mouse.set_cursor(*pg.cursors.arrow)

    def show_ground(self, name, cell):
        ground = self.Game.ground_dict[str(name)]
        position = fp.cell_to_pos(cell)
        ground.rect.center = position
        self.Game.sprites.add(ground)

    def show_prop(self, name, cell, *args, **kwargs):
        Prop = prop_dict[str(name)]
        prop = Prop(self.map, cell, *args, **kwargs)
        self.Game.sprites.add(prop)

    def update(self):
        self.Game.update(self.Game.dt)
        pass

    def draw(self):
        self.Game.allsprites.add(self.Game.bg_sprites, layer=1)

        self.Game.bg_sprites.draw(self.Game.game_screen.image)
        self.Game.allsprites.draw(self.Game.game_screen.image)
        self.Game.sprites.draw(self.Game.game_screen.image)

        self.Game.game_screen.image.blit(self.image, self.rect)
        self.Game.resize_app_screen()  # resize the game size to the app size
        self.Game.app_screen.blit(self.Game.resized_screen.image,
                                  self.Game.resized_screen.rect)
        fps = self.Game.clock.get_fps()
        pg.display.set_caption(f'{round(fps,2)}')

        pg.display.update(self.Game.resized_screen.rect)
        pass

    def run(self, dt):
        self.map = self.Game.current_map
        self.running = True

        self.Game.all_cells = self.map.Maps.map_reset_cells()[0]
        self.Game.all_cells.update(self.Game.cells_visible)

        while self.running:

            self.Game.clock.tick(80)/1000  # avoid taking init time into account
            self.events()  # look for commands

            self.update()  # update movement

            self.draw()  # draw everything after the movements

        self.Game.clock.tick()/1000  # avoid taking init time into account
        self.Game.dt = dt

        self.Game.mouse.unclicked()  # semi-obsolete: needed to avoid button to stick in clicked mode
        # without being unclicked -> get teleported each pause being clicked

        self.Game.sprites.empty()
        print("map_data = "+str(self.map.map_data))
        # print("\n")
        # print(self.Game.bg_sprites.sprites())
