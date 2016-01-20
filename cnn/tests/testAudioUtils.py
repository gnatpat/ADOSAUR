import pickle
import numpy as np
from testEnums import *
from ..utils import AudioUtils as AU
from ..utils import Utils as utils


##################$#
# AUDIOUTILS TESTS #
###################$

def testExtractAudioDataExtractsAnObject():
    actOutput = AU.extractAudioData(TEST_AUDIO_PATH)
    assert actOutput != None

def testExtractAudioDataExtractsCorrectObject():
    actOutput = AU.extractAudioData(TEST_AUDIO_PATH)
    expOutput = pickle.load(open(TEST_PICKLED_AUDIO_PATH, 'r'))
    assert np.array_equal(actOutput, expOutput)

def testSplitDataSplitsDataCorrectly():
    splitData = AU.splitData(AU.extractAudioData(TEST_AUDIO_PATH))
    actShape = (splitData.shape[1], splitData.shape[2])
    expShape = (1, AU.SIZE_CHUNKS)
    assert actShape == expShape

def testBuildExamplesAndTargetsBuildsTwoArrays():
    # use toy dictionary
    labelDict = {"203_1" : 3, "205_2" : 0, "207_2" : 1}
    actX, actY = AU.buildExamplesAndTargets(labelDict, 'rawData/' + AU.AUDIO_FOLDER)
    assert actX != None and actY != None

def testBuildExamplesAndTargetsBuildsTwoArraysOfCorrectSizes():
    # use toy dictionary
    labelDict = {"203_1" : 3, "205_2" : 0, "207_2" : 1}
    actX, actY = AU.buildExamplesAndTargets(labelDict, 'rawData/' + AU.AUDIO_FOLDER)
    assert len(actX) == len(actY)
