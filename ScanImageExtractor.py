# -*- coding: utf-8 -*-
"""
Created on Sat Aug  1 23:25:48 2020

@author: Torque
"""

import cv2
import numpy as np
import matplotlib.pyplot as plt

def crop_minAreaRect(img, rect):

    center = rect[0]
    size = rect[1]
    angle = rect[2]
    center, size = tuple(map(int, center)), tuple(map(int, size))

    # get row and col num in img
    height, width = img.shape[0], img.shape[1]
    print("width: {}, height: {}".format(width, height))

    M = cv2.getRotationMatrix2D(center, angle, 1)
    img_rot = cv2.warpAffine(img, M, (width, height))

    img_crop = cv2.getRectSubPix(img_rot, size, center)

    return img_crop

if __name__ == "__main__":
    
    input_image = cv2.imread("3.jpg")
    color_image = input_image.copy()
    gray_image = cv2.cvtColor(input_image, cv2.COLOR_BGR2GRAY)
    blurred_image = cv2.GaussianBlur(gray_image, (3,3), 0)
    ret, threshold_image = cv2.threshold(blurred_image, 215, 255, cv2.THRESH_BINARY_INV)
    kernel= np.ones((9,9),np.uint8)
    threshold_image = cv2.dilate(threshold_image, kernel, iterations=10)
    threshold_image = cv2.erode(threshold_image, kernel,iterations = 30)
    threshold_image = cv2.dilate(threshold_image, kernel, iterations=15)
    cv2.imshow("Image", threshold_image)
    cv2.waitKey(0)
    cv2.destroyAllWindows() 
    cv2.imwrite("Threshold.png", threshold_image)
    
    contours, hierarchy = cv2.findContours(threshold_image, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    contours = sorted(contours, key = cv2.contourArea, reverse=True)
    
    selected_contours = []
    file_number = 1
    for i in range(10):
        
        if(i == len(contours)):
            break

        accuracy = 0.01 * cv2.arcLength(contours[i], True)
        approx = cv2.approxPolyDP(contours[i], accuracy, True)
        
        if(len(approx) == 4):
            
            rect = cv2.minAreaRect(contours[i])
            print(rect)
            
            box = cv2.boxPoints(rect)
            print(box)
            box = np.int0(box)
            cv2.drawContours(input_image,[box],0,(0,0,255),1)
            cv2.imshow("temp", input_image)
            cv2.waitKey(0)
            cv2.destroyAllWindows()
            

            split_image = crop_minAreaRect(color_image, rect)
            cv2.imshow("temp", split_image)
            cv2.waitKey(0)
            cv2.destroyAllWindows()
            
            cv2.imwrite("Extrr"+str(file_number)+".png", split_image)
            file_number += 1
            
            selected_contours.append(contours[i])
    
    cv2.drawContours(color_image, selected_contours, -1, (0,255,0), 1)
    
    
    cv2.imshow("Image", color_image)
    cv2.waitKey(0)
    cv2.destroyAllWindows()
    
    
    
    
    
