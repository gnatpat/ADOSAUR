from PIL import Image
import numpy as np

def extractRGB(filepath):
    im = Image.open(filepath)
    return np.array(im.getdata())
