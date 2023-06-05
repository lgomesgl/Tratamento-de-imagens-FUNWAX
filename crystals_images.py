#import the libraries
import numpy as np
import pandas as pd
import cv2
import matplotlib.pyplot as plt
import seaborn as sns
import os 

# create the database
def database(file, data, cnt_ellipse, cnt_rect):    
    # properties
    properties = file[:-4].split('_')
    '''
        properties[0] -> Number of the teste
            ''    [1] -> Type(Macro, Micro, Mist)
            ''    [2] -> Concentration
            ''    [3] -> Reynolds
            ''    [4] -> Toil
            ''    [5] -> Tcool
            ''    [6] -> Time
    '''
    
    # get the contours(Leticia code)
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
    
    # filters
    if properties[1] == 'Macro':
        gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        # image = cv2.medianBlur(gray_image, 1) # !!!!!!!!!!!!!!
        image_blur = cv2.GaussianBlur(gray_image, (3,3), 0)
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
              
    # calculate AR
    for cnt in contours:
        '''
            cv2.fitEllipse needs 5 point in contours. Some contours have less than 5 points.
            Try to use the the function fitEllipse to calculate the AR. If don't work, use the function
            minAreaRect to calculate the AR.
        '''
        try:
            ellipse = cv2.fitEllipse(cnt)
                  
            major = max(ellipse[1][0], ellipse[1][1])
            minor = min(ellipse[1][0], ellipse[1][1])
            ar = major/minor
            
            row_to_append = pd.DataFrame([{'Type':properties[1], 'Reynolds':properties[3], 'Toil':properties[4], 'Tcool':properties[5], 'Time':properties[6], 'AR': ar}])
            data = pd.concat([data, row_to_append], ignore_index=True)
            
            cnt_ellipse += 1
            
            # draw the contours
            image = cv2.ellipse(image, ellipse[0], ellipse[1], ellipse[2], 0, 360, (0, 0, 255), 3)
            
        except:
            rect = cv2.minAreaRect(cnt)
            box = cv2.boxPoints(rect)
            box = np.int0(box)       
            '''
                rect -> ((x, y), (w, h), angle)
                https://namkeenman.wordpress.com/2015/12/18/open-cv-determine-angle-of-rotatedrect-minarearect/
            '''
            # calculate the AR 
            major = max(rect[1][0], rect[1][1])
            minor = min(rect[1][0], rect[1][1])
            ar = major/minor
            
            row_to_append = pd.DataFrame([{'Type':properties[1], 'Reynolds':properties[3], 'Toil':properties[4], 'Tcool':properties[5], 'Time':properties[6], 'AR': ar}])
            data = pd.concat([data, row_to_append], ignore_index=True)
            
            cnt_rect += 1
            
            #draw the contours
            image = cv2.drawContours(image, [box], 0, (0, 0, 255), 2)
      
    # validate the contours
    # cv2.imshow('Cristais', image)
    # cv2.waitKey(0)
    
    N_of_crystals = data.shape[0]
    
    return data, properties, N_of_crystals, cnt_ellipse, cnt_rect
       
def graphics(data, data_crystals):
    # 1: AR x Reynolds, hue = Type
    plt.subplot(2, 2, 1)
    sns.lineplot(x=data['Reynolds'], y=data['AR'], hue=data['Type'])
    plt.title('AR x Reynolds')

    # 2: AR x Reynolds, hue = Toil
    plt.subplot(2, 2, 2)
    sns.lineplot(x=data['Reynolds'], y=data['AR'], hue=data['Toil'])
    plt.title('AR x Reynolds')

    # 3: AR x Reynolds, hue = Tcool
    plt.subplot(2, 2, 3)
    sns.lineplot(x=data['Reynolds'], y=data['AR'], hue=data['Tcool'])
    plt.title('AR x Reynolds')
 
    # 4: AR x Time
    plt.subplot(2, 2, 4)
    df = data.copy()
    df['Time'] = df['Time'].astype(int)
    df = df.sort_values('Time', ascending=True).reset_index(drop=True)
    sns.lineplot(df, x=df['Time'], y=df['AR'], hue=df['Type'])
    plt.title('AR x Time')
    plt.show()
    
    # 5: Distribution of AR
    sns.histplot(data, x = data['AR'], bins=100, kde=True, hue=data['Type'])
    plt.title('Distribuiton of AR')
    plt.show()
  
    # --------------------------------------- N_of_crystals graphics ---------------------------------------------------
    # 6: N of crystals x Reynolds, hue = Type
    plt.subplot(2, 2, 1)
    sns.lineplot(x=data_crystals['Reynolds'], y=data_crystals['N_of_crystals'], hue=data_crystals['Type'])
    plt.title('N_of_crystals x Reynolds')
 
    # 7: N of crystals x Reynolds, hue = Toil
    plt.subplot(2, 2, 2)
    sns.lineplot(x=data_crystals['Reynolds'], y=data_crystals['N_of_crystals'], hue=data_crystals['Toil'])
    plt.title('N_of_crystals x Reynolds')
 
    # 8: N of crystals x Reynolds, hue = Tcool
    plt.subplot(2, 2, 3)
    sns.lineplot(x=data_crystals['Reynolds'], y=data_crystals['N_of_crystals'], hue=data_crystals['Tcool'])
    plt.title('N_of_crystals x Reynolds')
 
    # 10: N_of_crystals x Time
    plt.subplot(2, 2, 4)
    df_ = data_crystals.copy()
    df_['Time'] = df_['Time'].astype(int)
    df_ = df_.sort_values('Time', ascending=True).reset_index(drop=True)
    sns.lineplot(df_, x=df_['Time'], y=df_['N_of_crystals'], hue=df_['Type'])
    plt.title('AR x Time')
    plt.show()
    
    # 9: Distribution of N_of_crystals
    sns.histplot(data_crystals, x = data_crystals['N_of_crystals'], bins=100, kde=True, hue=data_crystals['Type'])
    plt.title('Distribuiton of N_of_crystals')
    plt.show()  
    
    
# FOLDER_PATH = '/home/lucas/FUNWAX/Images'
FOLDER_PATH = 'D:\LUCAS\IC\FUNWAX\Images'
data = pd.DataFrame(columns=['Type', 'Reynolds', 'Toil', 'Tcool', 'Time', 'AR'])
data_crystals = pd.DataFrame(columns=['Type', 'Reynolds', 'Toil', 'Tcool', 'Time', 'N_of_crystals'])

cnt_ellipse = 0
cnt_rect = 0

N_of_crystals_ = [0]

files = os.listdir(FOLDER_PATH) # list with all files in folder
for i, file in enumerate(files):
    if file.endswith('.jpg'): # take just the images
        data, properties, N_of_crystals, cnt_ellipse, cnt_rect = database(file, data, cnt_ellipse, cnt_rect)
        print('%s...OK' % file)
        N_of_crystals_.append(N_of_crystals)
        row_to_append = pd.DataFrame([{'Type':properties[1], 'Reynolds':properties[3], 'Toil':properties[4], 'Tcool':properties[5], 'Time':properties[6], 'N_of_crystals': int(N_of_crystals-N_of_crystals_[i])}])
        data_crystals = pd.concat([data_crystals, row_to_append], ignore_index=True)
        
# print(data)
graphics(data, data_crystals)

print('AR calculate by ellipse: %s' % cnt_ellipse)
print('AR calculate by rectangle: %s' % cnt_rect)
print('Total: %s' % (cnt_ellipse + cnt_rect))
print('Percentage of AR ellipse: %s' % (round((cnt_ellipse*100/(cnt_ellipse+cnt_rect)), 2)))