from PIL import Image, ImageOps
import math
import cv2
from matplotlib import pyplot as plt
import numpy as np
from PIL import ImageColor
import scipy.spatial as sp

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

img = Image.open('2.png')
img = ImageOps.exif_transpose(img)

newimgdata = []
for color in img.getdata():
    r, g, b, a = color
    if(a == 0):
        newimgdata.append(BLACK)
    else:
        newimgdata.append(WHITE)
newimg = Image.new(img.mode,img.size)
newimg.putdata(newimgdata)

newimg.save("2_mask.png", format="png")