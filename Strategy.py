from Individ import Individ

class Strategy(Individ):
    
    B = 10
    blueprint = [10] * B

    def __init__(self, parents = []):
        super().__init__(Strategy.blueprint, parents)
        self.resourceDistrib = []
        sum = 0
        for pheno in self.dna:
            sum += pheno.val

        if sum != 0:
            for pheno in self.dna:
                self.resourceDistrib.append(pheno.val / sum)
        else:
            for pheno in self.dna:
                self.resourceDistrib.append(1 / len(self.dna))