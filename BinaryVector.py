from Individ import Individ

class BinaryVector(Individ):
    
    blueprint = [40]

    def __init__(self, parents = [], crossovers = [], gray = False):
        super().__init__(BinaryVector.blueprint, parents, crossovers, gray)