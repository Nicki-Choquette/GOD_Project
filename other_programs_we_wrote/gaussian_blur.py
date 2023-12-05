from PIL import Image, ImageOps
import torch
import torchgeometry as tgm
import torchvision.transforms as transforms 
import cv2
import numpy as np

# image = cv2.imread('upsample.png')
image = Image.open('00891_00_upsampled.png')
image = ImageOps.exif_transpose(image)
# img = tgm.image_to_tensor(image)

transform_to_tensor = transforms.Compose([ 
    transforms.PILToTensor() 
]) 
img = transform_to_tensor(image)

# img = torch.unsqueeze(img.float(), dim=0)
# gauss = tgm.image.GaussianBlur((15, 15), (3, 3))
gauss = transforms.Compose([ 
    transforms.GaussianBlur((15, 15), (3, 3)) 
]) 

img_blur = gauss(img)
# img_blur = torch.reshape(img_blur, (3, 1024, 768))

# image_blur = tgm.tensor_to_image(img_blur.byte())

transform_to_image = transforms.Compose([ 
    transforms.ToPILImage() 
]) 
image_blur = transform_to_image(img_blur)
# img = torch.reshape(img, (3, 1024, 768))
# image_blur = transform_to_image(img)

image_blur.save("00891_00_blurred.png", format="png")



###########################################

# image = cv2.imread('00891_00_upsampled.png')
# blur_img = cv2.GaussianBlur(image, (6, 6))
# cv2.imwrite('burrrr.png', blur_img)