import cv2
import numpy as np
img = cv2.imread('1.png')
grayscaled = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

red_cascade= cv2.CascadeClassifier('cascade.xml')

rhouse= red_cascade.detectMultiScale(img, 1.3, 5)
print('no. of redhouses' , len(rhouse))

for(x,y,w,h) in rhouse:
    cv2.rectangle(img,(x,y),(x+w,y+h),(255,0,0),2)
    

#cv2.imshow('redhouse', roi)
cv2.imshow('img', img)
cv2.waitKey(0)
cv2.destroyAllWindows()
