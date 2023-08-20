# uastest
# this is the solution of problem asked in uas department test. i have tried my best to solve it.##
soo as i am completely new in opencv and doesnt know anything about numpy and opencv libraries in python 
initially i tried to learn basics about opening closing ,saving and performing basic tasks on images in opencv 


[UAS-DTU Round 2 Task First Year1 (2).pdf](https://github.com/Puneet-chauhan01/uastest/files/12385893/UAS-DTU.Round.2.Task.First.Year1.2.pdf)
this probelem has 5 tasks and i am trying to solve them one by one....
#soo..i tried to simply create a mask of burnt and unburnt areas chnge them to colours yellow and cyan and then i created another mask on it to extract yellow region
and performed morphological transformation in the image then i apllied gauss filter to get even smoother masked region for better detection of triangles in it.
after getting a mask for yellow color i applied graycale and then convert it to binary and thresholded it to detect contours and edges in it. Then i iterate a loop 
to get detect triangles using polyDP function and store no. of triangle detected in a list but in img 8 it was detecting a very large triangle in edges of cyan regn 
soooo i searched on how to detect only a specified size(length) of triangles in a region and then i used another loop which basically creates a rectangle over the detected triangle and than compare the its side length with the specified size length which is enough just for the small triangles or houses.
so i was able do detect triangles the same way in cyan mask too and then i researched to how to apply this code in all the 10 images at once and give me the desired output that is no. of houses in burnt and unburnt area in a list. then i created a loop to open the images one by one apply the code in them.
so i was able to complete task1 , task 2 and i still researching on how to detect objects of diff color in a region of different color. Probably its not possible using contours or edge detection as they involve grayscaling. It may require a complex mask creating may be i have to create a  mask to change the color all the colored objets inside a specified color region and then bring it in color range of bg to apply color based detection more easily ......


## if you have any suggestions or tips plz tell me ##

