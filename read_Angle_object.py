import cv2
import numpy as np
import matplotlib.pyplot as plt
from scipy.ndimage import gaussian_filter


# Function to calculate image contrast
def image_contrast(original, corrected):
    mean_intensity_original = np.mean(original)
    std_intensity_original = np.std(original)
    
    mean_intensity_corrected = np.mean(corrected)
    std_intensity_corrected = np.std(corrected)
    
    contrast_original = std_intensity_original / mean_intensity_original
    contrast_corrected = std_intensity_corrected / mean_intensity_corrected
    
    return contrast_original, contrast_corrected

# Load the image
img = cv2.imread('2_Macro_10_2000_32_6_30.jpg')

# Crop centered with a % of original size
height, width, _ = img.shape
crop_size = int(min(height, width) * 0.3)
x = int((width - crop_size) / 2)
y = int((height - crop_size) / 2)
img = img[y:y+crop_size, x:x+crop_size]

# Convert to grayscale
gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
mean = cv2.mean(gray)[0]
if mean < 100:
    img = cv2.bitwise_not(img)

# Apply adaptive histogram equalization
clahe = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(10, 10))
enhanced_gray = clahe.apply(gray)

# Range de busca para gamma
gamma_values = np.linspace(0.5, 3.5, num=31)
best_gamma = 1.0
best_contrast_increase = 0.0
original_contrast, _ = image_contrast(enhanced_gray, enhanced_gray)

for gamma in gamma_values:
    gamma_corrected = np.power(enhanced_gray / 255.0, gamma) * 255.0
    gamma_corrected = gamma_corrected.astype(np.uint8)

    _, corrected_contrast = image_contrast(enhanced_gray, gamma_corrected)
    contrast_increase = corrected_contrast - original_contrast

    if contrast_increase > best_contrast_increase:
        best_contrast_increase = contrast_increase
        best_gamma = gamma

print("Best Gamma:", best_gamma)
# Apply the best gamma correction
best_gamma_corrected = np.power(enhanced_gray / 255.0, best_gamma) * 255.0
best_gamma_corrected = best_gamma_corrected.astype(np.uint8)

# Apply Gaussian blur (adjust kernel size as needed)
blurred = cv2.GaussianBlur(best_gamma_corrected, (1, 1), 0)

# Use Otsu's thresholding
_, thresh = cv2.threshold(blurred, 90, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)

# Find contours and contour hierarchy
contours, hierarchy = cv2.findContours(thresh, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

# Filter contours based on area and aspect ratio
min_area = 10  # Adjust the minimum area as per your requirements
aspect_ratio_thresh =2  # Adjust the aspect ratio threshold as per your requirements
filtered_contours = []
for idx, cnt in enumerate(contours):
    if cv2.contourArea(cnt) > min_area:
        filtered_contours.append(cnt)
# Create lists to store the aspect ratios and rectangles of crystals inside the islands and outside the islands
crystal_aspect_ratios_inside_islands = []
crystal_rectangles_inside_islands = []
crystal_aspect_ratios_outside_islands = []
crystal_rectangles_outside_islands = []

# Iterate over all contours and store aspect ratios and rectangles based on inside/outside the islands
for i, cnt in enumerate(contours):
    if hierarchy[0, i, 3] != -1:  # Check if it's a child contour (inside an island)
        minAreaRect = cv2.minAreaRect(cnt)
        width, height = minAreaRect[1]
        if min(width, height) > 0:
            aspect_ratio = max(width, height) / min(width, height)
            crystal_aspect_ratios_inside_islands.append(aspect_ratio)
            box = cv2.boxPoints(minAreaRect)
            box = np.int0(box)
            crystal_rectangles_inside_islands.append(box)
    else:
        minAreaRect = cv2.minAreaRect(cnt)
        width, height = minAreaRect[1]
        if min(width, height) > 0:
            aspect_ratio = max(width, height) / min(width, height)
            crystal_aspect_ratios_outside_islands.append(aspect_ratio)
            box = cv2.boxPoints(minAreaRect)
            box = np.int0(box)
            crystal_rectangles_outside_islands.append(box)

# Draw rectangles for crystals inside the islands (red) and outside the islands (blue)
canvas = np.copy(img)
cv2.drawContours(canvas, crystal_rectangles_inside_islands, -1, (0, 0, 255), 2)
cv2.drawContours(canvas, crystal_rectangles_outside_islands, -1, (255, 0, 0), 2)

# Print the count of identified crystals inside and outside the islands
num_crystals_inside_islands = len(crystal_rectangles_inside_islands)
num_crystals_outside_islands = len(crystal_rectangles_outside_islands)
print("Number of Crystals Inside Islands:", num_crystals_inside_islands)
print("Number of Crystals Outside Islands:", num_crystals_outside_islands)

# Calculate and print mean aspect ratio of crystals inside and outside the islands
mean_aspect_ratio_inside_islands = np.mean(crystal_aspect_ratios_inside_islands)
mean_aspect_ratio_outside_islands = np.mean(crystal_aspect_ratios_outside_islands)
print("Mean Aspect Ratio Inside Islands:", mean_aspect_ratio_inside_islands)
print("Mean Aspect Ratio Outside Islands:", mean_aspect_ratio_outside_islands)

plt.figure(figsize=(12, 8))
plt.imshow(cv2.cvtColor(canvas, cv2.COLOR_BGR2RGB))
plt.title('Crystals Inside and Outside Islands')
plt.axis('off')
plt.show()


