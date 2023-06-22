import cv2

# Path 
image_path = "D:\LUCAS\IC\FUNWAX\Images\1_Micro_10_9000_47_6_33.jpg"

# lê imagem
img = cv2.imread(image_path)
print(img)

# Converte para escala de cinza
gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

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
cropped_color = img[y:y+h, x:x+w]

# Mostra crop
cv2.imshow("Cropped Gray", cropped_gray)
cv2.imshow("Cropped Color", cropped_color)

cv2.waitKey(0)
cv2.destroyAllWindows()
