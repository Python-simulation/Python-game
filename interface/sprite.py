from .interface_functions import NeededFunctions
from .findpath import FindPath
from .background import BackGround

nf = NeededFunctions()
fp = FindPath()
cell_sizes = fp.cell_sizes


class Sprite(BackGround):

    def __init__(self, image, cell_pos, markers=list(), **kwargs):
        if type(image) is str:  # OPTIMIZE: change this if merge anim and image
            super().__init__(image, -1, **kwargs)
        else:
            super().__init__()
            self.image = image
            self.rect = self.image.get_rect()

        position = fp.cell_to_pos(cell_pos)
        position = (position[0],
                    position[1] + cell_sizes[1]/2)
        self.rect.midbottom = position

        markers_pos = list()

        for cell in markers:
            cell = self.add_init_pos(cell)  # don't change cell anymore
            markers_pos.append(fp.cell_to_pos(cell))

        self.markers = self.add_markers(markers_pos)

    def add_init_pos(self, cell):
        init_pos = fp.pos_to_cell(self.rect.topleft)

        cell = (cell[0] + init_pos[0],
                cell[1] + init_pos[1])

        unit_pos = (int(cell[0]), int(cell[1]))
        return unit_pos

    def add_markers(self, markers):

        if len(markers) == 0:
            pos = self.rect.midbottom
            markers = [
                (pos[0], pos[1] - cell_sizes[1]/2),
            ]

        elif len(markers) == 1:
            raise NotImplementedError

        elif len(markers) == 2:
            markers = [
                (markers[0][0] - cell_sizes[0]/2, markers[0][1]),
                (markers[1][0] + cell_sizes[0]/2, markers[1][1]),
                ]
        elif len(markers) == 3:
            markers = [
                (markers[0][0] - cell_sizes[0]/2, markers[0][1]),
                (markers[1][0], markers[1][1] - cell_sizes[1]/2),
                (markers[2][0] + cell_sizes[0]/2, markers[2][1]),
                ]
        return markers

    def check_order(self, target):
        x0, y0 = target

        if len(self.markers) == 1:
            x1, y1 = self.markers[0]
            return True if y0 >= y1 else False

        elif len(self.markers) == 2:
            x1, y1 = self.markers[0]
            x2, y2 = self.markers[1]

            if x1 > x2:
                x1, y1 = self.markers[1]
                x2, y2 = self.markers[0]

            return self.check_line(target, (x1, y1), (x2, y2))

        elif len(self.markers) == 3:  # Work (not tested) but too complicated
            x1, y1 = self.markers[0]
            x2, y2 = self.markers[1]
            x3, y3 = self.markers[2]
            first_line = self.check_line(target, (x1, y1), (x2, y2))
            second_line = self.check_line(target, (x2, y2), (x3, y3))

            if y2 > y1 and y2 > y3:
                return True if first_line and second_line else False
            else:
                return True if first_line or second_line else False

        else:
            raise ValueError("can't have markers with len != 1,2,3")

    def check_line(self, target, marker1, marker2):
        x0, y0 = target
        x1, y1 = marker1
        x2, y2 = marker2

        if x2 == x1:
            error = "Can't have a vertical line as markers for a sprite"
            raise ZeroDivisionError(error)

        a = (y2 - y1) / (x2 - x1)
        b = y2 - a*x2

        return True if y0 >= a*x0 + b else False
