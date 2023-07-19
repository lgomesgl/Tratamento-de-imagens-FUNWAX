'''
    We start the project cropping the raw image in the center. But we noticed that micro type images
    have a different tendency in crystal formation. So we decide to create a low level filter to identify these formations(we called island),
    to correctly classify the crystals.
'''
import cv2
import os

# lê imagem
def get_image(folder_path, file):
    return cv2.imread('%s/%s' % (folder_path, file))

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

def crop_the_island(image):
    # Converte para escala de cinza
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    # thresholding
    ret, thresh = cv2.threshold(gray, 60, 255, cv2.THRESH_BINARY)

    # Encontra contornos
    contours, _ = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    # Encontra contorno com maior área
    largest_contour = max(contours, key=cv2.contourArea)

    # Retâgulo em torno do maior contorno
    x, y, w, h = cv2.boundingRect(largest_contour)

    # Crop 
    cropped_gray = gray[y:y+h, x:x+w]
    cropped_image = image[y:y+h, x:x+w]

    # Mostra crop
    # cv2.imshow("Cropped Gray", cropped_gray)
    # cv2.imshow("Cropped Color", cropped_image)

    # cv2.waitKey(0)
    # cv2.destroyAllWindows()
    
    return cropped_image

def main_island(folder_path):  
    print('---------------NEW IMAGES---------------')
    for file in os.listdir(folder_path):
        if get_properties(file)[1] == 'Micro' and (image_island(get_properties(file)) is False) and (check_if_image_island_exists(folder_path, file) is False): 
            image = get_image(folder_path, file)
            island_image = crop_the_island(image)
            save_the_image(folder_path, file, island_image)
            print('%s_island.jpg' % file)