import numpy as np
import scipy as sc
from Airfoilcoordiantesgenerator import *
import matplotlib.pyplot as plt

def airfoilinterpolater(airfoil1,airfoil2,chord1,chord2,y1,y2,y,frontspar,rearspar):
    #########open CST coeffs file and read data
    g = open("CSTs.dat", "r")
    lines = g.read().split(' ')
    CSTcoefs = list(np.float_(lines))
    #########resolution along the chord of the airfoil coordinates
    res = 21
    #########make empty arrays
    upperskin1 = np.zeros((res,2))
    lowerskin1 = np.zeros((res,2))
    upperskin2 = np.zeros((res,2))
    lowerskin2 = np.zeros((res,2))
    xx = np.zeros(res)
    #########calculate increments
    dist = (rearspar-frontspar)/(res-1)
    ydist = y2 - y1
    ything = (y-y1)/ydist

    #########this is to change the index such that the correct CST coeffs are taken so that the correct airfoils are interpolated
    if airfoil1 == 0:
        j = 0
    if airfoil2 == 2:
        j = 12
    else:
        j=0

    #########calculate all x and z coordinates along the chord
    for i in range(res):
        x = frontspar+dist*i
        xx[i] = x
        [up1, low1] = (Airfoilcoordinates(CSTcoefs[0 + j:6 + j], CSTcoefs[6 + j:12 + j], x))
        [up2, low2] = (Airfoilcoordinates(CSTcoefs[12 + j:18 + j], CSTcoefs[18 + j:24 + j],x))
        upperskin1[i] = up1,x
        lowerskin1[i] = low1,x
        upperskin2[i] = up2,x
        lowerskin2[i] = low2,x

    #########scale the generated airfoil
    upperskin = (upperskin1*chord1*(2-ything*2)+upperskin2*chord2*2*ything)/2
    lowerskin = (lowerskin1*chord1 * (2 - ything * 2) + lowerskin2*chord2 * 2 * ything) / 2

    return upperskin,lowerskin
'''
##############TEST###############
airfoil1="mid"
airfoil2="tip"
chord1=3.5
chord2=2.5
y1=0
y2=0.5
y=0.1
frontspar=0.25
rearspar=0.6
[upperskin,lowerskin]=airfoilinterpolater(airfoil1,airfoil2,chord1,chord2,y1,y2,y,frontspar,rearspar)
print(upperskin)
'''

