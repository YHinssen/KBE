from math import pi
from parapy.core import *
from parapy.geom import *

class Wing(GeomBase):
    span = Input(5)
    chord = Input(1)
    thickness = Input(0.2)

    # @attribute
    # def span(self):
    #     return(self.span = self.span)
    #
    # @attribute
    # def chord(self):
    #     return (self.chord=1)

    # @part
    # def planform(self):
    #     return (self.span,self.chord)

    n_step = Input(20)
    w_step = Input(3)
    l_step = Input(1)
    h_step = Input(1)
    t_step = Input(0.2)
    colors = Input(["red", "green", "blue", "yellow", "orange"])

    @Part
    def steps(self):
        return Box(quantify=self.n_step,
                   width=self.w_step,
                   length=self.l_step,
                   height=self.t_step,
                   color=self.colors[child.index % len(self.colors)],
                   position=translate(self.position,
                                      'y', child.index * self.l_step,
                                      'z', child.index * self.h_step))

    @Part
    def wingbox(self):
        return Box(width=self.span,
                   length=self.chord,
                   height=self.thickness)

    @Part
    def wingplanform(self):
        return RectangularSurface(width=self.span,
                   length=self.chord)#,
                   #height=self.thickness)

class Airfoil(self):
    # CST1 = Input(1)
    # CST2 = Input(1)
    # CST3 = Input(1)
    # CST4 = Input(1)
    # CST5 = Input(1)
    # CST6 = Input(1)
    # CST7 = Input(1)
    # CST8 = Input(1)
    # CST9 = Input(1)
    # CST10 = Input(1)
    # CST11 = Input(1)
    # CST12 = Input(1)
    CSTupper = Input([1, 1, 1, 1, 1, 1])
    CSTlower = Input([1, 1, 1, 1, 1, 1])
    AFresolution = Input(10)
    

if __name__ == '__main__':
    from parapy.gui import display

    obj = Wing()
    display(obj)













