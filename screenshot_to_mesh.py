#!/usr/bin/python
import pandas as pd
import numpy as np
import cv2
import argparse

from pyntcloud import PyntCloud   # https://github.com/daavoo/pyntcloud
from PIL import Image
from sklearn.preprocessing import normalize

def generate_mesh(filename):
    #   # Open an image as RGB
    print("Opening " + filename)
    original = Image.open(filename).convert('RGB')
    
    #   # Get the dimensions
    width, height = original.size
    
    #   # Split into left and right halves
    right  = original.crop( (0,       0, width/2, height))
    left   = original.crop( (width/2, 0, width,   height))
    
    #   # Optional - Save images
    # right.save(filename+"-right.png")
    # left.save(filename+"-left.png")
    
    #   # Convert to arrays
    image_left  = np.array(left) 
    image_right = np.array(right) 

    #   # Simple but less effective
    # stereo = cv2.StereoBM_create(numDisparities=0, blockSize=25)
    # disparity = stereo.compute(image_left,image_right)
    # depth_image = Image.fromarray(disparity).convert('L')

    #   # Parameters for dispartiy map
    print("Generating Depth Map")
    window_size = 15
     
    left_matcher = cv2.StereoSGBM_create(
        #   # Documentation at https://docs.opencv.org/trunk/d2/d85/classcv_1_1StereoSGBM.html
        minDisparity=0,
        numDisparities=16,
        blockSize=5,
        P1=8 * 3 * window_size ** 2,
        P2=32 * 3 * window_size ** 2,
        # disp12MaxDiff = 0,
        # preFilterCap = 0,
        # uniquenessRatio = 0,
        # speckleWindowSize = 0,
        # speckleRange = 0,
        # mode = StereoSGBM::MODE_SGBM  #   https://docs.opencv.org/trunk/d2/d85/classcv_1_1StereoSGBM.html#ad985310396dd4d95a003b83811bbc138
    )
    
    #   # Create matchers
    right_matcher = cv2.ximgproc.createRightMatcher(left_matcher)
     
    wls_filter = cv2.ximgproc.createDisparityWLSFilter(matcher_left=left_matcher)
    wls_filter.setLambda(80000)
    wls_filter.setSigmaColor(1.2)
     
    disparity_left  = left_matcher.compute(image_left, image_right)
    disparity_right = right_matcher.compute(image_right, image_left)
    disparity_left  = np.int16(disparity_left)
    disparity_right = np.int16(disparity_right)
    filtered_image  = wls_filter.filter(disparity_left, image_left, None, disparity_right)
    
    #   # Generate a depth map
    depth_map = cv2.normalize(src=filtered_image, dst=filtered_image, beta=0, alpha=255, norm_type=cv2.NORM_MINMAX);
    depth_map = np.uint8(depth_map)
    
    #   # Invert image. Optional depending on stereo pair
    depth_map = cv2.bitwise_not(depth_map)
    #   # Greyscale
    depth_image = Image.fromarray(depth_map, mode="L")
    #   # Optional - Save Disparity
    # depth_image.save(filename+"-depth.png")

    #   # Get the colour information from the left image - resize to full-width
    print("Creating Colour Map")
    colours_array  = np.array(left.resize(original.size).getdata()).reshape((height, width) + (3,))
    
    #   # Create a Pandas DataFrame of each pixel's position and colour
    indices_array = np.moveaxis(np.indices((height, width)), 0, 2)
    imageArray    = np.dstack((indices_array, colours_array)).reshape((-1,5))
    df = pd.DataFrame(imageArray, columns=["x", "y", "red","green","blue"])

    #   # Get depth information - resize to full width
    depths_array = np.array(depth_image.resize(original.size).getdata())
    
    #   # Add to DataFrame
    df.insert(loc=2, column='z', value=depths_array)
    
    #   # Set unit type correctly
    df[['red','green','blue']] = df[['red','green','blue']].astype(np.uint)
    df[['x','y','z']] = df[['x','y','z']].astype(float)
    
    #   # Optional - increase the intensity of the depth information
    df['z'] = df['z']*5

    #   # Generate mesh
    print("Generating Mesh")
    cloud = PyntCloud(df)
    
    #   # Save mesh to file
    print("Saving Mesh")
    cloud.to_file(filename+".ply", also_save=["mesh","points"],as_text=True)

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('image_file',   help='Filename of a stereo screenshot')
    args = parser.parse_args()

    generate_mesh(args.image_file)