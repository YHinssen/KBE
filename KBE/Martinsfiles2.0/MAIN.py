import numpy as np
from math import pi
#from parapy.core import *
#from parapy.geom import *


input_dat = open("EMWETfile.weight","r")
input_ro = input_dat.readlines()[4:]
input_rows = ''
for i in range(len(input_ro)):
    input_rows = input_rows + input_ro[i]
input_rowss = input_rows.split('\n')
width = 11
num_fields = 6
wingbox_thiccness = np.zeros((len(input_rowss)-1,6))
for j in range(len(input_rowss)-1):
    for input_row in input_rowss:
        if not input_row:
            continue
        lala = [float(input_rowss[j][width * i:width * (i + 1)].strip()) for i in range(num_fields)]
        wingbox_thiccness[j] = lala
    wingbox_thiccness = np.array(wingbox_thiccness)
print(len(wingbox_thiccness))




# import numpy
#
# input_data = """ 0.42617E-03-0.19725E+09-0.21139E+09 0.37077E+08
#  0.85234E-03-0.18031E+09-0.18340E+09 0.28237E+08
#  0.12785E-02-0.16583E+09-0.15887E+09 0.20637E+08"""
# #print(type(input_data))
# input_rows = input_data.split('\n')
#
# width = 12
# num_fields = 4
#
# data = []
# for input_row in input_rows:
#     if not input_row:
#         continue
#     data.append([float(input_row[width * i:width * (i + 1)].strip()) for i in range(num_fields)])
#
# data = numpy.array(data)
# #print(data)

'''

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




'''








