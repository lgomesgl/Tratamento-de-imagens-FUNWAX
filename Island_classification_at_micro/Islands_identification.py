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

def save_the_image(folder_path, filename, num, image):
    return cv2.imwrite(os.path.join(folder_path, '%s_island_%s.jpg' % (filename[:-4], num)), image)

def check_if_image_island_exists(folder_path, file):
    if file and '%s_island.jpg' % file[:-4] in os.listdir(folder_path):
        return True
    return False

def get_properties(file):
    properties = file[:-4].split('_')
    return properties

def image_island(properties):
    if len(properties) >= 8:
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


def data_each_image(data, n_cnt, n_of_crystals):
    n_cnt.append(n_of_crystals)

    if len(n_cnt) == 1:
        return data.iloc[0:n_of_crystals]
    else:  
        return data.iloc[n_cnt[-2]:n_cnt[-1]]  
    
def data_islands(data_image, quant_islands):
    data_image = data_image.sort_values("Area", ascending=False)
    return data_image[:quant_islands]

def check_island_is_full_image(data_islands,i,size_image):
    if int(data_islands.iloc[i,:]['Area']) > int(0.95 * size_image):
        return True
    return False

def draw_island(image, data_islands):
    for i in range(data_islands.shape[0]):
        mimAreaRect = cv2.minAreaRect(data_islands.iloc[i,:]['Countour'])
        box = cv2.boxPoints(mimAreaRect)
        box = np.int0(box)
        image = cv2.drawContours(image, [box], 0, (0, 0, 255), 1)
        
        # cv2.imshow('Image', image)
        # cv2.waitKey(0)
        # cv2.destroyAllWindows()
        
def crop_the_island(image, cnt):
    x, y, w, h = cv2.boundingRect(cnt)
    cropped_image = image[y:y+h, x:x+w]

    # cv2.imshow("Cropped Color", cropped_image)
    # cv2.waitKey(0)
    # cv2.destroyAllWindows()
    
    return cropped_image

def detect_if_island_is_legend(island_image):
    lower_red = np.array([0, 0, 200], dtype = "uint8")
    upper_red= np.array([0, 0, 255], dtype = "uint8")
    mask = cv2.inRange(island_image, lower_red, upper_red)
    size_image = island_image.shape[0]*island_image.shape[1]
    
    if not sum(sum(mask)) == 0 and size_image < 100000:
        return True
    return False
    
# Path 
# FOLDER_PATH = '/home/lucas/FUNWAX/Images' ## linux path
FOLDER_PATH = 'D:\LUCAS\IC\FUNWAX\Island_classification_at_micro\MicroImages'
data = create_dataframes(['Type', 'Reynolds', 'Toil', 'Tcool', 'Time','AR','Area','Countour'])
n_cnt = []
for file in (os.listdir(FOLDER_PATH)):
    if get_properties(file)[1] == 'Micro' and (image_island(get_properties(file)) is False) and (check_if_image_island_exists(FOLDER_PATH, file) is False): 
        print('%s' % file)
        image = get_image(file)
        image_df = image.copy()
        image_is = image.copy()
        contours, hierarchy = filter(image)
        data = classify(image,data,contours,hierarchy,get_properties(file))
        df = data_each_image(data, n_cnt, data.shape[0])
        df_islands = data_islands(df, 5)
        # draw_island(image_df, df_islands)
        count = 1
        for i in range(df_islands.shape[0]):
            island_image = crop_the_island(image_is, df_islands.iloc[i,:]['Countour'])
            
            if detect_if_island_is_legend(island_image):
                continue
            
            save_the_image(FOLDER_PATH, filename=file, num=count, image=island_image)
            count +=1
            if check_island_is_full_image(df_islands, i,image.shape[0]*image.shape[1]):
                break
        
def delete_islands(folder_path):
    for file in os.listdir(folder_path):
        if image_island(get_properties(file)) is True:
            os.remove('%s/%s' %(folder_path, file))
            
# delete_islands(FOLDER_PATH)
    