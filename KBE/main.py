# This will be the main document of the KBE app to design the wing of an electrical aircraft
# By Martin van Schie and Yara Hinssen
# See PyCharm help at https://www.jetbrains.com/help/pycharm/

import os
from tkinter import Tk, simpledialog, messagebox
from math import sqrt
from time import time, ctime

from parapy.core import Input, Part, Attribute
from parapy.core.base import Base
from parapy.exchange import STEPReader
from parapy.geom import Position, Point

THIS_DIR = os.path.dirname(__file__)

ROOT = Tk()
ROOT.withdraw()


@Part
def Placement(self):
    """
    This part places the batteries and wires in the wingbox.
    It optimizes this placement based on the evaluate function.
    """
    return Optimizedplacement()


    @Attribute
    def modifying_optimizer_output(self):
    """
    This attribute customizes the output of the optimizer. It gives colors to the batteries,
    wires and engine housings.
    """

    # Assign colors to parts
    for i in range(len(self.optimizer.top10)):
        for j in range(len(self.optimizer.top10[i].positioned_equipment)):
            if self.optimizer.top5[i].positioned_equipment[j].label == 'Battery':
                self.optimizer.top5[i].positioned_equipment[j].color = 'blue'
            elif self.optimizer.top5[i].positioned_equipment[j].label == 'Wire':
                self.optimizer.top5[i].positioned_equipment[j].color = 'green'
            elif self.optimizer.top5[i].positioned_equipment[j].label == 'Engine':
                self.optimizer.top5[i].positioned_equipment[j].color = 'red'

                # check clash else change back to original
                check = self.clash_check(i, j, x, y)
                if not check:
                    self.optimizer.top10[i].positioned_equipment[j].centered = True
                    self.optimizer.top10[i].positioned_equipment[j].position = Position(Point(x, y, 1.2))

    # move equipment to corners such that all corners are occupied
    # locate positions of the room
    # point in x,y coordinates
    # corner list: first the most left upward, right up, right down, left down
    for a in range(len(self.optimizer.top10)):
        corners_room = []
        center = self.optimizer.top10[a].room.box.position
        width = self.optimizer.top10[a].room.box.width
        height = self.optimizer.top10[a].room.box.length
        for b in range(2):
            x = center[0] + (-1) ** (b + 1) * width / 2
            y = center[1] - (-1) ** (b + 1) * height / 2
            x1 = center[0] - (-1) ** (b + 1) * width / 2
            y1 = center[1] - (-1) ** (b + 1) * height / 2
            corners_room.append([x, y])
            corners_room.append([x1, y1])

        # check closest equipment to corner left up corner
        for c in range(len(corners_room)):
            dist_minimum = 1000000
            for d in range(len(self.optimizer.top10[a].positioned_equipment)):
                dist_actual = (abs(
                    corners_room[c][0] - self.optimizer.top10[a].positioned_equipment[d].center[0]) ** 2 + abs(
                    corners_room[c][1] - self.optimizer.top10[a].positioned_equipment[d].center[1]) ** 2) ** 0.5
                if dist_actual <= dist_minimum and \
                        self.optimizer.top10[a].positioned_equipment[d].label is not None:
                    dist_minimum = dist_actual
                    eqp = d
            if c == 0:
                x = corners_room[c][0] + self.optimizer.top10[a].positioned_equipment[eqp].width / 2
                y = corners_room[c][1] - self.optimizer.top10[a].positioned_equipment[eqp].length / 2
            if c == 1:
                x = corners_room[c][0] - self.optimizer.top10[a].positioned_equipment[eqp].width / 2
                y = corners_room[c][1] - self.optimizer.top10[a].positioned_equipment[eqp].length / 2
            if c == 2:
                x = corners_room[c][0] - self.optimizer.top10[a].positioned_equipment[eqp].width / 2
                y = corners_room[c][1] + self.optimizer.top10[a].positioned_equipment[eqp].length / 2
            if c == 3:
                x = corners_room[c][0] + self.optimizer.top10[a].positioned_equipment[eqp].width / 2
                y = corners_room[c][1] + self.optimizer.top10[a].positioned_equipment[eqp].length / 2

            check = self.clash_check(a, eqp, x, y)
            if not check:
                self.optimizer.top10[a].positioned_equipment[eqp].centered = True
                self.optimizer.top10[a].positioned_equipment[eqp].position = Position(Point(x, y, 1.2))

    return self.optimizer.top10


    @Attribute
    def top10_final(self):
    """
    Rearranges the Top10 results to show them all in one view!
    """
    delta_x_total = 0
    for i in range(len(self.optimizer.top10)):
        delta_x = self.optimizer.top10[i].room.width / 2 + self.optimizer.top10[i - 1].room.width / 2 + \
                  self.optimizer.top10[i].aisle_width
        if 0 < i < 5:
            delta_x_total = delta_x + delta_x_total
            for j in range(len(self.optimizer.top10[i].positioned_equipment)):
                x = self.optimizer.top10[i].positioned_equipment[j].position.x
                y = self.optimizer.top10[i].positioned_equipment[j].position.y
                z = self.optimizer.top10[i].positioned_equipment[j].position.z
                self.optimizer.top10[i].positioned_equipment[j].position = Position(Point(x + delta_x_total, y, z))
        if i == 5:
            delta_x_total = 0
            delta_y = self.optimizer.top10[i].room.length / 2 + self.optimizer.top10[i - 5].room.length / 2 + \
                      self.optimizer.top10[i].aisle_width
            for j in range(len(self.optimizer.top10[i].positioned_equipment)):
                x = self.optimizer.top10[i].positioned_equipment[j].position.x
                y = self.optimizer.top10[i].positioned_equipment[j].position.y
                z = self.optimizer.top10[i].positioned_equipment[j].position.z
                self.optimizer.top10[i].positioned_equipment[j].position = Position(Point(x + delta_x_total,
                                                                                          y - delta_y, z))
        if i > 5:
            delta_x_total = delta_x + delta_x_total
            delta_y = self.optimizer.top10[i].room.length / 2 + self.optimizer.top10[i - 5].room.length / 2 + \
                      self.optimizer.top10[i].aisle_width
            for j in range(len(self.optimizer.top10[i].positioned_equipment)):
                x = self.optimizer.top10[i].positioned_equipment[j].position.x
                y = self.optimizer.top10[i].positioned_equipment[j].position.y
                z = self.optimizer.top10[i].positioned_equipment[j].position.z
                self.optimizer.top10[i].positioned_equipment[j].position = Position(Point(x + delta_x_total,
                                                                                          y - delta_y, z))

    return self.optimizer.top10


@Part
def output(self):
    """
    This part generates the desired outputs of the design.
    It makes a .step and a .txt file.
    """
    return OutputGeneration(total_width=self.total_width,
                            total_length=self.total_length,
                            number_of_people_userinput=self.number_of_people,
                            social_distance=social_distance_rules,
                            total_surface_area=self.total_surface_area,
                            dimensions_rooms=self.dimensions_rooms,
                            door_position=self.door_position,
                            router_position=self.router_position,
                            min_wifi_strength=self.min_wifi_strength,
                            room_generation=self.room_generation,
                            optimizer=self.optimizer)


# Clash function used in the modifying_optimizer_output attribute.
# Check if two rooms within a top10 optimization output do clash after modification.
# i indicates the integer of the top10 analysis under consideration.
# j indicates the integer of the equipment that you want to check clash with.
def clash_check(self, i, j, x, y):
    check = False
    for z in range(len(self.optimizer.top10[i].positioned_equipment)):
        if z == j:
            break
        # Room x is the equipment j that we want to analyse.
        distance_centers = (abs(x -
                                self.optimizer.top10[i].positioned_equipment[z].center[0]) ** 2 +
                            abs(y -
                                self.optimizer.top10[i].positioned_equipment[z].center[1]) ** 2) ** 0.5
        distance_required = ((self.optimizer.top10[i].positioned_equipment[j].width / 2 +
                              self.optimizer.top10[i].positioned_equipment[z].width / 2) ** 2 +
                             (self.optimizer.top10[i].positioned_equipment[j].length / 2 +
                              self.optimizer.top10[i].positioned_equipment[z].length / 2) ** 2) ** 0.5
        if distance_required >= distance_centers:
            check = True
    return check


#The parapy bit
from parapy.geom import Box
from parapy.gui import display
obj = Box(1, 2, 3)
display(obj)