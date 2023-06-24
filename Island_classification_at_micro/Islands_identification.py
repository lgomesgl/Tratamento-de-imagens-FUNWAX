import cv2

# lê imagem
def get_image(file):
    return cv2.imread('%s/%s' % (FOLDER_PATH, file))

def get_the_island(image):
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
    cv2.imshow("Cropped Color", cropped_image)

    cv2.waitKey(0)
    cv2.destroyAllWindows()
    return contours
    
# Path 
FOLDER_PATH = 'D:\LUCAS\IC\FUNWAX\Images'
file = '1_Micro_10_5000_47_6_58.jpg'
image = get_image(file)
contours = get_the_island(image)