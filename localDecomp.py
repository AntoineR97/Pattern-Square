from z3 import *
from tools import *
import numpy as np
#from scipy.io import savemat
#import multiprocessing
from functools import partial
#import time

B = BoolSort()
Z = IntSort()

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
    #start_time = time.time()
    alpha, beta, gamma, delta = Ints('alpha beta gamma delta')
    a, b, c, d = Ints('a b c d')
    P = tensor(pattern)
    s = Solver()

    pA = Array('pA', Z, B)
    pB = Array('pB', Z, B)
    pC = Array('pC', Z, B)
    pD = Array('pD', Z, B)

    interA = []
    interB = []
    interC = []
    interD = []
    for i in range(2*C**2):
        interA.append(Select(pA, i))
        interB.append(Select(pB, i))
        interC.append(Select(pC, i))
        interD.append(Select(pD, i))

    Pa = responseFunc(interA, C)
    Pb = responseFunc(interB, C)
    Pc = responseFunc(interC, C)
    Pd = responseFunc(interD, C)

    for delta in range(C):
        for alpha in range(C):
            s.add(Or(Pa[0][delta][alpha], Pa[1][delta][alpha]))
    for alpha in range(C):
        for beta in range(C):
            s.add(Or(Pb[0][alpha][beta], Pb[1][alpha][beta]))
    for beta in range(C):
        for gamma in range(C):
            s.add(Or(Pc[0][beta][gamma], Pc[1][beta][gamma]))
    for gamma in range(C):
        for delta in range(C):
            s.add(Or(Pd[0][gamma][delta], Pd[1][gamma][delta]))

    for a in [0, 1]:
        for b in [0, 1]:
            for c in [0, 1]:
                for d in [0, 1]:
                    Pabcd = Or([And(Pa[a][delta][alpha], Pb[b][alpha][beta],\
                    Pc[c][beta][gamma], Pd[d][gamma][delta])\
                    for alpha in range(C) for beta in range(C)\
                    for gamma in range(C) for delta in range(C)])

                    if P[a][b][c][d]:
                        s.add(Pabcd)
                    else:
                        s.add(Not(Pabcd))

                    if s.check() == unsat:
                        break

    #end_time = time.time()
    return s.check()

# def parallelRun(orbit, C):
#     s = []
#     u = []
#     pool_obj = multiprocessing.Pool(processes=1)
#     subFunc = partial(localDecomp, C=C)
#     ans = pool_obj.map(subFunc, (i for i in orbit))
#     return ans
