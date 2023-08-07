'''
    We start the project cropping the raw image in the center. But we noticed that micro type images
    have a different tendency in crystal formation. So we decide to create a filter to identify these formations(we called island),
    to correctly classify the crystals.
'''
import cv2
import os

def get_image(folder_path, file):
    return cv2.imread('%s/%s' % (folder_path, file))

def save_the_image(folder_path, filename, image):
    return cv2.imwrite(os.path.join(folder_path, '%s_island.jpg' % filename[:-4]), image)

def get_properties(file):
    properties = file[:-4].split('_')
    return properties

def is_island(properties):
    if len(properties) == 8:
        return True
    return False

def check_if_image_island_exists(folder_path, file):
    if file and '%s_island.jpg' % file[:-4] in os.listdir(folder_path):
        return True
    return False

def check_to_crop(folder_path, file):
    if get_properties(file)[1] == 'Micro' and (is_island(get_properties(file)) is False) and (check_if_image_island_exists(folder_path, file) is False):
        return True
    return False 
    
def crop_the_island(image):
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    ret, thresh = cv2.threshold(gray, 60, 255, cv2.THRESH_BINARY)
    contours, _ = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    
    largest_contour = max(contours, key=cv2.contourArea)
    x, y, w, h = cv2.boundingRect(largest_contour)
    cropped_gray = gray[y:y+h, x:x+w]
    cropped_image = image[y:y+h, x:x+w]

    # cv2.imshow("Cropped Gray", cropped_gray)
    # cv2.imshow("Cropped Color", cropped_image)
    # cv2.waitKey(0)
    # cv2.destroyAllWindows()
    
    return cropped_image

def smaler_island(cropped_image, image_size):
    cropped_size = []
    if cropped_image.shape[0] * cropped_image.shape[1] < image_size:
        image_size = cropped_image.shape[0] * cropped_image.shape[1]
        cropped_size.append(cropped_image.shape[0], cropped_image.shape[1])
    return cropped_size
    
def main_island(folder_path):  
    print('Start to crop the island at micro images')  
    print('---------------NEW IMAGES---------------')
    counter_new_images = 0
    for file in os.listdir(folder_path):
        if check_to_crop(folder_path, file):
            image = get_image(folder_path, file)
            island_image = crop_the_island(image)
            save_the_image(folder_path, file, island_image)
            print('%s_island.jpg' % file)
            counter_new_images += 1
    if counter_new_images == 0:
        print('All micro images has cropped')
    print('----------------------------------------')