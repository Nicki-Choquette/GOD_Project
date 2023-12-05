from PIL import Image, ImageOps
img = Image.open("C:/Users/nicki/Geometry_Of_Data/GOD_Project/VITON-HD/datasets/test/image/03615_00.jpg")
img = ImageOps.exif_transpose(img)
img = img.resize((192, 256), Image.LANCZOS)
img.save("datasets/CIHP/images/03615_00.jpg", format="jpeg")

img = Image.open("datasets/CIHP/images/03615_00.jpg")
img = ImageOps.exif_transpose(img)

width, height = img.size 

pixel_map = img.load() 

for i in range(width): 
    for j in range(height):   
        # setting the pixel value. 
        pixel_map[i, j] = (0, 0, 0) 
  
# Saving the final output 
img.save("datasets/CIHP/edges/03615_00.png", format="png")
img.save("datasets/CIHP/labels/03615_00.png", format="png")
img.save("datasets/CIHP/labels_rev/03615_00.png", format="png")