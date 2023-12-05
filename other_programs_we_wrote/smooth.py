from PIL import Image, ImageOps
import math
import cv2
from matplotlib import pyplot as plt
import numpy as np
from PIL import ImageColor
import scipy.spatial as sp

RED = (254, 0, 0)
BLUE = (0, 0, 254)
ORANGE = (254, 85, 0)
LIGHT_BLUE = (51, 169, 220)
BLACK = (0, 0, 0)
BROWN = (85, 51, 0)
PURPLE = (248, 3, 252)
TEAL = (0, 85, 85)
ORANGE_TO_BLACK = (116, 39, 0)
BLUE_TO_BLACK = (0, 0, 150)
RED_TO_BLACK = (91, 0, 0)
LIGHT_BLUE_TO_BLACK = (22, 73, 95)
ORANGE_TO_BLACK2 = (177, 59, 0)
ORANGE_TO_BLACK3 = (50, 17, 0)
ORANGE_TO_BLACK4 = (60, 23, 0)

COLORS = [RED, BLUE, ORANGE, LIGHT_BLUE, BLACK, BROWN, TEAL, ORANGE_TO_BLACK, ORANGE_TO_BLACK2, BLUE_TO_BLACK, ORANGE_TO_BLACK3, ORANGE_TO_BLACK4]

img = Image.open('00891_00_blurred.png')
img = ImageOps.exif_transpose(img)

newimgdata = []
for color in img.getdata():
    r, g, b = color
    if (r==255 or r==254) and g==85 and b==0:
        newimgdata.append(ORANGE)
    elif r==51 and (g==170 or g==169) and (b==221 or b==220):
        newimgdata.append(LIGHT_BLUE)
    elif r==0 and g==0 and (b==255 or b==254):
        newimgdata.append(BLUE)
    elif (r==255 or r==254) and g==0 and b==0:
        newimgdata.append(RED)
    elif r==85 and g==51 and b==0:
        newimgdata.append(BROWN)
    elif r==0 and g==85 and b==85:
        newimgdata.append(TEAL)
    elif r==0 and g==0 and b==0:
        newimgdata.append(BLACK)
    # else:
    #     newimgdata.append(BLACK)
    else:
        min_dist = 1000000
        min_col = (-1, -1, -1)
        for i in range(0, len(COLORS)):
            r2, g2, b2 = COLORS[i]
            distance = math.sqrt(((r-r2)**2)+((g-g2)**2)+((b-b2)**2))
            if distance < min_dist:
                min_dist = distance
                min_col = COLORS[i]
        if(min_col == ORANGE_TO_BLACK or min_col == ORANGE_TO_BLACK2):
            if len(newimgdata) > 153600:
                min_col = ORANGE
            else:
                min_col = RED
        elif(min_col == BLUE_TO_BLACK):
            min_col = BLUE
        elif(min_col == LIGHT_BLUE_TO_BLACK):
            min_col = LIGHT_BLUE
        elif(min_col == ORANGE_TO_BLACK3 or min_col == ORANGE_TO_BLACK4):
            min_col = BLACK
        # elif(min_col == BROWN):
        #     min_col = PURPLE
        newimgdata.append(min_col)
newimg = Image.new(img.mode,img.size)
newimg.putdata(newimgdata)

newimg.save("00891_00_smooth.png", format="png")
#--------------try the following after changing the main colors

# image = cv2.imread('00891_00_smooth.png')
# #convert BGR to RGB image
# image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

# main_colors = [RED, BLUE, ORANGE, BROWN, BLACK, TEAL, LIGHT_BLUE]#NEEEEEEEEEEEEEED TO CHANGE TO RGB

# h,w,bpp = np.shape(image)

# #Change colors of each pixel
# #reference :https://stackoverflow.com/a/48884514/9799700
# last_color_h = None
# for py in range(0,h):
#     last_color_w = None
#     for px in range(0,w):
      
#       py_beg = py-10

#       nearest_color = [?, ?, ?]
      
#       image[py][px][0]=nearest_color[0]
#       image[py][px][1]=nearest_color[1]
#       image[py][px][2]=nearest_color[2]

# # show image
# plt.imshow(image.astype(np.uint8))
# plt.imsave("00891_00_smooth2.png",image/255)

# im = cv2.imread('00891_00_smooth.png') # read input image

# def getClosestColor(pixel,color_set_rgb): # Get the closest color for the pixel
#     closest_color = None
#     cost_init = 10000
#     pixel = np.array(pixel)
#     for color in color_set_rgb:
#         color = np.array(color)
#         cost = np.sum((color - pixel)**2)
#         if cost < cost_init:
#             cost_init = cost
#             closest_color = color
#     return closest_color

# def getClosestImage(im): # Get the closest image
#     color_set = ['#33a9dc','#0000fe', '#fe0000', '#553300', '#fe5500', '#005555', '#000000'] # Given Colorset
#     color_set_rgb= [ImageColor.getrgb(color) for color in color_set] # RGB Colorset

#     height, width, channels = im.shape
#     im_out = np.zeros((height,width,channels))

#     for y in range(0, height):
#         for x in range(0, width):
#             closest_color = getClosestColor(im[y, x],color_set_rgb)
#             im_out[y,x,:] = closest_color
#     return im_out


# im_out = getClosestImage(im)

# plt.imshow(im_out.astype(np.uint8))
# plt.imsave("00891_00_smooth2.png",im_out/255)
# # plt.show()