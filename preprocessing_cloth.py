import os
import PIL.Image

from carvekit.api.interface import Interface
from carvekit.ml.wrap.fba_matting import FBAMatting
from carvekit.ml.wrap.tracer_b7 import TracerUniversalB7
from carvekit.pipelines.postprocessing import MattingMethod
from carvekit.pipelines.preprocessing import PreprocessingStub
from carvekit.trimap.generator import TrimapGenerator
from PIL import Image, ImageOps
import math
import cv2
from matplotlib import pyplot as plt
import numpy as np
from PIL import ImageColor
import scipy.spatial as sp
# get all the stuff for preprocessing

project_path = "c:/Users/nicki/Geometry_Of_Data/GOD_Project/"
shirt_dir_path = "c:/Users/nicki/Geometry_Of_Data/GOD_Project/clothing"

# shirts
def create_mask(input_path, output_path, cloth_path):
    # note the following code within this function up to but not including `WHITE = (255, 255, 255, 1)` was provided by the image-background-remove-tool (I made few alterations)
    # https://github.com/OPHoperHPO/image-background-remove-tool#if-you-want-control-everything
    seg_net = TracerUniversalB7(device='cpu',
              batch_size=1)

    fba = FBAMatting(device='cpu',
                    input_tensor_size=2048,
                    batch_size=1)

    trimap = TrimapGenerator()

    preprocessing = PreprocessingStub()

    postprocessing = MattingMethod(matting_module=fba,
                                trimap_generator=trimap,
                                device='cpu')

    interface = Interface(pre_pipe=preprocessing,
                        post_pipe=postprocessing,
                        seg_pipe=seg_net)

    image = PIL.Image.open(input_path)
    image = ImageOps.exif_transpose(image)
    img = image.convert("RGB")
    img.save(cloth_path)
    image_wo_bg = interface([image])[0]
    
    WHITE = (255, 255, 255, 1)
    BLACK = (0, 0, 0, 1)

    newimgdata = []
    for color in image_wo_bg.getdata():
        r, g, b, a = color
        if(a == 0):
            newimgdata.append(BLACK)
        else:
            newimgdata.append(WHITE)
    newimg = Image.new(image_wo_bg.mode,image_wo_bg.size)
    newimg.putdata(newimgdata)
    newimg = newimg.convert('L')
    newimg.save(output_path, format='jpeg')

shirt_images =  os.listdir(shirt_dir_path)

for img in shirt_images:
    ip = os.path.join(shirt_dir_path, img)
    mask_path = project_path + "VITON-HD/datasets/test/cloth-mask/" + img
    cloth_path = project_path + "VITON-HD/datasets/test/cloth/" + img
    create_mask(ip, mask_path, cloth_path)