"""
Title: Flow Property Calculator
Date: 2019
Author: Jared Thomas and Teagan Nakamoto
"""

import numpy as np

# Define viriginia tech calcs in python (converted by Teagan N.) - yes, I need to just turn this into a package
class State():
    def __init__(self):
        init = True


class GasTables():

    def __init__(self):

        self.init = True

        self.state = State()

    ############.  " Little Functions "

    def aas_calc(self, g, m):
        return 1. / self.rrs_calc(g, m) * np.sqrt(1. / self.tts_calc(g, m)) / m

    def nu(self, g, m):
        n = np.sqrt((g + 1.) / (g - 1.)) * np.arctan(np.sqrt((g - 1.) / (g + 1.) * (m * m - 1.)))
        n = n - np.arctan(np.sqrt(m * m - 1.))
        n = n * 180. / 3.14159265359
        return n

    def tts_calc(self, g, m):
        return self.tt0_calc(g, m) * (g / 2. + .5)

    def pps_calc(self, g, m):
        return self.pp0_calc(g, m) * ((g / 2. + .5) ** (g / (g - 1.)))

    def rrs_calc(self, g, m):
        return self.rr0_calc(g, m) * ((g / 2. + .5) ** (1. / (g - 1.)))

    def tt0_calc(self, g, m):
        return ((1. + (g - 1.) / 2. * m * m) ** (-1.))

    def pp0_calc(self, g, m):
        return ((1. + (g - 1.) / 2. * m * m) ** (-g / (g - 1.)))

    def rr0_calc(self, g, m):
        return ((1. + (g - 1.) / 2. * m * m) ** (-1. / (g - 1.)))

    def m2_calc(self, g, m1):
        return np.sqrt((1. + .5 * (g - 1.) * m1 * m1) / (g * m1 * m1 - .5 * (g - 1.)))

    ###############. " ISENTROPIC FLOW CALCULATOR "
    def isent(self, i, g, v):
        # i is choice of variable
        # g is value of gamma
        # v is value of variable choice
        if i == "M":
            i = 0
        elif i == "t/t0":
            i = 1
        elif i == "p/p0":
            i = 2
        elif i == "r/r0":
            i = 3
        elif i == "a/a*Sub":
            i = 4
        elif i == "a/a*Super":
            i = 5
        elif i == "MachAngle":
            i = 6
        elif i == "P-MAngle":
            i = 7
        else:
            raise Exception("Invalid input")

        if (g <= 1.0):
            raise Exception("gamma must be greater than 1")

        if (i == 1):
            if (v >= 1.0 or v <= 0.0):
                raise Exception("T/T0 must be between 0 and 1")
            m = np.sqrt(2. * ((1. / v) - 1.) / (g - 1.))

        elif (i == 2):
            if (v >= 1.0 or v <= 0.0):
                raise Exception("p/p0 must be between 0 and 1")
            m = np.sqrt(2. * ((1. / (v ** ((g - 1.) / g))) - 1.) / (g - 1.))

        elif (i == 3):
            if (v >= 1.0 or v <= 0.0):
                raise Exception("rho/rho0 must be between 0 and 1")
            m = np.sqrt(2. * ((1. / (v ** (g - 1.))) - 1.) / (g - 1.))

        elif (i == 4 or i == 5):
            if (v <= 1.0):
                raise Exception("A/A* must be greater than 1")
            mnew = 0.00001
            m = 0.0
            if (i == 5):
                mnew = 2.
            while (np.absolute(mnew - m) > 0.000001):
                m = mnew
                phi = self.aas_calc(g, m)
                s = (3. - g) / (1. + g)
                mnew = m - (phi - v) / (((phi * m) ** s) - phi / m)
        elif (i == 6):
            if (v <= 0.0 or v >= 90.0):
                raise Exception("Mach angle must be between 0 and 90")
            m = 1. / np.sin(v * 3.14159265359 / 180.)
        elif (i == 7):
            numax = (np.sqrt((g + 1.) / (g - 1.)) - 1) * 90.
            if (v <= 0.0 or v >= numax):
                raise Exception("Prandtl-Meyer angle must be between 0 and ", numax)
            mnew = 2.0
            m = 0.0
            while (np.absolute(mnew - m) > 0.00001):
                m = mnew
                fm = (self.nu(g, m) - v) * 3.14159265359 / 180.
                fdm = np.sqrt(m * m - 1.) / (1 + 0.5 * (g - 1.) * m * m) / m
                mnew = m - fm / fdm
        else:
            if (v <= 0.0):
                raise Exception("M must be greater than 0")
            m = v

        if (m > 1.):
            mu = np.arcsin(1. / m) * 180 / 3.14159265359
            nu = self.nu(g, m)
        elif (m == 1):
            mu = 90.
            nu = 0.
        else:
            mu = None
            nu = None
        tt0 = self.tt0_calc(g, m)
        pp0 = self.pp0_calc(g, m)
        rr0 = self.rr0_calc(g, m)
        tts = self.tts_calc(g, m)
        pps = self.pps_calc(g, m)
        rrs = self.rrs_calc(g, m)
        aas = self.aas_calc(g, m)

        self.state.m = m
        self.state.mu = mu
        self.state.nu = nu
        self.state.pp0 = pp0
        self.state.tt0 = tt0
        self.state.pps = pps
        self.state.tts = tts
        self.state.aas = aas

        return [m, mu, nu, pp0, rr0, tt0, pps, rrs, tts, aas]

    ############ " Normal shock relations "
    def nsr(self, i, g, v):
        # i is choice of variable
        # g is value of gamma
        # v is value of variable choice
        if i == "M1":
            i = 0
        elif i == "M2":
            i = 1
        elif i == "p2/p1":
            i = 2
        elif i == "r2/r1":
            i = 3
        elif i == "t2/t1":
            i = 4
        elif i == "p02/p01":
            i = 5
        elif i == "p1/p02":
            i = 6
        else:
            raise Exception("Invalid input")

        if (g <= 1.0):
            raise Exception("gamma must be greater than 1")

        if (i == 1):
            if (v >= 1.0 or v <= np.sqrt((g - 1.) / 2. / g)):
                raise Exception("M2 must be between ", np.sqrt((g - 1.) / 2. / g), " and 1")
            m1 = self.m2_calc(g, v)

        elif (i == 2):
            if (v <= 1.0):
                raise Exception("p2/p1 must be greater than 1")
            m1 = np.sqrt((v - 1.) * (g + 1.) / 2. / g + 1.)

        elif (i == 3):
            if (v <= 1.0 or v >= (g + 1.) / (g - 1.)):
                raise Exception("rho2/rho1 must be between 1 and ", ((g + 1.) / (g - 1.)))
            m1 = np.sqrt(2. * v / (g + 1. - v * (g - 1.)))

        elif (i == 4):
            if (v <= 1.0):
                raise Exception("T2/T1 must be greater than 1")
            aa = 2. * g * (g - 1.)
            bb = 4. * g - (g - 1.) * (g - 1.) - v * (g + 1.) * (g + 1.)
            cc = -2. * (g - 1.)
            m1 = np.sqrt((-bb + np.sqrt(bb * bb - 4. * aa * cc)) / 2. / aa)

        elif (i == 5):
            if (v >= 1.0 or v <= 0.0):
                raise Exception("p02/p01 must be between 0 and 1")
            mnew = 2.0
            m1 = 0.0
            while (np.absolute(mnew - m1) > 0.00001):
                m1 = mnew
                al = (g + 1.) * m1 * m1 / ((g - 1.) * m1 * m1 + 2.)
                be = (g + 1.) / (2. * g * m1 * m1 - (g - 1.))
                daldm1 = (2. / m1 - 2. * m1 * (g - 1.) / ((g - 1.) * m1 * m1 + 2.)) * al
                dbedm1 = -4. * g * m1 * be / (2. * g * m1 * m1 - (g - 1.))
                fm = np.power(al, g / (g - 1.)) * np.power(be, 1. / (g - 1.)) - v
                fdm = g / (g - 1.) * np.power(al, 1 / (g - 1.)) * daldm1 * np.power(be, 1. / (g - 1.)) + np.power(al,
                                                                                                                  g / (
                                                                                                                              g - 1.)) / (
                                  g - 1.) * np.power(be, (2. - g) / (g - 1.)) * dbedm1
                mnew = m1 - fm / fdm

        elif (i == 6):
            vmax = np.power((g + 1.) / 2., -g / (g - 1.))
            if (v >= vmax or v <= 0.0):
                raise Exception("p1/p02 must be between 0 and ", vmax)
            mnew = 2.0
            m1 = 0.0
            while (np.absolute(mnew - m1) > 0.00001):
                m1 = mnew
                al = (g + 1.) * m1 * m1 / 2.
                be = (g + 1.) / (2. * g * m1 * m1 - (g - 1.))
                daldm1 = m1 * (g + 1.)
                dbedm1 = -4. * g * m1 * be / (2. * g * m1 * m1 - (g - 1.))
                fm = np.power(al, g / (g - 1.)) * np.power(be, 1. / (g - 1.)) - 1. / v
                fdm = g / (g - 1.) * np.power(al, 1 / (g - 1.)) * daldm1 * np.power(be, 1. / (g - 1.)) + np.power(al,
                                                                                                                  g / (
                                                                                                                              g - 1.)) / (
                                  g - 1.) * np.power(be, (2. - g) / (g - 1.)) * dbedm1
                mnew = m1 - fm / fdm

        else:
            if (v <= 1.0):
                raise Exception("M1 must be greater than 1")
            m1 = v

        m1 = m1
        m2 = self.m2_calc(g, m1)
        p2p1 = 1. + 2. * g / (g + 1.) * (m1 * m1 - 1.)
        p2p1 = p2p1
        p02p01 = self.pp0_calc(g, m1) / self.pp0_calc(g, self.m2_calc(g, m1)) * p2p1
        p02p01 = p02p01
        r2r1 = self.rr0_calc(g, self.m2_calc(g, m1)) / self.rr0_calc(g, m1) * p02p01
        t2t1 = self.tt0_calc(g, self.m2_calc(g, m1)) / self.tt0_calc(g, m1)
        p1p02 = self.pp0_calc(g, m1) / p02p01

        self.state.m1 = m1
        self.state.m2 = m2
        self.state.p02p01 = p02p01
        self.state.p1p02 = p1p02
        self.state.p2p1 = p2p1
        self.state.r2r1 = r2r1
        self.state.t2t1 = t2t1

        return [m1, m2, p02p01, p1p02, p2p1, r2r1, t2t1]