import cv2
import numpy as np
img= cv2.imread('1.png')

gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
##to change black pixel into yellow pixel 
def changetoyellow(image):
    lowblk = np.array([0, 0, 0], dtype=np.uint8)
    upblk = np.array([65, 65, 65], dtype=np.uint8)  # Allowing for slight variations in black

    mask = cv2.inRange(image, lowblk, upblk)

    # Replace black pixels with yellow
    yellow_color = np.array([0, 255, 255], np.uint8)
    image[mask > 0] = yellow_color

    return image


lowbnd = (0, 0, 0)
#upper_bound = (120, 120, 255)
upbnd = (255, 255, 255)

# Create a mask
mask = cv2.inRange(img, lowbnd, upbnd)
res=cv2.bitwise_and(img,img,mask=mask)
kernel =np.ones((8,8),np.float32)/64
smoothed = cv2.filter2D(res,-1,kernel)
#cv2.imshow('smoothed',smoothed)

lower_brwn = np.array([10, 50, 50])  # Lower range of brown in HSV
upper_brwn = np.array([30, 255, 255])  # Upper range of brown in HSV

lower_blck = np.array([0, 0, 0])  # Lower range of black in HSV
upper_blck = np.array([180, 255, 30])  # Upper range of black in HSV

lower_grn = np.array([35, 50, 50])  # Lower range of green in HSV
upper_grn = np.array([85, 255, 255])  # Upper range of green in HSV



# Convert the image to HSV color space
hsv = cv2.cvtColor(smoothed, cv2.COLOR_BGR2HSV)


# Create masks for the brown and black and green pixels
brwn_mask = cv2.inRange(hsv, lower_brwn, upper_brwn)
blck_mask = cv2.inRange(hsv, lower_blck, upper_blck)
grn_mask = cv2.inRange(hsv, lower_grn, upper_grn)
# Create an all yellow image
yllw_img = np.zeros_like(img)
yllw_img[:] = (0, 255, 255)  # Yellow color in BGR
#create an all cyan image
cyan_img = np.zeros_like(img)
cyan_img[:] = (255, 255, 0)  # Cyan color in BGR


# Replace brown and black pixels with yellow in the original image
result_img = cv2.bitwise_and(img, img, mask=~(brwn_mask | grn_mask |blck_mask ))
result_img += cv2.bitwise_and(yllw_img, yllw_img, mask=(brwn_mask |blck_mask ))
result_img += cv2.bitwise_and(cyan_img, cyan_img, mask=grn_mask)

res_img=  changetoyellow(result_img)
cv2.imshow('res_image',res_img)

'''lower_black1 = np.array([0, 0, 0])  # Lower range of black in HSV
upper_black1 = np.array([180, 255, 30])  # Upper range of black in HSV
black_mask1 = cv2.inRange(result_image, lower_black1, upper_black1)
result_image += cv2.bitwise_and(yellow_image, yellow_image, mask=(black_mask1 ))'''


edges = cv2.Canny(res_img, 50, 150)
contours, _ = cv2.findContours(edges.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

#TRIANGLE DETECTION 
'''triangles = []
for contour in contours:
    perimeter = cv2.arcLength(contour, True)
    approx = cv2.approxPolyDP(contour, 0.04 * perimeter, True)
    if len(approx) == 3:  # Triangles have 3 vertices
        triangles.append(contour)
        
cv2.drawContours(res_img, triangles, -1, (0, 255, 0), 2)  # Draw triangles on the image
triangle_count = len(triangles)
print("Number of triangles:", triangle_count)
cv2.imshow("TRIANGLE DETECTION ", res_img)'''
#------->>>giving hundreds of diff triangles which are alse false positives probably not the way of solving this problem

#HAAR CASCADE DETECTION

red_cascade= cv2.CascadeClassifier('cascade.xml')

rhouse= red_cascade.detectMultiScale(res_img, 1.3, 5)
print('no. of redhouses' , len(rhouse))

for(x,y,w,h) in rhouse:
    cv2.rectangle(res_img,(x,y),(x+w,y+h),(255,0,0),2)
cv2.imshow("HAAR CASCADE", res_img)

##----->>>gives false positive ''


#TEMPLATE MATCHING
'''
gray = cv2.cvtColor(img, cv2.COLOR_HSV2BGR)
gray1 =cv2.cvtColor(gray, cv2.COLOR_BGR2GRAY)
template = cv2.imread('redhouse.png', 0)
w, h = template.shape[::-1]

res = cv2.matchTemplate(gray1, template, cv2.TM_CCOEFF_NORMED)
threshold = 0.42
loc = np.where(res>= threshold)

for pt in zip(*loc[::-1]):
    cv2.rectangle(gray1, pt, (pt[0]+w, pt[1]+h), (0,255,255), 2) 


cv2.imshow("TEMPLATE MATCHING", res_img)'''
'''gives error:
Traceback (most recent call last):
  File "D:/uas project/triangles.py", line 104, in <module>
    w, h = template.shape[::-1]
AttributeError: 'NoneType' object has no attribute 'shape'
probably because i am using hsv color and it runs in grayscale
i tried doing hsv to gray but its not there but hsv 2 bgr and then bgr2 gray is possible but it gives wrong results'''



cv2.imshow("Triangles", img)
cv2.imshow("hsv_image", hsv)


cv2.waitKey(0)
cv2.destroyAllWindows()
