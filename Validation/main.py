'''
    Validate each crystal that functions of open-cv classifier. The propose is to use
    the same filter that we apply in Classification. Create some graphics. 
    In the final create a training data
'''
import pandas as pd
import numpy as np
import cv2
import os

from cristal_class import CrystalsClassification
from accept import accept

def get_image(folder_path, file):
    return cv2.imread('%s/%s' % (folder_path, file))

def crop_the_image(image, scale_crop):
    height, width,_ = image.shape
    crop_size = int(min(height, width) * scale_crop)
    x = int((width - crop_size) / 2)
    y = int((height - crop_size) / 2)
    image = image[y:y+crop_size, x:x+crop_size]
    return image

def get_properties(file):
    '''
        properties[0] -> Number of the teste
            ''    [1] -> Type(Macro, Micro, Mist)
            ''    [2] -> Concentration
            ''    [3] -> Reynolds
            ''    [4] -> Toil
            ''    [5] -> Tcool
            ''    [6] -> Time
    '''
    properties = file[:-4].split('_')
    return properties

def filter(image, properties):
    # verify if the color of the image
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    mean = cv2.mean(gray)[0]
    if mean < 127:
        image = cv2.bitwise_not(image)

    # filters
    if properties[1] == 'Macro':
        gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        # image = cv2.medianBlur(gray_image, 1) # !!!!!!!!!!!!!!
        image_blur = cv2.GaussianBlur(gray_image, (3, 3), 0)
        # _, th = cv2.threshold(image_blur, 0, 255, cv2.THRESH_BINARY+cv2.THRESH_OTSU)
        image_eq = cv2.equalizeHist(image_blur)
        th_adap = cv2.adaptiveThreshold(image_eq, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY_INV, 11, 2)

        # Apply aperture morphological filter
        kernel = np.ones((5, 5),np.uint8)
        opening = cv2.morphologyEx(th_adap, cv2.MORPH_OPEN, kernel, iterations=1)
        # cv2.imshow('teste', opening)
        # cv2.waitKey(0)
        
        # indentify the contours 
        '''
            try to find the best image for input in cv2.findCountours
        '''
        contours, hierarchy = cv2.findContours(opening, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
           
    elif properties[1] == 'Micro':
        gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        # image = cv2.medianBlur(gray_image, 1) # !!!!!!!!!!!!!!
        image_blur = cv2.GaussianBlur(gray_image, (1, 1), 0)
        # _, th = cv2.threshold(image_blur, 0, 255, cv2.THRESH_BINARY+cv2.THRESH_OTSU)
        image_eq = cv2.equalizeHist(image_blur)
        th_adap = cv2.adaptiveThreshold(image_eq, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY_INV, 11, 2)

        # Apply aperture morphological filter
        kernel = np.ones((5, 5),np.uint8)
        opening = cv2.morphologyEx(th_adap, cv2.MORPH_OPEN, kernel, iterations=1)
        # cv2.imshow('teste', opening)
        # cv2.waitKey(0)
        
        # indentify the contours 
        '''
            try to find the best image for input in cv2.findCountours
        '''
        contours, hierarchy = cv2.findContours(opening, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

    return contours

def validate(image, contours):
    for cnt in contours:

        try:
            ellipse = cv2.fitEllipse(cnt)
                  
            cx = ellipse[0][0]
            cy = ellipse[0][1]
            major = max(ellipse[1][0], ellipse[1][1])
            minor = min(ellipse[1][0], ellipse[1][1])
            angle = ellipse[2]
            ar = major/minor
            
            # row_to_append = pd.DataFrame([{'Type':properties[1], 'Reynolds':properties[3], 'Toil':properties[4], 'Tcool':properties[5], 'Time':properties[6], 'cx': cx, 'cy': cy, 'major': major, 'minor': minor, 'angle':angle, 'AR': ar}])
            # data = pd.concat([data, row_to_append], ignore_index=True)
            
            # cnt_ellipse += 1
        
            # draw the contours
            image = cv2.ellipse(image, ellipse[0], ellipse[1], ellipse[2], 0, 360, (0, 255, 0), 3)
                   
            cv2.imshow('Cristais', image)
            cv2.waitKey(0)
            
            # accept()
           
        except:
            rect = cv2.minAreaRect(cnt)
            box = cv2.boxPoints(rect)
            box = np.int0(box)       

            # calculate the AR 
            cx = rect[0][0]
            cy = rect[0][1]
            major = max(rect[1][0], rect[1][1])
            minor = min(rect[1][0], rect[1][1])
            angle = rect[2]
            ar = major/minor
            
            # row_to_append = pd.DataFrame([{'Type':properties[1], 'Reynolds':properties[3], 'Toil':properties[4], 'Tcool':properties[5], 'Time':properties[6], 'cx': cx, 'cy': cy, 'major': major, 'minor': minor, 'angle':angle, 'AR': ar}])
            # data = pd.concat([data, row_to_append], ignore_index=True)
            
            # cnt_rect += 1
            
            #draw the contours
            image = cv2.drawContours(image, [box], 0, (0, 255, 0), 2)

            cv2.imshow('Cristais', image)
            cv2.waitKey(0)
            
            # accept()
            
    # # validate the contours
    # cv2.imshow('Cristais', image)
    # cv2.waitKey(0)
    

IMAGES_PATH = 'D:\LUCAS\IC\FUNWAX\Images'

files = os.listdir(IMAGES_PATH)
for file in files:
    propeties = get_properties(file)
    image = get_image(IMAGES_PATH, file)
    image = crop_the_image(image, 0.4)
    contours = filter(image, propeties)
    
    
    validate(image, contours)
    
    
    