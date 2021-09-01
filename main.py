from z3 import *
from observedDistribution import *
import numpy as np
from tqdm import *
import time
from cut import *
from ring8 import *
from ring12 import *
from localDecomp import *
from web import *
from scipy.io import savemat

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
            if Pbd[x][y] != Pb[x] and Pd[y]:
                ans2 = False

    ans = ans1 and ans2
    return ans

satSquare = []
satLocality23 = []
satLocality3 = []
unsatLocality = []
satRing8 = []
satRing12 = []
unsatRing8 = []
unsatRing12 = []
satWeb = []
unsatWeb = []
orbit = np.loadtxt('orbit.txt')

print('Square compatibility')
for i in tqdm(orbit, ncols=70):
    state = squareCompatibility(i)
    if state == True:
        satSquare.append(i)
savemat('satSquare.mat', {'satSquare':satSquare})

print('Locality condition')
for i in tqdm(satSquare, ncols=70):
    state3 = localDecomp(i, 3)
    if state3 == sat:
        state2 = localDecomp(i, 2)
        if state2 == sat:
            satLocality23.append(i)
        else:
            satLocality3.append(i)
    else:
        unsatLocality.append(i)
savemat('satLocality23.mat', {'satLocality23':satLocality23})
savemat('satLocality3.mat', {'satLocality3':satLocality3})
savemat('unsatLocality.mat', {'unsatLocality':unsatLocality})

print('Ring inflations')
for i in tqdm(unsatLocality, ncols=70):
    state8 = compatibilityRing8(i)
    if state8 == sat:
        satRing8.append(i)
        state12 = compatibilityRing12(i)
        if state12 == sat:
            satRing12.append(i)
        else:
            unsatRing12.append(i)
    else:
        unsatRing8.append(i)
savemat('satRing8.mat', {'satRing8':satRing8})
savemat('unsatRing8.mat',{'unsatRing8':unsatRing8})
savemat('satRing12.mat', {'satRing12':satRing12})
savemat('unsatRing12.mat', {'unsatRing12':unsatRing12})

print('Web inflation')
for i in tqdm(satRing12, ncols=70):
    state = compatibilityWeb(i)
    if state == sat:
        satWeb.append(i)
    else:
        unsatWeb.append(i)
savemat('satWeb.mat', {'satWeb':satWeb})
savemat('unsatWeb.mat', {'unsatWeb':unsatWeb})

print('Square compatibility:', len(satSquare),'/',len(orbit))
print('Sat locality condition:', len(satLocality3)+len(satLocality23),'/',len(satSquare))
print('Sat locality only for C>2:', len(satLocality3),'/',len(satLocality3)+len(satLocality23))
print('Nonlocal patterns:', len(unsatLocality),'/',len(satSquare))
print('Unsat ring8:', len(unsatRing8),'/',len(unsatLocality))
print('Sat ring8:', len(satRing8), '/', len(unsatLocality))
print('Unsat ring12:', len(unsatRing12), '/', len(satRing8))
print('Sat ring12:', len(satRing12),'/',len(satRing8))
print('Unsat web:', len(unsatWeb),'/',len(satRing12))
print('Sat web:', len(satWeb), '/', len(satRing12))

savemat('unsorted.mat', {'satWeb':satWeb})
print('Unsorted patterns')
for i in satWeb:
    print(i)
