import math
import random as rnd
import sys
from operator import attrgetter
import io,json
import matplotlib.pyplot as p
import numpy as np

from Individ import Individ
from Individ import Phenotype

class Evolution:

    class SelectionStrategy:
        Sigma = 1
        Boltz = 2
        Rank = 3

    m = 5   #number of grownups for mateselection
    n = 20  #number of children in population
    p = 2   #number of parents per child
    
    gray = False
    elitismFactor = 1.0
    tournamentCount = 1

    selectionStrategy = SelectionStrategy.Sigma
    
    Boltz_T = 2
    Rank_Min = 0.5
    Rank_Max = 1.5


    def __init__(self):
        self.individs = []
        #self.populationSize = Evolution.m + Evolution.n
        self.fitnessMean = 0.0
        self.fitnessSD = 0.0
        self.meanFitness = [0]
        self.SDinFitness = [0]
        self.BestFitness = [0]

    def run(self):
        print("\nPlease wright the number of generations you wish to add, or press enter to exit.")
        answer = sys.stdin.readline()[:-1]
        print ("")
        if answer != "":
            for i in range (int(answer)):
                print(str(round(i*100/int(answer))), end=" %\r")
                self.generationStep()
                self.meanFitness.append(str(round(self.fitnessMean, 2)))
                self.SDinFitness.append(str(round(self.fitnessSD, 2)))
                self.BestFitness.append(str(round(self.fitnessBest.fitness, 2)))

            l1 = p.plot(self.meanFitness, 'b')
            l2 = p.plot(self.SDinFitness, 'g')
            l3 = p.plot (self.BestFitness, 'r')
        
            p.legend(('mean','SD','Best'))
            p.xlabel('Generation')
            p.ylabel('Value')
            p.title('Graph')
            p.grid(True)
            p.savefig('Graph.png')

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
        #    individ.tested = False

        #tested = 0
        #for i in range (0, Evolution.tournamentCount):
        #    contesters = []
        #    for j in range (0, math.ceil(len(self.individs)/Evolution.tournamentCount)):
        #        while True:
        #            index = rnd.randint(0, len(self.individs) - 1)
        #            if self.individs[index].tested == False:
        #                break
        #        contesters.append(self.individs[index])
        #        self.individs[index].tested = True
        #        tested += 1
        #        if tested == len(self.individs):
        #            break
        #    self.fitnessTest(contesters)
        self.fitnessTest(self.individs)
        self.fitnessBest = max(self.individs, key = attrgetter('fitness'))
        
        for i in range(0, len(self.individs)):
            self.fitnessMean += self.individs[i].fitness
        self.fitnessMean /= len(self.individs)
        for i in range(0, len(self.individs)):
            self.fitnessSD += math.pow((self.individs[i].fitness - self.fitnessMean), 2)
        self.fitnessSD /= len(self.individs)
        self.fitnessSD = math.pow(self.fitnessSD, 0.5)
        if self.fitnessSD == 0:
            print("No variation in fitness!")
            sys.stdin.readline()

        #self.fitnessSDratio = self.fitnessSD / self.fitnessMean
        #if (self.fitnessSDratio > Evolution.maxSDration):
        #    for individ in self.individs:
        #        individ.fitness *= (Evolution.maxSDration / self.fitnessSDratio)
        #elif (self.fitnessSDratio < Evolution.minSDratio):
        #    for individ in self.individs:
        #        individ.fitness *= (Evolution.minSDration / self.fitnessSDratio)

        self.individs.sort(key=lambda individ: individ.fitness, reverse=True)
        
        while len(self.individs) > self.m:
            self.individs.pop();
        
        
    def mateSelection(self):
        if Evolution.selectionStrategy == Evolution.SelectionStrategy.Sigma:
            self.sigmaVal()
        elif Evolution.selectionStrategy == Evolution.SelectionStrategy.Boltz:
            self.boltzVal()
        elif Evolution.selectionStrategy == Evolution.SelectionStrategy.Rank:
            self.rankVal()

        self.sumExpVal = 0
        for individ in self.individs:
            self.sumExpVal += individ.expVal
            #print(str(individ.expVal) + " - " + str(individ.fitness))

        childPool = []
        for i in range(0, self.n):
            parents = []
            while len(parents) < self.p:
                ticket = rnd.random() * self.sumExpVal
                #print(ticket)
                for individ in self.individs:
                    ticket -= individ.expVal
                    if ticket <= 0:
                        if parents.count(individ) == 0:
                            parents.append(individ)
                        break
            
            child = self.individType(parents, Evolution.gray)
            childPool.append(child)

        for i in range (len(self.individs), round(len(self.individs) * (1 - Evolution.elitismFactor)), -1):
            self.individs.pop()

        self.individs.extend(childPool)

    def sigmaVal(self):
        for individ in self.individs:
            individ.expVal = individ.fitness#(individ.fitness - self.fitnessMean) / (2 * self.fitnessSD)
            #print(individ.expVal)

    def boltzVal(self):
        sumFitnessExp = 0
        for individ in self.individs:
            individ.fitnessExp = math.exp(individ.fitness/Evolution.Rank_T)
            sumFitnessExp += individ.fitnessExp
        avgFitnessExp = sumFitnessExp/len(self.individs)
        for individ in self.individs:
            individ.expVal = individ.fitnessExp / avgFitnessExp

    def rankVal(self):
        for i in range (0, len(self.individs)):
            self.individs[i].expVal = Evolution.Rank_Min + (Evolution.Rank_Max - Evolution.Rank_Min) * (((len(self.individs) - 1) - i + 1) / (len(self.individs) - 1))

    def print(self):
        
        print ("Populationsize: " + str(len(self.individs)))
        print ("Mean fitness: " + str(round(self.fitnessMean, 2)))
        print ("SD in fitness: " + str(round(self.fitnessSD, 2)))
        print ("Best fitness: " + str(round(self.fitnessBest.fitness, 2)))

if __name__ == '__main__':
    #c = O()
    ##json.dumps(c, default=lambda o: o.__dict__)
    #data = [ { 'a':'A', 'b':(2, 4), 'c':3.0 } ]
    #with io.open('data.txt', 'w', encoding='utf-8') as outfile:
    #    json.dump(c, outfile)
    sys.stdin.readline()