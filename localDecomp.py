# -*- coding: utf-8 -*-
from z3 import *
from tools import *
import numpy as np

B = BoolSort()
Z = IntSort()

def localDecomp(pattern, C):
    Pa = Function('Pa', Z, Z, Z, B)
    Pb = Function('Pb', Z, Z, Z, B)
    Pc = Function('Pc', Z, Z, Z, B)
    Pd = Function('Pd', Z, Z, Z, B)

    alpha, beta, gamma, delta = Ints('alpha beta gamma delta')
    a, b, c, d = Ints('a b c d')

    P = tensor(pattern)
    s = Solver()

    for delta in range(C):
        for alpha in range(C):
            s.add(Or(Pa(0,delta,alpha), Pa(1,delta,alpha)))
    for alpha in range(C):
        for beta in range(C):
            s.add(Or(Pb(0,alpha,beta), Pb(1,alpha,beta)))
    for beta in range(C):
        for gamma in range(C):
            s.add(Or(Pc(0,beta,gamma), Pc(1,beta,gamma)))
    for gamma in range(C):
        for delta in range(C):
            s.add(Or(Pd(0,gamma,delta), Pd(1,gamma,delta)))

    for a in [0, 1]:
        for b in [0, 1]:
            for c in [0, 1]:
                for d in [0, 1]:
                    Pabcd = Or([And(Pa(a,delta,alpha), Pb(b,alpha,beta),\
                    Pc(c,beta,gamma), Pd(d,gamma,delta))\
                    for alpha in range(C) for beta in range(C)\
                    for gamma in range(C) for delta in range(C)])

                    if P[a][b][c][d]:
                        s.add(Pabcd)
                    else:
                        s.add(Not(Pabcd))

                    if s.check() == unsat:
                        break
    return s.check()
