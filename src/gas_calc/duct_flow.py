import numpy as np
from scipy.optimize import newton


def solve_fm1(m1, gamma, fld, fldi, flde):

    fm1 = fld + flde - fldi

    gp1 = gamma + 1.
    gm1 = gamma - 1.

    a = gp1/gamma
    b = np.log((2.+gm1*m1**2)/(gp1*m1**2))
    c = 2.*(1.+gamma*m1**2)*(m1**2-1.)
    d = (gamma*m1**2)*(2.+gm1*m1**2)

    f = a*b + c/d

    return f - fm1

def solve_for_m1(gamma, fld, fldi, flde, m1_guess=1.7):

    m1 = newton(solve_fm1, m1_guess, args=[gamma, fld, fldi, flde], maxiter=100)

    return m1


if __name__ == "__main__":


    # prob 9.15 a

    gamma = 1.4

    fld = 0.5
    fldi = 0.36018
    flde = 0.

    m1 = solve_for_m1(gamma, fld, fldi, flde)

    print(np.round(m1,4))

    # prob 9.15 b

    flde = 0.1136

    m1 = solve_for_m1(gamma, fld, fldi, flde)

    print(np.round(m1, 4))
