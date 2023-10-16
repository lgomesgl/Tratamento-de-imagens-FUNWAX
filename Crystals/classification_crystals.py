#import the libraries
import numpy as np
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import cv2
import os 

def get_files(folder_path):
    return os.listdir(folder_path)

def get_image(folder_path, file):
    return cv2.imread('%s/%s' % (folder_path, file))

def images_to_verify(properties, island):
    if properties[1] == 'Macro' or (properties[1] == 'Micro' and is_island(properties) is island) or properties[1] == 'Mistura':
        return True
    return False

def images_to_crop(island):
    if island:
        return ['Macro', 'Mistura']
    return ['Macro','Micro','Mistura']
    
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
            ''    [7] -> Island, only Micro
    '''
    properties = file[:-4].split('_')
    return properties

def filter(image, properties):
    # Convert to grayscale
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    mean = cv2.mean(gray)[0]
    if mean < 100:
        image = cv2.bitwise_not(image)

    # Apply adaptive histogram equalization
    clahe = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(10, 10))
    enhanced_gray = clahe.apply(gray)

    # Function to calculate image contrast
    def image_contrast(original, corrected):
        mean_intensity_original = np.mean(original)
        std_intensity_original = np.std(original)
        
        mean_intensity_corrected = np.mean(corrected)
        std_intensity_corrected = np.std(corrected)
        
        contrast_original = std_intensity_original / mean_intensity_original
        contrast_corrected = std_intensity_corrected / mean_intensity_corrected
        
        return contrast_original, contrast_corrected

    # Range de busca para gamma
    gamma_values = np.linspace(0.5, 3.5, num=31)
    best_gamma = 1.0
    best_contrast_increase = 0.0
    original_contrast, _ = image_contrast(enhanced_gray, enhanced_gray)
    
    for gamma in gamma_values:
        gamma_corrected = np.power(enhanced_gray / 255.0, gamma) * 255.0
        gamma_corrected = gamma_corrected.astype(np.uint8)

        _, corrected_contrast = image_contrast(enhanced_gray, gamma_corrected)
        contrast_increase = corrected_contrast - original_contrast

        if contrast_increase > best_contrast_increase:
            best_contrast_increase = contrast_increase
            best_gamma = gamma
        
    # Apply the best gamma correction
    best_gamma_corrected = np.power(enhanced_gray / 255.0, best_gamma) * 255.0
    best_gamma_corrected = best_gamma_corrected.astype(np.uint8)

    # Apply Gaussian blur (adjust kernel size as needed)
    blurred = cv2.GaussianBlur(best_gamma_corrected, (1, 1), 0)

    # Use Otsu's thresholding
    _, thresh = cv2.threshold(blurred, 90, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)

    # Find contours and contour hierarchy
    contours, hierarchy = cv2.findContours(thresh, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
         
    return contours, hierarchy

def classification(image, data, contours, hierarchy, properties):
    cont_parent, cont_child, cont_else = 0, 0, 0
    # Iterate over all contours and store aspect ratios and rectangles based on inside/outside the islands
    for i, cnt in enumerate(contours):
        if hierarchy[0, i, 2] != -1:  # Check if it's a parent contour (island), does not enter in dataset
            minAreaRect = cv2.minAreaRect(cnt)
            width, height = minAreaRect[1]
            if min(width, height) > 0:
                aspect_ratio = max(width, height) / min(width, height)
                box = cv2.boxPoints(minAreaRect)
                box = np.int0(box)
                cont_parent += 1

                # draw the contours
                image = cv2.drawContours(image, [box], 0, (0, 255, 0), 1) 
                
        elif hierarchy[0, i, 3] != -1:  # Check if it's a child contour (inside an island)
            minAreaRect = cv2.minAreaRect(cnt)
            width, height = minAreaRect[1]
            if min(width, height) > 0:
                aspect_ratio = max(width, height) / min(width, height)
                box = cv2.boxPoints(minAreaRect)
                box = np.int0(box)
                cont_child += 1
                # row_to_append = pd.DataFrame([{'Type':properties[1], 'Reynolds':properties[3], 'Toil':properties[4], 'Tcool':properties[5], 'Time':properties[6], 'Island':'Inside', 'AR': aspect_ratio}])
                # data = pd.concat([data, row_to_append], ignore_index=True)
            
                # draw the contours
                image = cv2.drawContours(image, [box], 0, (255, 0, 0), 1)
                       
        else:
            minAreaRect = cv2.minAreaRect(cnt)
            width, height = minAreaRect[1]          
            if min(width, height) > 0:
                aspect_ratio = max(width, height) / min(width, height)
                box = cv2.boxPoints(minAreaRect)
                box = np.int0(box)         
                cont_else += 1
                # row_to_append = pd.DataFrame([{'Type':properties[1], 'Reynolds':properties[3], 'Toil':properties[4], 'Tcool':properties[5], 'Time':properties[6], 'cx': cx, 'cy': cy, 'major': major, 'minor': minor, 'angle':angle, 'AR': ar}])
                row_to_append = pd.DataFrame([{'Type':properties[1], 'Reynolds':properties[3], 'Toil':properties[4], 'Tcool':properties[5], 'Time':properties[6], 'Island':'Outside', 'AR': aspect_ratio}])
                data = pd.concat([data, row_to_append], ignore_index=True)
                        
                # draw the contours
                image = cv2.drawContours(image, [box], 0, (0, 0, 255), 1)
    
    perct_parent, perct_child, perct_else = proportion_contours(cont_parent,cont_child,cont_else)


    # validate the contours
    cv2.imshow('Cristais_%s_%s_%s' % (properties[1], properties[3], properties[6]), image)
    cv2.waitKey(0)
    cv2.destroyAllWindows()
    
    # Distribution
    sns.histplot(data, x = data['AR'], bins = 20, kde=True, hue=data['Type'])
    plt.title('Distribution')
    plt.show()
        
    
    n_of_crystals = data.shape[0]
    
    return data, n_of_crystals, perct_parent, perct_child, perct_else 

def is_island(properties):
    if len(properties) == 8 :
        return True
    return False
                  
def crystals_stage(properties):
    if properties[6] < 7: 
        return 'initial'
    return 'developed'

def proportion_contours(cont_parent, cont_child, cont_else):
    sum = cont_parent + cont_child + cont_else
    if sum == 0:
        return 0, 0, 0
    perct_parent = cont_parent/sum *100
    perct_child = cont_child/sum * 100
    perct_else = cont_else/sum * 100
    return round(perct_parent,2), round(perct_child,2), round(perct_else,2)