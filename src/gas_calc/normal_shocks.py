import numpy as np

def reflected_shock_velocity(a, v, vp=0., gamma=1.4):

    gp1 = gamma + 1.

    a = gp1/4.
    b = v+vp

    sr = a*b+np.sqrt((a*b)**2+a**2)

    return sr

def reflected_p3_over_p2(sr, v, a2, gamma=1.4):

    gm1 = gamma-1.
    gp1 = gamma+1.
    a = 2.*gamma/gp1
    b = (sr+v)/a2
    p3p2 = a*b**2-gm1/gp1

    return p3p2

if __name__ == "__main__":

    v = 741.097
    a = 548.059
    vp = 10.
    gamma = 1.4

    sr = reflected_shock_velocity(a, v, vp, gamma)

    print(sr)

    a2 = 548.059
    p3p2 = reflected_p3_over_p2(sr, v, a2, gamma)

    print('p3/p2: ', p3p2)

    