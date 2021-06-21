import math as m
import numpy as np
from parapy.core import *
from parapy.geom import *
from Airfoilcoordiantesgenerator import *
from Airfoilinterpolater import *

class Wingbox(Base):

    #####take in the input file
    lala= Input(np.loadtxt('inputexample.txt',dtype='str',delimiter=';'))

    @Attribute
    def run_structure_solver(self):
        #####this attribute makes the matlab file 'structuresolver' run, in order to obtain the mass of the wing and the thickness of the skin
        # import matlab.engine
        # eng = matlab.engine.start_matlab()
        # eng.structuresolver(nargout=0)
        # eng.quit()
        ########import the wing mass as returned from the EMWET program
        input_dat = open("EMWETfile.weight", "r")
        input_ro = input_dat.readlines()[1]
        input_rows = ''
        for i in range(len(input_ro)):
            input_rows = input_rows + input_ro[i]
        input_rowss = input_rows.split('\n')
        width = 21
        num_fields = 2
        wingmass = np.zeros((len(input_rowss) - 1, 6))
        for j in range(len(input_rowss) - 1):
            for input_row in input_rowss:
                if not input_row:
                    continue
                lala = [float(input_rowss[j][width * i:width * (i + 1)].strip()) for i in range(num_fields)]
                wingmass[j] = lala
            wingmass = np.array(wingmass)
        Ws = wingmass[0]
        print(Ws)
        return Ws

    @Attribute
    def innerbox_coordinates(self):
        #########obtain CST coeffs
        # import matlab.engine
        # eng = matlab.engine.start_matlab()
        # eng.AirfoilCSTgenerator(nargout=0)
        # eng.quit()

        #########open CST coeffs file and read data
        g = open("CSTs.dat","r")
        lines = g.read().split(' ')
        CSTcoefs = list(np.float_(lines))

        #########get corners of wingbox
        [upper_front_norm, lower_front_norm] = Airfoilcoordinates(CSTcoefs[0:6],CSTcoefs[6:12],float(self.lala[7,0])/100)
        [upper_rear_norm, lower_rear_norm] = Airfoilcoordinates(CSTcoefs[0:6],CSTcoefs[6:12],float(self.lala[8,0])/100)

        #########get chord of additional airfoil
        mid_AF_chord = (float(self.lala[3,0]) * (2-float(self.lala[23,0]) / 100 * 2) + float(self.lala[3,0]) * float(self.lala[4,0]) * 2 * float(self.lala[23,0]) / 100) / 2

        #########calculate leading edge coordinates of all airfoils
        x_root_AF = 0
        y_root_AF = 0
        z_root_AF = 0
        x_additional_AF = float(self.lala[3,0])/4-mid_AF_chord/4 + np.sin(np.radians(float(self.lala[5,0]))) * float(self.lala[23,0])*float(self.lala[2,0])/100
        y_additional_AF = float(self.lala[23,0])*float(self.lala[2,0])/100
        z_additional_AF = np.sin(np.radians(float(self.lala[6,0]))) * float(self.lala[23,0])*float(self.lala[2,0])/100
        x_tip_AF = float(self.lala[3,0])/4-float(self.lala[3,0]) * float(self.lala[4,0])/4 + np.sin(np.radians(float(self.lala[5,0]))) * float(self.lala[2,0])
        y_tip_AF = float(self.lala[2,0])
        z_tip_AF = np.sin(np.radians(float(self.lala[6,0]))) * float(self.lala[2,0])

        #########set the thickness of the spar and skin thickness, including stringers
        skin_stringerspace = 0.02
        sparskin_space = 0.01

        #########calculate coordinates of wingbox corners front side
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

        #########calculate coordinates of wingbox corners rear side
        innerbox_root_upper_rear_x = float(self.lala[3,0])*float(self.lala[8,0])/100+x_root_AF-sparskin_space
        innerbox_root_lower_rear_x = innerbox_root_upper_rear_x
        innerbox_root_upper_rear_z = upper_rear_norm*float(self.lala[3,0])+z_root_AF-skin_stringerspace
        innerbox_root_lower_rear_z = lower_rear_norm*float(self.lala[3,0])+z_root_AF+skin_stringerspace
        innerbox_additionalAF_upper_rear_x = mid_AF_chord*float(self.lala[8,0])/100+x_additional_AF-sparskin_space
        innerbox_additionalAF_lower_rear_x = innerbox_additionalAF_upper_rear_x
        innerbox_additionalAF_upper_rear_z = upper_rear_norm*mid_AF_chord+z_additional_AF-skin_stringerspace
        innerbox_additionalAF_lower_rear_z = lower_rear_norm*mid_AF_chord+z_additional_AF+skin_stringerspace
        innerbox_tip_upper_rear_x = float(self.lala[3,0])*float(self.lala[4,0])*float(self.lala[8,0])/100+x_tip_AF-sparskin_space
        innerbox_tip_lower_rear_x = innerbox_tip_upper_rear_x
        innerbox_tip_upper_rear_z = upper_rear_norm*float(self.lala[3,0])*float(self.lala[4,0])+z_tip_AF-skin_stringerspace
        innerbox_tip_lower_rear_z = lower_rear_norm*float(self.lala[3,0])*float(self.lala[4,0])+z_tip_AF+skin_stringerspace

        #########put wingbox coordinates in matrices, in the order of: upper front, lower front, lower rear, upper rear
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

        #########make a points list from the coordinates to be used for geometry
        points = []
        for i in range(3):
            row = []
            for j in range(4):
                pt = Point(xcoordinates[j+i*4], ycoordinates[i], zcoordinates[j+i*4])
                row.append((pt))
            points.append(row)
        return points
    '''
    @Attribute
    def outerbox_coordinates(self):

        #########obtain CST coeffs
        # import matlab.engine
        # eng = matlab.engine.start_matlab()
        # eng.AirfoilCSTgenerator(nargout=0)
        # eng.quit()

        #########open CST coeffs file and read data
        g = open("CSTs.dat","r")
        lines = g.read().split(' ')
        CSTcoefs = list(np.float_(lines))

        #########get corners of wingbox
        [upper_front_norm, lower_front_norm] = Airfoilcoordinates(CSTcoefs[0:6],CSTcoefs[6:12],float(self.lala[7,0])/100)
        [upper_rear_norm, lower_rear_norm] = Airfoilcoordinates(CSTcoefs[0:6],CSTcoefs[6:12],float(self.lala[8,0])/100)

        #########get chord of additional airfoil
        mid_AF_chord = (float(self.lala[3,0]) * (2-float(self.lala[23,0]) / 100 * 2) + float(self.lala[3,0]) * float(self.lala[4,0]) * 2 * float(self.lala[23,0]) / 100) / 2

        #########calculate leading edge coordinates of all airfoils
        x_root_AF = 0
        y_root_AF = 0
        z_root_AF = 0
        x_additional_AF = float(self.lala[3,0])/4-mid_AF_chord/4 + np.sin(np.radians(float(self.lala[5,0]))) * float(self.lala[23,0])*float(self.lala[2,0])/100
        y_additional_AF = float(self.lala[23,0])*float(self.lala[2,0])/100
        z_additional_AF = np.sin(np.radians(float(self.lala[6,0]))) * float(self.lala[23,0])*float(self.lala[2,0])/100
        x_tip_AF = float(self.lala[3,0])/4-float(self.lala[3,0]) * float(self.lala[4,0])/4 + np.sin(np.radians(float(self.lala[5,0]))) * float(self.lala[2,0])
        y_tip_AF = float(self.lala[2,0])
        z_tip_AF = np.sin(np.radians(float(self.lala[6,0]))) * float(self.lala[2,0])

        #########calculate coordinates of wingbox corners front side
        innerbox_root_upper_front_x = float(self.lala[3,0])*float(self.lala[7,0])/100+x_root_AF
        innerbox_root_lower_front_x = innerbox_root_upper_front_x
        innerbox_root_upper_front_z = upper_front_norm*float(self.lala[3,0])+z_root_AF
        innerbox_root_lower_front_z = lower_front_norm*float(self.lala[3,0])+z_root_AF
        innerbox_additionalAF_upper_front_x = mid_AF_chord*float(self.lala[7,0])/100+x_additional_AF
        innerbox_additionalAF_lower_front_x = innerbox_additionalAF_upper_front_x
        innerbox_additionalAF_upper_front_z = upper_front_norm*mid_AF_chord+z_additional_AF
        innerbox_additionalAF_lower_front_z = lower_front_norm*mid_AF_chord+z_additional_AF
        innerbox_tip_upper_front_x = float(self.lala[3,0])*float(self.lala[4,0])*float(self.lala[7,0])/100+x_tip_AF
        innerbox_tip_lower_front_x = innerbox_tip_upper_front_x
        innerbox_tip_upper_front_z = upper_front_norm*float(self.lala[3,0])*float(self.lala[4,0])+z_tip_AF
        innerbox_tip_lower_front_z = lower_front_norm*float(self.lala[3,0])*float(self.lala[4,0])+z_tip_AF

        #########calculate coordinates of wingbox corners rear side
        innerbox_root_upper_rear_x = float(self.lala[3,0])*float(self.lala[8,0])/100+x_root_AF
        innerbox_root_lower_rear_x = innerbox_root_upper_rear_x
        innerbox_root_upper_rear_z = upper_rear_norm*float(self.lala[3,0])+z_root_AF
        innerbox_root_lower_rear_z = lower_rear_norm*float(self.lala[3,0])+z_root_AF
        innerbox_additionalAF_upper_rear_x = mid_AF_chord*float(self.lala[8,0])/100+x_additional_AF
        innerbox_additionalAF_lower_rear_x = innerbox_additionalAF_upper_rear_x
        innerbox_additionalAF_upper_rear_z = upper_rear_norm*mid_AF_chord+z_additional_AF
        innerbox_additionalAF_lower_rear_z = lower_rear_norm*mid_AF_chord+z_additional_AF
        innerbox_tip_upper_rear_x = float(self.lala[3,0])*float(self.lala[4,0])*float(self.lala[8,0])/100+x_tip_AF
        innerbox_tip_lower_rear_x = innerbox_tip_upper_rear_x
        innerbox_tip_upper_rear_z = upper_rear_norm*float(self.lala[3,0])*float(self.lala[4,0])+z_tip_AF
        innerbox_tip_lower_rear_z = lower_rear_norm*float(self.lala[3,0])*float(self.lala[4,0])+z_tip_AF

        #########put wingbox coordinates in matrices, in the order of: upper front, lower front, lower rear, upper rear
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

        #########make a points list from the coordinates to be used for geometry
        points = []
        for i in range(3):
            row = []
            for j in range(4):
                pt = Point(xcoordinates[j+i*4], ycoordinates[i], zcoordinates[j+i*4])
                row.append((pt))
            points.append(row)
        return points
    
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

    @Attribute
    def crosssectionrootout(self):
        a = LineSegment(start=self.outerbox_coordinates[0][0], end=self.outerbox_coordinates[0][1])
        b = LineSegment(start=self.outerbox_coordinates[0][1], end=self.outerbox_coordinates[0][2])
        c = LineSegment(start=self.outerbox_coordinates[0][2], end=self.outerbox_coordinates[0][3])
        d = LineSegment(start=self.outerbox_coordinates[0][3], end=self.outerbox_coordinates[0][0])
        return a, b, c, d

    @Attribute
    def crosssectionmidAFout(self):
        a = LineSegment(start=self.outerbox_coordinates[1][0], end=self.outerbox_coordinates[1][1])
        b = LineSegment(start=self.outerbox_coordinates[1][1], end=self.outerbox_coordinates[1][2])
        c = LineSegment(start=self.outerbox_coordinates[1][2], end=self.outerbox_coordinates[1][3])
        d = LineSegment(start=self.outerbox_coordinates[1][3], end=self.outerbox_coordinates[1][0])
        return a, b, c, d

    @Attribute
    def crosssectiontipout(self):
        a = LineSegment(start=self.outerbox_coordinates[2][0], end=self.outerbox_coordinates[2][1])
        b = LineSegment(start=self.outerbox_coordinates[2][1], end=self.outerbox_coordinates[2][2])
        c = LineSegment(start=self.outerbox_coordinates[2][2], end=self.outerbox_coordinates[2][3])
        d = LineSegment(start=self.outerbox_coordinates[2][3], end=self.outerbox_coordinates[2][0])
        return a, b, c, d

    @Part
    def surfacefront(self):
        return RuledShell(profiles=(self.crosssectionroot[0], self.crosssectionmidAF[0], self.crosssectiontip[0]))

    @Part
    def surfacelower(self):
        return RuledShell(profiles=(self.crosssectionroot[1], self.crosssectionmidAF[1], self.crosssectiontip[1]))

    @Part
    def surfacerear(self):
        return RuledShell(profiles=(self.crosssectionroot[2], self.crosssectionmidAF[2], self.crosssectiontip[2]))

    @Part
    def surfacetop(self):
        return RuledShell(profiles=(self.crosssectionroot[3], self.crosssectionmidAF[3], self.crosssectiontip[3]))

    @Part
    def surfacefrontout(self):
        return RuledShell(profiles=(self.crosssectionrootout[0], self.crosssectionmidAFout[0], self.crosssectiontipout[0]))

    @Part
    def surfacelowerout(self):
        return RuledShell(profiles=(self.crosssectionrootout[1], self.crosssectionmidAFout[1], self.crosssectiontipout[1]))

    @Part
    def surfacerearout(self):
        return RuledShell(profiles=(self.crosssectionrootout[2], self.crosssectionmidAFout[2], self.crosssectiontipout[2]))

    @Part
    def surfacetopout(self):
        return RuledShell(profiles=(self.crosssectionrootout[3], self.crosssectionmidAFout[3], self.crosssectiontipout[3]))
    

    @Attribute
    def crosssections(self):
        ########make curves from the calculated coordinates, to be used for solids
        root = Polygon(points=self.outerbox_coordinates[0])
        mid = Polygon(points=self.outerbox_coordinates[1])
        tip = Polygon(points=self.outerbox_coordinates[2])
        rootin = Polygon(points=self.innerbox_coordinates[0])
        midin = Polygon(points=self.innerbox_coordinates[1])
        tipin = Polygon(points=self.innerbox_coordinates[2])
        return root,mid,tip,rootin,midin,tipin
    @Part
    def outersolid(self):
        ########make the outside of the square wingbox
        return RuledSolid(profiles=self.crosssections[0:3])
    
    @Part
    def thiccskin_box(self):
        ########make the square wingbox with its thickness
        return SubtractedSolid(shape_in=self.outersolid,tool=self.innersolid)

    '''
    @Attribute
    def crosssections(self):
        ########make curves from the calculated coordinates, to be used for solids
        rootin = Polygon(points=self.innerbox_coordinates[0])
        midin = Polygon(points=self.innerbox_coordinates[1])
        tipin = Polygon(points=self.innerbox_coordinates[2])
        return rootin, midin, tipin
    @Part
    def innersolid(self):
        ########make the inside of the square wingbox
        return RuledSolid(profiles=self.crosssections)
    @Attribute
    def outerskin_coordinates(self):
        #########get chord of additional airfoil
        mid_AF_chord = (float(self.lala[3, 0]) * (2 - float(self.lala[23, 0]) / 100 * 2) + float(
            self.lala[3, 0]) * float(self.lala[4, 0]) * 2 * float(self.lala[23, 0]) / 100) / 2
        #########get z distances of the skin for the three specifies airfoils
        [upperskinroot,lowerskinroot] = airfoilinterpolater(0, 1, float(self.lala[3,0]), mid_AF_chord, 0, float(self.lala[23, 0])/100, 0,float(self.lala[7,0])/100, float(self.lala[8,0])/100)
        [upperskinmid,  lowerskinmid] = airfoilinterpolater(0, 1, float(self.lala[3, 0]), mid_AF_chord, 0, float(self.lala[23, 0])/100, float(self.lala[23, 0])/100,float(self.lala[7, 0])/100, float(self.lala[8, 0])/100)
        [upperskintip,  lowerskintip] = airfoilinterpolater(1, 2, mid_AF_chord,float(self.lala[3, 0])*float(self.lala[4,0]),float(self.lala[23, 0])/100, 1, 1, float(self.lala[7, 0])/100, float(self.lala[8, 0])/100)

        #########calculate leading edge coordinates of all airfoils
        x_root_AF = 0
        y_root_AF = 0
        z_root_AF = 0
        x_additional_AF = float(self.lala[3,0])/4-mid_AF_chord/4 + np.sin(np.radians(float(self.lala[5,0]))) * float(self.lala[23,0])*float(self.lala[2,0])/100
        y_additional_AF = float(self.lala[23,0])*float(self.lala[2,0])/100
        z_additional_AF = np.sin(np.radians(float(self.lala[6,0]))) * float(self.lala[23,0])*float(self.lala[2,0])/100
        x_tip_AF = float(self.lala[3,0])/4-float(self.lala[3,0]) * float(self.lala[4,0])/4 + np.sin(np.radians(float(self.lala[5,0]))) * float(self.lala[2,0])
        y_tip_AF = float(self.lala[2,0])
        z_tip_AF = np.sin(np.radians(float(self.lala[6,0]))) * float(self.lala[2,0])
        ycoordinates = [y_root_AF, y_additional_AF, y_tip_AF]
        #########put all skin coordinates in an array in Point form for geometry
        points = []
        for i in range(3):
            row = []
            if i==0:
                for j in range(len(upperskinroot)):
                    pt = Point(upperskinroot[j,1]+x_root_AF, ycoordinates[i], upperskinroot[j,0]+z_root_AF)
                    row.append((pt))
                for j in range(len(upperskinroot)):
                    pt = Point(lowerskinroot[-(j+1),1]+x_root_AF, ycoordinates[i], lowerskinroot[-(j+1),0]+z_root_AF)
                    row.append((pt))
            if i==1:
                for j in range(len(upperskinroot)):
                    pt = Point(upperskinmid[j,1]+x_additional_AF, ycoordinates[i], upperskinmid[j,0]+z_additional_AF)
                    row.append((pt))
                for j in range(len(upperskinroot)):
                    pt = Point(lowerskinmid[-(j+1),1]+x_additional_AF, ycoordinates[i], lowerskinmid[-(j+1),0]+z_additional_AF)
                    row.append((pt))
            if i==2:
                for j in range(len(upperskinroot)):
                    pt = Point(upperskintip[j,1]+x_tip_AF, ycoordinates[i], upperskintip[j,0]+z_tip_AF)
                    row.append((pt))
                for j in range(len(upperskinroot)):
                    pt = Point(lowerskintip[-(j+1),1]+x_tip_AF, ycoordinates[i], lowerskintip[-(j+1),0]+z_tip_AF)
                    row.append((pt))
            points.append(row)
        return points

    @Attribute
    def innerskin_coordinates(self):
        #########get chord of additional airfoil
        mid_AF_chord = (float(self.lala[3, 0]) * (2 - float(self.lala[23, 0]) / 100 * 2) + float(
            self.lala[3, 0]) * float(self.lala[4, 0]) * 2 * float(self.lala[23, 0]) / 100) / 2

        #########calculate leading edge coordinates
        x_root_AF = 0
        z_root_AF = 0
        x_tip_AF = float(self.lala[3, 0]) / 4 - float(self.lala[3, 0]) * float(self.lala[4, 0]) / 4 + np.sin(
            np.radians(float(self.lala[5, 0]))) * float(self.lala[2, 0])
        z_tip_AF = np.sin(np.radians(float(self.lala[6, 0]))) * float(self.lala[2, 0])

        #########set the thickness of the spar and skin thickness, including stringers
        skin_stringerspace = 0.02
        sparskin_space = 0.01

        #########obtain the skin z-distances at various y-positions
        y = 0
        proffile = []
        for k in range(3):
            ponts = []
            y0 = y
            if k ==0:
                y = float(self.lala[23, 0])/100
            if k == 1:
                y = 1
            if k==2:
                y=1

            if y <= float(self.lala[23, 0]):
                [upperskininnb, lowerskininnb] = airfoilinterpolater(0, 1, float(self.lala[3, 0]), mid_AF_chord, 0,
                                                                     float(self.lala[23, 0]) / 100,
                                                                     y0, float(self.lala[7, 0]) / 100,
                                                                     float(self.lala[8, 0]) / 100)
            else:
                [upperskininnb, lowerskininnb] = airfoilinterpolater(1, 2, mid_AF_chord,
                                                                     float(self.lala[3, 0]) * float(self.lala[4, 0]),
                                                                     float(self.lala[23, 0]) / 100,
                                                                     1, y0, float(self.lala[7, 0]) / 100,
                                                                     float(self.lala[8, 0]) / 100)
            #########calculate leading edge coordinates at the specified span position
            xinn = (x_root_AF * (2 - y0 * 2) + x_tip_AF * 2 * y0) / 2
            zinn = (z_root_AF * (2 - y0 * 2) + z_tip_AF * 2 * y0) / 2

            #########shift the first an last points by the local thickness of the spars
            upperskininnb[0, 1] = upperskininnb[0, 1] + sparskin_space
            lowerskininnb[0, 1] = lowerskininnb[0, 1] + sparskin_space
            upperskininnb[-1, 1] = upperskininnb[-1, 1] - sparskin_space
            lowerskininnb[-1, 1] = lowerskininnb[-1, 1] - sparskin_space

            #########put all coordinates in Point form in an array
            for i in range(1):
                row = []
                for j in range(len(upperskininnb)):
                    pt = Point(upperskininnb[j, 1] + xinn, y0 * float(self.lala[2, 0]),
                                   upperskininnb[j, 0] + zinn - skin_stringerspace)
                    row.append((pt))
                for j in range(len(upperskininnb)):
                    pt = Point(lowerskininnb[-(j + 1), 1] + xinn, y0 * float(self.lala[2, 0]),
                                   lowerskininnb[-(j + 1), 0] + zinn + skin_stringerspace)
                    row.append((pt))
            ponts.append(row)
            a = Polygon(points=ponts[0])
            proffile.append(a)
        return proffile

    '''
    @Attribute
    def outerskin_coordinates(self):
        g = open("CSTs.dat", "r")
        lines = g.read().split(' ')
        CSTcoefs = list(np.float_(lines))
        y_root_AF = 0
        y_additional_AF = float(self.lala[23, 0]) * float(self.lala[2, 0]) / 100
        y_tip_AF = float(self.lala[2, 0])
        ycoordinates = [y_root_AF, y_additional_AF, y_tip_AF]
        res = 51
        upperskin1 = np.zeros(res)
        lowerskin1 = np.zeros(res)
        upperskin2 = np.zeros(res)
        lowerskin2 = np.zeros(res)
        upperskin1 = []
        lowerskin1 = []
        upperskin2 = []
        lowerskin2 = []
        # upperskin1 = np.zeros((res,2))
        # lowerskin1 = np.zeros((res,2))
        # upperskin2 = np.zeros((res,2))
        # lowerskin2 = np.zeros((res,2))
        x1 = np.zeros(res)
        #xx = np.zeros(res)
        xx = []
        x2 = np.zeros(res)
        upperskin = []
        lowerskin = []
        frontspar = self.lala[7,0]/100
        rearspar = self.lala[8,0]/100
        dist = (rearspar - frontspar) / (res - 1)
        ydist = 0.5 - 0
        ything = (0.1 - 0) / ydist
        chord = (chord1 * (2 - ything * 2) + chord2 * 2 * ything) / 2
        # if airfoil1 == 0:
        #     j = 0
        # if airfoil2 == 2:
        #     j = 12
        # else:
        j = 0

        for i in range(res):
            x = frontspar + dist * i
            # x1[i] = x * chord1
            xx.append(x * chord)
            # x2[i] = x * chord2
            # [upperskin1[i], lowerskin1[i]] = (Airfoilcoordinates(CSTcoefs[0+j:6+j], CSTcoefs[6+j:12+j],x))#*int(chord1)
            # [upperskin2[i], lowerskin2[i]]= (Airfoilcoordinates(CSTcoefs[12+j:18+j], CSTcoefs[18+j:24+j],x))#*int(chord2)
            [up1, low1] = (Airfoilcoordinates(CSTcoefs[0 + j:6 + j], CSTcoefs[6 + j:12 + j], x))  # * int(chord1)
            [up2, low2] = (Airfoilcoordinates(CSTcoefs[12 + j:18 + j], CSTcoefs[18 + j:24 + j], x))  # * int(chord2)
            # upperskin1[i] = up1#,x
            # lowerskin1[i] = low1#,x
            # upperskin2[i] = up2#,x
            # lowerskin2[i] = low2#,x
            upperskin1.append(up1)  # ,x
            lowerskin1.append(low1)  # ,x
            upperskin2.append(up2)  # ,x
            lowerskin2.append(low2)  # ,x
            upperint = (up1 * chord1 * (2 - ything * 2) + up2 * chord2 * 2 * ything) / 2
            lowerint = (low1 * chord1 * (2 - ything * 2) + low2 * chord2 * 2 * ything) / 2
            upperskin.append(upperint)
            lowerskin.append(lowerint)
        return    
    '''

    @Attribute
    def skin_crosssections_out(self):
        ########make curves from the calculated coordinates, to be used for solids
        root = Polygon(points=self.outerskin_coordinates[0])
        mid = Polygon(points=self.outerskin_coordinates[1])
        tip = Polygon(points=self.outerskin_coordinates[2])
        return root, mid, tip

    @Part
    def outerskin(self):
        ########make the outside of the wing(box)
        return RuledSolid(profiles=self.skin_crosssections_out)

    @Part
    def innerskin(self):
        ########make the outside of the wing(box)
        return RuledSolid(profiles=self.innerskin_coordinates)

    @Part
    def thiccskin_notmany(self):
        #########make the thick skin
        return SubtractedSolid(shape_in=self.outerskin, tool=self.innerskin)

    @Attribute
    def thiccness_data(self):
        ########import the thickness data as returned from the EMWET program
        input_dat = open("EMWETfile.weight", "r")
        input_ro = input_dat.readlines()[4:]
        input_rows = ''
        for i in range(len(input_ro)):
            input_rows = input_rows + input_ro[i]
        input_rowss = input_rows.split('\n')
        width = 11
        num_fields = 6
        wingbox_thiccness = np.zeros((len(input_rowss) - 1, 6))
        for j in range(len(input_rowss) - 1):
            for input_row in input_rowss:
                if not input_row:
                    continue
                lala = [float(input_rowss[j][width * i:width * (i + 1)].strip()) for i in range(num_fields)]
                wingbox_thiccness[j] = lala
            wingbox_thiccness = np.array(wingbox_thiccness)
        return wingbox_thiccness

    @Attribute
    def thiccouterskin(self):
        #########get chord of additional airfoil
        mid_AF_chord = (float(self.lala[3, 0]) * (2 - float(self.lala[23, 0]) / 100 * 2) + float(
            self.lala[3, 0]) * float(self.lala[4, 0]) * 2 * float(self.lala[23, 0]) / 100) / 2

        #########calculate leading edge coordinates
        x_root_AF = 0
        z_root_AF = 0
        x_tip_AF = float(self.lala[3, 0]) / 4 - float(self.lala[3, 0]) * float(self.lala[4, 0]) / 4 + np.sin(
            np.radians(float(self.lala[5, 0]))) * float(self.lala[2, 0])
        z_tip_AF = np.sin(np.radians(float(self.lala[6, 0]))) * float(self.lala[2, 0])

        #########obtain the skin z-distances at various y-positions
        proffile = []
        y = 0
        for k in range(len(self.thiccness_data)+1):
            ponts = []
            y0 = y
            if k ==len(self.thiccness_data):
                y = 1
            else:
                y = self.thiccness_data[k,0]

            if y <= float(self.lala[23,0]):
                [upperskininnb, lowerskininnb] = airfoilinterpolater(0, 1, float(self.lala[3, 0]), mid_AF_chord, 0, float(self.lala[23, 0])/100,
                                                                     y0, float(self.lala[7, 0]) / 100,float(self.lala[8, 0]) / 100)
                [upperskinoutb, lowerskinoutb] = airfoilinterpolater(0, 1, float(self.lala[3, 0]), mid_AF_chord, 0, float(self.lala[23, 0])/100,
                                                                   y, float(self.lala[7, 0]) / 100,float(self.lala[8, 0]) / 100)
            else:
                [upperskininnb, lowerskininnb] = airfoilinterpolater(1, 2, mid_AF_chord,float(self.lala[3, 0])*float(self.lala[4, 0]),  float(self.lala[23, 0])/100,
                                                                     1,y0, float(self.lala[7, 0]) / 100,float(self.lala[8, 0]) / 100)
                [upperskinoutb, lowerskinoutb] = airfoilinterpolater(1, 2, mid_AF_chord, float(self.lala[3, 0])*float(self.lala[4, 0]), float(self.lala[23, 0])/100, 1,
                                                                     y, float(self.lala[7, 0]) / 100,float(self.lala[8, 0]) / 100)
            #########calculate leading edge coordinates at the specified span position
            xinn = (x_root_AF * (2 - y0 * 2) + x_tip_AF * 2 * y0) / 2
            xout = (x_root_AF * (2 - y * 2) + x_tip_AF * 2 * y) / 2
            zinn = (z_root_AF * (2 - y0 * 2) + z_tip_AF * 2 * y0) / 2
            zout = (z_root_AF * (2 - y * 2) + z_tip_AF * 2 * y) / 2

            #########put all coordinates in Point form in an array
            for i in range(2):
                row = []
                if i == 0:
                    for j in range(len(upperskininnb)):
                        pt = Point(upperskininnb[j, 1] + xinn, y0*float(self.lala[2,0]),
                                    upperskininnb[j, 0] + zinn)
                        row.append((pt))
                    for j in range(len(upperskininnb)):
                        pt = Point(lowerskininnb[-(j + 1), 1] + xinn, y0*float(self.lala[2,0]),
                                    lowerskininnb[-(j + 1), 0] + zinn)
                        row.append((pt))
                if i == 1:
                    for j in range(len(upperskininnb)):
                        pt = Point(upperskinoutb[j, 1] + xout, y*float(self.lala[2,0]),
                                    upperskinoutb[j, 0] + zout)
                        row.append((pt))
                    for j in range(len(upperskininnb)):
                        pt = Point(lowerskinoutb[-(j + 1), 1] + xout, y*float(self.lala[2,0]),
                                    lowerskinoutb[-(j + 1), 0] + zout)
                        row.append((pt))
                ponts.append(row)
            a = Polygon(points=ponts[0])
            b = Polygon(points=ponts[1])
            proffile.append(a)
            proffile.append(b)
        return proffile

    @Part
    def outerskin_many(self):
        #########make the outer skin with its many sections, to be used for thick skin generation
        return RuledSolid(profiles=self.thiccouterskin)

    @Attribute
    def thiccinnerskin(self):
        #########get chord of additional airfoil
        mid_AF_chord = (float(self.lala[3, 0]) * (2 - float(self.lala[23, 0]) / 100 * 2) + float(
            self.lala[3, 0]) * float(self.lala[4, 0]) * 2 * float(self.lala[23, 0]) / 100) / 2

        #########calculate leading edge coordinates
        x_root_AF = 0
        z_root_AF = 0
        x_tip_AF = float(self.lala[3, 0]) / 4 - float(self.lala[3, 0]) * float(self.lala[4, 0]) / 4 + np.sin(
            np.radians(float(self.lala[5, 0]))) * float(self.lala[2, 0])
        z_tip_AF = np.sin(np.radians(float(self.lala[6, 0]))) * float(self.lala[2, 0])

        #########obtain the skin z-distances at various y-positions
        y = 0
        proffile = []
        for k in range(len(self.thiccness_data)+1):
            ponts = []
            y0 = y
            if k == len(self.thiccness_data):
                y = 1
                k = len(self.thiccness_data)-1
            else:
                y = self.thiccness_data[k, 0]

            if y <= float(self.lala[23, 0]):
                [upperskininnb, lowerskininnb] = airfoilinterpolater(0, 1, float(self.lala[3, 0]), mid_AF_chord, 0,
                                                                     float(self.lala[23, 0]) / 100,
                                                                     y0, float(self.lala[7, 0]) / 100,
                                                                     float(self.lala[8, 0]) / 100)
                [upperskinoutb, lowerskinoutb] = airfoilinterpolater(0, 1, float(self.lala[3, 0]), mid_AF_chord, 0,
                                                                     float(self.lala[23, 0]) / 100,
                                                                     y, float(self.lala[7, 0]) / 100,
                                                                     float(self.lala[8, 0]) / 100)
            else:
                [upperskininnb, lowerskininnb] = airfoilinterpolater(1, 2, mid_AF_chord,
                                                                     float(self.lala[3, 0]) * float(self.lala[4, 0]),
                                                                     float(self.lala[23, 0]) / 100,
                                                                     1, y0, float(self.lala[7, 0]) / 100,
                                                                     float(self.lala[8, 0]) / 100)
                [upperskinoutb, lowerskinoutb] = airfoilinterpolater(1, 2, mid_AF_chord,
                                                                     float(self.lala[3, 0]) * float(self.lala[4, 0]),
                                                                     float(self.lala[23, 0]) / 100, 1,
                                                                     y, float(self.lala[7, 0]) / 100,
                                                                     float(self.lala[8, 0]) / 100)
            #########calculate leading edge coordinates at the specified span position
            xinn = (x_root_AF * (2 - y0 * 2) + x_tip_AF * 2 * y0) / 2
            xout = (x_root_AF * (2 - y * 2) + x_tip_AF * 2 * y) / 2
            zinn = (z_root_AF * (2 - y0 * 2) + z_tip_AF * 2 * y0) / 2
            zout = (z_root_AF * (2 - y * 2) + z_tip_AF * 2 * y) / 2

            #########shift the first an last points by the local thickness of the spars
            upperskininnb[0, 1] = upperskininnb[0, 1] + self.thiccness_data[k, 4]/1000
            lowerskininnb[0, 1] = lowerskininnb[0, 1] + self.thiccness_data[k, 4]/1000
            upperskinoutb[0, 1] = upperskinoutb[0, 1] + self.thiccness_data[k, 4]/1000
            lowerskinoutb[0, 1] = lowerskinoutb[0, 1] + self.thiccness_data[k, 4]/1000
            upperskininnb[-1, 1] = upperskininnb[-1, 1] - self.thiccness_data[k, 5]/1000
            lowerskininnb[-1, 1] = lowerskininnb[-1, 1] - self.thiccness_data[k, 5]/1000
            upperskinoutb[-1, 1] = upperskinoutb[-1, 1] - self.thiccness_data[k, 5]/1000
            lowerskinoutb[-1, 1] = lowerskinoutb[-1, 1] - self.thiccness_data[k, 5]/1000

            #########put all coordinates in Point form in an array
            for i in range(2):
                row = []
                if i == 0:
                    for j in range(len(upperskininnb)):
                        pt = Point(upperskininnb[j, 1] + xinn, y0 * float(self.lala[2, 0]),
                                   upperskininnb[j, 0] + zinn - self.thiccness_data[k, 2]/1000)
                        row.append((pt))
                    for j in range(len(upperskininnb)):
                        pt = Point(lowerskininnb[-(j + 1), 1] + xinn, y0 * float(self.lala[2, 0]),
                                   lowerskininnb[-(j + 1), 0] + zinn + self.thiccness_data[k, 3]/1000)
                        row.append((pt))
                if i == 1:
                    for j in range(len(upperskininnb)):
                        pt = Point(upperskinoutb[j, 1] + xout, y * float(self.lala[2, 0])-0.001,
                                   upperskinoutb[j, 0] + zout - self.thiccness_data[k, 2]/1000)
                        row.append((pt))
                    for j in range(len(upperskininnb)):
                        pt = Point(lowerskinoutb[-(j + 1), 1] + xout, y * float(self.lala[2, 0])-0.001,
                                   lowerskinoutb[-(j + 1), 0] + zout + self.thiccness_data[k, 3]/1000)
                        row.append((pt))
                ponts.append(row)
            a = Polygon(points=ponts[0])
            b = Polygon(points=ponts[1])
            proffile.append(a)
            proffile.append(b)
        #print(proffile)
        return proffile

    @Part
    def innerskin_many(self):
        #########make the inner skin with its many sections, to be used for thick skin generation
        return RuledSolid(profiles=self.thiccinnerskin)

    ######### this one is taken out as it makes your computer crash due to the high load
    # @Part
    # def thiccskin(self):
    #     #########make the thick skin
    #     return SubtractedSolid(shape_in=self.outerskin,tool=self.innerskin_many)

    @Attribute
    def ribs_attribute(self):
        #########get chord of additional airfoil
        mid_AF_chord = (float(self.lala[3, 0]) * (2 - float(self.lala[23, 0]) / 100 * 2) + float(
            self.lala[3, 0]) * float(self.lala[4, 0]) * 2 * float(self.lala[23, 0]) / 100) / 2

        #########calculate leading edge coordinates
        x_root_AF = 0
        z_root_AF = 0
        x_tip_AF = float(self.lala[3, 0]) / 4 - float(self.lala[3, 0]) * float(self.lala[4, 0]) / 4 + np.sin(
            np.radians(float(self.lala[5, 0]))) * float(self.lala[2, 0])
        z_tip_AF = np.sin(np.radians(float(self.lala[6, 0]))) * float(self.lala[2, 0])

        #########set the thickness of the spar and skin thickness, including stringers
        skin_stringerspace = 0.02
        sparskin_space = 0.01

        #########obtain the skin z-distances at various y-positions
        proffile = []
        ribthiccness = 0.002 #thickness of the ribs
        pitch = float(self.lala[11, 0]) #rib pitch as defined in the inputs file
        fits = float(self.lala[2, 0])/pitch + 2 - (float(self.lala[2, 0]) / pitch) % 1 #number of ribs required (including ribs at the root and tip
        if (float(self.lala[2, 0]) / pitch) % 1 == 0:
            fits = fits - 1

        for k in range(int(fits)):
            ponts = []
            y0 = (k*pitch-ribthiccness)/float(self.lala[2, 0])
            if k == fits-1:
                y0 = 1-ribthiccness/float(self.lala[2, 0])
            if y0 <= float(self.lala[23, 0]):
                [upperskininnb, lowerskininnb] = airfoilinterpolater(0, 1, float(self.lala[3, 0]), mid_AF_chord, 0,
                                                                     float(self.lala[23, 0]) / 100,
                                                                     y0, float(self.lala[7, 0]) / 100,
                                                                     float(self.lala[8, 0]) / 100)
            else:
                [upperskininnb, lowerskininnb] = airfoilinterpolater(1, 2, mid_AF_chord,
                                                                     float(self.lala[3, 0]) * float(self.lala[4, 0]),
                                                                     float(self.lala[23, 0]) / 100,
                                                                     1, y0, float(self.lala[7, 0]) / 100,
                                                                     float(self.lala[8, 0]) / 100)
            #########calculate leading edge coordinates at the specified span position
            xinn = (x_root_AF * (2 - y0 * 2) + x_tip_AF * 2 * y0) / 2
            zinn = (z_root_AF * (2 - y0 * 2) + z_tip_AF * 2 * y0) / 2

            #########put all coordinates in Point form in an array
            for i in range(2):
                row = []
                if i == 0:
                    for j in range(len(upperskininnb)):
                        pt = Point(upperskininnb[j, 1] + xinn, y0 * float(self.lala[2, 0]),
                                   upperskininnb[j, 0] + zinn)
                        row.append((pt))
                    for j in range(len(upperskininnb)):
                        pt = Point(lowerskininnb[-(j + 1), 1] + xinn, y0 * float(self.lala[2, 0]),
                                   lowerskininnb[-(j + 1), 0] + zinn)
                        row.append((pt))
                if i == 1:
                    for j in range(len(upperskininnb)):
                        pt = Point(upperskininnb[j, 1] + xinn, y0 * float(self.lala[2, 0]) +ribthiccness,
                                   upperskininnb[j, 0] + zinn)
                        row.append((pt))
                    for j in range(len(upperskininnb)):
                        pt = Point(lowerskininnb[-(j + 1), 1] + xinn, y0 * float(self.lala[2, 0]) +ribthiccness,
                                   lowerskininnb[-(j + 1), 0] + zinn)
                        row.append((pt))
                ponts.append(row)
            a = Polygon(points=ponts[0])
            b = Polygon(points=ponts[1])
            proffile.append(a)
            proffile.append(b)
        return proffile

    @Part
    def ribs_solidsss(self):
        #########make all the ribs, using the defined coordinates and sizes
        return RuledSolid(quantify=int(len(self.ribs_attribute)/2),
                          profile1=self.ribs_attribute[(child.index)*2],
                          profile2=self.ribs_attribute[(child.index)*2+1])
    @Part
    def ribs_solids(self):
        #########make the inner skin with its many sections, to be used for thick skin generation
        return SubtractedSolid(shape_in=self.ribs_attribute,tool=self.thiccskin_notmany)


if __name__ == '__main__':
    from parapy.gui import display

    obj1 = Wingbox(label="staircase")

    display(obj1)












