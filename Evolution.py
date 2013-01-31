import math
import random
import FitnessMeasure
import sys
from Individ import Individ

class Evolution:

    def __init__(self, fitnessMeasure, m = 5, n = 20, p = 2):
        self.m = m
        self.n = n
        self.p = p
        self.populationSize = m + n
        self.childPool = []
        self.adultPool = []
        self.fitnessMean = 0.0
        self.fitnessSD = 0.0
        self.fitnessMeasure = fitnessMeasure
        for i in range (0, self.n):
            individ = Individ(fitnessMeasure)
            self.childPool.append(individ)
    
    def generationStep(self):
        self.adultSelection()
        self.mateSelection()
        
        
    def adultSelection(self):
        
        self.fitnessMean = 0.0
        self.fitnessSD = 0.0
        
        for child in self.childPool:
            self.adultPool.append(child)
            self.childPool.remove(child)
        
        for i in range(0, len(self.adultPool)):
            self.fitnessMean += self.adultPool[i].fitness
        self.fitnessMean /= len(self.adultPool)
        
        for i in range(0, len(self.adultPool)):
            self.fitnessSD += math.pow((self.adultPool[i].fitness - self.fitnessMean), 2)
        self.fitnessSD /= len(self.adultPool)
        self.fitnessSD = math.pow(self.fitnessSD, 0.5)
        
        self.adultPool.sort(key=lambda individ: individ.fitness, reverse=True)
        
        while len(self.adultPool) > self.m:
            self.adultPool.pop();
        
        
    def mateSelection(self):
        for i in range(0, self.n):
            parents = []
            while len(parents) < 2:
                ticket = random.random() * self.fitnessMean * self.populationSize
                for individ in self.adultPool:
                    ticket -= individ.fitness
                    if ticket <= 0:
                        if parents.count(individ) == 0:
                            parents.append(individ)
                        break
            
            child = Individ(self.fitnessMeasure, parents)
            self.childPool.append(child)
        

if __name__ == '__main__':
    evolution = Evolution(FitnessMeasure.oneMax, 10, 20)
    print "genes: " + str(len(evolution.childPool[0].genotype))
    print "genotype2: " + str(evolution.childPool[2].genotype)
    print "genotype3: " + str(evolution.childPool[3].genotype)
    print "fitness2: " + str(evolution.childPool[2].fitness)
    print "fitness3: " + str(evolution.childPool[3].fitness)
    for i in range (0, 12):
        evolution.generationStep()
    
    print "individs: " + str(len(evolution.childPool) + len(evolution.adultPool))
    print "genes: " + str(len(evolution.adultPool[0].genotype))
    print "genotype: " + str(evolution.adultPool[2].genotype)
    print "genotype: " + str(evolution.adultPool[3].genotype)
    
    sys.stdin.readline()
    
        