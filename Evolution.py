import math
import random
import sys
from operator import attrgetter
import io,json

from Individ import Individ
from Individ import Phenotype

class Evolution:

    m = 5   #number of grownups for mateselection
    n = 20  #number of children in population
    p = 2   #number of parents per child
    
    gray = False

    minSDratio = 0.1
    maxSDration = 0.5

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
        
        self.fitnessSDratio = self.fitnessSD / self.fitnessMean
        if (self.fitnessSDratio > Evolution.maxSDration):
            for individ in self.individs:
                individ.fitness *= (Evolution.maxSDration / self.fitnessSDratio)
        elif (self.fitnessSDratio < Evolution.minSDratio):
            for individ in self.individs:
                individ.fitness *= (Evolution.minSDration / self.fitnessSDratio)

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

class O:
    def __init__(self):
        self.a = "omg"
        self.b = 4

if __name__ == '__main__':
    #c = O()
    ##json.dumps(c, default=lambda o: o.__dict__)
    #data = [ { 'a':'A', 'b':(2, 4), 'c':3.0 } ]
    #with io.open('data.txt', 'w', encoding='utf-8') as outfile:
    #    json.dump(c, outfile)
    sys.stdin.readline()  