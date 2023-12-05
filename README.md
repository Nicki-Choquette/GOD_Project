# GOD_Project

Clone this repository:

```
git clone https://github.com/shadow2496/VITON-HD.git
cd ./VITON-HD/
```
Install Conda if not already: 
https://www.anaconda.com/download/
Open Anaconda Prompt > cd ./VITON-HD/

Install Cuda if not already: https://developer.nvidia.com/cuda-12-1-0-download-archive?target_os=Windows&target_arch=x86_64&target_version=10&target_type=exe_local

Install PyTorch and other dependencies:

```
conda create -y -n [ENV] python=3.8
conda activate [ENV]
conda install pytorch torchvision torchaudio pytorch-cuda=12.1 -c pytorch -c nvidia
pip install opencv-python torchgeometry
```

## Dataset

We collected 1024 x 768 virtual try-on dataset for **our research purpose only**.
You can download a preprocessed dataset from [VITON-HD DropBox](https://www.dropbox.com/s/10bfat0kg4si1bu/zalando-hd-resized.zip?dl=0).
The frontal view woman and top clothing image pairs are split into a training and a test set with 11,647 and 2,032 pairs, respectively. 


## Pre-trained networks

We provide pre-trained networks and sample images from the test dataset. Please download `*.pkl` and test images from the [VITON-HD Google Drive folder](https://drive.google.com/drive/folders/0B8kXrnobEVh9fnJHX3lCZzEtd20yUVAtTk5HdWk2OVV0RGl6YXc0NWhMOTlvb1FKX3Z1OUk?resourcekey=0-OIXHrDwCX8ChjypUbJo4fQ&usp=sharing) and unzip `*.zip` files. `test.py` assumes that the downloaded files are placed in `./checkpoints/` and `./datasets/` directories.

## Testing

To generate virtual try-on images, run:

```
set CUDA_VISIBLE_DEVICES=0 & python test.py --name "first_run"
```

The results are saved in the `./results/` directory. You can change the location by specifying the `--save_dir` argument. To synthesize virtual try-on images with different pairs of a person and a clothing item, edit `./datasets/test_pairs.txt` and run the same command. (did not do this part)

### After this point, we deviated from the VITON-HD instructions, and started making our own alterations

## We first started by rotating cloth and cloth-mask images to see how it would impact results

We wrote a python script, `rotate.py`, which rotated the `cloth` and `cloth-mask` images to see if they would still be able to be put on the human in a similar fashion.

We first tried 180 degrees, which we expected to have pretty poor results, and it did not dissapoint. These results are contained in `results/rotate_all_180_run`. (*Describe Further*)

We then tried 10 degrees, which we hoped would not impact the results too much. However, on some shirts, it still did decently, but on most the quality was not nearly as good, and there were several malformations. These results are contained in `results/rotate_all_10_run`. (*Describe Further*)

We also tried 2 degrees, which did significantly better. There were some minute distortions that were noticeably, however it still functioned effectively. These results are contained in `results/rotate_all_2_run`. (*Describe Further*)

## We then wanted to be able to 1) alter the human images and 2) use our own images. For this, we needed to be able to do similar preprocessing to what they had done.

# Preprocessing Step 1: Openpose
Followed this to ensure pre-requisites were met: https://github.com/CMU-Perceptual-Computing-Lab/openpose/blob/master/doc/installation/1_prerequisites.md
Needed to install Cmake: https://cmake.org/download/
Also needed to install models manually due to error: https://www.kaggle.com/datasets/changethetuneman/openpose-model/?select=pose_iter_102000.caffemodel

To run openpose (from powershell, from openpose-master folder):
build\x64\Release\OpenPoseDemo.exe --image_dir C:\Users\nicki\images\before --hand --disable_blending --display 0 --write_json C:\Users\nicki\images\after --write_images C:\Users\nicki\images\after\renders --num_gpu 1 --num_gpu_start 0

# Preprocessing Step 2: CIHP_PGN
Here is the CIHP_PGN github: https://github.com/Engineering-Course/CIHP_PGN/tree/master
Tried to run, but did not have tensorflow installed. Needed to install tensorflow with: python -m pip install tensorflow
The github code was using commands from tensorflow versions prior to 2.0, and my version of python/pip would not install tensorflow versions prior to 2.0 because they were not compatible. Thus I had to install python3.7.7 in order to pip install tensorflow version 1.15.
Then I had the issue using python3.7.7 of No module named 'cv2', which meant I needed to install OpenCV. As a prerequisite, I also needed to install matplotlib.
For installing OpenCV, I opencv-4.8.1-windows.exe from https://github.com/opencv/opencv/releases. I was following these instructions: https://docs.opencv.org/4.x/d5/de5/tutorial_py_setup_in_windows.html.

After this point, I was able to run CIHP_PGN with their dataset. 
However, there is some preprocessing that they do with their images, and so I needed to figure out how to do this preprocessing as well. It looked like they may have provided the code for this preprocessing via datasets/CIHP/tool/reverse_label.m and datasets/CIHP/tool/write_edge.m. However, I did not have matlap. So I needed to setup my MathWorks account through UVA and install MATLAB.

MATLAB: I also needed to install the addon Image Processing Toolbox in order to run the write_edge.m script. I tried running the write_edge.m script, but I did not know what the '../Human_ids' directory was. I assumed it was supposed to be the images, though, so I tried changing it to '../images', but then I ran into an error with using 'imgradient' because it expected 2-D input but instance map was 3d. At this point, I took this as a loss because there wasn't anything I could figure out to do to make write_edge.m work.

From here, I went back and more closely examined what preprocessing was happening: essentially, I needed an image the same size as the original, but all black, to go into the edges/, labels/, and labels_rev/ directory as a png. I decided to code the create_preprocessing.py file to do this for me. 

This then actually worked! I was able to apply it to an image from the VITON-HD dataset and it actually worked. I did run into another issue here though, which was that the parse map I had output was different than (and not as accurate as) the VITON-HD parse map. Examining part 2 of "Preprocessing for HR-VITON", I realized I needed to change the resolution, then output the parsemap, then upsample to the original image size, and then use torchgeometry.image.GaussianBlur. For changing the resolution, I edited create_preprocessing.py to do that first. Then to upsample, I wrote the script upsample.py. 

In order to use torchgeometry.image.GaussianBlur, I needed to pip install torch and torchgeometry for this version of python. I created gaussian_blur.py to do this part. Of note,
the output I got here did not match VITON-HD's output, although this time it at least looked more accurate than when I had just applied CIHP_PGN to the original image, so I think they had used a slightly different method for how exactly they got their parse map (or at least what they did to smooth it).

I was unable to get the same exact results and had tried the following methods and more:
- Tried different combinations of resample parameter (when using Image.resize()) for when I was downsampling and upsampling
- Tried different parameters for the gaussian_blur
- Tried using cv2 gaussian_blur
- One last thing I decided to try was downloading v10 of nvidia gpu computing toolkit; reason being that I was getting a warning when running test_pgn.py about it not being able to load several dll files, for example'cudart64_100.dll', so it was using my CPU instead of GPU. This is because I had v12, and the versions of the dll had been updated and thus weren't named the same. I hadn't tried to fix this initially because I assumed that it wouldn't perform any differently aside from perhaps being faster. For CUDA v10, I needed to also install VS 2017 because it was not compatible with the versions I already had. Then I copied the .dll files I needed from v10 into v12. The one remainin dll file that wasn't loading was 'cudnn64_7.dll' (again because I had a more updated version), so I also needed to download cuDNN v7.6.5 (November 5th, 2019), for CUDA 10.0, and I added that dll file to the path as well. At this point I tried running test_pgn.py again, but I was getting an odd error: "Internal: Invoking ptxas not supported on Windows
Relying on driver to perform ptx compilation. This message will be only logged once." followed by issues with allocating memory. I found a similar issue here, https://github.com/tensorflow/models/issues/7640, and based on this comment, https://github.com/tensorflow/models/issues/7640#issuecomment-553807645, I decided to try uninstalling tensorflow v15 and installing tensorflow v14. This did end up resolving this issue, and finally I ran test_pgn.py again, and this time it worked; however as expected, I was getting the same results that I was previously getting.

Nothing was yielding the same output as what VITON-HD had for their parse maps, so after much trial and error, I decided to just use the parse maps that I was able to produce (the blurry ones).

(Note, I did go back later and try to write smooth.py to smooth it out, but the brown color was too close to the colors of transition from orange to black, the orange was too close to the colors of the transition from red to black, etc.; It just didn't end up working.)

# Preprocessing Step 3: Cloth Mask
See this: https://github.com/OPHoperHPO/image-background-remove-tool
For this I needed Python 3.10.4. I had v3.10.1, so I needed to upgrade that python version. I think needed carvekit, so I executed `pip install carvekit --extra-index-url https://download.pytorch.org/whl/cu113`.
I then used code from the github and put it into remove_bg.py to remove the background, then I wrote create_mask.py to create the mask from the image with the removed background.

# Putting everything together
At this point, I started trying to put everything together.

This was the point at which I first tried to run all of this together. I took 'datasets/test/cloth/01260_00.jpg', copied it to my 'Project/clothing' directory, and renamed it to 'red_shirt.jpg'. Additionally, I took 'datasets/test/image/00891_00.jpg', copied it to my 'Project/people' directory, and renamed it to 'jane.jpg'.

I then ran all of the preprocessing & VITON-HD by writing a script 'preprocessing_script.ps1'.

If you setup your directory in the following manner:
Project[VITON-HD, image-background-remove-tool, openpose-master, CIHP_PGN, clothing, people, processing_cloth.py, preprocessing_people.py, preprocessing_people2.py, preprocessing_script.ps1]

Then the script I wrote preprocessing_script.ps1 (for Windows Powershell) can be run to conduct all the preprocessing on people images (kept in the 'people' folder) and shirt images (kept in the 'clothing' folder), and then VITON-HD is run, but on the pairs indicated in the 'VITON-HD/datasets/test_pairs.txt' file. Here is the code contained within preprocessing_script.ps1:

```
& C:/Users/nicki/AppData/Local/Programs/Python/Python310/python.exe c:/Users/nicki/Geometry_Of_Data/GOD_Project/preprocessing_cloth.py
& cd C:/Users/nicki/Geometry_Of_Data/GOD_Project/openpose-master
& build/x64/Release/OpenPoseDemo.exe --image_dir C:/Users/nicki/Geometry_Of_Data/GOD_Project/people --hand --disable_blending --display 0 --write_json C:/Users/nicki/Geometry_Of_Data/GOD_Project/VITON-HD/datasets/test/openpose-json --write_images C:/Users/nicki/Geometry_Of_Data/GOD_Project/VITON-HD/datasets/test/openpose-img --num_gpu 1 --num_gpu_start 0
& C:/Users/nicki/AppData/Local/Programs/Python/Python310/python.exe c:/Users/nicki/Geometry_Of_Data/GOD_Project/preprocessing_people.py
& cd C:/Users/nicki/Geometry_Of_Data/GOD_Project/CIHP_PGN
& C:/Users/nicki/AppData/Local/Programs/Python/Python37/python37.exe c:/Users/nicki/Geometry_Of_Data/GOD_Project/CIHP_PGN/test_pgn.py
& C:/Users/nicki/AppData/Local/Programs/Python/Python310/python.exe c:/Users/nicki/Geometry_Of_Data/GOD_Project/preprocessing_people2.py
& cd C:/Users/nicki/Geometry_Of_Data/GOD_Project/VITON-HD
& set CUDA_VISIBLE_DEVICES=0
& C:/Users/nicki/AppData/Local/Programs/Python/Python310/python.exe test.py --name "our_images"
```
However to work for other paths (aka not my specific PC) paths would need to be changed both within the preprocessing.py files and the .ps1 file. This is what paths should be in the .ps1 file:
```
& <path to python.exe for python v3.10> <path to project folder>/preprocessing_cloth.py
& cd <path to project folder>/openpose-master
& build/x64/Release/OpenPoseDemo.exe --image_dir <path to project folder>/people --hand --disable_blending --display 0 --write_json <path to project folder>VITON-HD/datasets/test/openpose-json --write_images <path to project folder>/VITON-HD/datasets/test/openpose-img --num_gpu 1 --num_gpu_start 0
& <path to python.exe for python v3.10> <path to project folder>/preprocessing_people.py
& cd <path to project folder>/CIHP_PGN
& <path to python.exe for python v3.7> <path to project folder>/CIHP_PGN/test_pgn.py
& <path to python.exe for python v3.10> <path to project folder>/preprocessing_people2.py
& cd <path to project folder>/VITON-HD
& set CUDA_VISIBLE_DEVICES=0
& <path to python.exe for python v3.10> test.py --name "our_images"
```

However, I ran into an issue here. VITON-HD was throwing an error when I was trying to run it with 'jane.jpg red_shirt.jpg' being the only line in the 'test_pairs.txt' file. I decided to run just VITON-HD, but on '00891_00.jpg red_shirt.jpg', for which I still got an error, and then I tried it on 'jane.jpg 01260_00.jpg', and still got an error. This told me that it was an issue with both the preprocessing of the person image and the preprocessing of the shirt image. I looked more closely at the error from the '00891_00.jpg red_shirt.jpg' run, "RuntimeError: The size of tensor a (768) must match the size of tensor b (3) at non-singleton dimension 4". Examining the location of this error in 'test.py', I printed the shapes of 'c' and 'cm', saw how they differed, reshaped 'cm' to match, and this fixed that error but resulted in another error. Thus I undid my edits in 'test.py' and figured I needed to fix the images for the shirt. I recalled when I had been researching images that there were modes for images, so on this hunch I printed the modes for my versions of the images and for VITON-HD's versions. Alas, my cloth-mask image was supposed to be 'L' mode, so I edited 'preprocessing_cloth.py' to do so.  Running VITON-HD again on '00891_00.jpg red_shirt.jpg', it worked!

Now I just needed to figure out what was wrong with the person images. I tried following the same hunch, and I did find out that my parse image was supposed to be in 'P' mode, so I edited 'preprocessing_people2.py' to correct that. Trying to run 'jane.jpg 01260_00.jpg' again, I just ran into a different error: "RuntimeError: index 51 is out of bounds for dimension 0 with size 20". I decided to target what I thought to be the most likely suspect, the parse image. I did so by renaming the 'image-parse/jane.png' to 'image-parse/temp.png' and renaming 'image-parse/00891_00.png' to 'image-parse/jane.png'. Then I ran 'jane.jpg 01260_00.jpg' again, and it worked. This means that aside from the parse map, the rest of the preprocessing worked with VITON-HD. While normally I would try to fix the issue when I know what it is, I already spent so many hours earlier trying to get the parse map to be more like what they got, and had failed. Thus I considered this a sign that I would not be able to get VITON-HD able to work with our own pictures.

What we were able to do though, was take a picture of a UVA shirt on carpet (i.e., not ideal sterile conditions like their test images) and have the provided people images transformed into that shirt. 

[Discuss results further]