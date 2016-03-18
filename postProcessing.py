# -*- coding: utf-8 -*-
"""
Takes a list of tripples, the first for the x coordinate and second for a y coordinate and the match likeleyness as third. 
returns a triplet with the x and y coords and a variance field

Created on Fri Mar 18 16:06:50 2016

@author: Youri Arkesteijn
"""
import numpy as np


"""
This function calculates the mean of the probabilities and removes all items with a prob less than the mean.
"""
def filterList(l) : filter(lambda e: e[2] > sum(map(lambda x: x[2]/len(l), l)), l)
    
"""
Gets the weigted average of the position
"""
def getAveragePosition(l) : (sum(map(lambda x: x[0]/len(l), l)), sum(map(lambda x: x[1]/len(l), l)))
    
"""
Get the 1d samplesize variance.
"""
def calculateVariance(p) : 

def getVarianceTuple(p) : 