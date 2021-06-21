#This file uses the geometry and parameters obtained to perform performance calculations on the aircraft
# Using theory from Aircraft Performance courses, the battery density, efficiency and number,
# power calculations can be performed and an idea of the vehicles performance can be obtaiend.

from math import *
import numpy as np
import matplotlib.pyplot as plt
import scipy.integrate as integrate

##---------------------## Power Curve Inputs--------------------------##

wing_area = Input(5.06)  ##From Pablo
wing_aspect_ratio = Input(6)  ##From Pablo
rho = 1.0739  ##At cruise level
# V_inf = 44
CD0 = Input(0.6) ##From ADSEE
MTOM = 168.2  ##First estimate                                                        #Change
MTOW = MTOM * 9.81
e = 0.78  ##From ADSEE

##--------------------## ROC Inputs-----------------------------------##

P_engine = Input(36800)
n_engines = Input(2)
eta_propeller = 0.85  ##From Book
eta_propulsive = 0.85
V_cruise = 48.3  ##m/s

##---------------------##Powers and times-------------------------------##
P_a = n_engines * P_engine * eta_propeller * eta_propulsive
Pr_cruise = 27  ##kW from calculation down below

##-----------------------## Battery inputs ---------------------------##
Batt_E = 250  ##Wh/kg

##---------------------## Code ---------------------------------------##

##The cruisepower function constructs the power curves and finds the maximum available power for climb and descent.
##The power for transition and hover comsed form the theoretical power calculations

def Cruisepower():
    V_inf = np.arange(5, 80, 0.001)
    Pr = (0.5 * rho * V_inf ** 3 * wing_area * CD0 + (
                (MTOW ** 2 / (0.5 * rho * V_inf * wing_area)) / (pi * e * wing_aspect_ratio))) / eta_propulsive
    Pr0 = 0.5 * rho * V_inf ** 3 * wing_area * CD0
    PrL = (MTOW ** 2 / (0.5 * rho * V_inf * wing_area)) / (pi * e * wing_aspect_ratio)
    P_cruise = np.interp(V_cruise, V_inf, Pr)
    P_cruise_del = np.interp(V_cruise_del, V_inf, Pr)
    P_cruise_log = np.interp(V_cruise_log, V_inf, Pr)
    P_min = np.min(Pr)
    V_minP = V_inf[np.where(Pr == P_min)]
    # print("test", V_minP) This was just to test
    return P_cruise, P_min, V_minP, P_cruise_del, P_cruise_log, Pr, Pr0, PrL, V_inf

def TotalEnergy():
    t_cruise = E_tot / P_a
    return t_cruise


