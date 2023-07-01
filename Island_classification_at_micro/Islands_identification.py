import cv2
import os

# lê imagem
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
    
# Path 
FOLDER_PATH = 'D:\LUCAS\IC\FUNWAX\Images'
# file = '1_Micro_10_5000_47_6_58.jpg'
for file in os.listdir(FOLDER_PATH):
    if get_properties(file)[1] == 'Micro' and len(get_properties(file)) != 8 and check_if_image_island_exists(FOLDER_PATH, file) is False: 
        image = get_image(file)
        island_image = crop_the_island(image)
        save_the_image(FOLDER_PATH, file, island_image)