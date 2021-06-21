## This file will fit the maximum number of batteries into the wingbox.
import os
from parapy.core import *
from parapy.core.base import Base
from parapy.geom import *
from parapy.geom import Position, Point

THIS_DIR = os.path.dirname(__file__)

class Battery(GeomBase):
    # The following are the inputs required for this part of the program to run, mostly from the external
    # analysis tool.
    width_wingbox = Input(100)
    height_wingbox = Input(20)
    depth_wingbox = Input(40)
    input_bat_width = Input(15)
    input_bat_height = Input(3)
    input_bat_depth = Input(5)
    Wireradius = Input(0.5)
    num_engines= Input(3)
    input_eng_depth =Input(10)
    input_eng_height = Input(10)
    input_eng_width = Input(10)

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
                    coordinates.append(Point(i*self.Batterywidth,j*(self.Batterydepth+6*self.Wireradius),k*self.Batteryheight))
        return coordinates

    @Attribute
    def wirecoordinates(self):
        wirecoordinates = []
        for i in range(self.num_bat_x):
            for j in range(self.num_bat_y):
                for k in range(self.num_bat_z):
                    if j != 0:
                        wirecoordinates.append(Point(0.5*self.Batterywidth + i*self.Batterywidth,j*(self.Batterydepth+6*self.Wireradius), k*self.Batteryheight +0.5*self.Batteryheight))
        return wirecoordinates

    @Attribute
    def mainwirecoordinates(self):
        mainwirecoordinates = []
        for i in range(self.num_bat_y):
            for j in range(self.num_bat_z):
                if i != 0:
                    mainwirecoordinates.append(Point(0.5*self.Batterywidth, i*(self.Batterydepth+6*self.Wireradius) - 3*self.Wireradius, j*self.Batteryheight +0.5*self.Batteryheight))
        return mainwirecoordinates
    @Part
    def batterypack(self):
            return Box(quantify=len(self.coordinates),
                       width=self.Batterywidth,
                       length=self.Batterydepth,
                       height=self.Batteryheight,
                       position=Position(self.coordinates[child.index]),
                       color='blue',
                       )
    @Part
    def HighVoltWire(self):
        return Cylinder(radius=self.Wireradius,
                        quantify = len(self.mainwirecoordinates),
                        height=self.num_bat_x*self.Batterywidth-self.Batterywidth,
                        position=rotate(Position(self.mainwirecoordinates[child.index]), 'y', 1.57079632679),
                        )

    @Part
    def Batwires(self):
        return Cylinder(radius=self.Wireradius,
                        quantify=len(self.wirecoordinates),
                        height=6*self.Wireradius,
                        position=rotate(Position(self.wirecoordinates[child.index]), 'x', 1.57
                                     ),)

    @Attribute
    def Enginewidth(self):
        Eng_width = self.input_eng_width
        return Eng_width

    @Attribute
    def Enginedepth(self):
        Eng_depth = self.input_eng_depth
        return Eng_depth

    @Attribute
    def Engineheight(self):
        Eng_height = self.input_eng_height
        return Eng_height

    @Attribute
    def enginecoordinates(self):
        enginecoordinates = []
        for i in range(self.num_engines):
            enginecoordinates.append(Point(( 0.5* (1 / self.num_engines) * self.width_wingbox-(0.5*self.Enginewidth) + i * ((1 / self.num_engines) * self.width_wingbox -(0.5*self.Enginewidth)) ),
                                                -1 * self.Enginedepth, 0.5 * self.height_wingbox -0.5*self.Engineheight))
        return enginecoordinates

    @Part
    def Engines(self):
        return Box(quantify=self.num_engines,
                   width=self.Enginewidth,
                   length=self.Enginedepth,
                   height=self.Engineheight,
                   position=Position(self.enginecoordinates[child.index]),
                   color='red',
                   )
from parapy.gui import display

obj = Battery()
display(obj)