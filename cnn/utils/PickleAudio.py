import AudioDataFormatter as ADF
import sPickle
import os

trainingX, trainingY, developmentX, developmentY, testX, testY = ADF.buildAudioData('../../rawData/RawAudio/wav/')

os.chdir('../../pickledData/')

print "Pickling training data..."
f = open('trainingX.save', 'w')
sPickle.dump(trainingX, f)
f.close()
f = open('trainingY.save', 'w')
sPickle.dump(trainingY, f)
f.close()

print "Pickling development data..."
f = open('developmentX.save', 'w')
sPickle.dump(developmentX, f)
f.close()
f = open('developmentY.save', 'w')
sPickle.dump(developmentY, f)
f.close()

print "Pickling test data..."
f = open('testX.save', 'w')
sPickle.dump(testX, f)
f.close()
f = open('testY.save', 'w')
sPickle.dump(testY, f)
f.close()
