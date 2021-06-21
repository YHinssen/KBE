## This file will fit the maximum number of batteries into the wingbox.
import os
from parapy.core import *
from parapy.core.base import Base
from parapy.geom import *
from parapy.geom import Position, Point

THIS_DIR = os.path.dirname(__file__)

class Wiring(GeomBase):

    @Part
    def HighVoltWire(self):
        return Cylinder(radius=1,
                        height=400,
                        angle=90,
                        position=Position(Point(20,0,0)))

    # @Attribute
    # def diameter_wire_HV(self):
    #         diameter = input_wire_thickness_HV
    #
    #         wire_thickness = Input(diameter_wire_HV)
    #
    # @Part
    # def LowVoltWire(self):
    #     @Attribute
    #     def diameter_wire_LV(self):
    #         diameter = input_wire_thickness_LV
    #
    #     wire_thickness_LV = Input(diameter_wire_LV)

class Battery(GeomBase):
    # The following are the inputs required for this part of the program to run, mostly from the external
    # analysis tool.
    l_step = Input(1)
    n_step = Input(20)
    width_wingbox = Input(400)
    height_wingbox = Input(20)
    depth_wingbox = Input(40)
    input_bat_width = Input(20)
    input_bat_height = Input(5)
    input_bat_depth = Input(10)
    Wireradius = Input(0.5)

    @Attribute
    def Batterywidth(self):
        Bat_width = self.input_bat_width
        return Bat_width

    @Attribute
    def Batterydepth(self):
        Bat_depth = self.input_bat_depth
        return Bat_depth

    @Attribute
    def Batteryheight(self):
        Bat_height = self.input_bat_height
        return Bat_height

    @Attribute
    def Batteryvolume(self):
        Battery_volume = self.Batterywidth * self.Batterydepth * self.Batteryheight
        return Battery_volume

    @Attribute
    def max_num_batteries(self):
        num_bat = (self.width_wingbox * self.height_wingbox * self.depth_wingbox) / self.Batteryvolume
        return num_bat

    @Attribute
    def num_bat_x(self):
        num_batx = round((self.width_wingbox/self.Batterywidth))
        return num_batx

    @Attribute
    def num_bat_y(self):
        num_baty = round(self.depth_wingbox/(self.Batterydepth + 3*self.Wireradius))
        return num_baty

    @Attribute
    def num_bat_z(self):
        num_batz = round((self.height_wingbox/self.Batteryheight))
        return num_batz

    @Attribute
    def coordinates(self):
        coordinates = []
        for i in range(self.num_bat_x):
            for j in range(self.num_bat_y):
                for k in range(self.num_bat_z):
                    coordinates.append((i*self.Batterywidth,j*(self.Batterydepth+6*self.Wireradius),k*self.Batteryheight))
        return coordinates

    @Part
    def batteryx(self):
            return Box(quantify=round(self.max_num_batteries),
                       width=self.Batterywidth,
                       length=self.Batterydepth,
                       height=self.Batteryheight,
                       position=Position(Point(self.coordinates[child.index])),
                       color='blue',
                       )


    @Part
    def batterytwo(self):
        return Box(quantify=self.num_bat_z,
                   width=self.Batterywidth,
                   length=self.Batterydepth,
                   height=self.Batteryheight,
                   position=translate(Position(Point(0, 0, 0)), 'z', child.index * self.Batteryheight),
                   color='blue',
                   )

    @Part
    def batterythree(self):
        return Box(quantify=len(self.coordinates),
                   width=self.Batterywidth,
                   length=self.Batterydepth,
                   height=self.Batteryheight,
                   position=Position(Point(self.coordinates[child.index])),
                   color='blue',
                   )

    @Part
    def HighVoltWire(self):
        return Cylinder(radius=self.Wireradius,
                        quantify = self.num_bat_y-1,
                        height=self.width_wingbox,
                        position=translate(rotate(Position(Point(0, (self.Batterydepth + 3* self.Wireradius), 0.5*self.Batteryheight)),'y', 1.6), 'y', child.index * (self.Batterydepth +1.5*self.Wireradius )),)

from parapy.gui import display

obj = Battery()
display(obj)