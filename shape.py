import cv2
import numpy as np
img = cv2.imread('1.png')
gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
_, t = cv2.threshold (gray,240,255,cv2.THRESH_BINARY)
cntrs,_= cv2.findContours(t,cv2.RETR_TREE, cv2.CHAIN_APPROX_NONE)
t = 0
for cntr in cntrs:
    approx = cv2.approxPolyDP(cntr, 0.01* cv2.arclength(cntr,True),True)
    cv2.drawContours(img,[approx],0,(0,0,0),5)
    if len(approx)==3:
       t += 1
tr = np.array([t])
cv2.imshow('img',img)
cv2.waitKey(0)
cv2.destroyAllWindows
print(tr)
