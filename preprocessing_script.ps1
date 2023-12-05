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