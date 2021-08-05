import sys
import os
sys.path.insert(0, '/Users/antoinerestivo/usr/lib/python-2.7/site-packages')
from z3 import *
from tools import *
from observedDistribution import *

B = BoolSort()
Z = IntSort()

def marginal6(k1, k2, k3, k4, k5, k6, v, P):
    w = []
    p = tensor([False for i in range(2**6)])

    for i in range(len(v)):
        if i!=k1 and i!=k2 and i!=k3 and i!= k4 and i!=k5 and i!=k6:
            w.append(i)

    for v[k1] in [0, 1]:
        for v[k2] in [0, 1]:
            for v[k2] in [0, 1]:
                for v[k3] in [0, 1]:
                    for v[k4] in [0, 1]:
                        for v[k5] in [0, 1]:
                            for v[k6] in [0, 1]:
                                p[v[k1]][v[k2]][v[k3]][v[k4]][v[k5]][v[k6]] = \
                                Or([P[v[0]][v[1]][v[2]][v[3]][v[4]][v[5]][v[6]]\
                                [v[7]]\
                                for v[w[0]] in [0, 1] for v[w[1]] in [0, 1]])
    return p

def compatibilityRing8(pattern):
    s = Solver()
    a1, b1, c1, d1, a2, b2, c2, d2 = Ints('a1 b1 c1 d1 a2 b2 c2 d2')
    v = [a1, b1, c1, d1, a2, b2, c2, d2]
    Pobs = observedDistr(pattern)
    Pabc = Pobs.marginal3([0,1,2])
    Pbcd = Pobs.marginal3([1,2,3])
    Pabd = Pobs.marginal3([0,1,3])
    Pacd = Pobs.marginal3([0,2,3])

    p = Array('p', Z, B)
    inter = []
    for i in range(2**8):
        inter.append(Select(p, i))
    P = tensor(inter)

    Pa1b1c1a2b2c2 = marginal6(0,1,2,4,5,6, v, P)
    Pb1c1d1b2c2d2 = marginal6(1,2,3,5,6,7, v, P)
    Pc1d1a2c2d2a1 = marginal6(2,3,4,6,7,0, v, P)
    Pd1a2b2d2a1b1 = marginal6(3,4,5,7,0,1, v, P)

    for x1 in [0, 1]:
        for x2 in [0, 1]:
            for x3 in [0, 1]:
                for x4 in [0, 1]:
                    for x5 in [0, 1]:
                        for x6 in [0, 1]:
                            s.add(Pa1b1c1a2b2c2[x1][x2][x3][x4][x5][x6] == And(Pabc[x1][x2][x3], Pabc[x4][x5][x6]))
                            s.add(Pb1c1d1b2c2d2[x1][x2][x3][x4][x5][x6] == And(Pbcd[x1][x2][x3], Pbcd[x4][x5][x6]))
                            s.add(Pc1d1a2c2d2a1[x1][x2][x3][x4][x5][x6] == And(Pacd[x3][x1][x2], Pacd[x6][x4][x5]))
                            s.add(Pd1a2b2d2a1b1[x1][x2][x3][x4][x5][x6] == And(Pabd[x2][x3][x1], Pabd[x5][x6][x4]))

    return s.check()
