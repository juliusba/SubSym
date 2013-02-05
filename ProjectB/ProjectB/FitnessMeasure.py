'''
Created on 31. jan. 2013

@author: juliusbuset
'''

def oneMax(individ):
    fitnessMeasure = 0.0
    for i in range (0, len(individ.genotype)):
        if individ.genotype[i] == 1:
            fitnessMeasure += 1
            
    fitnessMeasure /= len(individ.genotype)
    return fitnessMeasure