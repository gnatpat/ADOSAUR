import arff
import glob
import os
import csv


def parseAudioData(path_to_audio_data='depression_data/audio/', set='all'):

    # Parse training data (100 labelled examples)
    trainingData = parseArffDataFiles(path_to_audio_data + 'data/Training/*')
    trainingLabels = parseCsvLabelFiles(path_to_audio_data + 'labels/training_labels/')

    # Parse development data (100 labelled examples)
    developmentData = parseArffDataFiles(path_to_audio_data + 'data/Development/*')
    developmentLabels = parseCsvLabelFiles(path_to_audio_data + 'labels/development_labels')

    # Parse testing data (100 unlabelled examples)
    testingData = parseArffDataFiles(path_to_audio_data + 'data/Testing/*')

    return trainingData, trainingLabels, developmentData, developmentLabels, testingData


# Helper function to parse .arff files which contain the data
def parseArffDataFiles(path_to_arff_files):
    data = []
    for filePath in glob.glob(os.path.join(path_to_arff_files, '*')):
        fileData = arff.load(open(filePath))
        # Remove first 3 and last useless attributes (2267 attributes in total)
        attributesData = fileData['data'][0][3:-1]
        data.append(attributesData)
    return data


# Helper function to parse .csv files which contain the labels
def parseCsvLabelFiles(path_to_csv_label_files):
    labels = []
    for filePath in glob.glob(os.path.join(path_to_csv_label_files, '*')):
        csvLabelFile = open(filePath, 'rb')
        csvReader = csv.reader(csvLabelFile)
        for label in csvReader:
            labels.append(int(label[0]))
        csvLabelFile.close()
    # Append the same labels again because we have Freeform + Northwind
    labels.extend(labels)
    return labels
