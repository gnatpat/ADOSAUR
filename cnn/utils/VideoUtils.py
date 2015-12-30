import cv2
import os

# Takes image and returns a numpy array of tuples (R,G,B)
def extractRGB(filepath):
    return cv2.imread(filepath)

# Takes video file path and outputs frames numbered 1.jpg, 2.jpg, ...
# into the output folder (e.g. outputImages/)
def extractFramesFromVideo(filepath, outputPath):
    vc = cv2.VideoCapture(filepath)
    count = 1

    if vc.isOpened():
        rval , frame = vc.read()
    else:
        rval = False

    if not os.path.isdir(outputPath):
        os.makedirs(outputPath)

    while rval: # still frames to read
        cv2.imwrite(outputPath + str(count) + '.jpg', frame)
        count = count + 1
        cv2.waitKey(1)
        rval, frame = vc.read()
                                
    vc.release()


def videoDataFormatter():
    return None

