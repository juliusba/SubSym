'''
Created on 31. jan. 2013

@author: juliusbuset
'''
import random
import math
from ctypes.wintypes import DOUBLE

class Individ(object):

    def __init__(self, fitnessMeasure, blueprint, parents = []):

        self.genotype = []
        if parents == []:
            for i in range (0,len(blueprint)):
                self.genotype.append([])
                for j in range (0, blueprint[i]):
                    self.genotype[i].append(random.randint(0,1))
        else:
            for i in range (0, len(parents[0].genotype)):
                self.genotype.append([])
                for j in range (0, len(parents[0].genotype[i])):
                    if random.random() < 0.01:
                        gen = random.randint(0,1)
                    else:
                        gen = parents[random.randint(0, len(parents)-1)].genotype[i]
                    self.genotype.append(gen)
        
        self.fitness = fitnessMeasure(self)


    def integerToBinary(integer):
        return "{0:b}".format(integer)

    def binaryToInteger(b):
        return int(b, 2)

    def binaryToGray(b):
        temp = b >> 1
        ret = []
        for i in range (0, len(b)):
            ret.append((b[i] + temp[i]) % 2)
        return ret

    def grayToBinary(g):
        shift = 1
        while shift < len(g):
            temp = b >> shift
            ret = []
            for i in range (0, len(b)):
                ret.append((g[i] + temp[i]) % 2)
            g = ret
            shift *= 2

class Phenotype:

    def __init__(self, genotype, gray = false):
        if gray:
            self.genotype = genotype
            self.val = 0
            for i in range (0, len(genotype)):
                self.val += genotype[i] * math.pow(2, i-1)
        else:
            self.val = 0


    def __init__(self, geneCount, val):
        self.val = val
        self.geneCount = geneCount
        self.genotype = []
        for i in range (0, geneCount):
            if math.pow(2, geneCount - i - 1) < val:
                self.genotype.append(1)
                val -= math.pow(2, geneCount - i - 1)
            else:
                self.genotype.append(0)



