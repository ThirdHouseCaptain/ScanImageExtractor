# -*- coding: utf-8 -*-
"""
Created on Sat Aug  1 23:25:48 2020

@author: Torque
"""

import cv2
import numpy as np
import matplotlib.pyplot as plt
import glob
import os
import ntpath
from tqdm import tqdm

def crop_minAreaRect(img, rect):

    center = rect[0]
    size = rect[1]
    angle = rect[2]
    center, size = tuple(map(int, center)), tuple(map(int, size))

    # get row and col num in img
    height, width = img.shape[0], img.shape[1]
    #print("width: {}, height: {}".format(width, height))

    M = cv2.getRotationMatrix2D(center, angle, 1)
    img_rot = cv2.warpAffine(img, M, (width, height))

    img_crop = cv2.getRectSubPix(img_rot, size, center)

    return img_crop

if __name__ == "__main__":
    
    path = os.getcwd()+"/*.jpg"
    
    try:
        os.mkdir("Extracted_Images")
    except OSError as error:
        pass
    
    for file_path in tqdm(glob.glob(path)):
    
        input_image = cv2.imread(file_path)
        file_path = ntpath.basename(file_path)
        
        file_name, file_ext = os.path.splitext(file_path)
        
        color_image = input_image.copy()
        
        gray_image = cv2.cvtColor(input_image, cv2.COLOR_BGR2GRAY)
        
        blurred_image = cv2.GaussianBlur(gray_image, (5,5), 0)
        
        ret, threshold_image = cv2.threshold(blurred_image, 215, 255, cv2.THRESH_BINARY_INV)
        #cv2.imwrite("Threshold1.png", threshold_image)
        
        kernel= np.ones((9,9),np.uint8)
        threshold_image = cv2.dilate(threshold_image, kernel, iterations=10)
        #cv2.imwrite("Threshold2.png", threshold_image)
        
        threshold_image = cv2.erode(threshold_image, kernel, iterations = 40)
        #cv2.imwrite("Threshold3.png", threshold_image)
        
        threshold_image = cv2.dilate(threshold_image, kernel, iterations=26)
        
       
        contours, hierarchy = cv2.findContours(threshold_image, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
        contours = sorted(contours, key = cv2.contourArea, reverse=True)
        
        selected_contours = []
        file_number = 1
        
        for i in range(10):
            
            if(i == len(contours)):
                break
                
            rect = cv2.minAreaRect(contours[i])
            split_image = crop_minAreaRect(color_image, rect)
            split_image = cv2.rotate(split_image, cv2.ROTATE_90_COUNTERCLOCKWISE)
            #cv2.imshow("Hello", split_image)
            #cv2.waitKey(0)
            #cv2.destroyAllWindows()
            cv2.imwrite("Extracted_Images/"+ file_name +"-"+str(file_number)+".png", split_image)
            file_number += 1
        