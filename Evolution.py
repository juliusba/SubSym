import math
import random
import FitnessMeasure
import sys
import Individ
from operator import attrgetter
from Individ import Phenotype

class Evolution:

    def __init__(self, stopAfterGen = 1, m = 5, n = 20, p = 2):
        self.stopAfterGen = stopAfterGen
        self.m = m
        self.n = n
        self.p = p
        self.individs = []
        self.populationSize = m + n
        self.fitnessMean = 0.0
        self.fitnessSD = 0.0

    def run(self):
        for i in range (self.stopAfterGen):
            self.generationStep()
        
        print ("Populationsize: " + str(len(self.individs)))
        print ("Mean fitness: " + str(self.fitnessMean))
        print ("SD in fitness: " + str(self.fitnessSD))
        print ("Best fitness: " + str(self.fitnessBest.fitness))
                
        if sys.stdin.readline() == 'y':
            self.run()

    def generationStep(self):
        self.adultSelection()
        self.mateSelection()

    def adultSelection(self):
        self.fitnessTest()
        self.fitnessBest = max(self.individs, key = attrgetter('fitness'))
        
        self.fitnessMean = 0.0
        self.fitnessSD = 0.0
        for i in range(0, len(self.individs)):
            self.fitnessMean += self.individs[i].fitness
        self.fitnessMean /= len(self.individs)
        for i in range(0, len(self.individs)):
            self.fitnessSD += math.pow((self.individs[i].fitness - self.fitnessMean), 2)
        self.fitnessSD /= len(self.individs)
        self.fitnessSD = math.pow(self.fitnessSD, 0.5)
        
        self.individs.sort(key=lambda individ: individ.fitness, reverse=True)
        
        while len(self.individs) > self.m:
            self.individs.pop();
        
        
    def mateSelection(self):
        for i in range(0, self.n):
            parents = []
            while len(parents) < 2:
                ticket = random.random() * self.fitnessMean * self.populationSize
                for individ in self.individs:
                    ticket -= individ.fitness
                    if ticket <= 0:
                        if parents.count(individ) == 0:
                            parents.append(individ)
                        break
            
            child = self.individType(parents)
            self.individs.append(child)
        

if __name__ == '__main__':
    sys.stdin.readline()  