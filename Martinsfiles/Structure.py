import math as m
import numpy as np
from parapy.core import *
from parapy.geom import *
from Airfoilcoordiantesgenerator import *

class Wingbox(Base):

    #####take in the input file
    lala= Input(np.loadtxt('inputexample.txt',dtype='str',delimiter=';'))

    #ik zou zeggen dit is een attribute
    '''
    #print('ervoor')
    import matlab.engine
    eng = matlab.engine.start_matlab()
    eng.structuresolver(nargout=0)
    eng.quit()
    #print('erna')
    '''

    # input_dat = open("EMWETfile.weight","r")
    # input_rows = input_dat.readlines()[4:]
    # width = 11
    # num_fields = 6
    # wingbox_thiccness = []
    # for input_row in input_rows:
    #     if not input_row:
    #         continue
    #     wingbox_thiccness.append([float(self.input_row[width * i:width * (i + 1)].strip()) for i in range(num_fields)])
    # wingbox_thiccness = np.array(wingbox_thiccness)
    # #print(data)

    @Attribute
    def innerbox_coordinates(self):

        #########obtain CST coeffs
        # import matlab.engine
        # eng = matlab.engine.start_matlab()
        # eng.AirfoilCSTgenerator(nargout=0)
        # eng.quit()

        g = open("CSTs.dat","r")
        lines = g.read().split(' ')
        CSTcoefs = list(np.float_(lines))
        #print(CSTcoefs[0:6])
        #print(CSTcoefs[6:12])
        [upper_front_norm, lower_front_norm] = Airfoilcoordinates(CSTcoefs[0:6],CSTcoefs[6:12],float(self.lala[7,0])/100)
        [upper_rear_norm, lower_rear_norm] = Airfoilcoordinates(CSTcoefs[0:6],CSTcoefs[6:12],float(self.lala[8,0])/100)
        halfspan = float(self.lala[2,0])
        mid_AF_chord = (float(self.lala[3,0]) * (2-float(self.lala[23,0]) / 100 * 2) + float(self.lala[3,0]) * float(self.lala[4,0]) * 2 * float(self.lala[23,0]) / 100) / 2
        x_root_AF = 0
        y_root_AF = 0
        z_root_AF = 0
        x_additional_AF = float(self.lala[3,0])/4-mid_AF_chord/4 + np.sin(np.radians(float(self.lala[5,0]))) * float(self.lala[23,0])*float(self.lala[2,0])/100
        y_additional_AF = float(self.lala[23,0])*float(self.lala[2,0])/100
        z_additional_AF = np.sin(np.radians(float(self.lala[6,0]))) * float(self.lala[23,0])*float(self.lala[2,0])/100
        x_tip_AF = float(self.lala[3,0])/4-float(self.lala[3,0]) * float(self.lala[4,0])/4 + np.sin(np.radians(float(self.lala[5,0]))) * float(self.lala[2,0])
        y_tip_AF = float(self.lala[2,0])
        z_tip_AF = np.sin(np.radians(float(self.lala[6,0]))) * float(self.lala[2,0])
        #print(upper_front_norm, lower_front_norm)
        skin_stringerspace = 0.02
        sparskin_space = 0.01
        #innerbox_upper_front_z

        innerbox_root_upper_front_x = float(self.lala[3,0])*float(self.lala[7,0])/100+x_root_AF+sparskin_space
        innerbox_root_lower_front_x = innerbox_root_upper_front_x
        innerbox_root_upper_front_z = upper_front_norm*float(self.lala[3,0])+z_root_AF-skin_stringerspace
        innerbox_root_lower_front_z = lower_front_norm*float(self.lala[3,0])+z_root_AF+skin_stringerspace
        innerbox_additionalAF_upper_front_x = mid_AF_chord*float(self.lala[7,0])/100+x_additional_AF+sparskin_space
        innerbox_additionalAF_lower_front_x = innerbox_additionalAF_upper_front_x
        innerbox_additionalAF_upper_front_z = upper_front_norm*mid_AF_chord+z_additional_AF-skin_stringerspace
        innerbox_additionalAF_lower_front_z = lower_front_norm*mid_AF_chord+z_additional_AF+skin_stringerspace
        innerbox_tip_upper_front_x = float(self.lala[3,0])*float(self.lala[4,0])*float(self.lala[7,0])/100+x_tip_AF+sparskin_space
        innerbox_tip_lower_front_x = innerbox_tip_upper_front_x
        innerbox_tip_upper_front_z = upper_front_norm*float(self.lala[3,0])*float(self.lala[4,0])+z_tip_AF-skin_stringerspace
        innerbox_tip_lower_front_z = lower_front_norm*float(self.lala[3,0])*float(self.lala[4,0])+z_tip_AF+skin_stringerspace

        innerbox_root_upper_rear_x = float(self.lala[3,0])*float(self.lala[8,0])/100+x_root_AF-sparskin_space
        innerbox_root_lower_rear_x = innerbox_root_upper_front_x
        innerbox_root_upper_rear_z = upper_rear_norm*float(self.lala[3,0])+z_root_AF-skin_stringerspace
        innerbox_root_lower_rear_z = lower_rear_norm*float(self.lala[3,0])+z_root_AF+skin_stringerspace
        innerbox_additionalAF_upper_rear_x = mid_AF_chord*float(self.lala[8,0])/100+x_additional_AF-sparskin_space
        innerbox_additionalAF_lower_rear_x = innerbox_additionalAF_upper_front_x
        innerbox_additionalAF_upper_rear_z = upper_rear_norm*mid_AF_chord+z_additional_AF-skin_stringerspace
        innerbox_additionalAF_lower_rear_z = lower_rear_norm*mid_AF_chord+z_additional_AF+skin_stringerspace
        innerbox_tip_upper_rear_x = float(self.lala[3,0])*float(self.lala[4,0])*float(self.lala[8,0])/100+x_tip_AF-sparskin_space
        innerbox_tip_lower_rear_x = innerbox_tip_upper_front_x
        innerbox_tip_upper_rear_z = upper_rear_norm*float(self.lala[3,0])*float(self.lala[4,0])+z_tip_AF-skin_stringerspace
        innerbox_tip_lower_rear_z = lower_rear_norm*float(self.lala[3,0])*float(self.lala[4,0])+z_tip_AF+skin_stringerspace

        #coordinates = [innerbox_root_upper_front_x ,innerbox_root_lower_front_x ,innerbox_root_upper_front_z,
        #               innerbox_root_lower_front_z,innerbox_additionalAF_upper_front_x,innerbox_additionalAF_lower_front_x,
        #               innerbox_additionalAF_upper_front_z,innerbox_additionalAF_lower_front_z,innerbox_tip_upper_front_x,
        #               innerbox_tip_lower_front_x,innerbox_tip_upper_front_z,innerbox_tip_lower_front_z,innerbox_root_upper_rear_x,
        #               innerbox_root_lower_rear_x,innerbox_root_upper_rear_z,innerbox_root_lower_rear_z,innerbox_additionalAF_upper_rear_x,
        #               innerbox_additionalAF_lower_rear_x,innerbox_additionalAF_upper_rear_z,innerbox_additionalAF_lower_rear_z,
        #               innerbox_tip_upper_rear_x,innerbox_tip_lower_rear_x,innerbox_tip_upper_rear_z,innerbox_tip_lower_rear_z,
        #               y_root_AF,y_additional_AF,y_tip_AF]
        # xcoordinates = [innerbox_root_upper_front_x, innerbox_root_lower_front_x, innerbox_additionalAF_upper_front_x,
        #                innerbox_additionalAF_lower_front_x, innerbox_tip_upper_front_x,
        #                innerbox_tip_lower_front_x, innerbox_root_upper_rear_x,
        #                innerbox_root_lower_rear_x, innerbox_additionalAF_upper_rear_x,
        #                innerbox_additionalAF_lower_rear_x, innerbox_tip_upper_rear_x, innerbox_tip_lower_rear_x]
        # zcoordinates = [innerbox_root_upper_front_z,innerbox_root_lower_front_z, innerbox_additionalAF_upper_front_z,
        #                 innerbox_additionalAF_lower_front_z,innerbox_tip_upper_front_z, innerbox_tip_lower_front_z,
        #                 innerbox_root_upper_rear_z, innerbox_root_lower_rear_z,innerbox_additionalAF_upper_rear_z,
        #                 innerbox_additionalAF_lower_rear_z,innerbox_tip_upper_rear_z,innerbox_tip_lower_rear_z]
        # ycoordinates = [y_root_AF,y_additional_AF,y_tip_AF]
        xcoordinates = [innerbox_root_upper_front_x, innerbox_root_lower_front_x,
                        innerbox_root_lower_rear_x,innerbox_root_upper_rear_x,
                        innerbox_additionalAF_upper_front_x, innerbox_additionalAF_lower_front_x,
                        innerbox_additionalAF_lower_rear_x,innerbox_additionalAF_upper_rear_x,
                        innerbox_tip_upper_front_x, innerbox_tip_lower_front_x,
                        innerbox_tip_lower_rear_x, innerbox_tip_upper_rear_x]
        zcoordinates = [innerbox_root_upper_front_z, innerbox_root_lower_front_z,
                        innerbox_root_lower_rear_z,innerbox_root_upper_rear_z,
                        innerbox_additionalAF_upper_front_z,innerbox_additionalAF_lower_front_z,
                        innerbox_additionalAF_lower_rear_z,innerbox_additionalAF_upper_rear_z,
                        innerbox_tip_upper_front_z, innerbox_tip_lower_front_z,
                        innerbox_tip_lower_rear_z, innerbox_tip_upper_rear_z]
        ycoordinates = [y_root_AF, y_additional_AF, y_tip_AF]
        points = []
        # for i in range(len(xcoordinates)):
        #     #j = (i/4):1
        #     if i <12:
        #         pt = Point(xcoordinates[i],ycoordinates[2],zcoordinates[i])
        #     if i <8:
        #         pt = Point(xcoordinates[i],ycoordinates[1],zcoordinates[i])
        #     if i <4:
        #         pt = Point(xcoordinates[i],ycoordinates[0],zcoordinates[i])
        #     points.append(pt)
        for i in range(3):
            row = []
            for j in range(4):
                #if j != 4:
                pt = Point(xcoordinates[j+i*4], ycoordinates[i], zcoordinates[j+i*4])
                #if j == 4:
                #    pt = Point(xcoordinates[i * 4], ycoordinates[i], zcoordinates[i * 4])

                row.append((pt))
            points.append(row)
        # for i in range(3):
        #     row = []
        #     for j in range(5):
        #         if j != 4:
        #             pt = [int(xcoordinates[j+i*4]), int(ycoordinates[i]), int(zcoordinates[j+i*4])]
        #         if j == 4:
        #             pt = [int(xcoordinates[i * 4]), int(ycoordinates[i]), int(zcoordinates[i * 4])]
        #
        #         row.append((pt))
        #     points.append(row)
        print(points[0][0])
        print(type(points[0][0]))
        #return coordinates
        return points

    #@Attribute
    #def innerbox_points(self):


    @Part
    def innerbox(self):
        #return BSplineSurface(control_points=points)
        return BezierSurface(control_points=self.innerbox_coordinates)

    @Attribute
    def crosssectionroot(self):
        a = LineSegment(start=self.innerbox_coordinates[0][0],end=self.innerbox_coordinates[0][1])
        b = LineSegment(start=self.innerbox_coordinates[0][1],end=self.innerbox_coordinates[0][2])
        c = LineSegment(start=self.innerbox_coordinates[0][2],end=self.innerbox_coordinates[0][3])
        d = LineSegment(start=self.innerbox_coordinates[0][3],end=self.innerbox_coordinates[0][0])
        return a,b,c,d

    @Attribute
    def crosssectionmidAF(self):
        a = LineSegment(start=self.innerbox_coordinates[1][0], end=self.innerbox_coordinates[1][1])
        b = LineSegment(start=self.innerbox_coordinates[1][1], end=self.innerbox_coordinates[1][2])
        c = LineSegment(start=self.innerbox_coordinates[1][2], end=self.innerbox_coordinates[1][3])
        d = LineSegment(start=self.innerbox_coordinates[1][3], end=self.innerbox_coordinates[1][0])
        return a, b, c, d

    @Attribute
    def crosssectiontip(self):
        a = LineSegment(start=self.innerbox_coordinates[2][0], end=self.innerbox_coordinates[2][1])
        b = LineSegment(start=self.innerbox_coordinates[2][1], end=self.innerbox_coordinates[2][2])
        c = LineSegment(start=self.innerbox_coordinates[2][2], end=self.innerbox_coordinates[2][3])
        d = LineSegment(start=self.innerbox_coordinates[2][3], end=self.innerbox_coordinates[2][0])
        return a, b, c, d

    # @Part
    # def crosssection2(self):
    #     return LineSegment(start=self.innerbox_coordinates[1][0], end=self.innerbox_coordinates[1][1])
    # @Part
    # def crosssection3(self):
    #     return LineSegment(start=self.innerbox_coordinates[2][0], end=self.innerbox_coordinates[2][1])

    @Part
    def surfacefront(self):
        return RuledShell(profiles=(self.crosssectionroot[0], self.crosssectionmidAF[0], self.crosssectiontip[0]))

    @Part
    def surfacelower(self):
        return RuledShell(profiles=(self.crosssectionroot[1], self.crosssectionmidAF[1], self.crosssectiontip[1]))

    @Part
    def surfacerear(self):
        return RuledShell(profiles=(self.crosssectionroot[2], self.crosssectionmidAF[2], self.crosssectiontip[3]))

    @Part
    def surfacetop(self):
        return RuledShell(profiles=(self.crosssectionroot[3], self.crosssectionmidAF[3], self.crosssectiontip[3]))


    # for i in range(12):
    #     aaaa = 'crosssectionline'+i
    #     @Part
    #     def aaaa(self):


    @Part
    def bezier_srf(self):
        return BezierCurve(control_points=[Point(0,0,0),Point(1,0,0),Point(1,1,0),Point(0,1,0)])




if __name__ == '__main__':
    from parapy.gui import display

    obj1 = Wingbox(label="staircase")

    display(obj1)












