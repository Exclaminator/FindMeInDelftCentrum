#!/usr/bin/env python

import argparse
import pickle
import cv2
import matplotlib.pyplot as plt
import numpy as np
import feature_extraction as ft
import sys
import image_search
import os
import os.path
import metadata_distance 
from PIL import Image

# global variable
sift_candidates = None


#This is an adapted version of the original query.py. Instead of using a Argument Parser, we changed to a function with two arguments:
#The database and the list of images we want to query. Each of the images is processed one by one. Then the function returns both a 
#list of image names and a list of distances linked to this image.
def sifting(database, im_list):

    base = os.path.splitext(database)[0] 
    db_name = database
    search = image_search.Searcher(db_name)
    
    print 'Loading SIFT vocabulary ...'
    fname = base + '_sift_vocabulary.pkl'
    # Load the vocabulary to project the features of our query image on
    with open(fname, 'rb') as f:
        sift_vocabulary = pickle.load(f)
        
    all_winners = []
    all_distances = []        
    count = 0
    print 'Start processing each of the interesting frames'
    for im in im_list: 
        count = count + 1
        result = Image.fromarray((im).astype(np.uint8))
        
        #Save the image to a temporary file
        result.save('out.jpg')
        query = 'out.jpg' 
        
        sift_query = ft.get_sift_features([query])[query]
        # Get a histogram of visual words for the query image
        image_words = sift_vocabulary.project(sift_query)
        # Use the histogram to search the database
        sift_candidates = search.query_iw('sift', image_words)
    
        sift_winners = [search.get_filename(cand[1]) for cand in sift_candidates][0:10]
        sift_distances = [cand[0] for cand in sift_candidates][0:10]
        
        
        for win in sift_winners:
            all_winners.append(win)
        
        for dis in sift_distances:
            all_distances.append(dis)
        
        print 'Progress: ', count, '/' , len(im_list), ' frames processed'
        
    os.remove('out.jpg')
    return all_winners, all_distances       





