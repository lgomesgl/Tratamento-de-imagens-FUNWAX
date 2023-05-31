# -*- coding: utf-8 -*-
"""
Created on Wed Mar 29 21:06:10 2023

@author: asuspc
"""

import numpy as np
import matplotlib.pyplot as plt
import cv2
import statistics

#fecha gráficos abertos
plt.close('all')

# fecha gráficos abertos
cv2.destroyAllWindows()

#Leitura do arquivo de imagem
img = cv2.imread('Macro_1.jpg')

# Verificar se a imagem tem fundo preto ou branco
gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
mean = cv2.mean(gray)[0]
if mean < 127:
    img = cv2.bitwise_not(img)

# Fazer crop de uma porcentagem da imagem
# Crop centralizado com % do tamanho original
height, width,_ = img.shape
crop_size = int(min(height, width) * 0.35)
x = int((width - crop_size) / 2)
y = int((height - crop_size) / 2)
img = img[y:y+crop_size, x:x+crop_size]

# Conversão para escala de cinza
gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

# Aplicar filtro de mediana para remover ruído
img = cv2.medianBlur(gray, 1)
img = cv2.GaussianBlur(gray, (3,3), 0)
_, th = cv2.threshold(img, 0, 255, cv2.THRESH_BINARY+cv2.THRESH_OTSU)
# Aplicar a equalização do histograma
img = cv2.equalizeHist(img)

# Aplicar threshold adaptativo
th = cv2.adaptiveThreshold(img, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY_INV, 11, 2)

# Aplicar filtro morfológico de abertura
kernel = np.ones((5,5),np.uint8)
opening = cv2.morphologyEx(th, cv2.MORPH_OPEN, kernel, iterations=1)
cv2.imshow('teste', opening)

# Identificar contornos
contours, hierarchy = cv2.findContours(opening, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

# Exibir a imagem resultante com os contornos identificados
cv2.imshow('Contornos', opening)
# Converter a imagem de cinza para colorida
img = cv2.cvtColor(img, cv2.COLOR_GRAY2BGR)
# Desenhar retângulos nos contornos
for cnt in contours:
    # Obter o menor retângulo que envolve o contorno
    rect = cv2.minAreaRect(cnt)
    box = cv2.boxPoints(rect)
    box = np.int0(box)

    # Calcular o ângulo de rotação do retângulo
    angle = rect[-1]

    # Desenhar o retângulo rotacionado na imagem
    cv2.drawContours(img,[box],0,(0,0,255),2)



# Exibir a imagem resultante
cv2.imshow('Cristais', img)
cv2.waitKey(0)
cv2.destroyAllWindows()
