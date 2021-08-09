from z3 import *
import numpy as np
from scipy.io import savemat
import time

B = BoolSort()
Z = IntSort()

def tensor(pattern):
    k = len(pattern)

    if k > 2:
        p = [tensor(pattern[0:int(k/2)]), tensor(pattern[int(k/2):k])]
    else:
        p = pattern

    return p

def responseFunc(inter, C):
    p = []
    count = 0
    for output in [0, 1]:
        inter1 = []
        for lhv1 in range(C):
            inter2 = []
            for lhv2 in range(C):
                inter2.append(inter[count])
                count = count+1
            inter1.append(inter2)
        p.append(inter1)
    return p

def localDecomp(pattern, C):
    alpha, beta, gamma, delta = Ints('alpha beta gamma delta')
    a, b, c, d = Ints('a b c d')
    P = tensor(pattern)
    g = Tactic('smt').solver()

    Pa = responseFunc(BoolVector('pA', 2*C**2), C)
    Pb = responseFunc(BoolVector('pB', 2*C**2), C)
    Pc = responseFunc(BoolVector('pC', 2*C**2), C)
    Pd = responseFunc(BoolVector('pD', 2*C**2), C)

    start_time = time.time()

    for delta in range(C):
        for alpha in range(C):
            g.add(Or(Pa[0][delta][alpha], Pa[1][delta][alpha]))
    for alpha in range(C):
        for beta in range(C):
            g.add(Or(Pb[0][alpha][beta], Pb[1][alpha][beta]))
    for beta in range(C):
        for gamma in range(C):
            g.add(Or(Pc[0][beta][gamma], Pc[1][beta][gamma]))
    for gamma in range(C):
        for delta in range(C):
            g.add(Or(Pd[0][gamma][delta], Pd[1][gamma][delta]))

    for a in [0, 1]:
        for b in [0, 1]:
            for c in [0, 1]:
                for d in [0, 1]:
                    Pabcd = Or([And(Pa[a][delta][alpha], Pb[b][alpha][beta],\
                    Pc[c][beta][gamma], Pd[d][gamma][delta])\
                    for alpha in range(C) for beta in range(C)\
                    for gamma in range(C) for delta in range(C)])

                    if P[a][b][c][d]:
                        g.add(Pabcd)
                    else:
                        g.add(Not(Pabcd))

    ans = g.check()
    end_time = time.time()
    print('Running time:', end_time-start_time)
    return ans
