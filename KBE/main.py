## This file will fit the maximum number of batteries into the wingbox.
import os
from tkinter import Tk, simpledialog, messagebox
from math import sqrt

from parapy.core import Input, Part, Attribute
from parapy.core.base import Base
from parapy.geom import Position, Point

THIS_DIR = os.path.dirname(__file__)

ROOT = Tk()
ROOT.withdraw()

class battery(Base):
    @Part
    def Battery(self):
        @Attribute
        def int_width_wingbox(self):
            width = width_Q3D_input

        internalwidth = Input(int_width_wingbox)

    @Attribute
    def int_depth_wingbox(self):
        depth = depth_Q3D_input

    internaldepth = Input(int_depth_wingbox)

    @Attribute
    def int_height_wingbox(self):
        height = height_Q3D_input

    internalheight = Input(int_height_wingbox)

    @Attribute
    def int_volume(self):
        volume = self.internalwidth*self.internalheight*self.internaldepth

    internalvolume = Input(int_volume)

    @Attribute
    def Batterylength(self):
        Bat_length = input_bat_length

    @Attribute
    def Batterydepth(self):
        Bat_depth = input_bat_depth

    @Attribute
    def Batteryheight(self):
        Bat_height = input_bat_height

    Battery_length = Input(Batterylength)
    Battery_depth = Input(Batterydepth)
    Battery_height = Input(Batteryheight)

    @Attribute
    def Batteryvolume(self):
        Battery_volume = self.Battery_length*self.Battery_depth*self.Battery_height

    Battery_volume = Input(Batteryvolume)

    @Attribute
    def max_num_batteries(self):
        num_bat = self.internalvolume/self.Battery_volume


from parapy.gui import display
obj = battery()
display(obj)