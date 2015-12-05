import sPickle
import os

def loadData():

    print "Loading training..."
    f = open('../pickledData/trainingX.save', 'r')
    trainingX = sPickle.load(f)
    f.close()

    f = open('../pickledData/trainingY.save', 'r')
    trainingY = sPickle.load(f)
    f.close()

    print "Loading development..."
    f = open('../pickledData/developmentX.save', 'r')
    developmentX = sPickle.load(f)
    f.close()

    f = open('../pickledData/developmentY.save', 'r')
    developmentY = sPickle.load(f)
    f.close()

    print "Loading test..."
    f = open('../pickledData/testX.save', 'r')
    testX = sPickle.load(f)
    f.close()

    f = open('../pickledData/testY.save', 'r')
    testY = sPickle.load(f)
    f.close()

    return trainingX, trainingY, developmentX, developmentY, testX, testY
