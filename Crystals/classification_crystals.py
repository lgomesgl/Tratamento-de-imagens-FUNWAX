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
            ''    [8] -> Island number, only Micro
    '''
    return file[:-4].split('_')

def images_to_verify(properties, island):
    if properties[1] == 'Macro' or (properties[1] == 'Micro' and is_island(properties) is island):
        return True
    return False

def is_island(properties):
    if len(properties) >= 8 :
        return True
    return False
                 
def images_to_crop(island):
    if island:
        return ['Macro','Mistura']
    return ['Macro','Micro','Mistura']
    
def crop_the_image(image, scale_crop):
    height, width,_ = image.shape
    crop_size = int(min(height, width) * scale_crop)
    x = int((width - crop_size) / 2)
    y = int((height - crop_size) / 2)
    image = image[y:y+crop_size, x:x+crop_size]
    return image

def filter_nucleated_crystals(image):
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    # avg_tone = np.mean(gray)  
    blurImg = cv2.GaussianBlur(gray, (5, 5), 0)
    thresh = cv2.adaptiveThreshold(blurImg, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 7,-5)
    contours, _ = cv2.findContours(thresh, cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)
    return contours, _

def filter_non_nucleated_crystals(image):
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    # avg_tone = np.mean(gray)  
    blurImg = cv2.GaussianBlur(gray, (5, 5), 0)
    thresh = cv2.adaptiveThreshold(blurImg, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 49,11)
    contours, _ = cv2.findContours(thresh, cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)
    return contours, _

def status_color_image(image):
    if np.mean(image) < 100 and np.max(image) - np.min(image) > 100:
        status = "Imagem com Fundo Escuro e Cristais Claros"
    elif np.mean(image) > 150 and np.max(image) - np.min(image) > 100:
        status = "Imagem com Fundo Claro e Cristais Escuros"
    else:
        status = "Imagem com Tons Médios"
    return status

def filter(image, properties,status):
                
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    blurImg = cv2.GaussianBlur(gray, (5, 5), 0)
    
    filter_1 = cv2.adaptiveThreshold(blurImg, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 7, -5)
    filter_2 = cv2.adaptiveThreshold(blurImg, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 49, 11)            

    if status == "Imagem com Fundo Escuro e Cristais Claros":
        # threshold_img = cv2.adaptiveThreshold(blurImg, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 7, -5)
        threshold_img = filter_1
    elif status == "Imagem com Fundo Claro e Cristais Escuros":
        # threshold_img = cv2.adaptiveThreshold(blurImg, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 49, 11)
        threshold_img = filter_2
    else:
        for filter in [filter_2, filter_1]:
            # threshold_img = cv2.adaptiveThreshold(blurImg, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 7, -5)
            threshold_img = filter
    
    print(status)
    contours, _ = cv2.findContours(threshold_img, cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)
    # gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    # avg_tone = np.mean(gray)
    # limiar_tone = 150
    # equal_tone = all(abs(tone - avg_tone) < limiar_tone for tone in gray.flatten())
    # blurImg = cv2.blur(gray, (5, 5))
    
    # print(avg_tone)
    # if equal_tone:
    # # if avg_tone > 110:
    #     print("Image with average equal tones.")
        
    #     #blur filter

    #     #Set the threshold (version applied to light images)
    #     thresh = cv2.adaptiveThreshold(blurImg, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 19,11)
    #     contours, hierarchy = cv2.findContours(thresh, cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)
    #     return contours, hierarchy
    # else:
        
    #     print("Image with differences in tonality.")
    #     #Set the threshold (version applied to microwax)
    #     thresh = cv2.adaptiveThreshold(blurImg, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 13,-5)

    #     # Identify the contours
    #     contours, hierarchy = cv2.findContours(thresh, cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)
        
    #     return contours, hierarchy
    
    # if properties[1] == 'Micro':
        # #Convert to grayscale
        # gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        # mean = cv2.mean(gray)[0]
        # if mean < 127:
        #     image = cv2.bitwise_not(image)

        # #blur filter
        # blurImg = cv2.blur(gray, (5, 5))

        # #Set the threshold (version applied to microwax)
        # thresh = cv2.adaptiveThreshold(blurImg, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 13,-5)

        # # Identify the contours
        # contours, hierarchy = cv2.findContours(thresh, cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)
        
        # return contours, hierarchy
        
    # else:
    #     # Convert to grayscale
    #     gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    #     mean = cv2.mean(gray)[0]
    #     if mean < 100:
    #         image = cv2.bitwise_not(image)

    #     # Apply adaptive histogram equalization
    #     clahe = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(10, 10))
    #     enhanced_gray = clahe.apply(gray)

    #     # Function to calculate image contrast
    #     def image_contrast(original, corrected):
    #         mean_intensity_original = np.mean(original)
    #         std_intensity_original = np.std(original)
            
    #         mean_intensity_corrected = np.mean(corrected)
    #         std_intensity_corrected = np.std(corrected)
            
    #         contrast_original = std_intensity_original / mean_intensity_original
    #         contrast_corrected = std_intensity_corrected / mean_intensity_corrected
            
    #         return contrast_original, contrast_corrected

    #     # Range de busca para gamma
    #     gamma_values = np.linspace(0.5, 3.5, num=31)
    #     best_gamma = 1.0
    #     best_contrast_increase = 0.0
    #     original_contrast, _ = image_contrast(enhanced_gray, enhanced_gray)
        
    #     for gamma in gamma_values:
    #         gamma_corrected = np.power(enhanced_gray / 255.0, gamma) * 255.0
    #         gamma_corrected = gamma_corrected.astype(np.uint8)

    #         _, corrected_contrast = image_contrast(enhanced_gray, gamma_corrected)
    #         contrast_increase = corrected_contrast - original_contrast

    #         if contrast_increase > best_contrast_increase:
    #             best_contrast_increase = contrast_increase
    #             best_gamma = gamma
            
    #     # Apply the best gamma correction
    #     best_gamma_corrected = np.power(enhanced_gray / 255.0, best_gamma) * 255.0
    #     best_gamma_corrected = best_gamma_corrected.astype(np.uint8)

    #     # Apply Gaussian blur (adjust kernel size as needed)
    #     blurred = cv2.GaussianBlur(best_gamma_corrected, (1, 1), 0)

    #     # Use Otsu's thresholding
    #     _, thresh = cv2.threshold(blurred, 90, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)

    #     # Find contours and contour hierarchy
    #     contours, hierarchy = cv2.findContours(thresh, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
            
    return contours, _

def classification(image, data, contours, hierarchy, properties,status):
    if status == 'nucleated':
        color = (255, 0, 0)
    else:
        color = (0, 0, 255)
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
                
                if width < 0.9*image.shape[0]:
                    row_to_append = pd.DataFrame([{'Type':properties[1], 'Reynolds':properties[3], 'Toil':properties[4], 'Tcool':properties[5], 'Time':int(properties[6]), 'Island':'Outside', 'AR': aspect_ratio,'Status': status}])
                    data = pd.concat([data, row_to_append], ignore_index=True)
                            
                    # draw the contours
                    image = cv2.drawContours(image, [box], 0, color, 1)
    
    perct_parent, perct_child, perct_else = proportion_contours(cont_parent,cont_child,cont_else)

    # validate the contours
    # cv2.imshow('Cristais_%s_%s_%s' % (properties[1], properties[3], properties[6]), image)
    # cv2.waitKey(0)
    # cv2.destroyAllWindows()
             
    n_of_crystals = data.shape[0]
    
    return data, n_of_crystals, perct_parent, perct_child, perct_else 

def proportion_contours(cont_parent, cont_child, cont_else):
    sum = cont_parent + cont_child + cont_else
    if sum == 0:
        return 0, 0, 0
    perct_parent = cont_parent/sum *100
    perct_child = cont_child/sum * 100
    perct_else = cont_else/sum * 100
    return round(perct_parent,2), round(perct_child,2), round(perct_else,2)