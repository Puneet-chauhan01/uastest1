import cv2
import numpy as np

# Load the original image
img = cv2.imread('10.png')

# Convert the image to the HSV color space for better color segmentation
hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
tr =[]
tr1=[]
min = 0
max = 100
# Define the lower and upper bounds for green color in HSV color space
lowergrass = np.array([1, 30, 1])   # Lower bound for green (adjust as needed)
uppergrass = np.array([85, 255, 255])  # Upper bound for green (adjust as needed)

# Define the lower and upper bounds for brown color in HSV color space
burntashes = np.array([5, 50, 5])   # Lower bound for brown (adjust as needed)
burntgrass = np.array([30, 255, 255])  # Upper bound for brown (adjust as needed)
#create mask fro identifying red houses
lowred = np.array([0, 100, 90])   # Lower bound for red (adjust as needed)
upred = np.array([10, 255, 255])  # Upper bound for red (adjust as needed)

# Create masks for green and brown regions
green = cv2.inRange(hsv, lowergrass, uppergrass)
brown = cv2.inRange(hsv, burntashes, burntgrass)

# Create cyan color (for green areas) and yellow color (for brown areas)
cyan = (230, 230, 0)   # Cyan color in BGR
yellow = (0, 230, 230)  # Yellow color in BGR

# Replace green areas with cyan color and brown areas with yellow color
result = np.copy(img)
result[np.where(green)] = cyan 
result[np.where(brown)] = yellow


#####################                                   #######################
##################### Detection of houses in burnt area #######################
#####################                                   #######################
lowylw = np.array([0, 100, 100])  
upylw = np.array([80, 255, 255]) 

lowcyn = np.array([150, 0, 0])  # Lower cyan
upcyn = np.array([250, 255, 255])  # upper cyan


ylwmask = cv2.inRange(result,lowylw,upylw)
cynmask = cv2.inRange(result,lowcyn,upcyn)
kernel = np.ones((5, 5), np.uint8)
yellow_mask = cv2.morphologyEx(ylwmask, cv2.MORPH_OPEN, kernel)
yellow_mask = cv2.morphologyEx(yellow_mask, cv2.MORPH_CLOSE, kernel)
yelrgn = cv2.bitwise_and(result, result, mask=yellow_mask)
yelrgn= cv2.GaussianBlur(yelrgn,(15,15),0)

cyanmask = cv2.morphologyEx(cynmask, cv2.MORPH_OPEN, kernel)
cyanmask = cv2.morphologyEx(cyanmask, cv2.MORPH_CLOSE, kernel)
cyanrgn = cv2.bitwise_and(result, result, mask=cyanmask)
cyanrgn= cv2.GaussianBlur(cyanrgn,(15,15),0)

# HOUSE DETECTION IN BURNT AREA

gray = cv2.cvtColor(yelrgn,cv2.COLOR_BGR2GRAY)
ret,binary = cv2.threshold(gray,100,255,cv2.THRESH_BINARY+cv2.THRESH_OTSU)
edges = cv2.Canny(binary, 3, 5)

contours, _ = cv2.findContours(edges.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        
for contour in contours:
    approx = cv2.approxPolyDP(contour, 0.06 * cv2.arcLength(contour, True), True)
    if len(approx) == 3:
        x1, y1, w1, h1 = cv2.boundingRect(approx)
        triangle_width1 = w1
        triangle_height1 = h1
        
        # Check if the bounding rectangle dimensions are within the desired range
        if min <= triangle_width1 <= max and \
            min <= triangle_height1 <= max:
                tr.append(approx)
cv2.drawContours(result, tr, -1, (255, 255, 0), 2)
#cv2.drawContours(result, triangles, -1, (0, 255, 0), 2)  # Draw triangles on the image
print("Number of triangles:", len(tr))
cv2.imshow("TRIANGLE DETECTION ", result)

# HOUSE DETECTION IN UNBURNT AREA

gray1 = cv2.cvtColor(cyanrgn,cv2.COLOR_BGR2GRAY)
ret,binary1 = cv2.threshold(gray1,100,255,cv2.THRESH_BINARY+cv2.THRESH_OTSU)
edges1 = cv2.Canny(binary1, 3, 5)
cv2.imshow('edges1',edges1)
contours1, _ = cv2.findContours(edges1.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

for contour1 in contours1:
    approx1 = cv2.approxPolyDP(contour1, 0.06 * cv2.arcLength(contour1, True), True)
    if len(approx1) == 3:
            x, y, w, h = cv2.boundingRect(approx1)
            triangle_width = w
            triangle_height = h
        
        # Check if the bounding rectangle dimensions are within the desired range
            if min <= triangle_width <= max and \
                 min <= triangle_height <= max:
                 tr1.append(approx1)

cv2.drawContours(result, tr1, -1, (0, 255, 255), 2)
#cv2.drawContours(result, triangles, -1, (0, 255, 0), 2)  # Draw triangles on the image
print("Number of triangles:", len(tr1))
cv2.imshow("TRIANGLE DETECTION ", result)

task2 = [len(tr),len(tr1)]
print('task2', task2)
cv2.imshow('edges', edges)
cv2.imshow('corner',img)
cv2.imshow('binary',binary)
cv2.waitKey(0)
cv2.destroyAllWindows()