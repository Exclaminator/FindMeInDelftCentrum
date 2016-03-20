import argparse
import numpy as np
import cv2
from video_tools import *
import feature_extraction as ft    
from video_features import *

#Program to detect the interesting frams of a video. Takes as input a video-file
#and returns an array of frames which contain interesting data to analyze.

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
#while(cap.isOpened() and cap.get(cv2.CAP_PROP_POS_MSEC) < q_total * 1000):

while(cap.isOpened() and cap.get(cv2.CAP_PROP_POS_MSEC) < q_total * 100):
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

#For each frame, determine if the frame is interesting enough to analyze. We will look at two features:
#1. The color histogram should contain a variety of colours. Otherwise, you have a frame which doesn't
#contain enough meaningful data, since there is too much of the same color (for example a frame of the sky)
#2. The frame should differ enough from the previous selected frame.
#The chosen values might need to be adjusted

for i in range(frame_nbr - 1):
    difference = difference + td_features[i]
    if(np.max(ch_features[i]) < 0.6 and difference > 25000):
        difference = 0;
        interesting_frames.append(frames[i])

#interesting_frames contains a matrix of the interesting frames from your query video.
