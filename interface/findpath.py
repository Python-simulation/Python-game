"""find path"""
import math
from math import pi

from .A_algorithm import A_algorithm


cell_sizes = (128, 64)
authorized_angle = math.atan(0.5)


class FindPath:
    """Clas with cell manipulation function and with find_path function."""
    cell_sizes = cell_sizes
    authorized_angle = authorized_angle

    def cell_to_pos(self, cell):
        """Convert the matrix position of a cell into its pixel position"""
        cart_x = cell[0] * cell_sizes[0]/2
        cart_y = cell[1] * cell_sizes[0]/2  # x not a mistake
        iso_x = (cart_x - cart_y)
        iso_y = (cart_x + cart_y)/2

        pos = (iso_x + 7.5*cell_sizes[0],
               iso_y - 7.5*cell_sizes[1])

        return pos

    def pos_to_cell(self, pos):
        """Convert the pixel position of a cell into its matrix position."""
        iso = (pos[0] - 7.5*cell_sizes[0],
               pos[1] + 7.5*cell_sizes[1])
        cart = (iso[0]/2 + iso[1],
                -iso[0]/2 + iso[1])
        row = (2*cart[0]/cell_sizes[0],
               2*cart[1]/cell_sizes[0])
        cell = (int(row[0]), int(row[1]))

        return cell

    def theta_cardinal(self, theta, cardinal):
        """"Round theta to the authorized angles defined by cardinal."""
        if cardinal == 4:  # allows only cross
            first = 0
            second = pi/2
            third = pi
            fourth = -pi/2

            if first <= theta <= second:
                theta = authorized_angle
            elif second <= theta <= third:
                theta = pi - authorized_angle
            elif -third <= theta <= fourth:
                theta = -pi + authorized_angle
            elif fourth <= theta <= first:
                theta = -authorized_angle

            else:
                raise ValueError("theta", theta, theta*180/pi)
            # print(first <= second)
            # print(second <= third)
            # print(-third <= fourth)
            # print(fourth <= first)

        elif cardinal == 8:  # allows cross + diagonal mov
            first = authorized_angle/2
            second = 3*first
            third = pi - second
            fourth = pi - first
            fifth = -fourth
            sixth = -third
            seventh = -second
            eight = -first

            if eight <= theta <= first:
                theta = 0
            elif first <= theta <= second:
                theta = authorized_angle
            elif second <= theta <= third:
                theta = pi/2
            elif third <= theta <= fourth:
                theta = pi - authorized_angle
            elif (fourth <= theta <= pi) or (-pi <= theta <= fifth):
                theta = pi
            elif fifth <= theta <= sixth:
                theta = -(pi - authorized_angle)
            elif sixth <= theta <= seventh:
                theta = -pi/2
            elif seventh <= theta <= eight:
                theta = -authorized_angle
            else:
                print(theta, theta*180/pi)
                raise ValueError

        else:
            raise ValueError("error with alloyed direction, cardinal="
                             + str(cardinal)
                             + ". Alloyed values: 4 and 8")

        return theta

    def find_path(self, all_cells, begin_pos, dest_pos, cardinal=4):
        """function returning the path between two given cell.
        First try a direct path without obsacle.
        Switch to a A* algorithm if encounter an obstacle."""

        dest_cell = self.pos_to_cell(dest_pos)
        cell = all_cells.get(dest_cell)

        if cell is None or not cell.active:
            return list()

        road = list()
        prev_pos = begin_pos
        nbr_step = 0

        while prev_pos != dest_pos:

            nbr_step += 1
            if nbr_step > len(all_cells):  # OPTIMIZE: temporary for dev
                # road = [dest_cell]  # if remove cell preview, remove this
                road = list()
                # print("bad road", road)
                break

            x_length = dest_pos[0] - prev_pos[0]
            y_length = dest_pos[1] - prev_pos[1]
            theta = math.atan2(y_length, x_length)

            theta = self.theta_cardinal(theta, cardinal)

            if theta == 0:  # ugly but work
                next_pos = (prev_pos[0]+cell_sizes[0],
                            prev_pos[1])
            elif theta in (pi, -pi):
                next_pos = (prev_pos[0]-cell_sizes[0],
                            prev_pos[1])
            elif theta == pi/2:
                next_pos = (prev_pos[0],
                            prev_pos[1]+cell_sizes[1])
            elif theta == -pi/2:
                next_pos = (prev_pos[0],
                            prev_pos[1]-cell_sizes[1])
            elif theta == authorized_angle:
                next_pos = (prev_pos[0]+cell_sizes[0]/2,
                            prev_pos[1]+cell_sizes[1]/2)
            elif theta == (pi - authorized_angle):
                next_pos = (prev_pos[0]-cell_sizes[0]/2,
                            prev_pos[1]+cell_sizes[1]/2)
            elif theta == -authorized_angle:
                next_pos = (prev_pos[0]+cell_sizes[0]/2,
                            prev_pos[1]-cell_sizes[1]/2)
            elif theta == -(pi - authorized_angle):
                next_pos = (prev_pos[0]-cell_sizes[0]/2,
                            prev_pos[1]-cell_sizes[1]/2)
            else:
                print("error with angle", theta, theta*180/pi)
                # road = [dest_cell]  # BUG: temporaire just pour test
                break

            unit_pos = self.pos_to_cell(next_pos)

            if (all_cells.get(unit_pos) is None
                    or not all_cells.get(unit_pos).active):
                begin_cell = self.pos_to_cell(begin_pos)
                dest_cell = self.pos_to_cell(dest_pos)

                road = A_algorithm(all_cells,
                                   begin_cell, dest_cell,
                                   cardinal=cardinal)

                road_pos = []

                if road != []:
                    for cell in road:
                        road_pos.append(self.cell_to_pos(cell))

                return road_pos

            road.append(next_pos)
            prev_pos = next_pos

        return road
