import cv2
import numpy as np
from skimage import measure

#Loading the image
img = cv2.imread('/Users/kukub/Desktop/jeden.png')
#Converting the image into gray-scale
img = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
cv2.imshow("okno",img)
cv2.waitKey(0)
#ret,thresh_img = cv2.threshold(img,127, 255, cv2.THRESH_BINARY)

#Finding edges of the image
edge_image = cv2.Canny(img,200,50)
#showing Edged image
cv2.imshow("okno2",edge_image)
cv2.waitKey(0)

# Finding all the lines in an image based on given parameters
contours, hierarchy = cv2.findContours(edge_image,
    cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)
#Reverting the original image back to BGR so we can draw in colors
img2 = cv2.cvtColor(img,cv2.COLOR_GRAY2BGR)
#parameter -1 specifies that we want to draw all the contours
i=0
k=0
o=255
for con in contours:
    cv2.drawContours(img2, contours[i], -1, (50, k, o), 2)
    i+=1
    k+=10
    o-=10
#cv2.drawContours(img2, contours[9], -1, (50, k, o), 2)
cv2.imshow("okno3",img2)
cv2.waitKey(0)
print(len(contours))
