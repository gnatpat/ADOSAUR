#!/usr/bin/python

import sys
import utils.Utils as utils
import utils.AudioUtils as AU
import utils.VideoUtils as VU
import os
import glob


videoFilePath = sys.argv[1]
audioFilePath = sys.argv[2]

# print videoFilePath
# print audioFilePath

# print "Loading audio network..."
network = utils.loadNet('../../cnn/audioCNN13.pickle')

# print "Predicting audio..."
audioPrediction = AU.predictAudio(audioFilePath, network)

print audioPrediction

# print "Loading video network..."
network = utils.loadNet('../../cnn/videoCNN1.save')

# print "Predicting video..."
videoPrediction = VU.predictVideo(videoFilePath, network)

print videoPrediction

filelist = glob.glob("../../tmp/*")
for f in filelist:
    os.remove(f)
