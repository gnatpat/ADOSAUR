import cv2
import os

vc = cv2.VideoCapture('./rawData/RawVideo/Training/Freeform/203_1_Freeform_video.mp4')
count = 1

if vc.isOpened():
  rval , frame = vc.read()
else:
  rval = False

if not os.path.isdir('testExtraction'):
  os.makedirs('testExtraction')

while rval: # still frames to read
  path = 'testExtraction/'
  cv2.imwrite(path + str(count) + '.jpg', frame)
  count = count + 1
  cv2.waitKey(1)
  rval, frame = vc.read()

vc.release()
