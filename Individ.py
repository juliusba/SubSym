'''
Created on 31. jan. 2013

@author: juliusbuset
'''
import random
import math
import array
import sys

class Individ(object):

    mutationRate = 0.05
    crossoverRate = 0.3
    
    def __init__(self, blueprint, parents = [], crossovers = [], gray = False):
        self.fitness = 0
        self.dna = []
        if parents == []:
            for i in range (0,len(blueprint)):
                self.dna.append(Phenotype(blueprint[i], [], gray))
        else:
            for i in range (0, len(parents[0].dna)):
                parentsPheno = []
                for j in range (0,len(parents)):
                    parentsPheno.append(parents[j].dna[i])
                self.dna.append(Phenotype(blueprint[i], parentsPheno, crossovers[i], gray))

class Phenotype:

    def __init__(self, bits, parents = [], crossovers = [], gray = False):
        self.genotype = []
        if parents == []:
            for i in range (0, bits):
                self.genotype.append(random.randint(0,1))
        else:
            for i in range (0, bits):
                if random.random() < Individ.mutationRate:
                    self.genotype.append(random.randint(0,1))
                else:
                    self.genotype.append(parents[crossovers[i]].genotype[i])
        if gray:
            self.val = Phenotype.grayToInteger(self.genotype)
        else:
            self.val = Phenotype.binaryToInteger(self.genotype)


    def integerToBinary(integer, bits):
        bin = []
        while(bits >=1):
            if integer >= math.pow(2, bits -1):
                bin.append(1)
                integer -= math.pow(2, bits -1)
            else:
                bin.append(0)
            bits -= 1
        return bin

    def binaryToInteger(b):
        integer = int(0)
        bits = len(b)
        for i in range(0, len(b)):
            if b[i] == 1:
                integer += int(math.pow(2, bits - i -1))
        return integer

    def binaryToGray(b):
        g = [b[0]]
        for i in range (1, len(b)):
            g.append((b[i] + b[i-1]) % 2)
        return g

    def grayToBinary(g):
        b = [g[0]]
        for i in range (1, len(g)):
            b.append((b[i-1] + g[i]) % 2)
        return b

    def integerToGray(integer, bits):
        b = Phenotype.integerToBinary(integer, bits)
        return Phenotype.binaryToGray(b)

    def grayToInteger(g):
        b = Phenotype.grayToBinary(g)
        return Phenotype.binaryToInteger(b)

if __name__ == '__main__':
    for i in range (10, 0, -1):
        print (i)

    sys.stdin.readline()