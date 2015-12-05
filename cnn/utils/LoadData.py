def loadData():
    print "Loading training..."
    f = file('../../pickledData/trainingX.save', 'rb')
    trainingX = cPickle.load(f)
    f.close()

    f = file('../../pickledData/trainingY.save', 'rb')
    trainingY = cPickle.load(f)
    f.close()

    print "Loading development..."
    f = file('../../pickledData/developmentX.save', 'rb')
    developmentX = cPickle.load(f)
    f.close()

    f = file('../../pickledData/developmentY.save', 'rb')
    developmentY = cPickle.load(f)
    f.close()

    print "Loading test..."
    f = file('../../pickledData/testX.save', 'rb')
    testX = cPickle.load(f)
    f.close()

    f = file('../../pickledData/testY.save', 'rb')
    testY = cPickle.load(f)
    f.close()

    return trainingX, trainingY, developmentX, developmentY, testX, testY
