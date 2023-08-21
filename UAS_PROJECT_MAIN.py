import cv2
import numpy as np


image_filenames = ['1.png', '2.png', '3.png', '4.png','5.png','6.png','7.png','8.png','9.png','10.png']  # Add more filenames
housecount =[]
priority=[]
pratio = []
imglist= []
imgoutput =[]
Pratio=[]
for filename in image_filenames:
    img = cv2.imread(filename)


#####################                                                                               #######################
#####################   CREATING A MASK TO CONVERT GREEN AND BURNT AREA INTO CYAN AND YELLOW COLOR  #######################
#####################                                                                               #######################

    hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
    lowergrass = np.array([1, 30, 1])   # Lower grass color
    uppergrass = np.array([85, 255, 255])  # upper grass color

# Define the lower and upper bounds for brown color in HSV color space
    burntashes = np.array([5, 50, 5])   # to detect burnt black spots
    burntgrass = np.array([30, 255, 255])  # to detect brown 

# Create masks for green and brown regions
    green = cv2.inRange(hsv, lowergrass, uppergrass)
    brown = cv2.inRange(hsv, burntashes, burntgrass)

    cyan = (230, 230, 0)   # Cyan color in BGR

    yellow = (0, 230, 230)  # Yellow color in BGR

# Replace green areas with cyan color and brown areas with yellow color
    result = np.copy(img)
    result[np.where(green)] = cyan 
    result[np.where(brown)] = yellow
    cv2.imshow('task1',result)

#create red mask for detecting red houses and blu mask for blu houses and doing morphological transformation for better detection
    lwrd = np.array([0,0,0])
    uprd = np.array([25,25,255])

    lwblu = np.array([0,0,0])
    upblu = np.array([255,25,25])

    kernel = np.ones((5, 5), np.uint8)
    red_mask = cv2.inRange(result, lwrd,uprd)
    red_mask = cv2.morphologyEx(red_mask, cv2.MORPH_OPEN, kernel)
    red_mask = cv2.morphologyEx(red_mask, cv2.MORPH_CLOSE, kernel)

    blu_mask = cv2.inRange(result, lwblu,upblu)
    blu_mask = cv2.morphologyEx(blu_mask, cv2.MORPH_OPEN, kernel)
    blu_mask = cv2.morphologyEx(blu_mask, cv2.MORPH_CLOSE, kernel)

# creating contours to detect houses

    contours, _ = cv2.findContours(red_mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    contours1, _ = cv2.findContours(blu_mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    redylw_houses = []
    redcyn_houses = []
    blucyn_houses = []
    bluylw_houses = []

#####################                                         #######################
#####################   DETECTING RED HOUSES IN BURNT GRASS   #######################
#####################                                         #######################


    for contour in contours:
    # Approximate the contour with a polygon
        epsilon = 0.04 * cv2.arcLength(contour, True)
        approx = cv2.approxPolyDP(contour, epsilon, True)
    
    # If the contour has 3 vertices, it's a triangle
        if len(approx) == 3:
        # Get the moments of the contour to calculate the centroid
            moments = cv2.moments(contour)
            centroid_x = int(moments["m10"] / moments["m00"])
            centroid_y = int(moments["m01"] / moments["m00"])
        
        # Get the BGR pixel value at the centroid
            centroid_pixel_value = result[centroid_y, centroid_x]
        
        # Check if the centroid pixel value is within the specified region color bounds
            if np.all(np.logical_and(centroid_pixel_value >= lwrd, centroid_pixel_value <= uprd)):
            # Create a bounding rectangle around the detected red triangle
                x_tri, y_tri, w_tri, h_tri = cv2.boundingRect(approx)
            
            # Create an ROI using the bounding rectangle of the detected triangle
                roi = result[y_tri:y_tri+h_tri, x_tri:x_tri+w_tri]
            
            # Calculate the number of yellow pixels in the ROI
                num_yellow_pixels = np.sum(np.logical_and(roi[:, :, 0] == 0, roi[:, :, 1] == 230, roi[:, :, 2] == 230))
            
            # Check if the number of yellow pixels exceeds a threshold
                yellow_pixel_threshold = 3  # Adjust as needed
                if num_yellow_pixels > yellow_pixel_threshold:
                # Draw a rectangle around the detected triangle
                    cv2.rectangle(result, (x_tri, y_tri), (x_tri + w_tri, y_tri + h_tri), (0, 255, 0), 2)
                    redylw_houses.append(approx)

#####################                                          #######################
#####################   DETECTING RED HOUSES IN UNBURNT GRASS  #######################
#####################                                          #######################


    for contour in contours:
    # Approximate the contour with a polygon
        epsilon = 0.04 * cv2.arcLength(contour, True)
        approx1 = cv2.approxPolyDP(contour, epsilon, True)
    
    # If the contour has 3 vertices, it's a triangle
        if len(approx1) == 3:
        # Get the moments of the contour to calculate the centroid
            moments = cv2.moments(contour)
            centroid_x = int(moments["m10"] / moments["m00"])
            centroid_y = int(moments["m01"] / moments["m00"])
        
        # Get the BGR pixel value at the centroid
            centroid_pixel_value = result[centroid_y, centroid_x]
        
        # Check if the centroid pixel value is within the specified region color bounds
            if np.all(np.logical_and(centroid_pixel_value >= lwrd, centroid_pixel_value <= uprd)):
            # Create a bounding rectangle around the detected red triangle
                x_tri, y_tri, w_tri, h_tri = cv2.boundingRect(approx1)
            
            # Create an ROI using the bounding rectangle of the detected triangle
                roi = result[y_tri:y_tri+h_tri, x_tri:x_tri+w_tri]
            
            # Calculate the number of yellow pixels in the ROI
                num_cyan_pixels = np.sum(np.logical_and(roi[:, :, 0] == 230, roi[:, :, 1] == 230, roi[:, :, 2] == 0))
            
            # Check if the number of yellow pixels exceeds a threshold
                cyan_pixel_threshold = 3  # Adjust as needed
                if num_cyan_pixels > cyan_pixel_threshold:
                # Draw a rectangle around the detected triangle
                    cv2.rectangle(result, (x_tri, y_tri), (x_tri + w_tri, y_tri + h_tri), (0, 255, 255), 2)
                    redcyn_houses.append(approx1)

#####################                                          #######################
#####################   DETECTING BLUE HOUSES IN UNBURNT GRASS  #######################
#####################                                          #######################

    for contour in contours1:
    # Approximate the contour with a polygon
        epsilon = 0.04 * cv2.arcLength(contour, True)
        approx2 = cv2.approxPolyDP(contour, epsilon, True)
    
    # If the contour has 3 vertices, it's a triangle
        if len(approx2) == 3:
        # Get the moments of the contour to calculate the centroid
            moments = cv2.moments(contour)
            centroid_x = int(moments["m10"] / moments["m00"])
            centroid_y = int(moments["m01"] / moments["m00"])
        
        # Get the BGR pixel value at the centroid
            centroid_pixel_value = result[centroid_y, centroid_x]
        
        # Check if the centroid pixel value is within the specified region color bounds
            if np.all(np.logical_and(centroid_pixel_value >= lwblu, centroid_pixel_value <= upblu)):
            # Create a bounding rectangle around the detected red triangle
                x_tri, y_tri, w_tri, h_tri = cv2.boundingRect(approx2)
            
            # Create an ROI using the bounding rectangle of the detected triangle
                roi = result[y_tri:y_tri+h_tri, x_tri:x_tri+w_tri]
            # Calculate the number of yellow pixels in the ROI
                num_cyan_pixels = np.sum(np.logical_and(roi[:, :, 0] == 230, roi[:, :, 1] == 230, roi[:, :, 2] == 0))
            
            # Check if the number of yellow pixels exceeds a threshold
                cyan_pixel_threshold = 3  # Adjust as needed
                if num_cyan_pixels > cyan_pixel_threshold:
                # Draw a rectangle around the detected triangle
                    cv2.rectangle(result, (x_tri, y_tri), (x_tri + w_tri, y_tri + h_tri), (255, 255, 255), 2)
                    blucyn_houses.append(approx2)

#####################                                        #######################
#####################   DETECTING BLU HOUSES IN BURNT GRASS  #######################
#####################                                        #######################

    for contour in contours1:
    # Approximate the contour with a polygon
        epsilon = 0.04 * cv2.arcLength(contour, True)
        approx3 = cv2.approxPolyDP(contour, epsilon, True)
    
    # If the contour has 3 vertices, it's a triangle
        if len(approx3) == 3:
        # Get the moments of the contour to calculate the centroid
            moments = cv2.moments(contour)
            centroid_x = int(moments["m10"] / moments["m00"])
            centroid_y = int(moments["m01"] / moments["m00"])
        
        # Get the BGR pixel value at the centroid
            centroid_pixel_value = result[centroid_y, centroid_x]
        
        # Check if the centroid pixel value is within the specified region color bounds
            if np.all(np.logical_and(centroid_pixel_value >= lwblu, centroid_pixel_value <= upblu)):
            # Create a bounding rectangle around the detected red triangle
                x_tri, y_tri, w_tri, h_tri = cv2.boundingRect(approx3)
            
            # Create an ROI using the bounding rectangle of the detected triangle
                roi = result[y_tri:y_tri+h_tri, x_tri:x_tri+w_tri]
            # Calculate the number of yellow pixels in the ROI
                num_yellow_pixels = np.sum(np.logical_and(roi[:, :, 0] == 0, roi[:, :, 1] == 230, roi[:, :, 2] == 230))
            
            # Check if the number of yellow pixels exceeds a threshold
                yellow_threshold = 3  # Adjust as needed
                if num_yellow_pixels > yellow_threshold:
                # Draw a rectangle around the detected triangle
                    cv2.rectangle(result, (x_tri, y_tri), (x_tri + w_tri, y_tri + h_tri), (0, 0, 0), 2)
                    bluylw_houses.append(approx3)
    
                    

    Hb =(len(bluylw_houses)+len(redylw_houses))
    Hg = (len(redcyn_houses)+len(blucyn_houses))
    Pb= (len(bluylw_houses)*2+len(redylw_houses))
    Pg= (len(redcyn_houses)+len((blucyn_houses*2)))
    priority.append([Pb,Pg])
    housecount.append([Hb,Hg])
    pr =(Pb/Pg)
    Pr= round(pr,2)

    pratio = [Pr]
    Pratio.append(pratio)
    print('no_of_houses',housecount)
    print('priority_houses',priority)
    
    imglist.append([Pr,filename])
    imglist.sort(reverse=True)
    for pratio, filename in imglist:
        imgoutput.append(filename)
    cv2.imshow('Detected Red Triangles with Specified Centroid Color', result)
    cv2.waitKey(0)
    cv2.destroyAllWindows()
print('Priority_ratio',Pratio)
print('img_rescue_ratio_desc_order',imgoutput[45:55])
                    