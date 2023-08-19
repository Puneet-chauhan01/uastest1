# uastest
this is the solution of problem asked in uas department test. i have tried my best to solve it.
soo as i am completely new in opencv and doesnt know anything about numpy and opencv libraries in python initially 
initially i tried to learn basics about opening closing ,saving and performing basic tasks on images in opencv



#tried thresholding and template detection

so problem has 4 parts, i initially tried to solve first 2 parts i.e to print clearly distinct burnt and unburnt area and print no of houses in both regions in a list.
To solve the problem i tried to threshold the whole sample pitcure provided in task document and then i tried template detection which doesnt yield desired result 
it was not able to detect all the triangles because during thresholding a lot the green area was getting messed up.
So i thought of applying filters like gauss and blur but thresholding was not giving the desired result.
so this method failed......

#using haar cascade with help of gui
soo.. template detection  was failing than i thought of making a haar cascade with help of gui tool by aemin ahmadi, i created a haar cascade to detect red triangles
then i used roi thresholding by doing some research so basically i created arrays to store uint8 values for color of brown black and green in hsv which was the bg color of image
then i changed image to hsv and created roi fro green black and brown color and changed them blck/brwn=yellow and green=cyan for better detection of triangles 
and to distinguish burnt and unburnt area.

[UAS-DTU Round 2 Task First Year1 (2).pdf](https://github.com/Puneet-chauhan01/uastest/files/12385893/UAS-DTU.Round.2.Task.First.Year1.2.pdf)

i was able to get a image with much simpler colours than the one provided.
but it has too many black pixels in brown area which probably got thresholded to black while doing  roi based thresholding so i created a function by doing some research to convert rest of black pixels into yellow and now its able to distinguish burnt and unburnt area much easily i.e was first output asked in q but i am not able to process whole 11 images to get an output for that i will need to do more research moreover the cascader which i prepared is now giving false positives and also not detecting many triangles probably i have to remake another cascader with help of proccessed images which are cyan and yellow which will give accurate result but if you can tell me any other approach to this q plz tell me.

##please tell me if i am doing it right or do i have to change my approach in some other technique or rebuff the thresholding as most of the space in my code is for thresholding only##

