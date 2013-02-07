from Strategy import Strategy
from Evolution import Evolution

class ColonelBlotto(Evolution):

    def __init__(self, stopAfterGen = 1, B = 10, m = 10, n = 20, p = 2):
        super().__init__(stopAfterGen, m, n, p)
        self.B = B
        for i in range (self.populationSize):
            self.individs.append(Strategy())

        self.individType = Strategy

    def fitnessTest(self):
        for i in range (0, len(self.individs)):
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
        for i in range (self.B):
            winnerIndexes = [0]
            for j in range (1, len(strategies)):
                if strategies[j].resourceDistrib[i] > strategies[winnerIndexes[0]].resourceDistrib[i]:
                    winnerIndexes = [j]
                elif strategies[j].resourceDistrib[i] == strategies[winnerIndexes[0]].resourceDistrib[i]:
                    winnerIndexes.append(j)
            for index in winnerIndexes:
                battlePoints[index] += 1 / len(winnerIndexes)

        warWinners = [0]
        for i in range (1, len(strategies)):
            if battlePoints[i] > battlePoints[winnerIndexes[0]]:
                warWinners = [i]
            elif battlePoints[i] == battlePoints[winnerIndexes[0]]:
                warWinners.append(i)
        return warWinners

if __name__ == '__main__':
    
    colonelBlotto = ColonelBlotto()

    colonelBlotto.run()