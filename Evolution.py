import math
import random
import sys
from pylab import *
import numpy
from Individ import Individ
from operator import attrgetter
from Individ import Phenotype

class Evolution:

    def __init__(self, gray = False, m = 5, n = 20, p = 2):
        self.gray = gray
        self.m = m
        self.n = n
        self.p = p
        self.individs = []
        self.populationSize = m + n
        self.fitnessMean = 0.0
        self.fitnessSD = 0.0

    def run(self):
        print("\nPlease wright the number of generations you wish to add, or press enter to exit.")
        answer = sys.stdin.readline()[:-1]
        if answer != "":
            for i in range (int(answer)):
                self.generationStep()
            self.print()
            self.run()

    def generationStep(self):
        self.adultSelection()
        self.mateSelection()

    def adultSelection(self):
        self.fitnessMean = 0.0
        self.fitnessSD = 0.0
        for individ in self.individs:
            individ.fitness = 0

        self.fitnessTest()
        self.fitnessBest = max(self.individs, key = attrgetter('fitness'))
        
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
        picked = []
        for i in range(0, self.n):
            parents = []
            while len(parents) < self.p:
                ticket = random.random() * self.fitnessMean * self.populationSize
                for individ in self.individs:
                    ticket -= individ.fitness
                    if ticket <= 0:
                        if parents.count(individ) == 0 and picked.count(individ) == 0:
                            parents.append(individ)
                        break
            
            child = self.individType(parents, self.gray)
            self.individs.append(child)

            picked.append(parents)
        
    def print(self):
        print ("Populationsize: " + str(len(self.individs)))
        print ("Mean fitness: " + str(round(self.fitnessMean, 2)))
        print ("SD in fitness: " + str(round(self.fitnessSD, 2)))
        print ("Best fitness: " + str(round(self.fitnessBest.fitness, 2)))

if __name__ == '__main__':
    #x = [1,2,3]
    #y = [4,6,5]
    #pylab.plot(x,y)
    #pylab.show()
    print("lol")
    plot([1,2,3,4], [1,4,9,16])
    savefig('wykresik.png')

    sys.stdin.readline()  