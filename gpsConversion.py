# -*- coding: utf-8 -*-
"""
Created on Thu Mar 24 12:14:26 2016

@author: student
"""

g = "52 deg 0' 42.60\" N, 4 deg 21' 34.21\" E"

def gpsStringToNumV(g):
    p = g.split(",")
    (gpsNToNumV(p[0]), gpsEToNumV(p[1]))

def gpsNToNumV(l):
    float(l.split(" ")[3].split("\"")[0])
    
def gpsEToNumV(l):
    r = l.split(" ")
    m = float(r[3].split("'")[0])-21
    s = float(r[4].split("\"")[0])
    60*m+s

def numVToGps(n):
    # Needs to be defined