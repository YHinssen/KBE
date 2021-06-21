import numpy as np

def Airfoilcoordinates(CSTupper,CSTlower,x):
    ############ this file uses the CST-coefficients method, with bezier curves and ......
    ########setting some coefficients
    N1u = 0.5
    N2u = 1
    N1l = 0.5
    N2l = 1
    ########calculating the ...... equation/part at given x
    Cu = x ** N1u * (1 - x) ** N2u
    Cl = (x ** N1l * (1 - x) ** N2l)

    ########calculating the ...... equation/part/curves at given x
    b05 = (1 - x) ** 5
    b15 = 5 * x * ((1 - x) ** 4)
    b25 = 10 * (x ** 2) * ((1 - x) ** 3)
    b35 = 10 * (x ** 3) * ((1 - x) ** 2)
    b45 = 5 * (x ** 4) * (1 - x)
    b55 = x ** 5

    ########multiplying the equation/part/curves with the CST-coefficients
    Scu = CSTupper[0] * b05 + CSTupper[1] * b15 + CSTupper[2] * b25 + CSTupper[3] * b35 + CSTupper[4] * b45 + CSTupper[5] * b55
    Scl = CSTlower[0] * b05 + CSTlower[1] * b15 + CSTlower[2] * b25 + CSTlower[3] * b35 + CSTlower[4] * b45 + CSTlower[5] * b55

    ########obtaining the final airfoil coordinate, for upper and lower surface
    AFu = Cu * Scu
    AFl = Cl * Scl
    return AFu, AFl

'''
###########TEST############
CSTupper = [1, 1, 1, 1, 1, 1]
CSTlower = [1, 1, 1, 1, 1, 1]
AFresolution = 10

AFuu, AFll = Airfoilcoordinates(CSTlower,CSTupper,AFresolution)
print(AFuu)
print(AFll)
'''





