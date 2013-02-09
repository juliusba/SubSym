from Individ import Individ

class BinaryVector(Individ):
    
    blueprint = [20]

    def __init__(self, parents = [], gray = False):
        super().__init__(BinaryVector.blueprint, parents, gray)