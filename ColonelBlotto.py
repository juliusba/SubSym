import math
from Strategy import *
from Evolution import Evolution
#import pylab as p
import matplotlib.pyplot as p
import numpy as np

class ColonelBlotto(Evolution):

    RF = 1.0
    LF = 0.0
    B = 10

    def __init__(self):
        super().__init__()
        Strategy.B = ColonelBlotto.B
        for i in range (round(Evolution.m * Evolution.elitismFactor) + Evolution.n):
            self.individs.append(Strategy([], self.gray))
        self.individType = Strategy

    def fitnessTest(self, individs):
        for i in range (0, len(individs)):
            #self.individs[i].fitness = 0
            for j in range (len(individs) - 1, i, -1):
                res = self.runWar([individs[i], individs[j]])
                if res == [0]:
                    individs[i].fitness += 2
                    #print ( individs[i].dna[0].val - individs[j].dna[0].val)
                elif res == [1]:
                    individs[j].fitness += 2
                elif res == [0, 1]:
                    individs[i].fitness += 1
                    individs[j].fitness += 1
                else:
                    print ("OMGOMGOMGOMGOMGOMG")

    def runWar(self, strategies):
        battlePoints = [0] * len(strategies)
        for s in strategies:
            s.rf = 0.0
            s.strength = 1.0
            s.battlePoints = 0
        for i in range (self.B):
            temp = strategies[:]
            temp.sort(key=lambda strategy: (strategy.resourceDistrib[i] + strategy.rf) * strategy.strength, reverse=True)
            for j in range (1, len(strategies)):
                #print(temp[0].rf - temp[j].rf)  
                dif = (temp[0].resourceDistrib[i] + temp[0].rf) * temp[0].strength - (temp[j].resourceDistrib[i] + temp[j].rf) * temp[j].strength
                if dif > 0:
                    #print(temp[0].rf - temp[j].rf)
                    if j == 1:
                        #print(dif * ColonelBlotto.RF / (ColonelBlotto.B - (i + 1)))
                        if i != ColonelBlotto.B -1:
                            temp[0].rf += dif * ColonelBlotto.RF / (ColonelBlotto.B - (i + 1))
                    for k in range(0, j):
                        temp[k].battlePoints += 1.0 / (j + 1)
                    for p in range(j, len(strategies)):
                        temp[k].strength *= (1 - ColonelBlotto.LF)

        warWinners = [0]
        for i in range (1, len(strategies)):
            if strategies[i].battlePoints > strategies[warWinners[0]].battlePoints:
                warWinners = [i]
            elif strategies[i].battlePoints == strategies[warWinners[0]].battlePoints:
                warWinners.append(i)
        return warWinners

    def print(self):
        super().print()
        resourceDistrib = "| "
        entropy = 0
        for battleProportion in self.fitnessBest.resourceDistrib:
            resourceDistrib += str(round(battleProportion, 2)) + " | "
            if battleProportion != 0:
               entropy -= battleProportion * math.log(battleProportion, 2)
        resourceDistrib += "\n| "
        for pheno in self.fitnessBest.dna:
            resourceDistrib += str(pheno.val) + " | "
        resourceDistrib.strip()
        print (resourceDistrib)
        print (entropy)

if __name__ == '__main__':
    Evolution.gray = True
    Evolution.m = 10
    Evolution.n = 20
    Evolution.p = 2

    ColonelBlotto.RF = 1.0
    ColonelBlotto.LF = 0.0
    ColonelBlotto.B = 10

    colonelBlotto = ColonelBlotto()
    i = Strategy()
    for p in i.dna:
        p.val = 0
        for b in p.genotype:
            b = 0
    i.dna[0].val = 15
    for b in i.dna[0].genotype:
        b = 1
    colonelBlotto.individs.append(i)
    colonelBlotto.run()