# Optical_Flow_GPU_Opencv3
Extracting optical flow based on GPU in Opencv3

### Preface
This code was adapted from https://github.com/feichtenhofer/gpu_flow and we truly appreciate the work of feichtenhofer. 
The most of the detailed information can be seen in that repository. 

### Install Opencv3
My opencv version is 3.4.3. It will appear some problems when making opencv3 according to official documents. It concluds that 
following command is fine.

`cmake -D CMAKE_BUILD_TYPE=Release -D CMAKE_INSTALL_PREFIX=/usr/local -D WITH_CUDA=ON -D OPENCV_EXTRA_MODULES_PATH=../../opencv_contrib/modules -D BUILD_TIFF=ON ..`

### Explaination of Output
The output is three channels JPG images. BGR of the image represents x, y, and magnitude of the optical flow value, 
respectively. 

### Example
./compute_flow --gpuID=0 --type=1 --skip=1 --vid_path xxx --out_path xxx


### Compile 
cmake -D CMAKE_BUILD_TYPE=RELEASE     -D CMAKE_INSTALL_PREFIX=/usr/local     -D WITH_CUDA=ON     -D ENABLE_FAST_MATH=1     -D CUDA_FAST_MATH=1     -D WITH_CUBLAS=1     -D INSTALL_PYTHON_EXAMPLES=ON     -D OPENCV_EXTRA_MODULES_PATH=../../opencv_contrib-3.4.5/modules     -D BUILD_EXAMPLES=ON ..

### Run
./compute_flow --gpuID=0 --type=1 --skip=100 --vid_path='/home/dmitry/Documents/Projects/opticalFlow_TwoStreamNN/dataset/videos' --out_path='/home/dmitry/Documents/Projects/opticalFlow_TwoStreamNN/dataset/output'