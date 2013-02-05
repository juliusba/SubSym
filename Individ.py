'''
Created on 31. jan. 2013

@author: juliusbuset
'''
import random
from ctypes.wintypes import DOUBLE

class Individ(object):
    '''
    classdocs
    '''
    '''
    genotype = []
    fitness = float
    '''
    def __init__(self, fitnessMeasure, parents = []):
        '''
        Constructor
        '''
        self.genotype = []
        if parents == []:
            for i in range (0,20):
                self.genotype.append(random.randint(0,1))
        else:
            for i in range (0,20):
                if random.random() < 0.01:
                    gen = random.randint(0,1)
                else:
                    gen = parents[random.randint(0, len(parents)-1)].genotype[i]
                self.genotype.append(gen)
        
        self.fitness = fitnessMeasure(self)

    def lol():
        pass