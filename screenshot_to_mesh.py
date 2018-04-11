#!/usr/bin/python
import pandas as pd
import numpy as np
import cv2
import argparse

from pyntcloud import PyntCloud   # https://github.com/daavoo/pyntcloud
from PIL import Image

def generate_mesh(filename):
    #   # Open an image as RGB
    print("Opening " + filename)
    original = Image.open(filename).convert('RGB')
    
    #   # Get the dimensions of the image
    width, height = original.size
    
    #   # Split into left and right halves.  The left eye sees the right image.
    right  = original.crop( (0,       0, width/2, height))
    left   = original.crop( (width/2, 0, width,   height))
    
    
    #   # Over/Under. Split into top and bottom halves. The right eye sees the top image.
    top    = original.crop( (0,        0, width, height/2))
    bottom = original.crop( (0, height/2, width,   height))

    #   # Calculate the similarity of the left/right & top/bottom.
    left_right_similarity = mse(np.array(right), np.array(left))
    top_bottom_similarity = mse(np.array(top),   np.array(bottom))

    if (top_bottom_similarity < left_right_similarity):
        #   # This is an Over/Under image
        print("Over-Under image detected")
        left  = bottom
        right = top
    else:
        print("Side-By-Side image detected")

    #   # Optional. Save split images
    # left.resize(original.size).save(filename + "-left.png")
    # right.resize(original.size).save(filename + "-right.png")
    
    #   # Convert to arrays
    image_left  = np.array(left) 
    image_right = np.array(right) 

    #   # Simple but less effective
    # stereo = cv2.StereoBM_create(numDisparities=32, blockSize=25)
    # disparity = stereo.compute(image_left,image_right)
    # depth_image = Image.fromarray(disparity).convert('L')

    #   # Parameters for dispartiy map
    print("Generating Depth Map")
    window_size = 15
    
    #   # These values can be tuned depending on the image.
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
    # depth_image.resize(original.size).save(filename+"-depth.png")

    #   # Get the colour information from the left image. Resized to original.  Rotated 90 degrees for STL.
    print("Creating Colour Map")
    colours_array  = np.array(left.resize(original.size)
                                  .rotate(-90, expand=True)
                                  .getdata()
                    ).reshape(original.size + (3,))
    
    #   # Create a Pandas DataFrame of each pixel's position and colour
    indices_array = np.moveaxis(np.indices(original.size), 0, 2)
    imageArray    = np.dstack((indices_array, colours_array)).reshape((-1,5))
    df = pd.DataFrame(imageArray, columns=["x", "y", "red","green","blue"])

    #   # Get depth information. Resized to original.  Rotated 90 degrees for STL.
    depths_array = np.array(depth_image.resize(original.size)
                                       .rotate(-90, expand=True)
                                       .getdata())
    
    #   # Add depth to DataFrame
    df.insert(loc=2, column='z', value=depths_array)
    
    #   # Set unit types correctly
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

def mse(imageA, imageB):
    # the 'Mean Squared Error' between the two images is the
    # sum of the squared difference between the two images;
    # NOTE: the two images must have the same dimension
    # From https://www.pyimagesearch.com/2014/09/15/python-compare-two-images/
    err = np.sum((imageA.astype("float") - imageB.astype("float")) ** 2)
    err /= float(imageA.shape[0] * imageA.shape[1])

    # return the MSE, the lower the error, the more "similar"
    # the two images are
    return err

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('image_file',   help='Filename of a stereo screenshot')
    args = parser.parse_args()

    generate_mesh(args.image_file)