'''
    We start the project cropping the raw image in the center. But we noticed that micro type images
    have a different tendency in crystal formation. So we decide to create a low level filter to identify these formations(we called island),
    to correctly classify the crystals.
'''
import numpy as np
import pandas as pd
import cv2
import os

def create_dataframes(columns):
    return pd.DataFrame(columns=columns)

def row_to_append(dataframe, columns, values):
    dict = {}
    for i, column in enumerate(columns):
        dict[column] = values[i]
    row_to_append = pd.DataFrame([dict])
    return pd.concat([dataframe, row_to_append], ignore_index=True)

def get_image(file):
    return cv2.imread('%s/%s' % (FOLDER_PATH, file))

def save_the_image(folder_path, filename, image):
    return cv2.imwrite(os.path.join(folder_path, '%s_island.jpg' % filename[:-4]), image)

def check_if_image_island_exists(folder_path, file):
    if file and '%s_island.jpg' % file[:-4] in os.listdir(folder_path):
        return True
    return False

def get_properties(file):
    properties = file[:-4].split('_')
    return properties

def image_island(properties):
    if len(properties) == 8:
        return True
    return False

def filter(image):
    # Converte para escala de cinza
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    # thresholding
    ret, thresh = cv2.threshold(gray, 60, 255, cv2.THRESH_BINARY)

    # Encontra contornos
    contours, hierarchy = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    return contours, hierarchy

def classify(image, data, contours, hierarchy, properties):
    # contours = sorted(contours, key=cv2.contourArea, reverse=True)[1:20]
    for i, cnt in enumerate(contours):
        if hierarchy[0, i, 2] != -1:  # Check if it's a parent contour (island), does not enter in dataset
            minAreaRect = cv2.minAreaRect(cnt)
            width, height = minAreaRect[1]
            if min(width, height) > 0:
                aspect_ratio = max(width, height) / min(width, height)
                box = cv2.boxPoints(minAreaRect)
                box = np.int0(box)

                # draw the contours
                image = cv2.drawContours(image, [box], 0, (0, 255, 0), 1) 
                
        elif hierarchy[0, i, 3] != -1:  # Check if it's a child contour (inside an island)
            minAreaRect = cv2.minAreaRect(cnt)
            width, height = minAreaRect[1]
            if min(width, height) > 0:
                aspect_ratio = max(width, height) / min(width, height)
                box = cv2.boxPoints(minAreaRect)
                box = np.int0(box)
            
                # draw the contours
                image = cv2.drawContours(image, [box], 0, (255, 0, 0), 1)
                        
        else:
            minAreaRect = cv2.minAreaRect(cnt)
            width, height = minAreaRect[1]          
            if min(width, height) > 0:
                major = max(width, height)
                minor = min(width, height)
                aspect_ratio = major / minor
                area = major * minor
                box = cv2.boxPoints(minAreaRect)
                box = np.int0(box)         
                row_to_append = pd.DataFrame([{'Type':properties[1], 'Reynolds':properties[3], 'Toil':properties[4], 'Tcool':properties[5], 'Time':int(properties[6]), 'AR': aspect_ratio,'Area':area, 'Countour': cnt}])
                data = pd.concat([data, row_to_append], ignore_index=True)   
                                 
                # draw the contours
                image = cv2.drawContours(image, [box], 0, (0, 0, 255), 1)    

    # validate the contours
    # cv2.imshow('Image', image)
    # cv2.waitKey(0)
    # cv2.destroyAllWindows()      
    
    return data          

def crop_the_island(image):
    # Converte para escala de cinza
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    # thresholding
    ret, thresh = cv2.threshold(gray, 60, 255, cv2.THRESH_BINARY)

    # Encontra contornos
    contours, hierarchy = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    # Encontra contorno com maior área
    largest_contour = max(contours, key=cv2.contourArea)

    # Retâgulo em torno do maior contorno
    x, y, w, h = cv2.boundingRect(largest_contour)

    # Crop 
    cropped_gray = gray[y:y+h, x:x+w]
    cropped_image = image[y:y+h, x:x+w]

    # Mostra crop
    # cv2.imshow("Cropped Gray", cropped_gray)
    cv2.imshow("Cropped Color", cropped_image)

    cv2.waitKey(0)
    cv2.destroyAllWindows()
    
    return cropped_image, contours, hierarchy

def data_each_image(data, n_cnt, n_of_crystals):
    n_cnt.append(n_of_crystals)

    if len(n_cnt) == 1:
        return data.iloc[0:n_of_crystals]
    else:  
        return data.iloc[n_cnt[-2]:n_cnt[-1]]  
    
def data_islands(data_image, quant_islands):
    data_image = data_image.sort_values("Area", ascending=False)
    return data_image[:quant_islands]

def exclude_island_full_image(data_islands, size_image):
    for i in range(data_islands.shape[0]):
        if data_islands.iloc[i,:]['Area'] == size_image:
            data_islands = data_islands.drop(data_islands.iloc[i,:].name, axis=0)
    return data_islands
    
    
# Path 
# FOLDER_PATH = '/home/lucas/FUNWAX/Images' ## linux path
FOLDER_PATH = 'D:\LUCAS\IC\FUNWAX\Island_classification_at_micro\MicroImages'
data = create_dataframes(['Type', 'Reynolds', 'Toil', 'Tcool', 'Time','AR','Area','Countour'])
n_cnt = []
for i,file in enumerate(os.listdir(FOLDER_PATH)):
    if get_properties(file)[1] == 'Micro' and (image_island(get_properties(file)) is False) and (check_if_image_island_exists(FOLDER_PATH, file) is False): 
        image = get_image(file)
        contours, hierarchy = filter(image)
        data = classify(image,data,contours,hierarchy,get_properties(file))
        df = data_each_image(data, n_cnt, data.shape[0])
        df_ = data_islands(df, 5)
        df__ = exclude_island_full_image(df_, image.shape[0]*image.shape[1])
        
        # island_image = crop_the_island(image)
        # save_the_image(FOLDER_PATH, file, island_image)
    print('%s...OK' % file)