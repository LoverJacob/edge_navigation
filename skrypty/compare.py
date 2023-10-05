import cv2
import numpy as np
from skimage import measure


def find_coordinates(contours, cor_list):
    for con in contours:
        xmin = np.min(con, axis=0)[0][0]
        xmax = np.max(con, axis=0)[0][0]
        ymin = np.min(con, axis=0)[0][1]
        ymax = np.max(con, axis=0)[0][1]
        area = (xmax - xmin) * (ymax - ymin)
        if area > 100:
            cor_list.append([xmin, xmax, ymin, ymax])
    return cor_list
# wczytanie zdjec
# img1 = cv2.imread('/Users/Kochan/Desktop/zrzuty2/1.png')
# img2 = cv2.imread('/Users/Kochan/Desktop/zrzuty2/3.png')
img1 = cv2.imread('/Users/kukub/Desktop/zrzuty/1.png')
img2 = cv2.imread('/Users/kukub/Desktop/zrzuty/2.png')

# zmiana barw obrazów
img1 = cv2.cvtColor(img1,cv2.COLOR_BGR2GRAY)
img2 = cv2.cvtColor(img2,cv2.COLOR_BGR2GRAY)

# detektor CANNY
edge_image1 = cv2.Canny(img1,100,300)
edge_image2 = cv2.Canny(img2,100,300)

# odszukanie kontorow
contours1, hierarchy1 = cv2.findContours(edge_image1,
    cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
contours2, hierarchy2 = cv2.findContours(edge_image2,
    cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

#zmienne
real_w = 32 # prawdziwa szerokosc FOV
real_h = 24 # prawdziwa dlugosc FOV
cor1 = [] # tablica na obiekty z ramki
cor2 = [] # tablica na obiekty z kolejnej ramki

# petle szukania wspolrzednych i odrzucania za malych obszarow
cor1 = find_coordinates(contours1,cor1)
cor2 = find_coordinates(contours2,cor2)

# wycinanie obiektow ze zdjec
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
    crop2 = img2[cor2[i][2]:cor2[i][3], cor2[i][0]:cor2[i][1]]
    if max > 0.5:
        crop2 = img2[cor2[i][2]:cor2[i][3],cor2[i][0]:cor2[i][1]]
        # cv2.imwrite("crop.png",crop1)
        cv2.rectangle(img1,(items1[0],items1[2]),(items1[1],items1[3]),(0,255,0),1)
        cv2.rectangle(img2,(cor2[i][0],cor2[i][2]),(cor2[i][1],cor2[i][3]),(0,255,0),1)
        cv2.imshow("okno1",img1)
        cv2.imshow("okno2",img2)
        odlx_p = items1[0]-cor2[i][0]
        odly_p = items1[2]-cor2[i][2]
        first = "x1=" + str(items1[0]) + "[px] y1=" + str(items1[2])+ "[px]"
        second = "x2=" + str(cor2[i][0]) + "[px] y2=" + str(cor2[i][2])+"[px]"
        print(first)
        print(second)
        odleglosci_p = "delta_x=" + str(odlx_p) + "[px]   delta_y=" + str(odly_p)+"[px]"
        print(odleglosci_p)
        odlx_m = (real_w/640)*odlx_p
        odly_m = (real_h/480)*odly_p
        odleglosci_m = "metry x=" + str(odlx_m) + "  y=" + str(odly_m)
        print(odleglosci_m)

        cv2.waitKey(0)
        # cv2.imwrite("img1.png",img1)
        # cv2.imwrite("img2.png", img2)