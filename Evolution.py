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
        #Global 1 - 10
        Fitness = 1
        Sigma = 2
        Boltz = 3
        Rank = 4
        #Local 11 - 20
        Tournament = 11


    m = 128   #number of grownups for mateselection
    n = 128  #number of children in population
    p = 2   #number of parents per child
    
    gray = False
    elitismFactor = 0.0
    tournamentCount = 1


    selectionStrategy = SelectionStrategy.Rank
    
    Boltz_T = 2
    Rank_Min = 0.5
    Rank_Max = 1.5
    TournamentE = 0.1
    TournamentK = 4

    noVarShown = False

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
                self.saveData()
                if i % 1 == 0:
                    self.print()

            self.plot()
            self.print()
            self.run()

    def saveData(self):
        self.meanFitness.append(str(round(self.fitnessMean, 2)))
        self.SDinFitness.append(str(round(self.fitnessSD, 2)))
        self.BestFitness.append(str(round(self.fitnessBest.fitness, 2)))

    def plot(self):
        p.plot(self.meanFitness, 'b')
        p.plot(self.SDinFitness, 'g')
        p.plot(self.BestFitness, 'r')
        #p.plot(self.avgEntropy, 'brown')

        p.legend(('mean','SD','Best', 'Entropy'))
        p.xlabel('Generation')
        p.ylabel('Value')
        p.title('Graph')
        p.grid(True)
        p.savefig('Graph.png')

    def generationStep(self):
        self.adultSelection()
        self.mateSelection()

    def adultSelection(self):
        self.fitnessMean = 0.0
        self.fitnessSD = 0.0
        for individ in self.individs:
            individ.fitness = 0
            individ.tournamentNr = -1

        tested = 0
        for i in range (0, Evolution.tournamentCount):
            contesters = []
            for j in range (0, math.ceil(len(self.individs)/Evolution.tournamentCount)):
                while True:
                    index = rnd.randint(0, len(self.individs) - 1)
                    if self.individs[index].tournamentNr == -1:
                        break
                contesters.append(self.individs[index])
                self.individs[index].tournamentNr = j
                tested += 1
                if tested == len(self.individs):
                    break
            self.fitnessTest(contesters)
        self.fitnessBest = max(self.individs, key = attrgetter('fitness'))
        
        for i in range(0, len(self.individs)):
            self.fitnessMean += self.individs[i].fitness
        self.fitnessMean /= len(self.individs)
        for i in range(0, len(self.individs)):
            self.fitnessSD += math.pow((self.individs[i].fitness - self.fitnessMean), 2)
        self.fitnessSD /= len(self.individs)
        self.fitnessSD = math.pow(self.fitnessSD, 0.5)
        if self.fitnessSD == 0 and not Evolution.noVarShown:
            print("No variation in fitness!")
            Evolution.noVarShown = True
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
        if Evolution.selectionStrategy <= 10:
            if Evolution.selectionStrategy == Evolution.SelectionStrategy.Fitness:
                self.fitnessProportionate()
            elif Evolution.selectionStrategy == Evolution.SelectionStrategy.Sigma:
                self.sigmaVal()
            elif Evolution.selectionStrategy == Evolution.SelectionStrategy.Boltz:
                self.boltzVal()
            elif Evolution.selectionStrategy == Evolution.SelectionStrategy.Rank:
                self.rankVal()

            self.sumExpVal = 0
            for individ in self.individs:
                self.sumExpVal += individ.expVal

        childPool = []
        for i in range(0, round(self.n/self.p)):
            parents = []
            while len(parents) < self.p:
                
                if Evolution.selectionStrategy > 10:
                    contesters = []
                    for j in range (0, Evolution.TournamentK):
                        while True:
                            index = rnd.randint(0, len(self.individs) - 1)
                            if contesters.count(self.individs[index]) == 0:
                                break
                        contesters.append(self.individs[index])
                    if rnd.random() < Evolution.TournamentE:
                        parents.append(contesters[rnd.randint(0, len(contesters) - 1)])
                    else:
                        parents.append(max(contesters, key = attrgetter('fitness')))

                else:
                    ticket = rnd.random() * self.sumExpVal
                    for individ in self.individs:
                        ticket -= individ.expVal
                        if ticket <= 0:
                            if parents.count(individ) == 0:
                                parents.append(individ)
                            break
            
            #child = self.individType(parents, Evolution.gray)
            #childPool.append(child)
            childPool.extend(self.mate(parents))

        for i in range (0, round(len(self.individs) * (1 - Evolution.elitismFactor))):
            self.individs.pop()

        self.individs.extend(childPool)

    def mate(self, parents):
        crossovers = []
        parentIndex = 0
        i = 0
        for pheno in parents[0].dna:
            crossovers.append([])
            for j in range(0, len(pheno.genotype)):
                if rnd.random() < Individ.crossoverRate:
                    parentIndex = (parentIndex + 1) % len(parents)
                crossovers[i].append(parentIndex)
            i += 1
        children = []
        children.append(self.individType(parents, crossovers, Evolution.gray))
        
        for p in range(1, len(parents)):
            i = 0
            for pheno in parents[0].dna:
                for j in range(0, len(pheno.genotype)):
                    crossovers[i][j] = (crossovers[i][j] + 1) % len(parents)
                i += 1
            children.append(self.individType(parents, crossovers, Evolution.gray))
        
        return children

    def fitnessProportionate(self):
        for individ in self.individs:
            individ.expVal = individ.fitness
            #print(individ.expVal)

    def sigmaVal(self):
        for individ in self.individs:
            individ.expVal = 1 + ((individ.fitness - self.fitnessMean) / max(2 * self.fitnessSD, 0.0001))
            individ.expVal = max(0, individ.expVal)

    def boltzVal(self):
        sumFitnessExp = 0
        for individ in self.individs:
            individ.fitnessExp = math.exp(individ.fitness/Evolution.Boltz_T)
            sumFitnessExp += individ.fitnessExp
        avgFitnessExp = sumFitnessExp/len(self.individs)
        for individ in self.individs:
            individ.expVal = individ.fitnessExp / avgFitnessExp

    def rankVal(self):
        for i in range (0, len(self.individs)):
            self.individs[i].expVal = Evolution.Rank_Min + (Evolution.Rank_Max - Evolution.Rank_Min) * (((len(self.individs) - 1) - i + 1) / (len(self.individs) - 1))

    def print(self):
        pass
        #print ("Populationsize: " + str(len(self.individs)))
        #print ("Mean fitness: " + str(round(self.fitnessMean, 2)))
        #print ("SD in fitness: " + str(round(self.fitnessSD, 2)))
        #print ("Best fitness: " + str(round(self.fitnessBest.fitness, 2)))

if __name__ == '__main__':
    sys.stdin.readline()