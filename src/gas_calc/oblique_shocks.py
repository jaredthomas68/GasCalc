"""
Title: Oblique Shocks
Description: relationships useful when dealing with oblique shocks
Date: Oct. 2019
Author: Jared J. Thomas
"""

import numpy as np

def max_turning_angle(gamma, m1):

    gp1 = gamma+1.
    gm1 = gamma-1.
    a = 1./(gamma*m1**2)
    b = (gp1/4.)*m1**2-1.
    c = np.sqrt(gp1*(gp1*m1**4/16.+gm1*m1**2/2.+1.))

    theta_max = np.arcsin(a*(b+c))**2

    return theta_max*180./np.pi