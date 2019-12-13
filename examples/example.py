"""
Title: example for using GasCalc
Date: Oct. 2019
Author: Jared J. Thomas
"""

import numpy as np

import gascalc.api as gc

if __name__ == "__main__":

    # provide known properties
    gamma = 1.4     #
    T = 300.0       # K
    R = 287.0       # J/(kg*K)
    M = 2.0         # Mach number
    Pa = 200.0      # kPa

    # create instance of gas table
    table = gc.GasTables()

    # pass known properties to isentropic flow tables
    table.isent('M', gamma, M)

    # retrieve desired property from table state
    ppa = table.state.pp0
    P = ppa*Pa
    print('P = %.2f kPa' % (P))

    # pass known properties to normal shock tables
    table.nsr('M1', gamma, M)

    # retrieve desired property from table state
    M2 = table.state.m2
    print('M2 = %.2f' % (M2))

    # calculate max turning angle for oblique shock
    theta_max = gc.max_shock_angle(gamma, M)
    print('Max shock angle = %.2f deg' % (theta_max*180./np.pi))

    # calculate max deflection angle for oblique shock
    delta_max = gc.max_deflection_angle(gamma, M)
    print('Max deflection angle = %.2f deg' % (delta_max*180./np.pi))
