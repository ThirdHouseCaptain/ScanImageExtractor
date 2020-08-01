# -*- coding: utf-8 -*-
"""
Created on Sat Aug  1 23:25:48 2020

@author: Torque
"""

import cv2
from win32api import GetSystemMetrics

if __name__ == "__main__":
    
    input_image = cv2.imread("2.jpg")
    color_image = input_image.copy()
    gray_image = cv2.cvtColor(input_image, cv2.COLOR_BGR2GRAY)
    blurred_image = cv2.GaussianBlur(gray_image, (3,3), 0)
    ret, threshold_image = cv2.threshold(blurred_image, 215, 255, cv2.THRESH_BINARY_INV)
    cv2.imshow("Image", threshold_image)
    cv2.waitKey(0)
    cv2.destroyAllWindows() 
    
    contours, hierarchy = cv2.findContours(threshold_image, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    contours = sorted(contours, key = cv2.contourArea, reverse=True)
    
    selected_contours = []
    
    for i in range(10):

        accuracy = 0.01 * cv2.arcLength(contours[i], True)
        approx = cv2.approxPolyDP(contours[i], accuracy, True)
        if(len(approx) == 4):
            
    
    cv2.drawContours(color_image, selected_contours, -1, (0,255,0), 1)
    
    
    cv2.imshow("Image", color_image)
    cv2.waitKey(0)
    cv2.destroyAllWindows()
    
    
    
    
    
