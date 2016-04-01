import argparse
import numpy as np
import cv2
from video_tools import *
import feature_extraction as ft    
from video_features import *
import image_search
import os.path
import pickle
import query
from PIL import Image
import re

#Program to detect the interesting frams of a video. Takes as input a video-file
#and returns an array of frames which contain interesting data to analyze.

#Converting an array of 2 numbers to a GPS-Coordinate
def numVToGps(n):
    s = n[1]%60
    m = ((n[1]-s)/60) + 21.0
    return "52°0'"+str(n[0])+"\"N, 4°"+str(m)+"'"+str(s)+"\"E"

#The argumentparser, which takes 1 argument: the path to the video-file you want to analyze
parser = argparse.ArgumentParser(description="Video Query tool")
parser.add_argument("query", help="query video")
args = parser.parse_args()

#Getting frame-rate, frame-count and video duration from the input video.
cap = cv2.VideoCapture(args.query)
frame_count = get_frame_count(args.query) + 1
frame_rate = get_frame_rate(args.query )
q_total = get_duration(args.query)

#Initializing the previous frame to nothing
prev_frame = None
frame_nbr = 0
cap.set(cv2.CAP_PROP_POS_MSEC, 0)

#Matrices for storing color histogram data and temporal difference data.
ch_features = []
td_features = []

#Matrix for storing the frames
frames = []

#Reading the frames and calculating the color histograms and temporal differences

#Use the following line if you want to analyze the entire video, currently only the first 10% of the video is looked at
print("Start reading")
while(cap.isOpened() and cap.get(cv2.CAP_PROP_POS_MSEC) < q_total * 1000):

#while(cap.isOpened() and cap.get(cv2.CAP_PROP_POS_MSEC) < q_total * 100):
    ret, frame = cap.read()
    
    if frame == None:
        break

    h_ch = ft.colorhist(frame)
    h_td = temporal_diff(prev_frame, frame, 10)
    if (h_ch != None) and (h_td != None):
        frames.append(frame)
        ch_features.append(h_ch)
        td_features.append(h_td)
        
    prev_frame = frame
    frame_nbr += 1

#Matrix for storing interesting frames    
interesting_frames = []

#Integer that keeps track how much the frames have changed since the previous selected frame.
difference = 0;
max_frame_skipped = 0;
frame_location = 0;
frames_skipped = 0;

#For each frame, determine if the frame is interesting enough to analyze. We will look at two features:
#1. The color histogram should contain a variety of colours. Otherwise, you have a frame which doesn't
#contain enough meaningful data, since there is too much of the same color (for example a frame of the sky)
#2. The frame should differ enough from the previous selected frame.
#The chosen values might need to be adjusted

print("Finished reading")\

total_td = sum(td_features)

print("Start selecting interesting frames")
for i in range(frame_nbr - 1):
    frames_skipped = frames_skipped + 1;
    difference = difference + td_features[i]
    if(np.max(ch_features[i]) < 0.6 and difference > total_td / q_total):
        difference = 0;
        interesting_frames.append(frames[i]);
print("Finished selecting interesting frames")

#interesting_frames contains a matrix of the interesting frames from your query video.

#Apply SIFT on all the selected frames
print("Start the SIFT-process on the interesting frames")
all_winners, all_distances = query.sifting("db/MMA.db" , interesting_frames)
print("Finished the SIFT process")

#Opening the database file per line
gpsFile = open('positionDB.txt', 'r')
gpsPerLine = gpsFile.readlines()

gps_names = []

#Splitting the words at each line
for i in range(len(gpsPerLine)):
    gps_names.append(gpsPerLine[i].split())

#Finding the gps coordinates of a image-name in a gps-database.    
def lookupGPS(gps, name):
    for i in range(len(gps)):
        if(gps[i][0] == name):
            return float(gps[i][1]), float(gps[i][2])
            
    return 0, 0
    
GPS_Distances = []

#Link the image names to gps coordinates and save them together with the distance    
for i in range(len(all_winners)):
    xCoord, yCoord = lookupGPS(gps_names, all_winners[i])
    ar = [xCoord, yCoord, all_distances[i] ]
    GPS_Distances.append(ar)

GPS_Distances_per_frame = []

#Grouping the found GPS data back into the frame they came from
for i in range(len(interesting_frames)):
    frame = []
    for j in range(10):
        frame.append(GPS_Distances[i*10 + j])
    GPS_Distances_per_frame.append(frame)
    
#GPS_Distances_per_frame is an array, which contains an array for each frame in interesting_frames.
#These arrays contain 10 arrays, which depict the 10 best matches with the SIFT database.
#These arrays contain 3 numbers: the x-Coordinate and y-Coordinate of the GPS data and the distance of the SIFT-match. 
