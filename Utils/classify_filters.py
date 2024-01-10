import cv2
import numpy as np
import os

def classify_and_display(image_path, crop_percentage=30):
    # Leitura da imagem
    img = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)

    #dimensões da imagem
    height, width = img.shape

    #Calcular a altura e largura de corte
    crop_height = int(height * (crop_percentage / 100.0))
    crop_width = int(width * (crop_percentage / 100.0))

    #Calcular as coordenadas para o corte centralizado
    top = (height - crop_height) // 2
    bottom = top + crop_height
    left = (width - crop_width) // 2
    right = left + crop_width

    #Cortar a imagem centralizada
    cropped_img = img[top:bottom, left:right]

    #GaussianBlur
    blurImg = cv2.GaussianBlur(cropped_img, (5, 5), 0)

    #Aplicar thresholds específicos para cada classificação
    if np.mean(cropped_img) < 100 and np.max(cropped_img) - np.min(cropped_img) > 100:
        threshold_img = cv2.adaptiveThreshold(blurImg, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 7, -5)
        classification = "Imagem com Fundo Escuro e Cristais Claros"
    elif np.mean(cropped_img) > 150 and np.max(cropped_img) - np.min(cropped_img) > 100:
        threshold_img = cv2.adaptiveThreshold(blurImg, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 49, 11)
        classification = "Imagem com Fundo Claro e Cristais Escuros"
    else:
        threshold_img = cv2.adaptiveThreshold(blurImg, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 49, 11)
        classification = "Imagem com Tons Médios"

    #Encontrar contornos na imagem thresholded
    contours, _ = cv2.findContours(threshold_img, cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)

    #Inicializar uma lista para armazenar razões de aspecto
    aspect_ratios = []

    #Iterar sobre os contornos e desenhar contornos na imagem final
    for i, contour in enumerate(contours):
        #Calcular retângulo delimitador
        x, y, w, h = cv2.boundingRect(contour)
        aspect_ratio = max(w, h) / min(w, h)
        aspect_ratios.append(aspect_ratio)

        #Desenhar contorno na imagem final
        cv2.drawContours(cropped_img, [contour], -1, (0, 255, 0), 2)

    #Calcular a razão de aspecto média
    average_aspect_ratio = np.mean(aspect_ratios) if aspect_ratios else 0.0

    #Mostrar informações na imagem final
    cv2.putText(cropped_img, f"Numero de Cristais: {len(contours)}", (10, 20), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 1)
    cv2.putText(cropped_img, f"Razao de Aspecto Media: {average_aspect_ratio:.2f}", (10, 40), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 1)

    # Exibir informações
    print(f"Imagem: {os.path.basename(image_path)}")
    print(f"Classificação: {classification}")
    print(f"Número de Cristais: {len(contours)}")
    print(f"Razão de Aspecto Média: {average_aspect_ratio}")

    # Exibir a imagem final
    cv2.imshow("Imagem Final", cropped_img)
    cv2.waitKey(0)
    cv2.destroyAllWindows()

# Caminho completo da pasta de imagens
folder_path = 'D:\\Tratamento-de-imagens-FUNWAX\\ImagesNew'

# Listar os arquivos na pasta
image_files = [f for f in os.listdir(folder_path) if os.path.isfile(os.path.join(folder_path, f))]

# Iterar sobre os arquivos
for image_file in image_files:
    image_path = os.path.join(folder_path, image_file)

    # Classificar e exibir a imagem
    classify_and_display(image_path)
