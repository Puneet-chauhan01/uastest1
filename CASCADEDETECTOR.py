import cv2
import numpy as np

# Load the original image
img = cv2.imread('2.png')
# Convert the image to the HSV color space for better color segmentation
hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)

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
cynrgn = cv2.bitwise_and(result, result, mask=cynmask)
'''kernel = np.ones((5, 5), np.uint8)
yellow_mask = cv2.morphologyEx(ylwmask, cv2.MORPH_OPEN, kernel)
yellow_mask = cv2.morphologyEx(yellow_mask, cv2.MORPH_CLOSE, kernel)
yelrgn = cv2.bitwise_and(result, result, mask=yellow_mask)'''

cascade= cv2.CascadeClassifier('cascade.xml')

rhouse= cascade.detectMultiScale(ylwmask, 1.1, 5)
print('no. of houses in burnt area' , len(rhouse))

for(x,y,w,h) in rhouse:
    cv2.rectangle(result,(x,y),(x+w,y+h),(255,0,0),2)

#cv2.imshow('yelrgn', yelrgn)
######################                                       #######################
######################   Detection of houses in unburnt area ##################
######################                                       ##################

kernel1 = np.ones((5, 5), np.uint8)
cyanmask = cv2.morphologyEx(cynmask, cv2.MORPH_OPEN, kernel1)
cyanmask = cv2.morphologyEx(cyanmask, cv2.MORPH_CLOSE, kernel1)

unbhouse= cascade.detectMultiScale(cyanmask, 1.05, 10)
print('no. of houses in  unburnt area' , len(unbhouse))

for(x1,y1,w1,h1) in unbhouse:
    cv2.rectangle(result,(x1,y1),(x1+w1,y1+h1),(0,255,0),2)
#####################
#####################
#####################
# Display the result
print("Lower Cyan HSV Bound:", lowcyn)
print("Upper Cyan HSV Bound:", upcyn)
task2 =np.array([len(rhouse),len(unbhouse)])
print(task2)
cv2.imshow('task1', result)
cv2.waitKey(0)
cv2.destroyAllWindows()