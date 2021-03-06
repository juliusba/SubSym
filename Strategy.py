from ColonelBlotto import ColonelBlotto
from Individ import Individ

class Strategy(Individ):

    Blueprint = [4] * ColonelBlotto.B

    def __init__(self, parents = [], crossovers = [], gray = False):
        super().__init__(Strategy.Blueprint, parents, crossovers, gray)
        self.resourceDistrib = []
        sum = 0
        for pheno in self.dna:
            sum += pheno.val
        if sum != 0:
            for pheno in self.dna:
                self.resourceDistrib.append(float(pheno.val) / sum)
        else:
            for pheno in self.dna:
                self.resourceDistrib.append(1.0 / len(self.dna))