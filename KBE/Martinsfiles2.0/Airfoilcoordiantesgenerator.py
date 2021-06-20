import numpy as np

def Airfoilcoordinates(CSTupper,CSTlower,x):
    N1u = 0.5
    N2u = 1
    N1l = 0.5
    N2l = 1
    Cu = x ** N1u * (1 - x) ** N2u
    Cl = (x ** N1l * (1 - x) ** N2l)

    b05 = (1 - x) ** 5
    b15 = 5 * x * ((1 - x) ** 4)
    b25 = 10 * (x ** 2) * ((1 - x) ** 3)
    b35 = 10 * (x ** 3) * ((1 - x) ** 2)
    b45 = 5 * (x ** 4) * (1 - x)
    b55 = x ** 5

    Scu = CSTupper[0] * b05 + CSTupper[1] * b15 + CSTupper[2] * b25 + CSTupper[3] * b35 + CSTupper[4] * b45 + CSTupper[5] * b55
    Scl = CSTlower[0] * b05 + CSTlower[1] * b15 + CSTlower[2] * b25 + CSTlower[3] * b35 + CSTlower[4] * b45 + CSTlower[5] * b55

    AFu = Cu * Scu
    AFl = Cl * Scl
    return AFu, AFl

'''
def Airfoilcoordinates(CSTlower,CSTupper,AFresolution):


    N1u = 0.5
    N2u = 1
    N1l = 0.5
    N2l = 1
    n = 1
    step = 1 / AFresolution
    #eta = np.array(0,n,step)#:step: n)
    #eta = np.array(list(range(0, n, step)))  #:step: n)
    eta = np.arange(0,n,step)
    etaa = (1 - eta)
    Cu = np.zeros(len(eta))
    Cl = np.zeros(len(eta))
    for i in range(len(eta)):
        Cu[i] = eta[i] ** N1u * (1 - eta[i]) ** N2u
        Cl[i] = (eta[i] ** N1l * (1 - eta[i]) ** N2l)

    b05 = np.zeros(len(eta))
    b15 = np.zeros(len(eta))
    b25 = np.zeros(len(eta))
    b35 = np.zeros(len(eta))
    b45 = np.zeros(len(eta))
    b55 = np.zeros(len(eta))
    for i in range(len(eta)):
        b05[i] = (1 - eta[i]) ** 5
        b15[i] = 5 * eta[i] * ((1 - eta[i]) ** 4)
        b25[i] = 10 * (eta[i] ** 2) * ((1 - eta[i]) ** 3)
        b35[i] = 10 * (eta[i] ** 3) * ((1 - eta[i]) ** 2)
        b45[i] = 5 * (eta[i] ** 4) * (1 - eta[i])
        b55[i] = eta[i] ** 5

    Scu = CSTupper[0] * b05 + CSTupper[1] * b15 + CSTupper[2] * b25 + CSTupper[3] * b35 + CSTupper[4] * b45 + CSTupper[5] * b55
    Scl = CSTlower[0] * b05 + CSTlower[1] * b15 + CSTlower[2] * b25 + CSTlower[3] * b35 + CSTlower[4] * b45 + CSTlower[5] * b55

    AFu = np.multiply(Cu, Scu)
    AFl = np.multiply(Cl, Scl)

    return AFu, AFl


###########TEST############
CSTupper = [1, 1, 1, 1, 1, 1]
CSTlower = [1, 1, 1, 1, 1, 1]
AFresolution = 10

AFuu, AFll = Airfoilcoordinates(CSTlower,CSTupper,AFresolution)
print(AFuu)
print(AFll)
'''





