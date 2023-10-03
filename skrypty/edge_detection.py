import cv2
import numpy as np
from skimage import measure

#Loading the image
img = cv2.imread('/Users/kukub/Desktop/zrzuty/2.png')
#Converting the image into gray-scale
img = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
cv2.imshow("okno",img)
cv2.waitKey(0)
#ret,thresh_img = cv2.threshold(img,127, 255, cv2.THRESH_BINARY)

#Finding edges of the image
edge_image = cv2.Canny(img,50,200)
#showing Edged image
cv2.imshow("okno2",edge_image)
cv2.imwrite("edge1.png",edge_image)
cv2.waitKey(0)

# Finding all the lines in an image based on given parameters
contours, hierarchy = cv2.findContours(edge_image,
    cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
#Reverting the original image back to BGR so we can draw in colors
img2 = cv2.cvtColor(img,cv2.COLOR_GRAY2BGR)
#parameter -1 specifies that we want to draw all the contours
i=0
k=0
o=255
x_min = []
x_max = []
y_min = []
y_max = []
for con in contours:
    # cv2.drawContours(img2, contours[i], -1, (50, k, o), 2)
    #print("i="+str(i)+str(contours[i]))
    xmin = np.min(con,axis=0)[0][0]
    xmax = np.max(con,axis=0)[0][0]
    ymin = np.min(con,axis=0)[0][1]
    ymax = np.max(con,axis=0)[0][1]
    cv2.rectangle(img2,(xmin,ymin),(xmax,ymax),(0,255,0),1)
    i+=1
    k+=5
    o-=10
# print(xmin)
cv2.drawContours(img2, contours, -1, (255, 0, 0), 1)
cv2.imshow("okno3",img2)
cv2.waitKey(0)
cv2.imwrite("contour1.png",img2)