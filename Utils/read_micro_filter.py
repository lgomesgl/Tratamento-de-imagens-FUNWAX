import numpy as np
import matplotlib.pyplot as plt
import cv2
import statistics

#Close all 
plt.close('all')

#Load 
img = cv2.imread('1_Micro_10_1000_47_6_120_island.jpg')

#Crop 
height, width, _ = img.shape
crop_size = int(min(height, width) * 0.9)
x = int((width - crop_size) / 2)
y = int((height - crop_size) / 2)
img = img[y:y+crop_size, x:x+crop_size]

#Convert to grayscale
gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
mean = cv2.mean(gray)[0]
if mean < 127:
    img = cv2.bitwise_not(img)

#Create a new figure and display the grayscale image
plt.figure(1)
plt.imshow(gray, cmap='gray')

#blur filter
blurImg = cv2.blur(gray, (5, 5))

#Set the threshold (version applied to microwax)
thresh = cv2.adaptiveThreshold(blurImg, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 13,-5)

# Identify the contours
contours, hier = cv2.findContours(thresh, cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)

# # Calculate the areas of all contours
# areas = [cv2.contourArea(cnt) for cnt in contours]
# # Find the contour with the maximum area (external contour)
# max_area_idx = np.argmax(areas)

# # Exclude the contour with the maximum area
# filtered_contours = contours[:max_area_idx] + contours[max_area_idx + 1:]
#filtered_contours = contours
# # Proceed only if there are contours remaining
# if len(filtered_contours) > 0:
#Draw the contours
gray_contours = np.copy(gray)
for cnt in contours:
    cv2.drawContours(gray_contours, [cnt], 0, (0, 100, 100), 1)
plt.figure(2)
plt.imshow(gray_contours, cmap='gray')

#aspect ratio
aspect_ratio = np.zeros(len(contours))
heightPlot = np.zeros(len(contours))
widthPlot = np.zeros(len(contours))

i = 0
for cnt in contours:
    rect = cv2.minAreaRect(cnt)
    (x, y), (width, height), theta = rect
    if height >0 and width>0:
       aspect_ratio[i] = max(height,width)/min(height,width)
       widthPlot[i] = width
       heightPlot[i]= height
       i += 1
    else: 
       aspect_ratio[i] = 0
       i += 1
#copy of the original image
canvas = np.copy(img)

#Draw rectangles around the contours
i = 0
for cnt in contours:
   rect = cv2.minAreaRect(cnt)
   rectCnt = np.int64(cv2.boxPoints(rect))
   cv2.polylines(img=canvas, pts=[rectCnt], isClosed=True, color=(255, 0, 0), thickness=2)
   i += 1

plt.figure(4)
cv2.imshow("Rectangles", canvas)
    
plt.figure(5)
media = statistics.mean(aspect_ratio)
num_crystals = len(contours)
plt.hist(aspect_ratio, bins=7, range=[1, 8])
plt.gca().set(title='Frequency Histogram', ylabel='Frequency', xlabel='Aspect ratio [-]')
plt.xlim(1, 10)
plt.ylim(0, 1000)


print('Num particles: ', num_crystals)
print('AR: ', media)

#bin ranges
bins = [1, 2, 3, 4, 5, 6, 7, 8]

# Create histogram
hist, bin_edges = np.histogram(aspect_ratio, bins=bins)

#total values of aspect ratios
total_values = len(aspect_ratio)

#calc %
percentage = (hist / total_values) * 100

#labels to intervals
labels = [f'{bins[i]}-{bins[i+1]}' for i in range(len(bins) - 1)]

# #save 
# results = np.column_stack((labels, percentage))
# np.savetxt('histogram_results.csv', results, delimiter=',', fmt='%s')

#Plot histogram
plt.figure()
plt.bar(labels, percentage, width=0.7, align='center', edgecolor='k')
plt.gca().set(ylabel='Percentage of crystals [%]', xlabel='Aspect ratio intervals [-]')
plt.ylim(0, 100)

#labels with %
for i, v in enumerate(percentage):
    plt.text(i, v + 1, f'{v:.2f}%', ha='center', va='bottom')

plt.xticks(rotation=45)
plt.show()



