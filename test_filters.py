import cv2
import numpy as np
import os

'''
    Function to test the filters, have three option to see the image:
    1) Original image
    2) After the filters are apply
    3) With the contours 
'''
def filters(file):
    # read the image    
    image = cv2.imread('%s/%s' % (FOLDER_PATH, file))
    
    # verify if the color of the image
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    mean = cv2.mean(gray)[0]
    if mean < 127:
        image = cv2.bitwise_not(image)
        
    # crop the image
    height, width,_ = image.shape
    crop_size = int(min(height, width) * 0.40)
    x = int((width - crop_size) / 2)
    y = int((height - crop_size) / 2)
    image = image[y:y+crop_size, x:x+crop_size]
    
    # 1 option:
    # cv2.imshow('Original image', image)
    # cv2.waitKey(0)
    
    # filters
    gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    # image = cv2.medianBlur(gray_image, 1) # !!!!!!!!!!!!!!
    image_blur = cv2.GaussianBlur(gray_image, (1, 1), 0)
    # image_blur = cv2.blur(gray_image, (3, 3))
    # _, th = cv2.threshold(image_blur, 0, 255, cv2.THRESH_BINARY+cv2.THRESH_OTSU)
    image_eq = cv2.equalizeHist(image_blur)
    th_adap = cv2.adaptiveThreshold(image_eq, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY_INV, 11, 2)

    # Apply aperture morphological filter
    kernel = np.ones((5, 5),np.uint8)
    opening = cv2.morphologyEx(th_adap, cv2.MORPH_OPEN, kernel, iterations=1)
    
    # 2 option:
    # cv2.imshow('Filter image', opening)
    # cv2.waitKey(0)
    
    # indentify the contours 
    '''
        try to find the best image for input in cv2.findCountours
    '''
    contours, hierarchy = cv2.findContours(opening, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    
    # calculate AR
    image_cnt = image.copy()
    for cnt in contours:
        '''
            cv2.fitEllipse needs 5 point in contours. Some contours have less than 5 points.
            Try to use the the function fitEllipse to calculate the AR. If don't work, use the function
            minAreaRect to calculate the AR.
        '''
        try:
            ellipse = cv2.fitEllipse(cnt)
                           
            # draw the contours
            image_cnt = cv2.ellipse(image_cnt, ellipse[0], ellipse[1], ellipse[2], 0, 360, (0, 0, 255), 3)
            
        except:
            rect = cv2.minAreaRect(cnt)
            box = cv2.boxPoints(rect)
            box = np.int0(box)       

            #draw the contours
            image_cnt = cv2.drawContours(image_cnt, [box], 0, (0, 0, 255), 2)
      
    # 3 option:
    cv2.imshow('Contours', image_cnt)
    cv2.waitKey(0)
    
# FOLDER_PATH = 'D:\LUCAS\IC\FUNWAX\Images'
FOLDER_PATH = '/home/lucas/FUNWAX/Images'
files = os.listdir(FOLDER_PATH)
for file in files:
    type = file[:-4].split('_')[1]
    if file.endswith('.jpg') and type == 'Micro':
        filters(file)
