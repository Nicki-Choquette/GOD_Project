import os
from PIL import Image, ImageOps
import torch
import torchgeometry as tgm
import torchvision.transforms as transforms 
import numpy as np

project_path = "c:/Users/nicki/Geometry_Of_Data/GOD_Project/"
people_dir_path = "c:/Users/nicki/Geometry_Of_Data/GOD_Project/people/"

def upsample(input_path):
    img = Image.open(input_path)
    img = ImageOps.exif_transpose(img)

    img = img.resize((768, 1024), Image.NEAREST)

    # img.save("00891_00_upsampled.png", format="png")
    return img

def gaussian_blur(up_image, output_path):

    transform_to_tensor = transforms.Compose([ 
        transforms.PILToTensor() 
    ])

    img = transform_to_tensor(up_image)
    gauss = transforms.Compose([ 
        transforms.GaussianBlur((15, 15), (3, 3)) 
    ])
    img_blur = gauss(img)

    transform_to_image = transforms.Compose([ 
        transforms.ToPILImage() 
    ]) 
    image_blur = transform_to_image(img_blur)

    image_blur = image_blur.convert('P')

    image_blur.save(output_path, format="png")


people_images =  os.listdir(people_dir_path)

CIHP_path = project_path + "CIHP_PGN/output/cihp_parsing_maps/"

for img in people_images:
    ip = os.path.join(CIHP_path, img[:-4])
    parse_path = project_path + "VITON-HD/datasets/test/image-parse/" + img[:-4] + ".png"
    up_img = upsample(ip + "_vis.png")
    gaussian_blur(up_img, parse_path) 
    # up_img = up_img.convert('P') # attempt to fix error with parse image (did not work, so I once again uncommented the above line and commented out this line and below)
    # up_img.save(parse_path, format="png")