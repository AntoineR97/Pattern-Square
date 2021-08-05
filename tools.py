import itertools as iter
from itertools import combinations, permutations, compress, product
import copy
from copy import deepcopy

def tensor(pattern):
    k = len(pattern)

    if k > 2:
        p = [tensor(pattern[0:int(k/2)]), tensor(pattern[int(k/2):k])]
    else:
        p = pattern

    return p

def getComb(input, l):
    comb = list(iter.combinations(input, l))
    inter = []

    for c in comb:
        inter.append(list(c))

    comb = inter

    if l == 1:
        res = [c[0] for c in comb]
        comb = res

    return comb

def partition(collection):
    if len(collection) == 1:
        yield [ collection ]
        return

    first = collection[0]
    for smaller in partition(collection[1:]):
        # insert `first` in each of the subpartition's subsets
        for n, subset in enumerate(smaller):
            yield smaller[:n] + [[ first ] + subset]  + smaller[n+1:]
        # put `first` in its own subset
        yield [ [ first ] ] + smaller

def getSubSet(list):
    output = []

    for p in partition(list):
        output.append(p)

    return output

def removeIdx(input):
    output = []

    if not isinstance(input, list):
        output = input[0]

    else:
        for i in input:
            output.append(i[0])

    return output

def getIdx(input, set):
    idx = []

    for i in input:
        idx.append(set.index(i))

    return idx

def ordering(input, dict):
    for i in range(len(input)-1):
        for j in range(i+1, len(input)):
            if ord(dict[input[i]][0]) > ord(dict[input[j]][0]):
                input[i], input[j] = input[j], input[i]

def lexicalOrder(decomp, dict):
    for d in decomp:
        if len(d) > 1:
            for i in range(len(d)-1):
                for j in range(i+1, len(d)):
                    if ord(dict[d[i]][0]) > ord(dict[d[j]][0]):
                        d[i], d[j] = d[j], d[i]

    return decomp

def Union(v, lst):
    output = set([])

    for i in v:
        output = output.union(set(lst[i]))

    return list(output)
