# -*- coding: utf-8 -*-
import sys
import os
from tools import *
import numpy as np

class observedDistr:

    def __init__(self, pattern):
        inter = []

        for p in pattern:
            inter.append(bool(p))

        self.jointDistr = tensor(inter)
        self.vert = ['a', 'b', 'c', 'd']

    def marginal3(self, v):
        Pabcd = self.jointDistr
        Pabc = tensor([False for i in range(2**3)])
        Pbcd = tensor([False for i in range(2**3)])
        Pacd = tensor([False for i in range(2**3)])
        Pabd = tensor([False for i in range(2**3)])

        for x in [0, 1]:
            for y in [0, 1]:
                for z in [0, 1]:
                    Pabc[x][y][z] = Pabcd[x][y][z][0] or Pabcd[x][y][z][1]
                    Pbcd[x][y][z] = Pabcd[0][x][y][z] or Pabcd[1][x][y][z]
                    Pacd[x][y][z] = Pabcd[x][0][y][z] or Pabcd[x][1][y][z]
                    Pabd[x][y][z] = Pabcd[x][y][0][z] or Pabcd[x][y][1][z]

        if 0 in v and 1 in v and 2 in v:
            return Pabc
        elif 1 in v and 2 in v and 3 in v:
            return Pbcd
        elif 0 in v and 2 in v and 3 in v:
            return Pacd
        elif 0 in v and 1 in v and 3 in v:
            return Pabd

    def marginal2(self, v):
        Pab = tensor([False for i in range(2**2)])
        Pac = tensor([False for i in range(2**2)])
        Pad = tensor([False for i in range(2**2)])
        Pbc = tensor([False for i in range(2**2)])
        Pbd = tensor([False for i in range(2**2)])
        Pcd = tensor([False for i in range(2**2)])

        Pabc = self.marginal3([0,1,2])
        Pbcd = self.marginal3([1,2,3])
        Pabd = self.marginal3([0,1,3])

        for x in [0, 1]:
            for y in [0, 1]:
                Pab[x][y] = Pabc[x][y][0] or Pabc[x][y][1]
                Pac[x][y] = Pabc[x][0][y] or Pabc[x][1][y]
                Pad[x][y] = Pabd[x][0][y] or Pabd[x][1][y]
                Pbc[x][y] = Pabc[0][x][y] or Pabc[1][x][y]
                Pbd[x][y] = Pabd[0][x][y] or Pabd[1][x][y]
                Pcd[x][y] = Pbcd[0][x][y] or Pbcd[1][x][y]

        if 0 in v and 1 in v:
            return Pab
        elif 0 in v and 2 in v:
            return Pac
        elif 0 in v and 3 in v:
            return Pad
        elif 1 in v and 2 in v:
            return Pbc
        elif 1 in v and 3 in v:
            return Pbd
        elif 2 in v and 3 in v:
            return Pcd

    def marginal1(self, v):
        Pa = [False, False]
        Pb = [False, False]
        Pc = [False, False]
        Pd = [False, False]

        Pab = self.marginal2([0,1])
        Pcd = self.marginal2([2,3])

        for x in [0, 1]:
            Pa[x] = Pab[x][0] or Pab[x][1]
            Pb[x] = Pab[0][x] or Pab[1][x]
            Pc[x] = Pcd[x][0] or Pcd[x][1]
            Pd[x] = Pcd[0][x] or Pcd[1][x]

        if 0 in v:
            return Pa
        elif 1 in v:
            return Pb
        elif 2 in v:
            return Pc
        elif 3 in v:
            return Pd

    def marginal(self, v):
        if len(v) == 4:
            return self.jointDistr
        elif len(v) == 3:
            return self.marginal3(v)
        elif len(v) == 2:
            return self.marginal2(v)
        elif len(v) == 1:
            return self.marginal1(v)
