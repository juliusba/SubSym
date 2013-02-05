from Individ import Individ

class Strategy(Individ):
    

    def __init__(self, B, parents = []):
        super().__init__(fitnessMeasure, B*4, parents)
        self.resourceDistrib = []
        for i in range (0, B):
            self.resourceDistrib.append(super().phenoFromGeno(i, B))