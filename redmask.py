import cv2
import numpy as np

# Load the image
img = cv2.imread('1.png')
hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
tr =[]
tr1=[]
min = 0
max = 100
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
lwrd = np.array([0,0,0])
uprd = np.array([25,25,255])
red_mask = cv2.inRange(result, lwrd,uprd)
res = cv2.bitwise_and(result,result,mask =red_mask)
cv2.imshow('res',res)
cv2.waitKey(0)
cv2.destroyAllWindows