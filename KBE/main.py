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

import math as m
import numpy as np
from parapy.core import *
from parapy.geom import *
from Airfoilcoordiantesgenerator import *
from Airfoilinterpolater import *

from Battery import *
from Structure import *

THIS_DIR = os.path.dirname(__file__)

ROOT = Tk()
ROOT.withdraw()
total_width_userinput = 400
total_height_userinput = 20
total_depth_userinput = 50


class Main(Base):
    #####take in the input file
    lalala = Input(np.loadtxt('inputexample.txt', dtype='str', delimiter=';'))

    @Attribute
    def total_width(self):
        """
        This attribute determines the width of the wingbox as follows from the external analysis tool.
        """
        width = total_width_userinput
        return width

    @Attribute
    def total_depth(self):
        """
        This determines the input depth of the wingbox as follows from the external analysis tool
        """
        depth = total_depth_userinput
        return depth

    @Attribute
    def total_height(self):
        """
        This determines the input height of the wingbox as follows from the external analysis tool
        """
        height = total_height_userinput
        return height

    @Attribute
    def total_surface_area(self):
        """
        This attribute calculates the total surface area using the inputs width and depth.
        """
        return self.total_width * self.total_depth

    @Attribute
    def total_volume(self):
        """
        This attribute calculates the total volume of the wingbox using width, depth and height
        """
        return self.total_width * self.total_height * self.total_depth

    @Attribute
    def dimensions_inputs(self):
        """
        To input the batteries into the structure, the dimensions of the batteries need to be found.
        This is done in the Battery.py and will be implemented in the main file here.
        """
        # Batterysize
        Bat_width = self.battery.Battery_width
        Bat_length = self.battery.Battery_length
        Bat_height = self.battery.Battery_height

        return Bat_width, Bat_length, Bat_height

    @Part
    def batterygeneration(self):
        return Battery(width_wingbox=self.total_width,
                       height_wingbox=self.total_height,
                       depth_wingbox=self.total_depth,
                       color='blue'
                       )

    @Part
    def habox(self):
        return Wingbox(lala=self.lalala)

    @Part
    def hobox(self):
        return Line(reference=Point(0, 0, 0),
                    direction=Vector(1, 0, 0))


    # @Part
    # def Placement(self):
    #     """
    #     This part places the batteries in the wingbox.
    #     """
    #     for i in range(len(self.total_number_batteries)):
    #         x = 0
    #         y = 0
    #         z = 0
    #         if self.total_width > y + battery.Batterywidth:
    #             x = x + battery.Batterywidth
    #             return self.batterygeneration(position=Position(Point(x,y,z))
    #                         )
    #         elif self.total_width < y+ battery.Batterywidth:
    #             x = 0
    #             y = 0
    #             z = 0
    #             if self.total_depth > x+ battery.Batterydepth:
    #                 battery(position=Position(Point(x,y,z))
    #                             )
    #                 y = y + battery.Batterydepth
    #             elif self.total_depth < y+ battery.Batterydepth:
    #                 x = 0
    #                 y = 0
    #                 z = 0
    #                 if self.total_height > z+ battery.Batteryheight:
    #                     battery(position=Position(Point(x,y,z))
    #                                 )
    #                     z = z + battery.Batteryheight
    #                 else:
    #                     x = 0
    #                     y = 0
    #                     z = 0

# @Part
# def output(self):
#     """
#     This part generates the desired outputs of the design.
#     It makes a .step and a .txt file.
#     """
#     return OutputGeneration(total_width=self.total_width,
#                             total_length=self.total_length,
#                             number_of_people_userinput=self.number_of_people,
#                             social_distance=social_distance_rules,
#                             total_surface_area=self.total_surface_area,
#                             dimensions_rooms=self.dimensions_rooms,
#                             door_position=self.door_position,
#                             router_position=self.router_position,
#                             min_wifi_strength=self.min_wifi_strength,
#                             room_generation=self.room_generation,
#                             optimizer=self.optimizer)
#
#
# # Clash function used in the modifying_optimizer_output attribute.
# # Check if two rooms within a top10 optimization output do clash after modification.
# # i indicates the integer of the top10 analysis under consideration.
# # j indicates the integer of the equipment that you want to check clash with.
# def clash_check(self, i, j, x, y):
#     check = False
#     for z in range(len(self.optimizer.top10[i].positioned_equipment)):
#         if z == j:
#             break
#         # Room x is the equipment j that we want to analyse.
#         distance_centers = (abs(x -
#                                 self.optimizer.top10[i].positioned_equipment[z].center[0]) ** 2 +
#                             abs(y -
#                                 self.optimizer.top10[i].positioned_equipment[z].center[1]) ** 2) ** 0.5
#         distance_required = ((self.optimizer.top10[i].positioned_equipment[j].width / 2 +
#                               self.optimizer.top10[i].positioned_equipment[z].width / 2) ** 2 +
#                              (self.optimizer.top10[i].positioned_equipment[j].length / 2 +
#                               self.optimizer.top10[i].positioned_equipment[z].length / 2) ** 2) ** 0.5
#         if distance_required >= distance_centers:
#             check = True
#     return check


#The parapy bit
from parapy.geom import Box
from parapy.gui import display
obj = Main(label="staircase")
display(obj)

# if __name__ == '__main__':
#     from parapy.gui import display
#
#     obj1 = Main(label="staircase")
#
#     display(obj1)