from PIL import Image

im = Image.open('/Users/LeeHyunAh/Desktop/sacha.png')
pixels = list(im.getdata())
print pixels
