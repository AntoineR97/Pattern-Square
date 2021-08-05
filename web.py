import sys
import os
sys.path.insert(0, '/Users/antoinerestivo/usr/lib/python-2.7/site-packages')
from z3 import *
from tools import *
from observedDistribution import *
import numpy as np

B = BoolSort()
Z = IntSort()

def marginal5(k1, k2, k3, k4, k5, v, P):
    w = []
    p = tensor([False for i in range(2**5)])

    for i in range(len(v)):
        if i != k1 and i != k2 and i != k3 and i != k4 and i != k5:
            w.append(i)

    for v[k1] in [0, 1]:
        for v[k2] in [0, 1]:
            for v[k3] in [0, 1]:
                for v[k4] in [0, 1]:
                    for v[k5] in [0, 1]:
                        p[v[k1]][v[k2]][v[k3]][v[k4]][v[k5]] = \
                        Or([P[v[0]][v[1]][v[2]][v[3]][v[4]][v[5]][v[6]][v[7]]\
                        [v[8]][v[9]][v[10]][v[11]][v[12]][v[13]][v[14]][v[15]]\
                        for v[w[0]] in [0, 1] for v[w[1]] in [0, 1]\
                        for v[w[2]] in [0, 1] for v[w[3]] in [0, 1]\
                        for v[w[4]] in [0, 1] for v[w[5]] in [0, 1]\
                        for v[w[6]] in [0, 1] for v[w[7]] in [0, 1]\
                        for v[w[8]] in [0, 1] for v[w[9]] in [0, 1]\
                        for v[w[10]] in [0, 1]])
    return p

def marginal8(k1, k2, k3, k4, k5, k6, k7, k8, v, P):
    w = []
    p = tensor([False for i in range(2**8)])

    for i in range(len(v)):
        if i!=k1 and i!=k2 and i!=k3 and i!=k4 and i!=k5 and i!=k6 and i!=k7 and i!=k8:
            w.append(i)

    for v[k1] in [0, 1]:
        for v[k2] in [0, 1]:
            for v[k3] in [0, 1]:
                for v[k4] in [0, 1]:
                    for v[k5] in [0, 1]:
                        for v[k6] in [0, 1]:
                            for v[k7] in [0, 1]:
                                for v[k8] in [0, 1]:
                                    p[v[k1]][v[k2]][v[k3]][v[k4]][v[k5]][v[k6]][v[k7]][v[k8]] = \
                                    Or([P[v[0]][v[1]][v[2]][v[3]][v[4]][v[5]][v[6]][v[7]]\
                                    [v[8]][v[9]][v[10]][v[11]][v[12]][v[13]][v[14]][v[15]]\
                                    for v[w[0]] in [0, 1] for v[w[1]] in [0, 1]\
                                    for v[w[2]] in [0, 1] for v[w[3]] in [0, 1]\
                                    for v[w[4]] in [0, 1] for v[w[5]] in [0, 1]\
                                    for v[w[6]] in [0, 1] for v[w[7]] in [0, 1]])
    return p

def compatibilityWeb(pattern):
    s = Solver()
    a11, b11, c11, d11, a12, b12, c12, d12, a21, b21, c21, d21,\
    a22, b22, c22, d22 = Ints('a11 b11 c11 d11 a12 b12 c12 d12 a21 b21 c21 d21 a22 b22 c22 d22')
    v = [a11, b11, c11, d11, a12, b12, c12, d12, a21, b21, c21, d21, a22, b22, c22, d22]

    Pobs = observedDistr(pattern)
    Pabcd = Pobs.jointDistr
    Pab = Pobs.marginal2([0,1])
    Pad = Pobs.marginal2([0,3])
    Pbc = Pobs.marginal2([1,2])
    Pcd = Pobs.marginal2([2,3])
    Pa = Pobs.marginal1([0])
    Pb = Pobs.marginal1([1])
    Pc = Pobs.marginal1([2])
    Pd = Pobs.marginal1([3])

    p = Array('p', Z, B)
    inter = []
    for i in range(2**16):
        inter.append(Select(p, i))
    P = tensor(inter)

    # A12B21C12D21 A21B12C21D12
    Pa12b21c12d21a21b12c21d12 = marginal8(4,9,6,11,8,5,10,7,v,P)
    # A11B11C12D21 A22B22C21D12
    Pa11b11c12d21a22b22c21d12 = marginal8(0,1,6,11,12,13,10,7,v,P)
    # A11B12C22D21 A22B21C11D12
    Pa11b12c22d21a22b21c11d12 = marginal8(0,5,14,11,12,9,2,7,v,P)
    # A12B22C22D21 A21B11C11D12
    Pa12b22c22d21a21b11c11d12 = marginal8(4,13,14,11,8,1,2,7,v,P)
    # A11B12C21D11 A22B21C12D22
    Pa11b12c21d11a22b21c12d22 = marginal8(0,5,10,3,12,9,6,15,v,P)
    # A12B22C21D11 A21B11C12D22
    Pa12b22c21d11a21b11c12d22 = marginal8(4,13,10,3,8,1,6,15,v,P)
    # A12B21C11D11 A21B12C22D22
    Pa12b21c11d11a21b12c22d22 = marginal8(4,9,2,3,8,5,14,15,v,P)
    # A11B11C11D11 A22B22C22D22
    Pa11b11c11d11a22b22c22d22 = marginal8(0,1,2,3,12,13,14,15,v,P)

    for x1 in [0, 1]:
        for x2 in [0, 1]:
            for x3 in [0, 1]:
                for x4 in [0, 1]:
                    for x5 in [0, 1]:
                        for x6 in [0, 1]:
                            for x7 in [0, 1]:
                                for x8 in [0, 1]:
                                    s.add(Pa12b21c12d21a21b12c21d12[x1][x2][x3][x4][x5][x6][x7][x8] == And(Pabcd[x1][x2][x3][x4], Pabcd[x5][x6][x7][x8]))
                                    s.add(Pa11b11c12d21a22b22c21d12[x1][x2][x3][x4][x5][x6][x7][x8] == And(Pabcd[x1][x2][x3][x4], Pabcd[x5][x6][x7][x8]))
                                    s.add(Pa11b12c22d21a22b21c11d12[x1][x2][x3][x4][x5][x6][x7][x8] == And(Pabcd[x1][x2][x3][x4], Pabcd[x5][x6][x7][x8]))
                                    s.add(Pa12b22c22d21a21b11c11d12[x1][x2][x3][x4][x5][x6][x7][x8] == And(Pabcd[x1][x2][x3][x4], Pabcd[x5][x6][x7][x8]))
                                    s.add(Pa11b12c21d11a22b21c12d22[x1][x2][x3][x4][x5][x6][x7][x8] == And(Pabcd[x1][x2][x3][x4], Pabcd[x5][x6][x7][x8]))
                                    s.add(Pa12b22c21d11a21b11c12d22[x1][x2][x3][x4][x5][x6][x7][x8] == And(Pabcd[x1][x2][x3][x4], Pabcd[x5][x6][x7][x8]))
                                    s.add(Pa12b21c11d11a21b12c22d22[x1][x2][x3][x4][x5][x6][x7][x8] == And(Pabcd[x1][x2][x3][x4], Pabcd[x5][x6][x7][x8]))
                                    s.add(Pa11b11c11d11a22b22c22d22[x1][x2][x3][x4][x5][x6][x7][x8] == And(Pabcd[x1][x2][x3][x4], Pabcd[x5][x6][x7][x8]))

    if s.check() == unsat:
        return s.check()

    # A12D11 A21B12 C12
    Pa12d11a21b12c12 = marginal5(4,3,8,5,6,v,P)
    # A21B12 B21C12 D11
    Pa21b12b21c12d11 = marginal5(8,5,9,6,3,v,P)
    # A11D11 A22B22 C12
    Pa11d11a22b22c12 = marginal5(0,3,12,13,6,v,P)
    # A22B22 B11C12 D11
    Pa22b22b11c12d11 = marginal5(12,13,1,6,3,v,P)
    # A22 B11C12 C21D11
    Pa22b11c12c21d11 = marginal5(12,1,6,10,3,v,P)
    # A21 B21C12 C21D11
    Pa21b21c12c21d11 = marginal5(8,9,6,10,3,v,P)
    # A12D11 A21B11 C22
    Pa12d11a21b11c22 = marginal5(4,3,8,1,14,v,P)
    # A11D11 A22B21 C22
    Pa11d11a22b21c22 = marginal5(0,3,12,9,14,v,P)

    for x1 in [0, 1]:
        for x2 in [0, 1]:
            for x3 in [0, 1]:
                for x4 in [0, 1]:
                    for x5 in [0, 1]:
                        s.add(Pa12d11a21b12c12[x1][x2][x3][x4][x5] == And(Pad[x1][x2],Pab[x3][x4],Pc[x5]))
                        s.add(Pa21b12b21c12d11[x1][x2][x3][x4][x5] == And(Pab[x1][x2],Pbc[x3][x4],Pd[x5]))
                        s.add(Pa11d11a22b22c12[x1][x2][x3][x4][x5] == And(Pad[x1][x2],Pab[x3][x4],Pc[x5]))
                        s.add(Pa22b22b11c12d11[x1][x2][x3][x4][x5] == And(Pab[x1][x2],Pbc[x3][x4],Pd[x5]))
                        s.add(Pa22b11c12c21d11[x1][x2][x3][x4][x5] == And(Pa[x1],Pbc[x2][x3],Pcd[x4][x5]))
                        s.add(Pa21b21c12c21d11[x1][x2][x3][x4][x5] == And(Pa[x1],Pbc[x2][x3],Pcd[x4][x5]))
                        s.add(Pa12d11a21b11c22[x1][x2][x3][x4][x5] == And(Pad[x1][x2],Pab[x3][x4],Pc[x5]))
                        s.add(Pa11d11a22b21c22[x1][x2][x3][x4][x5] == And(Pad[x1][x2],Pab[x3][x4],Pc[x5]))

    if s.check() == unsat:
        return s.check()

    # A22B21 B12C22 D11
    Pa22b21b12c22d11 = marginal5(12,9,5,14,3,v,P)
    # A21B11 B22C22 D11
    Pa21b11b22c22d11 = marginal5(8,1,13,14,3,v,P)
    # A22 B12C22 C11D11
    Pa22b12c22c11d11 = marginal5(12,5,14,2,3,v,P)
    # A21 B22C22 C11D11
    Pa21b22c22c11d11 = marginal5(8,13,14,2,3,v,P)
    # A11B12 A22D12 C12
    Pa11b12a22d12c12 = marginal5(0,5,12,7,6,v,P)
    # A11B12 B21C12 D12
    Pa11b12b21c12d12 = marginal5(0,5,9,6,7,v,P)
    # A12B22 A21D12 C12
    Pa12b22a21d12c12 = marginal5(4,13,8,7,6,v,P)
    # A12B22 B11C12 D12
    Pa12b22b11c12d12 = marginal5(4,13,1,6,7,v,P)

    for x1 in [0, 1]:
        for x2 in [0, 1]:
            for x3 in [0, 1]:
                for x4 in [0, 1]:
                    for x5 in [0, 1]:
                        s.add(Pa22b21b12c22d11[x1][x2][x3][x4][x5] == And(Pab[x1][x2],Pbc[x3][x4],Pd[x5]))
                        s.add(Pa21b11b22c22d11[x1][x2][x3][x4][x5] == And(Pab[x1][x2],Pbc[x3][x4],Pd[x5]))
                        s.add(Pa22b12c22c11d11[x1][x2][x3][x4][x5] == And(Pa[x1],Pbc[x2][x3],Pcd[x4][x5]))
                        s.add(Pa21b22c22c11d11[x1][x2][x3][x4][x5] == And(Pa[x1],Pbc[x2][x3],Pcd[x4][x5]))
                        s.add(Pa11b12a22d12c12[x1][x2][x3][x4][x5] == And(Pab[x1][x2],Pad[x3][x4],Pc[x5]))
                        s.add(Pa11b12b21c12d12[x1][x2][x3][x4][x5] == And(Pab[x1][x2],Pbc[x3][x4],Pd[x5]))
                        s.add(Pa12b22a21d12c12[x1][x2][x3][x4][x5] == And(Pab[x1][x2],Pad[x3][x4],Pc[x5]))
                        s.add(Pa12b22b11c12d12[x1][x2][x3][x4][x5] == And(Pab[x1][x2],Pbc[x3][x4],Pd[x5]))

    if s.check() == unsat:
        return s.check()
    
    # A12 B11C12 C21D12
    Pa12b11c12c21d12 = marginal5(4,1,6,10,7,v,P)
    # A11 B21C12 C21D12
    Pa11b21c12c21d12 = marginal5(0,9,6,10,7,v,P)
    # A11B11 A22D12 C22
    Pa11b11a22d12c22 = marginal5(0,1,12,7,14,v,P)
    # A12B21 A21D12 C22
    Pa12b21a21d12c22 = marginal5(4,9,8,7,14,v,P)
    # A12B21 B12C22 D12
    Pa12b21b12c22d12 = marginal5(4,9,5,14,7,v,P)
    # A11B11 B22C22 D12
    Pa11b11b22c22d12 = marginal5(0,1,13,14,7,v,P)
    # A12 B12C22 C11D12
    Pa12b12c22c11d12 = marginal5(4,5,14,2,7,v,P)
    # A11 B22C22 C11D12
    Pa11b22c22c11d12 = marginal5(0,13,14,2,7,v,P)

    for x1 in [0, 1]:
        for x2 in [0, 1]:
            for x3 in [0, 1]:
                for x4 in [0, 1]:
                    for x5 in [0, 1]:
                        s.add(Pa12b11c12c21d12[x1][x2][x3][x4][x5] == And(Pa[x1],Pbc[x2][x3],Pcd[x4][x5]))
                        s.add(Pa11b21c12c21d12[x1][x2][x3][x4][x5] == And(Pa[x1],Pbc[x2][x3],Pcd[x4][x5]))
                        s.add(Pa11b11a22d12c22[x1][x2][x3][x4][x5] == And(Pab[x1][x2],Pad[x3][x4],Pc[x5]))
                        s.add(Pa12b21a21d12c22[x1][x2][x3][x4][x5] == And(Pab[x1][x2],Pad[x3][x4],Pc[x5]))
                        s.add(Pa12b21b12c22d12[x1][x2][x3][x4][x5] == And(Pab[x1][x2],Pbc[x3][x4],Pd[x5]))
                        s.add(Pa11b11b22c22d12[x1][x2][x3][x4][x5] == And(Pab[x1][x2],Pbc[x3][x4],Pd[x5]))
                        s.add(Pa12b12c22c11d12[x1][x2][x3][x4][x5] == And(Pa[x1],Pbc[x2][x3],Pcd[x4][x5]))
                        s.add(Pa11b22c22c11d12[x1][x2][x3][x4][x5] == And(Pa[x1],Pbc[x2][x3],Pcd[x4][x5]))

    if s.check() == unsat:
        return s.check()

    # A12D21 A21B12 C11
    Pa12d21a21b12c11 = marginal5(4,11,8,5,2,v,P)
    # A21B12 B21C11 D21
    Pa21b12b21c11d21 = marginal5(8,5,9,2,11,v,P)
    # A11D21 A22B22 C11
    Pa11d21a22b22c11 = marginal5(0,11,12,13,2,v,P)
    # A22B22 B11C11 D21
    Pa22b22b11c11d21 = marginal5(12,13,1,2,11,v,P)
    # A12D21 A21B11 C21
    Pa12d21a21b11c21 = marginal5(4,11,8,1,10,v,P)
    # A11D21 A22B21 C21
    Pa11d21a22b21c21 = marginal5(0,11,12,9,10,v,P)
    # A22B21 B12C21 D21
    Pa22b21b12c21d21 = marginal5(12,9,5,10,11,v,P)
    # A21B11 B22C21 D21
    Pa21b11b22c21d21 = marginal5(8,1,13,10,11,v,P)

    for x1 in [0, 1]:
        for x2 in [0, 1]:
            for x3 in [0, 1]:
                for x4 in [0, 1]:
                    for x5 in [0, 1]:
                        s.add(Pa12d21a21b12c11[x1][x2][x3][x4][x5] == And(Pad[x1][x2],Pab[x3][x4],Pc[x5]))
                        s.add(Pa21b12b21c11d21[x1][x2][x3][x4][x5] == And(Pab[x1][x2],Pbc[x3][x4],Pd[x5]))
                        s.add(Pa11d21a22b22c11[x1][x2][x3][x4][x5] == And(Pad[x1][x2],Pab[x3][x4],Pc[x5]))
                        s.add(Pa22b22b11c11d21[x1][x2][x3][x4][x5] == And(Pab[x1][x2],Pbc[x3][x4],Pd[x5]))
                        s.add(Pa12d21a21b11c21[x1][x2][x3][x4][x5] == And(Pad[x1][x2],Pab[x3][x4],Pc[x5]))
                        s.add(Pa11d21a22b21c21[x1][x2][x3][x4][x5] == And(Pad[x1][x2],Pab[x3][x4],Pc[x5]))
                        s.add(Pa22b21b12c21d21[x1][x2][x3][x4][x5] == And(Pab[x1][x2],Pbc[x3][x4],Pd[x5]))
                        s.add(Pa21b11b22c21d21[x1][x2][x3][x4][x5] == And(Pab[x1][x2],Pbc[x3][x4],Pd[x5]))

    if s.check() == unsat:
        return s.check()

    # A22 B12C21 C12D21
    Pa22b12c21c12d21 = marginal5(12,5,10,6,11,v,P)
    # A21 B22C21 C12D21
    Pa21b22c21c12d21 = marginal5(8,13,10,6,11,v,P)
    # A22 B11C11 C22D21
    Pa22b11c11c22d21 = marginal5(12,1,2,14,11,v,P)
    # A21 B21C11 C22D21
    Pa21b21c11c22d21 = marginal5(8,9,2,14,11,v,P)
    # A12D21 B12 C11D12
    Pa12d21b12c11d12 = marginal5(4,11,5,2,7,v,P)
    # A11D21 B22 C11D12
    Pa11d21b22c11d12 = marginal5(0,11,13,2,7,v,P)
    # A22D12 B12 C12D21
    Pa22d12b12c12d21 = marginal5(12,7,5,6,11,v,P)
    # A21D12 B22 C12D21
    Pa21d12b22c12d21 = marginal5(8,7,13,6,11,v,P)

    for x1 in [0, 1]:
        for x2 in [0, 1]:
            for x3 in [0, 1]:
                for x4 in [0, 1]:
                    for x5 in [0, 1]:
                        s.add(Pa22b12c21c12d21[x1][x2][x3][x4][x5] == And(Pa[x1],Pbc[x2][x3],Pcd[x4][x5]))
                        s.add(Pa21b22c21c12d21[x1][x2][x3][x4][x5] == And(Pa[x1],Pbc[x2][x3],Pcd[x4][x5]))
                        s.add(Pa22b11c11c22d21[x1][x2][x3][x4][x5] == And(Pa[x1],Pbc[x2][x3],Pcd[x4][x5]))
                        s.add(Pa21b21c11c22d21[x1][x2][x3][x4][x5] == And(Pa[x1],Pbc[x2][x3],Pcd[x4][x5]))
                        s.add(Pa12d21b12c11d12[x1][x2][x3][x4][x5] == And(Pad[x1][x2],Pb[x3],Pcd[x4][x5]))
                        s.add(Pa11d21b22c11d12[x1][x2][x3][x4][x5] == And(Pad[x1][x2],Pb[x3],Pcd[x4][x5]))
                        s.add(Pa22d12b12c12d21[x1][x2][x3][x4][x5] == And(Pad[x1][x2],Pb[x3],Pcd[x4][x5]))
                        s.add(Pa21d12b22c12d21[x1][x2][x3][x4][x5] == And(Pad[x1][x2],Pb[x3],Pcd[x4][x5]))

    if s.check() == unsat:
        return s.check()

    # A12D21 B11 C21D12
    Pa12d21b11c21d12 = marginal5(4,11,1,10,7,v,P)
    # A11D21 B21 C21D12
    Pa11d21b21c21d12 = marginal5(0,11,9,10,7,v,P)
    # A22D12 B11 C22D21
    Pa22d12b11c22d21 = marginal5(12,7,1,14,11,v,P)
    # A21D12 B21 C22D21
    Pa21d12b21c22d21 = marginal5(8,7,9,14,11,v,P)
    # A11B12 A22D22 C11
    Pa11b12a22d22c11 = marginal5(0,5,12,15,2,v,P)
    # A11B12 B21C11 D22
    Pa11b12b21c11d22 = marginal5(0,5,9,2,15,v,P)
    # A12B22 A21D22 C11
    Pa12b22a21d22c11 = marginal5(4,13,8,15,2,v,P)
    # A12B22 B11C11 D22
    Pa12b22b11c11d22 = marginal5(4,13,1,2,15,v,P)

    for x1 in [0, 1]:
        for x2 in [0, 1]:
            for x3 in [0, 1]:
                for x4 in [0, 1]:
                    for x5 in [0, 1]:
                        s.add(Pa12d21b11c21d12[x1][x2][x3][x4][x5] == And(Pad[x1][x2],Pb[x3],Pcd[x4][x5]))
                        s.add(Pa11d21b21c21d12[x1][x2][x3][x4][x5] == And(Pad[x1][x2],Pb[x3],Pcd[x4][x5]))
                        s.add(Pa22d12b11c22d21[x1][x2][x3][x4][x5] == And(Pad[x1][x2],Pb[x3],Pcd[x4][x5]))
                        s.add(Pa21d12b21c22d21[x1][x2][x3][x4][x5] == And(Pad[x1][x2],Pb[x3],Pcd[x4][x5]))
                        s.add(Pa11b12a22d22c11[x1][x2][x3][x4][x5] == And(Pab[x1][x2],Pad[x3][x4],Pc[x5]))
                        s.add(Pa11b12b21c11d22[x1][x2][x3][x4][x5] == And(Pab[x1][x2],Pbc[x3][x4],Pd[x5]))
                        s.add(Pa12b22a21d22c11[x1][x2][x3][x4][x5] == And(Pab[x1][x2],Pad[x3][x4],Pc[x5]))
                        s.add(Pa12b22b11c11d22[x1][x2][x3][x4][x5] == And(Pab[x1][x2],Pbc[x3][x4],Pd[x5]))

    if s.check() == unsat:
        return s.check()

    # A11B11 A22D22 C21
    Pa11b11a22d22c21 = marginal5(0,1,12,15,10,v,P)
    # A12B21 A21D22 C21
    Pa12b21a21d22c21 = marginal5(4,9,8,15,10,v,P)
    # A12B21 B12C21 D22
    Pa12b21b12c21d22 = marginal5(4,9,5,10,15,v,P)
    # A11B11 B22C21 D22
    Pa11b11b22c21d22 = marginal5(0,1,13,10,15,v,P)
    # A12 B12C21 C12D22
    Pa12b12c21c12d22 = marginal5(4,5,10,6,15,v,P)
    # A11 B22C21 C12D22
    Pa11b22c21c12d22 = marginal5(0,13,10,6,15,v,P)
    # A12 B11C11 C22D22
    Pa12b11c11c22d22 = marginal5(4,1,2,14,15,v,P)
    # A11 B21C11 C22D22
    Pa11b21c11c22d22 = marginal5(0,9,2,14,15,v,P)

    for x1 in [0, 1]:
        for x2 in [0, 1]:
            for x3 in [0, 1]:
                for x4 in [0, 1]:
                    for x5 in [0, 1]:
                        s.add(Pa11b11a22d22c21[x1][x2][x3][x4][x5] == And(Pab[x1][x2],Pad[x3][x4],Pc[x5]))
                        s.add(Pa12b21a21d22c21[x1][x2][x3][x4][x5] == And(Pab[x1][x2],Pad[x3][x4],Pc[x5]))
                        s.add(Pa12b21b12c21d22[x1][x2][x3][x4][x5] == And(Pab[x1][x2],Pbc[x3][x4],Pd[x5]))
                        s.add(Pa11b11b22c21d22[x1][x2][x3][x4][x5] == And(Pab[x1][x2],Pbc[x3][x4],Pd[x5]))
                        s.add(Pa12b12c21c12d22[x1][x2][x3][x4][x5] == And(Pa[x1],Pbc[x2][x3],Pcd[x4][x5]))
                        s.add(Pa11b22c21c12d22[x1][x2][x3][x4][x5] == And(Pa[x1],Pbc[x2][x3],Pcd[x4][x5]))
                        s.add(Pa12b11c11c22d22[x1][x2][x3][x4][x5] == And(Pa[x1],Pbc[x2][x3],Pcd[x4][x5]))
                        s.add(Pa11b21c11c22d22[x1][x2][x3][x4][x5] == And(Pa[x1],Pbc[x2][x3],Pcd[x4][x5]))

    if s.check() == unsat:
        return s.check()

    # A22D22 B12 C11D11
    Pa22d22b12c11d11 = marginal5(12,15,5,2,3,v,P)
    # A21D22 B22 C11D11
    Pa21d22b22c11d11 = marginal5(8,15,13,2,3,v,P)
    # A12D11 B12 C12D22
    Pa12d11b12c12d22 = marginal5(4,3,5,6,15,v,P)
    # A11D11 B22 C12D22
    Pa11d11b22c12d22 = marginal5(0,3,13,6,15,v,P)
    # A22D22 B11 C21D11
    Pa22d22b11c21d11 = marginal5(12,15,1,10,3,v,P)
    # A21D22 B21 C21D11
    Pa21d22b21c21d11 = marginal5(8,15,9,10,3,v,P)
    # A12D11 B11 C22D22
    Pa12d11b11c22d22 = marginal5(4,3,1,14,15,v,P)
    # A11D11 B21 C22D22
    Pa11d11b21c22d22 = marginal5(0,3,9,14,15,v,P)

    for x1 in [0, 1]:
        for x2 in [0, 1]:
            for x3 in [0, 1]:
                for x4 in [0, 1]:
                    for x5 in [0, 1]:
                        s.add(Pa22d22b12c11d11[x1][x2][x3][x4][x5] == And(Pad[x1][x2],Pb[x3],Pcd[x4][x5]))
                        s.add(Pa21d22b22c11d11[x1][x2][x3][x4][x5] == And(Pad[x1][x2],Pb[x3],Pcd[x4][x5]))
                        s.add(Pa12d11b12c12d22[x1][x2][x3][x4][x5] == And(Pad[x1][x2],Pb[x3],Pcd[x4][x5]))
                        s.add(Pa11d11b22c12d22[x1][x2][x3][x4][x5] == And(Pad[x1][x2],Pb[x3],Pcd[x4][x5]))
                        s.add(Pa22d22b11c21d11[x1][x2][x3][x4][x5] == And(Pad[x1][x2],Pb[x3],Pcd[x4][x5]))
                        s.add(Pa21d22b21c21d11[x1][x2][x3][x4][x5] == And(Pad[x1][x2],Pb[x3],Pcd[x4][x5]))
                        s.add(Pa12d11b11c22d22[x1][x2][x3][x4][x5] == And(Pad[x1][x2],Pb[x3],Pcd[x4][x5]))
                        s.add(Pa11d11b21c22d22[x1][x2][x3][x4][x5] == And(Pad[x1][x2],Pb[x3],Pcd[x4][x5]))

    return s.check()

# orbit = np.loadtxt('satLocalDecomp.txt')
# for p in orbit:
#     state = compatibilityWeb(p)
#     print(p, state)
