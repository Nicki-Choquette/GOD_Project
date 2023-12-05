from PIL import Image
import numpy as np
import os


def rotate_shirt(input_path, output_path, degrees):
    # Open the image file
    original_image = Image.open(input_path)

    # Rotate the image by the specified degrees
    rotated_image = original_image.rotate(degrees)

    rotated_image = np.array(rotated_image)
    for i in range(len(rotated_image)):
        for j in range(len(rotated_image[0])):
            if sum(rotated_image[i][j]) == 0:
                rotated_image[i][j][0] = 246
                rotated_image[i][j][1] = 246
                rotated_image[i][j][2] = 246
            else:
                break
    for i in range(len(rotated_image)):
        for j in range(len(rotated_image[0])-1, -1, -1):
            if sum(rotated_image[i][j]) == 0:
                rotated_image[i][j][0] = 246
                rotated_image[i][j][1] = 246
                rotated_image[i][j][2] = 246
            else:
                break

    rotated_image = Image.fromarray(np.uint8(rotated_image))
    # Save the rotated image to the specified output path
    rotated_image.save(output_path)

    print(f"Image rotated by {degrees} degrees and saved to {output_path}")

def rotation_shirt_mask(mask_input_path, mask_output_path, rotation_degrees):
    original_image = Image.open(mask_input_path)

    # Rotate the image by the specified degrees
    rotated_image = original_image.rotate(rotation_degrees)

    # Save the rotated image to the specified output path
    rotated_image.save(mask_output_path)

    print(f"Image rotated by {rotation_degrees} degrees and saved to {mask_output_path}")


if __name__ == '__main__':
    #dir_path = "/Users/naksh/Documents/Sem_3/GOD/imgs"

    shirt_dir_path = "c:/Users/nicki/Geometry_Of_Data/GOD_Project/VITON-HD/datasets/test/cloth"

    shirt_images =  os.listdir(shirt_dir_path)
    rotation_degrees = 180

    for img in shirt_images:
        ip = os.path.join(shirt_dir_path, img)
        base_name = img[0:8] + "rotate.jpg"
        # base_name = os.path.basename(img)+"rotate.jpg"
        op = os.path.join(shirt_dir_path, base_name)
        rotate_shirt(ip, op, rotation_degrees)

    
    mask_dir_path = "c:/Users/nicki/Geometry_Of_Data/GOD_Project/VITON-HD/datasets/test/cloth-mask"

    mask_images =  os.listdir(mask_dir_path)

    for img in mask_images:
        ip = os.path.join(mask_dir_path, img)
        base_name = img[0:8] + "rotate.jpg"
        # base_name = os.path.basename(img)+"rotate.jpg"
        op = os.path.join(mask_dir_path, base_name)
        rotation_shirt_mask(ip, op, rotation_degrees)
    


    """shirt_input_path = "c:/Users/nicki/Geometry_Of_Data/GOD_Project/VITON-HD/datasets/test/cloth/01260_00.jpg"
    shirt_output_path = "c:/Users/nicki/Geometry_Of_Data/GOD_Project/VITON-HD/datasets/test/cloth/01260_00_rotate.jpg"

    mask_input_path = "c:/Users/nicki/Geometry_Of_Data/GOD_Project/VITON-HD/datasets/test/cloth-mask/01260_00.jpg"
    mask_output_path = "c:/Users/nicki/Geometry_Of_Data/GOD_Project/VITON-HD/datasets/test/cloth-mask/01260_00_rotate.jpg"
    

    #rotate_image('4863_h_e97a54e7-3545-41aa-9e7a-021e12164890.jpg', 'output.png', rotation_degrees)
    rotate_shirt(shirt_input_path, shirt_output_path, rotation_degrees)

    rotation_shirt_mask(mask_input_path, mask_output_path, rotation_degrees)"""
