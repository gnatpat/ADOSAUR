import pickle
from testEnums import *  # filepaths for testing material
from ..utils import Utils

TEST_LABEL_PATH = '../../rawData/labels/'
TEST_NETWORK_PATH = TEST_FILES_PATH + 'testNetwork.pickle'
TRAINING_LABELS_PICKLE = TEST_FILES_PATH + 'trainingLabels.pickle'

#############$#
# UTILS TESTS #
##############$

def testCreateLabelledDictReturnsAnObject():
    actOutput = Utils.createLabelDict('../../rawData/labels/Training/')
    expOutput = pickle.load(open(TRAINING_LABELS_PICKLE,'r'))
    assert (actOutput == expOutput).all()

def testCreateLabelledDictReturnsCorrectObject():
    pass  # need data

def testTestCnnPrintsCorrectReportForTestNetwork():
    pass  # check stdout is correct for test network

def testLoadNetLoadsAnObject():
    pass # need data

def testSavingAndLoadingNetwork():
    pass # build a network and save it, the load and see if the same

def testLoadNetLoadsTheTestNetCorrectly():
    pass # need data
