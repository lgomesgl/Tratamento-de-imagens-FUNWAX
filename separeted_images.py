#import the libraries
import numpy as np
import pandas as pd
import cv2
import matplotlib.pyplot as plt
import seaborn as sns
import os 

# create the database
def database(file, data):    
    # properties
    properties = file[:-4].split('_')
    '''
        properties[0] -> Number of the teste
            ''    [1] -> Type(Macro, Micro, Mist)
            ''    [2] -> Concentration
            ''    [3] -> Reynolds
            ''    [4] -> Toil
            ''    [5] -> Tcool
            ''    [6] -> ?????
    '''
    
    # get the contours(Leticia code)
    # read the image
    image = cv2.imread('%s\%s' % (FOLDER_PATH, file))
    
    # verify if the color of the image
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    mean = cv2.mean(gray)[0]
    if mean < 127:
        image = cv2.bitwise_not(image)
        
    # crop the image
    height, width,_ = image.shape
    crop_size = int(min(height, width) * 0.35)
    x = int((width - crop_size) / 2)
    y = int((height - crop_size) / 2)
    image = image[y:y+crop_size, x:x+crop_size]
    
    # filters
    gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    image = cv2.medianBlur(gray_image, 1)
    image = cv2.GaussianBlur(gray_image, (3,3), 0)
    _, th = cv2.threshold(image, 0, 255, cv2.THRESH_BINARY+cv2.THRESH_OTSU)
    image = cv2.equalizeHist(image)
    th = cv2.adaptiveThreshold(image, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY_INV, 11, 2)

    # Apply aperture morphological filter
    kernel = np.ones((5,5),np.uint8)
    opening = cv2.morphologyEx(th, cv2.MORPH_OPEN, kernel, iterations=1)
    # cv2.imshow('teste', opening)
    # cv2.waitKey(0)
    
    # indentify the contours 
    contours, hierarchy = cv2.findContours(opening, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    
    # Exibir a imagem resultante com os contornos identificados
    # cv2.imshow('Contornos', opening)
    # cv2.waitKey(0)
    
    # Converter a imagem de cinza para colorida
    # img = cv2.cvtColor(image, cv2.COLOR_GRAY2BGR)
    
    # Desenhar retângulos nos contornos
    for cnt in contours:
        try:
            ellipse = cv2.fitEllipse(cnt)
                  
            major = max(ellipse[1][0], ellipse[1][1])
            minor = min(ellipse[1][0], ellipse[1][1])
            ar = major/minor
            
            row_to_append = pd.DataFrame([{'Type':properties[1], 'Reynolds':properties[3], 'Toil':properties[4], 'Tcool':properties[5], 'N_of_crystals': None, 'AR': ar}])
            data = pd.concat([data, row_to_append], ignore_index=True)
 
        except:
            rect = cv2.minAreaRect(cnt)
            box = cv2.boxPoints(rect)
            box = np.int0(box)       
            '''
                rect -> ((x, y), (w, h), angle)
            '''
            # calculate the AR -- this formula is correct?????
            major = max(abs(2*rect[1][0]*np.cos(-1*rect[2])), abs(2*rect[1][0]*np.sin(-1*rect[2])))
            minor = min(abs(2*rect[1][0]*np.cos(-1*rect[2])), abs(2*rect[1][0]*np.sin(-1*rect[2])))
            ar = major/minor
            
            row_to_append = pd.DataFrame([{'Type':properties[1], 'Reynolds':properties[3], 'Toil':properties[4], 'Tcool':properties[5], 'N_of_crystals': None, 'AR': ar}])
            data = pd.concat([data, row_to_append], ignore_index=True)
        
    return data
    
def graphics(data):
    # 1: AR x Reynolds, hue = Type
    sns.lineplot(x=data['Reynolds'], y=data['AR'], hue=data['Type'])
    plt.title('AR x Reynolds')
    plt.show()
    
    # # 2: AR x Reynolds, hue = Toil
    # sns.lineplot(x=data['Reynolds'], y=data['AR'], hue=data['Toil'])
    # plt.title('AR x Reynolds')
    # # plt.show()
    
    # # 3: AR x Reynolds, hue = Tcool
    # sns.lineplot(x=data['Reynolds'], y=data['AR'], hue=data['Tcool'])
    # plt.title('AR x Reynolds')
    # # plt.show()
    
    # # 4: N of crystals x Reynolds, hue = Type
    # sns.lineplot(x=data['N_of_crystals'], y=data['AR'], hue=data['Type'])
    # plt.title('AR x Reynolds')
    # # plt.show()
    
    # # 5: N of crystals x Reynolds, hue = Toil
    # sns.lineplot(x=data['N_of_crystals'], y=data['AR'], hue=data['Toil'])
    # plt.title('AR x Reynolds')
    # # plt.show()
    
    # # 6: N of crystals x Reynolds, hue = Tcool
    # sns.lineplot(x=data['N_of_crystals'], y=data['AR'], hue=data['Tcool'])
    # plt.title('AR x Reynolds')
    # # plt.show()
    
FOLDER_PATH = 'D:\LUCAS\IC\FUNWAX\Images'
data = pd.DataFrame(columns=['Type', 'Reynolds', 'Toil', 'Tcool', 'N_of_crystals', 'AR'])

files = os.listdir(FOLDER_PATH) # list with all files in folder
for file in files:
    if file.endswith('.jpg'): # take just the images
        data = database(file, data)

print(data)
# graphics(data)

