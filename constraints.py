import sys
import os
sys.path.insert(0, '/Users/antoinerestivo/usr/lib/python-2.7/site-packages')
from z3 import *
from tools import *
from observedDistribution import *
import numpy as np
from tqdm import *
import time
from cut import *
from ring8 import *
from ring12 import *
from localDecomp import *
from web import *
from spiral import *
from scipy.io import savemat

B = BoolSort()
Z = IntSort()

def squareCompatibility(pattern):
    Pobs = observedDistr(pattern)
    Pa = Pobs.marginal1([0])
    Pb = Pobs.marginal1([1])
    Pc = Pobs.marginal1([2])
    Pd = Pobs.marginal1([3])
    Pac = Pobs.marginal2([0,2])
    Pbd = Pobs.marginal2([1,3])

    ans1 = True
    ans2 = True

    for x in [0, 1]:
        for y in [0, 1]:
            if Pac[x][y] != Pa[x] and Pc[y]:
                ans1 = False

    for x in [0, 1]:
        for y in [0, 1]:
            if Pbd[x][y] != Pb[x] and Pd[y]:
                ans2 = False

    ans = ans1 and ans2
    return ans

orbit = np.loadtxt('/Users/antoinerestivo/Desktop/squarePattern/orbit.txt')

unsatSquare = []
satSquare = []
unsatLocalDecomp = []
satLocalDecomp = []
satLocalDecomp3 = []
satRing = []
unsatRing = []
unsatSpiral = []
satSpiral = []
unsatWeb = []
satWeb = []

print('Square compatibility')
for i in tqdm(orbit, ncols=70):
    state = squareCompatibility(i)
    if state == True:
        satSquare.append(i)
    elif state == False:
        unsatSquare.append(i)

print('Locality condition')
for i in tqdm(satSquare, ncols=70):
    state = localDecomp(i, 3)
    if state == sat:
        satLocalDecomp.append(i)
        state2 = localDecomp(i, 2)
        if state2 == unsat:
            satLocalDecomp3.append(i)
    elif state == unsat:
        unsatLocalDecomp.append(i)

print('Ring inflations')
for i in tqdm(unsatLocalDecomp, ncols=70):
    state8 = compatibilityRing8(i)
    if state8 == sat:
        state12 = compatibilityRing12(i)
        if state12 == sat:
            satRing.append(i)
        elif state12 == unsat:
            unsatRing.append(i)
    elif state8 == unsat:
        unsatRing.append(i)

# savemat('satRing.mat', {'satRing':satRing})

# print('Spiral inflation')
# for i in tqdm(satRing, ncols=70):
#     state = compatibilitySpiral(i)
#     if state == unsat:
#         unsatSpiral.append(i)
#     elif state == sat:
#         satSpiral.append(i)

print('Web inflation')
for i in tqdm(satRing, ncols=70):
    state = compatibilityWeb(i)
    if state == sat:
        satWeb.append(i)
    elif state == unsat:
        unsatWeb.append(i)

print('square compatible patterns:', len(satSquare),'/', len(orbit))
print('unsat locality condition:', len(unsatLocalDecomp), '/', len(satSquare))
print('Local patterns for C > 2:', len(satLocalDecomp3), '/', len(satLocalDecomp))
print('non-signalling patterns:', len(satRing), '/', len(unsatLocalDecomp))
#print('non-signalling but nonlocal patterns (spiral)', len(unsatSpiral), '/', len(satRing))
print('non-signalling but nonlocal patterns (web)', len(unsatWeb), '/', len(satRing))

savemat('satWeb.mat', {'satWeb': satWeb})
savemat('unsatWeb.mat', {'unsatWeb': unsatWeb})
