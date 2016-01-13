#!/usr/bin/python

import sys
import utils.Utils as utils
import utils.AudioUtils as AU
import utils.VideoUtils as VU
import os

videoFilePath = sys.argv[1]
audioFilePath = sys.argv[2]

# print "Loading audio network..."
network = utils.loadNet('../../cnn/audioCNN13.pickle')

# print "Prediciting audio..."
audioPrediction = AU.predictAudio(audioFilePath, network)

print audioPrediction

# print "Loading video network..."
network = utils.loadNet('../../cnn/videoCNN1.save')

# print "Prediciting video..."
videoPrediction = VU.predictVideo(videoFilePath, network)

print videoPrediction

os.remove(videoFilePath)
os.remove(audioFilePath)

