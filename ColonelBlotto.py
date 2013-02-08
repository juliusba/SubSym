import math
from Strategy import Strategy
from Evolution import Evolution

class ColonelBlotto(Evolution):

    def __init__(self, stopAfterGen = 1, RF = 0.0, LF = 0.0, B = 10, m = 10, n = 20, p = 2):
        super().__init__(stopAfterGen, m, n, p)
        self.RF = RF
        self.LF = LF
        self.B = B
        for i in range (self.populationSize):
            self.individs.append(Strategy())

        self.individType = Strategy

    def fitnessTest(self):
        for i in range (0, len(self.individs)):
            self.individs[i].fitness = 0
            for j in range (len(self.individs) - 1, i, -1):
                res = self.runWar([self.individs[i], self.individs[j]])
                if res == [0]:
                    self.individs[i].fitness += 2
                elif res == [1]:
                    self.individs[j].fitness += 2
                elif res == [0, 1]:
                    self.individs[i].fitness += 1
                    self.individs[j].fitness += 1
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
                dif = (temp[0].resourceDistrib[i] + temp[0].rf) * temp[0].strength - (temp[j].resourceDistrib[i] + temp[j].rf) * temp[j].strength
                if dif > 0:
                    if j == 1:
                        temp[0].rf += dif * self.RF
                    for k in range(0, j):
                        temp[k].battlePoints += 1.0 / (j + 1)
                    for p in range(j, len(strategies)):
                        temp[k].strength -= self.LF

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
        for battleProportion in self.fitnessBest.resourceDistrib:
            resourceDistrib += str(round(battleProportion, 2)) + " | "
        resourceDistrib += "\n| "
        for pheno in self.fitnessBest.dna:
            resourceDistrib += str(pheno.val) + " | "
        resourceDistrib.strip()
        print (resourceDistrib)

if __name__ == '__main__':
    
    colonelBlotto = ColonelBlotto(10, 0.3, 0.3)

    colonelBlotto.run()