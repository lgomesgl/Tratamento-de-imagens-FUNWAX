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
    image_cnt = image.copy()
    
    image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    image = cv2.GaussianBlur(image, (3, 3), 0)
    kernel = np.ones((4, 4), np.uint8)
    # image = cv2.erode(image, kernel) 
    image = cv2.dilate(image, kernel, iterations=1)
    ret, image = cv2.threshold(image, 220, 255, cv2.THRESH_BINARY)
    # image = cv2.equalizeHist(image)
    # image = cv2.adaptiveThreshold(image, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY_INV, 11, 2)
    # image = cv2.morphologyEx(image, cv2.MORPH_OPEN, kernel, iterations=1)
    
    contours, hierarchy = cv2.findContours(image, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    
    # calculate AR
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
    
    cv2.namedWindow('raw image', cv2.WINDOW_NORMAL)
    cv2.imshow('raw image', image_cnt)
    cv2.waitKey(0)
    cv2.destroyAllWindows()
    
    return image
    
FOLDER_PATH = 'D:\LUCAS\IC\FUNWAX\Images'
# FOLDER_PATH = '/home/lucas/FUNWAX/Images'
# files = os.listdir(FOLDER_PATH)
# for file in files:
#     type = file[:-4].split('_')[1]
#     if file.endswith('.jpg') and type == 'Micro':
#         filters(file)

file ='1_Micro_10_5000_47_6_31_island.jpg'
image = filters(file)