'''
Created on 31. jan. 2013

@author: juliusbuset
'''
import random
import math
import array

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
            print (i)
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

    def integerToGrey(integer, bits):
        b = Individ.integerToBinary(integer, bits)
        return Individ.binaryToGray(b)

    def greyToInteger(g):
        b = Individ.grayToBinary(g)
        return Individ.binaryToInteger(b)

#class Phenotype:

#    def __init__(self, genotype, gray = false):
#        if gray:
#            self.genotype = genotype
#            self.val = 0
#            for i in range (0, len(genotype)):
#                self.val += genotype[i] * math.pow(2, i-1)
#        else:
#            self.val = 0


#    def __init__(self, geneCount, val):
#        self.val = val
#        self.geneCount = geneCount
#        self.genotype = []
#        for i in range (0, geneCount):
#            if math.pow(2, geneCount - i - 1) < val:
#                self.genotype.append(1)
#                val -= math.pow(2, geneCount - i - 1)
#            else:
#                self.genotype.append(0)



