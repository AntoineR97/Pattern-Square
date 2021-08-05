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
        if i!=k1 and i!=k2 and i!=k3 and i!=k4 and i!=k5 and i!=k6:
            w.append(i)

    for v[k1] in [0, 1]:
        for v[k2] in [0, 1]:
            for v[k3] in [0, 1]:
                for v[k4] in [0, 1]:
                    for v[k5] in [0, 1]:
                        for v[k6] in [0, 1]:
                            p[v[k1]][v[k2]][v[k3]][v[k4]][v[k5]][v[k6]] = \
                            Or([P[v[0]][v[1]][v[2]][v[3]][v[4]][v[5]]\
                            [v[6]][v[7]][v[8]][v[9]][v[10]][v[11]]\
                            for v[w[0]] in [0, 1] for v[w[1]] in [0, 1]\
                            for v[w[2]] in [0, 1] for v[w[3]] in [0, 1]\
                            for v[w[4]] in [0, 1] for v[w[5]] in [0, 1]])
    return p

def marginal9(k1, k2, k3, k4, k5, k6, k7, k8, k9, v, P):
    w = []
    p = tensor([False for i in range(2**9)])

    for i in range(len(v)):
        if i!=k1 and i!=k2 and i!=k3 and i!=k4 and i!=k5 and i!=k6 and i!=k7 and i!=k8 and i!=k9:
            w.append(i)

    for v[k1] in [0, 1]:
        for v[k2] in [0, 1]:
            for v[k3] in [0, 1]:
                for v[k4] in [0, 1]:
                    for v[k5] in [0, 1]:
                        for v[k6] in [0, 1]:
                            for v[k7] in [0, 1]:
                                for v[k8] in [0, 1]:
                                    for v[k9] in [0, 1]:
                                        p[v[k1]][v[k2]][v[k3]][v[k4]][v[k5]][v[k6]][v[k7]][v[k8]][v[k9]] = \
                                        Or([P[v[0]][v[1]][v[2]][v[3]][v[4]][v[5]]\
                                        [v[6]][v[7]][v[8]][v[9]][v[10]][v[11]]\
                                        for v[w[0]] in [0, 1] for v[w[1]] in [0, 1]\
                                        for v[w[2]] in [0, 1]])
    return p

def compatibilityRing12(pattern):
    s = Solver()
    a1, b1, c1, d1, a2, b2, c2, d2, a3, b3, c3, d3 = Ints('a1 b1 c1 d1 a2 b2 c2 d2 a3 b3 c3 d3')
    v = [a1, b1, c1, d1, a2, b2, c2, d2, a3, b3, c3, d3]
    Pobs = observedDistr(pattern)
    Pabc = Pobs.marginal3([0,1,2])
    Pbcd = Pobs.marginal3([1,2,3])
    Pacd = Pobs.marginal3([0,2,3])
    Pabd = Pobs.marginal3([0,1,3])

    p = Array('p', Z, B)
    inter = []
    for i in range(2**12):
        inter.append(Select(p, i))
    P = tensor(inter)

    Pa1b1c1b2c2d2 = marginal6(0,1,2,5,6,7,v,P)
    Pa1b1c1a3c2d2 = marginal6(0,1,2,8,6,7,v,P)
    Pa1b1c1a3b3d2 = marginal6(0,1,2,8,9,7,v,P)
    Pb1c1d1a3c2d2 = marginal6(1,2,3,8,6,7,v,P)
    Pb1c1d1a3b3d2 = marginal6(1,2,3,8,9,7,v,P)
    Pb1c1d1a3b3c3 = marginal6(1,2,3,8,9,10,v,P)
    Pa2c1d1a3b3d2 = marginal6(4,2,3,8,9,7,v,P)
    Pa2c1d1a3b3c3 = marginal6(4,2,3,8,9,10,v,P)
    Pa2c1d1b3c3d3 = marginal6(4,2,3,9,10,11,v,P)
    Pa2b2d1a3b3c3 = marginal6(4,5,3,8,9,10,v,P)
    Pa2b2d1b3c3d3 = marginal6(4,5,3,9,10,11,v,P)
    Pa2b2d1a1c3d3 = marginal6(4,5,3,0,10,11,v,P)

    for x1 in [0, 1]:
        for x2 in [0, 1]:
            for x3 in [0, 1]:
                for x4 in [0, 1]:
                    for x5 in [0, 1]:
                        for x6 in [0, 1]:
                            s.add(Pa1b1c1b2c2d2[x1][x2][x3][x4][x5][x6]==And(Pabc[x1][x2][x3],Pbcd[x4][x5][x6]))
                            s.add(Pa1b1c1a3c2d2[x1][x2][x3][x4][x5][x6]==And(Pabc[x1][x2][x3],Pacd[x4][x5][x6]))
                            s.add(Pa1b1c1a3b3d2[x1][x2][x3][x4][x5][x6]==And(Pabc[x1][x2][x3],Pabd[x4][x5][x6]))
                            s.add(Pb1c1d1a3c2d2[x1][x2][x3][x4][x5][x6]==And(Pbcd[x1][x2][x3],Pacd[x4][x5][x6]))
                            s.add(Pb1c1d1a3b3d2[x1][x2][x3][x4][x5][x6]==And(Pbcd[x1][x2][x3],Pabd[x4][x5][x6]))
                            s.add(Pb1c1d1a3b3c3[x1][x2][x3][x4][x5][x6]==And(Pbcd[x1][x2][x3],Pabc[x4][x5][x6]))
                            s.add(Pa2c1d1a3b3d2[x1][x2][x3][x4][x5][x6]==And(Pacd[x1][x2][x3],Pabd[x4][x5][x6]))
                            s.add(Pa2c1d1a3b3c3[x1][x2][x3][x4][x5][x6]==And(Pacd[x1][x2][x3],Pabc[x4][x5][x6]))
                            s.add(Pa2c1d1b3c3d3[x1][x2][x3][x4][x5][x6]==And(Pacd[x1][x2][x3],Pbcd[x4][x5][x6]))
                            s.add(Pa2b2d1a3b3c3[x1][x2][x3][x4][x5][x6]==And(Pabd[x1][x2][x3],Pabc[x4][x5][x6]))
                            s.add(Pa2b2d1b3c3d3[x1][x2][x3][x4][x5][x6]==And(Pabd[x1][x2][x3],Pbcd[x4][x5][x6]))
                            s.add(Pa2b2d1a1c3d3[x1][x2][x3][x4][x5][x6]==And(Pabd[x1][x2][x3],Pacd[x4][x5][x6]))

    Pa1b1c1a2b2c2a3b3c3 = marginal9(0,1,2,4,5,6,8,9,10, v, P)
    Pb1c1d1b2c2d2b3c3d3 = marginal9(1,2,3,5,6,7,9,10,11, v, P)
    Pc1d1a2c2d2a3c3d3a1 = marginal9(2,3,4,6,7,8,10,11,0, v, P)
    Pd1a2b2d2a3b3d3a1b1 = marginal9(3,4,5,7,8,9,11,0,1, v, P)

    for x1 in [0, 1]:
        for y1 in [0, 1]:
            for z1 in [0, 1]:
                for x2 in [0, 1]:
                    for y2 in [0, 1]:
                        for z2 in [0, 1]:
                            for x3 in [0, 1]:
                                for y3 in [0, 1]:
                                    for z3 in [0, 1]:
                                        s.add(Pa1b1c1a2b2c2a3b3c3[x1][y1][z1][x2][y2][z2][x3][y3][z3]\
                                        == And(Pabc[x1][y1][z1], Pabc[x2][y2][z2], Pabc[x3][y3][z3]))

                                        s.add(Pb1c1d1b2c2d2b3c3d3[x1][y1][z1][x2][y2][z2][x3][y3][z3]\
                                        == And(Pbcd[x1][y1][z1], Pbcd[x2][y2][z2], Pbcd[x3][y3][z3]))

                                        s.add(Pc1d1a2c2d2a3c3d3a1[x1][y1][z1][x2][y2][z2][x3][y3][z3]\
                                        == And(Pacd[x1][y1][z1], Pacd[x2][y2][z2], Pacd[x3][y3][z3]))

                                        s.add(Pd1a2b2d2a3b3d3a1b1[x1][y1][z1][x2][y2][z2][x3][y3][z3]\
                                        == And(Pabd[x1][y1][z1], Pabd[x2][y2][z2], Pabd[x3][y3][z3]))

    return s.check()
