import AudioDataFormatter as ADF
import cPickle
import os

trainingX, trainingY, developmentX, developmentY, testX, testY = ADF.buildAudioData('../../rawData/RawAudio/wav/')

os.chdir('../../pickledData/')

print "Pickling training data..."
f = file('trainingX.save', 'wb')
cPickle.dump(trainingX, f, protocol=cPickle.HIGHEST_PROTOCOL)
f.close()
f = file('trainingY.save', 'wb')
cPickle.dump(trainingY, f, protocol=cPickle.HIGHEST_PROTOCOL)
f.close()

print "Pickling development data..."
f = file('developmentX.save', 'wb')
cPickle.dump(developmentX, f, protocol=cPickle.HIGHEST_PROTOCOL)
f.close()
f = file('developmentY.save', 'wb')
cPickle.dump(developmentY, f, protocol=cPickle.HIGHEST_PROTOCOL)
f.close()

print "Pickling test data..."
f = file('testX.save', 'wb')
cPickle.dump(testX, f, protocol=cPickle.HIGHEST_PROTOCOL)
f.close()
f = file('testY.save', 'wb')
cPickle.dump(testY, f, protocol=cPickle.HIGHEST_PROTOCOL)
f.close()
