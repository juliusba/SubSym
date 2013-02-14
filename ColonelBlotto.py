import math
from Strategy import *
from Evolution import Evolution
#import pylab as p
import matplotlib.pyplot as p
import numpy as np

class ColonelBlotto(Evolution):

    RF = 2.0
    LF = 0.0
    B = 10

    def __init__(self):
        super().__init__()
        Strategy.B = ColonelBlotto.B
        for i in range (round(Evolution.m * Evolution.elitismFactor) + Evolution.n):
            self.individs.append(Strategy([], self.gray))
        self.individType = Strategy

    def saveData(self):
        super().saveData()
        entropy = 0
        for individ in self.individs:
            for b in individ.resourceDistrib:
                if b != 0:
                    entropy -= b * math.log2(b)
        entropy /= len(self.individs)
        entropy *= 20
        self.avgEntropy.append(entropy)

    def fitnessTest(self, individs):
        for i in range (0, len(individs)):
            #self.individs[i].fitness = 0
            for j in range (len(individs) - 1, i, -1):
                res = self.runWar([individs[i], individs[j]])
                if res == [0]:
                    individs[i].fitness += 2
                elif res == [1]:
                    individs[j].fitness += 2
                elif res == [0, 1]:
                    individs[i].fitness += 1
                    individs[j].fitness += 1
                else:
                    
                    ("OMGOMGOMGOMGOMGOMG")

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
                dif = (temp[0].resourceDistrib[i] + temp[0].rf) * temp[0].strength - (temp[j].resourceDistrib[i] + temp[j].rf) * temp[j].strength
                if dif > 0:
                    if j == 1:
                        if i != ColonelBlotto.B -1:
                            temp[0].rf += dif * ColonelBlotto.RF / (ColonelBlotto.B - (i + 1))
                    for k in range(0, j):
                        temp[k].battlePoints += 1.0 / (j + 1)
                    for p in range(j, len(strategies)):
                        temp[p].strength *= (1 - ColonelBlotto.LF)

        warWinners = [0]
        for i in range (1, len(strategies)):
            if strategies[i].battlePoints > strategies[warWinners[0]].battlePoints:
                warWinners = [i]
            elif strategies[i].battlePoints == strategies[warWinners[0]].battlePoints:
                warWinners.append(i)

        return warWinners

    def print(self):
        super().print()
        resourceDistrib = "|"
        for battleProportion in self.fitnessBest.resourceDistrib:
            resourceDistrib += str(round(battleProportion, 2)) + "|"
        #resourceDistrib += "\n| "
        #for pheno in self.fitnessBest.dna:
        #    resourceDistrib += str(pheno.val) + "|"
        #resourceDistrib.strip()
        print (resourceDistrib + "  --- entropy: " + str(round(self.avgEntropy[len(self.avgEntropy)-1],2)))

if __name__ == '__main__':
    Individ.crossoverRate = 0.2
    Individ.mutationRate = 0.065
    
    Evolution.gray = True
    Evolution.m = 10
    Evolution.n = 20
    Evolution.p = 2
    Evolution.elitismFactor = 1.0

    Evolution.selectionStrategy = Evolution.SelectionStrategy.Tournament
    Evolution.Boltz_T = 2
    Evolution.Rank_Max = 1.5
    Evolution.Rank_Min = 0.5
    Evolution.TournamentE = 0.1
    Evolution.tournamentK = 5

    ColonelBlotto.RF = 1.0
    ColonelBlotto.LF = 0.0

    colonelBlotto = ColonelBlotto()
    colonelBlotto.run()