from Individ import Individ

class Strategy(Individ):

    B = 10
    Blueprint = [4] * B

    def __init__(self, parents = [], gray = False):
        super().__init__(Strategy.Blueprint, parents, gray)
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