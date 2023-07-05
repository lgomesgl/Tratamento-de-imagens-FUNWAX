# -*- coding: utf-8 -*-
"""
Created on Mon Jan 10 22:07:54 2022

@author: asuspc
"""

import numpy as np
import matplotlib.pyplot as plt
import cv2
import statistics


#fecha gráficos abertos
plt.close('all')

#Leitura do arquivo de imagem
#img = cv2.imread('45_ponta.tif') #macro
#img = cv2.imread('25Macro10C12.tif')
#img = cv2.imread('Snap-93copia.jpg') #macro
#img = cv2.imread('S_Macro 10% E75 - 25C 20x.tif') #micro
img = cv2.imread('1_Micro_10_2000_47_6_35.jpg')

# Fazer crop de uma porcentagem da imagem
# Crop centralizado com % do tamanho original
height, width,_ = img.shape
crop_size = int(min(height, width) * 0.95)
x = int((width - crop_size) / 2)
y = int((height - crop_size) / 2)
img = img[y:y+crop_size, x:x+crop_size]


#Transforma imagem em escala de cinza e inverte se necessário
gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
mean = cv2.mean(gray)[0]
if mean < 127:
    img = cv2.bitwise_not(img)
    
    
#cria novo gráfico e mostra imagem em tons de cinza
plt.figure(1)
plt.imshow(gray,cmap='gray')

#Aplica Filtro blur
blurImg=cv2.blur(gray,(7,7))
#blurImg = cv2.GaussianBlur(gray,(5,5),0)

#Estabelece o threshold para identificar os contornos
#ret,thresh = cv2.threshold(blurImg,130,255,1)
#ret,thresh = cv2.threshold(blurImg,118,255,cv2.THRESH_BINARY+cv2.THRESH_OTSU) 
# ret,thresh = cv2.threshold(blurImg,130,255,cv2.THRESH_TOZERO_INV)
thresh = cv2.adaptiveThreshold(blurImg, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 5, -2)

#Identifica os contornos
contours, hier = cv2.findContours(thresh,1,2)

#Desenha os contornos
for cnt in contours:
    cv2.drawContours(gray,[cnt],0,(0,100,100),2)
plt.figure(2)
plt.imshow(gray,cmap='gray')
cnt2 = contours[0]
(x,y,w,h)=cv2.boundingRect(cnt)

#Calcula o aspect ratio
aspect_ratio=np.zeros(len(contours)) 
i=0   
for cidx,cnt in enumerate(contours):
    ((cx, cy), (width, height), theta) = cv2.minAreaRect(cnt)
    
    if height > width:
        aspect_ratio[i]=height/width
        i=i+1
        
    if width > height:
        if height > 0:
            aspect_ratio[i]=width/height
        else:
            aspect_ratio[i]=0
        i=i+1
    
       
print('center: cx=%.3f, cy=%.3f, width=%.3f, height=%.3f, roate_angle=%.3f'%(cx, cy, width, height, theta))

minAreaRect = cv2.minAreaRect(cnt)

#cria uma cópia da imagem original
canvas = np.copy(img)
#
#for cidx,cnt in enumerate(contours):
#    minAreaRect = cv2.minAreaRect(cnt)
#    rectCnt = np.int64(cv2.boxPoints(minAreaRect))
#    cv2.drawContours(canvas, [rectCnt], 0, (0,255,0), 3)
#
#cv2.imwrite("number_minarearect_canvas.png", canvas)
i=0
for cidx,cnt in enumerate(contours):
    minAreaRect = cv2.minAreaRect(cnt)
    # 转换为整数点集坐标
    rectCnt = np.int64(cv2.boxPoints(minAreaRect))
    # 绘制多边形
    cv2.polylines(img=canvas, pts=[rectCnt], isClosed=True, color=(255,0,0), thickness=3)
    (x, y), (width, height), angle = minAreaRect
    if min(width, height) > 0:
        aspect_ratio[i] = max(width, height)/ min(width, height)
    i=i+1
    
    
    
    
#print(cv2.boxPoints(minAreaRect))

#cv2.imwrite("number_minarearect_canvas.png", canvas)
#inputImageCopy = cv2.resize(canvas, (1100, 900))

plt.figure(4)
cv2.imshow("Rectangles", canvas)


media=statistics.mean(aspect_ratio)
num_crystals=len(contours)
plt.hist(aspect_ratio, bins=50,range=[0, 7])
plt.gca().set(title='Frequency Histogram', ylabel='Frequency',xlabel='Aspect ratio [-]');
plt.xlim(0,10)
plt.figure(5)
plt.imshow(canvas)

#c=np.linspace(0,len(contours),len(contours))
#plt.figure(5)
#plt.plot(c,aspect_ratio)
#frame = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
#frame=cv2.blur(frame,(3,3))
#ret, frame = cv2.threshold(frame, 90, 255, cv2.THRESH_BINARY)
#
#contours, hierarchy = cv2.findContours(frame, cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)
#
#areas = []
#
#for i in range(0, len(contours)):
#    areas.append(cv2.contourArea(contours[i]))
#print ('Num particles: ', len(contours))
#
#for i in range(0, len(contours)):
#    print ('Area', (i + 1), ':', areas[i])
#
#
#cv2.imshow("Frame", frame)


