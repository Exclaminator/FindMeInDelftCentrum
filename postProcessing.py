# -*- coding: utf-8 -*-
"""
Takes a list of tripples, the first for the x coordinate and second for a y coordinate and the match likeleyness as third. 
returns a triplet with the x and y coords and a variance field

Created on Fri Mar 18 16:06:50 2016

@author: Youri Arkesteijn
"""
import numpy as np

 (lambda S (x) (S (- x 1))) => (let (fn (lambda (f) (lambda (x) (f (- x 1))))) (fn fn))  


"""
This function calculates the mean of the probabilities and removes all items with a prob less than the mean.
"""
def filterList(l) : filter(lambda e: e[2] > sum(map(lambda x: x[2]/len(l), l)), l)
    
"""
Gets the weigted average of the position
"""
def getAveragePosition(l, a) : sum(map(lambda x: x[a]/len(l), l))
    
"""
Get the 1d samplesize variance.
"""
def calculateVariance(l, a) : np.var(map(lambda x: x[a], l))

def getVarianceTuple(l) : (calculateVariance(l, 0), calculateVariance(l, 1))
    
def getPoints(p) : 
    l = filterList(p)
    (getAveragePosition(l, 0), getAveragePosition(l, 1), getVarianceTuple(l))