import cv2
import numpy as np
from skimage import measure

img1 = cv2.imread('/Users/kukub/Desktop/trzy.png')
img2 = cv2.imread('/Users/kukub/Desktop/cztery.png')

img1 = cv2.cvtColor(img1,cv2.COLOR_BGR2GRAY)
img2 = cv2.cvtColor(img2,cv2.COLOR_BGR2GRAY)

edge_image1 = cv2.Canny(img1,280,300)
edge_image2 = cv2.Canny(img2,280,300)

contours1, hierarchy1 = cv2.findContours(edge_image1,
    cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
contours2, hierarchy2 = cv2.findContours(edge_image2,
    cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)


cor1 = []
cor2 = []
for con in contours1:
    # cv2.drawContours(img2, contours[i], -1, (50, k, o), 2)
    #print("i="+str(i)+str(contours[i]))
    xmin = np.min(con,axis=0)[0][0]
    xmax = np.max(con,axis=0)[0][0]
    ymin = np.min(con,axis=0)[0][1]
    ymax = np.max(con,axis=0)[0][1]
    area = (xmax-xmin)*(ymax-ymin)
    if area>100:
        cor1.append([xmin,xmax,ymin,ymax])
        crop = img1[ymin:ymax, xmin:xmax]

for con in contours2:
    # cv2.drawContours(img2, contours[i], -1, (50, k, o), 2)
    #print("i="+str(i)+str(contours[i]))
    xmin = np.min(con,axis=0)[0][0]
    xmax = np.max(con,axis=0)[0][0]
    ymin = np.min(con,axis=0)[0][1]
    ymax = np.max(con,axis=0)[0][1]
    area = (xmax-xmin)*(ymax-ymin)
    if area>50:
        cor2.append([xmin,xmax,ymin,ymax])

for items1 in cor1:
    crop1 = img1[items1[2]:items1[3],items1[0]:items1[1]]
    hist1 = cv2.calcHist(crop1, [0, 1, 2], None, [256, 256, 256], [0, 256, 0, 256, 0, 256])
    print("zaczynam")
    i=0
    max=0
    for index, items2 in enumerate(cor2):
        crop2 = img2[items2[2]:items2[3],items2[0]:items2[1]]
        hist2 = cv2.calcHist(crop2, [0, 1, 2], None, [256, 256, 256], [0, 256, 0, 256, 0, 256])
        correlation = cv2.compareHist(hist1, hist2, cv2.HISTCMP_CORREL)
        print('Korelacja histogramów:', correlation)
        if correlation>max:
            i = index
            max = correlation
    print(i)
    print("koncze")
    if max > 0.5:
        crop2 = img2[cor2[i][2]:cor2[i][3],cor2[i][0]:cor2[i][1]]

        cv2.rectangle(img1,(items1[0],items1[2]),(items1[1],items1[3]),(0,255,0),1)
        cv2.rectangle(img2,(cor2[i][0],cor2[i][2]),(cor2[i][1],cor2[i][3]),(0,255,0),1)
        cv2.imshow("okno1",img1)
        cv2.imshow("okno2",img2)
        cv2.waitKey(0)
# crop1 = img1[cor1[0][2]:cor1[0][3],cor1[0][0]:cor1[0][1]]
# crop2 = img2[cor2[2][2]:cor2[2][3],cor2[2][0]:cor2[2][1]]
# res = cv2.absdiff(crop1, crop2)
# res = res.astype(np.uint8)
# percentage = (np.count_nonzero(res) * 100) / res.size
# print(percentage)
#
# hist1 = cv2.calcHist(crop1, [0, 1, 2], None, [256, 256, 256], [0, 256, 0, 256, 0, 256])
# hist2 = cv2.calcHist(crop2, [0, 1, 2], None, [256, 256, 256], [0, 256, 0, 256, 0, 256])
#
# # Porównaj histogramy np. za pomocą korelacji histogramów
# correlation = cv2.compareHist(hist1, hist2, cv2.HISTCMP_CORREL)
# print('Korelacja histogramów:', correlation)
# print(type(correlation))