"""
Title: Oblique Shocks
Description: relationships useful when dealing with oblique shocks
Date: 2019
Author: Jared J. Thomas
"""

import numpy as np

def max_deflection_angle(gamma, m1, theta_max=None):
    # from Gas Dynamics by John Keith, eq. 6.18

    if theta_max == None:
        theta_max = max_shock_angle(gamma, m1)

    a = m1**2*np.sin(theta_max)**2-1.
    b = ((gamma+1)/2.)*m1**2 - (m1**2*np.sin(theta_max)**2-1.)
    c = 1./np.tan(theta_max)
    delta_max = np.arctan(c*(a/b))

    return delta_max

def max_shock_angle(gamma, m1):
    # from Gas Dynamics by John Keith, eq. 6.24

    gp1 = gamma+1.
    gm1 = gamma-1.
    a = 1./(gamma*m1**2)
    b = (gp1/4.)*m1**2-1.
    c = np.sqrt(gp1*(gp1*m1**4/16.+gm1*m1**2/2.+1.))

    theta_max = np.arcsin(np.sqrt(a*(b+c)))

    return theta_max


if __name__ == "__main__":
    gamma = 1.4
    M = 2.0
    theta_max = max_deflection_angle(gamma, M)
    print('Max turning angle = %.2f deg' % (theta_max*180./np.pi))
