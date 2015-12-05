from PIL import Image

def extractRGB(filepath):
    im = Image.open(filepath)
    pixels = list(im.getdata())
    print pixels
