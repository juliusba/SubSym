from Evolution import Evolution
from BinaryVector import BinaryVector

class OneMax(Evolution):
    
    def __init__(self, m = 5, n = 20, p = 2):
        super().__init__(False, m, n, p)

        for i in range (self.populationSize):
            self.individs.append(BinaryVector())

        self.individType = BinaryVector

    def fitnessTest(self):
        for individ in self.individs:
            for bit in individ.dna[0].genotype:
                individ.fitness += bit

    def print(self):
        super().print()

if __name__ == '__main__':
    
    oneMax = OneMax()

    oneMax.run()