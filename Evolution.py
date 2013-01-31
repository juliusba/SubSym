import math
import random
import FitnessMeasure
import sys
import operator
from Individ import Individ
from ctypes.wintypes import DOUBLE

class Evolution:
    '''
    individs = []
    
    p = int
    m = int
    n = int
    populationSize = int
    
    fitnessMean = float
    fitnessSD = float
    '''
    def __init__(self, fitnessMeasure, m = 10, n = 20, p = 2):
        self.m = m
        self.n = n
        self.p = p
        self.populationSize = m + n
        self.individs = []
        for i in range (0, self.populationSize):
            individ = Individ(fitnessMeasure)
            self.individs.append(individ)
    
    def generationStep(self, fitnessMeasure):
        for i in range(0, len(self.individs)):
            self.fitnessMean += self.individs[i].fitness
        self.fitnessMean /= len(self.individs)
        
        for i in range(0, len(self.individs)):
            self.fitnessSD += math.pow((self.individs[i].fitness - self.fitnessMean), 2)
        self.fitnessSD /= len(self.individs)
        self.fitnessSD = math.pow(self.fitnessSD, 0.5)
        
        self.mateSelection(fitnessMeasure)
        self.adultSelection()
            
    def adultSelection(self):
        self.individs.sort(cmp=Individ, key= operator.attrgetter('fitness'), reverse=False)
        for individ in self.individs:
            print individ.fitness
        
    def mateSelection(self, fitnessMeasure):
        for i in range(0, self.n):
            parents = []
            while len(parents) < 2:
                ticket = random.random() * self.fitnessMean * self.populationSize
                print ticket
                for individ in self.individs:
                    ticket -= individ.fitness
                    if ticket <= 0:
                        if parents.count(individ) == 0:
                            parents.append(individ)
                        break
            
            print len(parents)
            child = Individ(fitnessMeasure, parents)
            self.individs.append(child)
        

if __name__ == '__main__':
    evolution = Evolution(FitnessMeasure.oneMax, 10, 20)
    print "individs: " + str(len(evolution.individs))
    print "genes: " + str(len(evolution.individs[0].genotype))
    print "genotype: " + str(evolution.individs[2].genotype)
    print "genotype: " + str(evolution.individs[3].genotype)
    for i in range (0, 50):
        evolution.generationStep(FitnessMeasure.oneMax)
    
    print "individs: " + str(len(evolution.individs))
    print "genes: " + str(len(evolution.individs[0].genotype))
    print "genotype: " + str(evolution.individs[2].genotype)
    print "genotype: " + str(evolution.individs[3].genotype)
    
    sys.stdin.readline()
    
        