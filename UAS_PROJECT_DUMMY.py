import cv2
import numpy as np


image_filenames = ['1.png', '2.png', '3.png', '4.png','5.png','6.png','7.png','8.png','9.png','10.png']  # Add more filenames
trnglcont=[]
min = 0
max = 100

for filename in image_filenames:

#####################                                                                          #######################
##################### creating masks for grass and burnt area and change them to solid colors  #######################
#####################                                                                          #######################
    img = cv2.imread(filename)

    tr=[]
    tr1=[]

    hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)

    lowergrass = np.array([1, 30, 1])   # Lower green
    uppergrass = np.array([85, 255, 255])  # Upper green

    burntashes = np.array([5, 50, 5])   # Lower brown 
    burntgrass = np.array([30, 255, 255])  # Upper brown 

# Create masks for green and brown regions
    green = cv2.inRange(hsv, lowergrass, uppergrass)
    brown = cv2.inRange(hsv, burntashes, burntgrass)

    cyan = (230, 230, 0)   
    yellow = (0, 230, 230)  

# Replace unburnt area with cyan color and burnt areas with yellow color
    result = np.copy(img)
    result[np.where(green)] = cyan 
    result[np.where(brown)] = yellow
    cv2.imshow('task1',result)
#####################                                                 #######################
##################### applying filters and blur for better detetction #######################
#####################                                                 #######################

    lowylw = np.array([0, 100, 100])  
    upylw = np.array([80, 255, 255]) 

    lowcyn = np.array([150, 0, 0])  
    upcyn = np.array([250, 255, 255])  


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

#####################                                   #######################
##################### Detection of houses in burnt area #######################
#####################                                   #######################

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

            
    cv2.drawContours(result, tr, -1, (255, 255, 255), 2)

#####################                                   #######################
##################### Detection of houses in unburnt area #######################
#####################                                   #######################

    gray1 = cv2.cvtColor(cyanrgn,cv2.COLOR_BGR2GRAY)
    ret,binary1 = cv2.threshold(gray1,100,255,cv2.THRESH_BINARY+cv2.THRESH_OTSU)
    edges1 = cv2.Canny(binary1, 3, 5)
    contours1, _ = cv2.findContours(edges1.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    for contour1 in contours1:
        approx1 = cv2.approxPolyDP(contour1, 0.06 * cv2.arcLength(contour1, True), True)
        if len(approx1) == 3:
            tr1.append(approx1)
    cv2.drawContours(result, tr1, -1, (0, 255, 0), 2)

    # Display the result for each image
    cv2.imshow('Result for ' + filename, result)
 
    trnglcont.append([len(tr), len(tr1)])
    print(trnglcont)
    cv2.waitKey(0)
    cv2.destroyAllWindows()