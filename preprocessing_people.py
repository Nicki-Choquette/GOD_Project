import os
from PIL import Image, ImageOps
# get all the stuff for preprocessing

project_path = "c:/Users/nicki/Geometry_Of_Data/GOD_Project/"
people_dir_path = "c:/Users/nicki/Geometry_Of_Data/GOD_Project/people"

# people
def parse_map(input_path, output_path, CIHP_path, person_path, image_name):

    image = Image.open(input_path)
    image = ImageOps.exif_transpose(image)
    image.save(person_path)
    image = image.resize((192, 256), Image.LANCZOS)
    image.save(CIHP_path + "images/" + image_name, format="jpeg")

    image = Image.open(CIHP_path + "images/" + image_name)
    image = ImageOps.exif_transpose(image)

    width, height = image.size 

    pixel_map = image.load() 
    
    for i in range(width): 
        for j in range(height):   
            # setting the pixel value. 
            pixel_map[i, j] = (0, 0, 0) 
    
    # Saving the final output 
    image.save(CIHP_path + "edges/" + image_name[:-4] + ".png", format="png")
    image.save(CIHP_path + "labels/" + image_name[:-4] + ".png", format="png")
    image.save(CIHP_path + "labels_rev/" + image_name[:-4] + ".png", format="png")

people_images =  os.listdir(people_dir_path)

vals = []
val_ids = []
CIHP_path = project_path + "CIHP_PGN/datasets/CIHP/"
for img in people_images:
    i = people_images.index(img)
    if(i == len(people_images)-1):
        vals.append("/images/" + img + " /labels/" + img[:-4] + ".png")
        val_ids.append(img[:-4])
    else:
        vals.append("/images/" + img + " /labels/" + img[:-4] + ".png\n")
        val_ids.append(img[:-4] + "\n")
    ip = os.path.join(people_dir_path, img)
    parse_path = project_path + "VITON-HD/datasets/test/image-parse/" + img
    person_path = project_path + "VITON-HD/datasets/test/image/" + img
    parse_map(ip, parse_path, CIHP_path, person_path, img)

with open(CIHP_path+"list/val.txt", 'w') as file: 
    file.writelines(vals)
with open(CIHP_path+"list/val_id.txt", 'w') as file: 
    file.writelines(val_ids)