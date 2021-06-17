## This file will compute the parameters of the wiring that will be used in the wing
## This is based on either input or default parameters obtained from the internet
import os
from tkinter import Tk, simpledialog, messagebox
from math import sqrt

from parapy.core import Input, Part, Attribute
from parapy.core.base import Base
from parapy.geom import Position, Point

THIS_DIR = os.path.dirname(__file__)

ROOT = Tk()
ROOT.withdraw()


class High_Voltage_Wires(Base):

    @Part
    def HighVoltWire(self):

        @Attribute
        def diameter_wire_HV(self):
            diameter = input_wire_thickness_HV

            wire_thickness = Input(diameter_wire_HV)

class Low_Voltage_Wires(Base):
    @Part
    def LowVoltWire(self):

        @Attribute
        def diameter_wire_LV(self):
            diameter = input_wire_thickness_LV

        wire_thickness_LV = Input(diameter_wire_LV)







    @Attribute
    def wire_weight(self):
        wire_weight =
