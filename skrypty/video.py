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
        abs_x = abs(xmin - xmax)
        abs_y = abs(ymin - ymax)

        if area > 100 and area < 5000 and abs_x>10 and abs_y>10:
            cor_list.append([xmin, xmax, ymin, ymax])
    return cor_list


#zmienne
real_w = 32 # prawdziwa szerokosc FOV
real_h = 24 # prawdziwa dlugosc FOV
cor1 = [] # tablica na obiekty z ramki
cor2 = [] # tablica na obiekty z kolejnej ramki
h_level = 150
l_level = 50
first_event = 0

# odtworzenie nagrania
cap = cv2.VideoCapture('/Users/Kochan/PycharmProjects/edge_navigation/data/1.mp4')
# cap = cv2.VideoCapture('/Users/kukub/PycharmProjects/edge_detection/data/1.mp4')

# cap = cv2.VideoCapture(0)
# cap.set(cv2.CAP_PROP_FPS, 120)
# cap.set(cv2.CAP_PROP_FOURCC, cv2.VideoWriter.fourcc('M','J','P','G'))
# cap.set(cv2.CAP_PROP_SETTINGS, 1)
# cap.set(cv2.CAP_PROP_EXPOSURE, -12)
# cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
# cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)

frame_check = 0

# sprawdzenie czy udało sie otworzyc nagranie
if (cap.isOpened()== False):
   print("Error opening video stream or file")
# pętla każdej klatki nagrania
while (cap.isOpened()):
    ret, frame = cap.read()
    frame = cv2.resize(frame, (640, 480))
    img_copy = cv2.cvtColor(frame,cv2.COLOR_BGR2GRAY)
    # print(ret)
    # img_copy = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    cv2.imshow('live',frame)
    if frame_check > 6:
        if ret == True:
            if first_event == 0:
                img_new = cv2.cvtColor(frame,cv2.COLOR_BGR2GRAY)
                img_old = cv2.cvtColor(frame,cv2.COLOR_BGR2GRAY)
                first_event +=1
            else:
                img_new = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

            edge_image1 = cv2.Canny(img_new,l_level,h_level)
            edge_image2 = cv2.Canny(img_old,l_level,h_level)
            # edge_image1 = cv2.cvtColor(edge_image1, cv2.COLOR_BGR2GRAY)
            # edge_image2 = cv2.cvtColor(edge_image2, cv2.COLOR_BGR2GRAY)
            # odszukanie kontorow
            contours1, hierarchy1 = cv2.findContours(edge_image1,
                cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
            contours2, hierarchy2 = cv2.findContours(edge_image2,
                cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
            cor1.clear()
            cor2.clear()
            cor1 = find_coordinates(contours1,cor1)
            cor2 = find_coordinates(contours2,cor2)
            # wycinanie obiektow ze zdjec
            for items1 in cor1[:5]:
                crop1 = img_new[items1[2]:items1[3],items1[0]:items1[1]]
                hist1 = cv2.calcHist(crop1, [0], None, [256], [0, 256])
                # print("zaczynam")
                i=0
                max=0
                for index, items2 in enumerate(cor2):
                    crop2 = img_old[items2[2]:items2[3],items2[0]:items2[1]]
                    hist2 = cv2.calcHist(crop2, [0], None, [256], [0, 256])
                    correlation = cv2.compareHist(hist1, hist2, cv2.HISTCMP_CORREL)
                    # print('Korelacja histogramów:', correlation)
                    if correlation>max:
                        i = index
                        max = correlation
                    if max > 0.98: # hist1 = hist2
                        break
                # print(i)
                # print("koncze")
                if i == 0:
                     break
                if max > 0.95:
                    crop2 = img_old[cor2[i][2]:cor2[i][3],cor2[i][0]:cor2[i][1]]

                    cv2.rectangle(img_new,(items1[0],items1[2]),(items1[1],items1[3]),(0,255,0),4)
                    cv2.rectangle(img_old,(cor2[i][0],cor2[i][2]),(cor2[i][1],cor2[i][3]),(0,255,0),4)

                    odlx_p = items1[0]-cor2[i][0]
                    odly_p = items1[2]-cor2[i][2]
                    first = "x1=" + str(items1[0]) + " y1=" + str(items1[2])
                    second = "x2=" + str(cor2[i][0]) + " y2=" + str(cor2[i][2])
                    # print(first)
                    # print(second)
                    img_new = cv2.putText(img_new, first, (50, 50), cv2.FONT_HERSHEY_SIMPLEX,
                                        1, (255,0,0), 2, cv2.LINE_AA)
                    img_new = cv2.putText(img_new, second, (50, 100), cv2.FONT_HERSHEY_SIMPLEX,
                                          1, (255, 0, 0), 2, cv2.LINE_AA)
                    odleglosci_p = "piksele x=" + str(odlx_p) + "  y=" + str(odly_p)
                    img_old = cv2.putText(img_old, odleglosci_p, (50, 50), cv2.FONT_HERSHEY_SIMPLEX,
                                          1, (255, 0, 0), 2, cv2.LINE_AA)
                    print(odleglosci_p)
                    odlx_m = (real_w/640)*odlx_p
                    odly_m = (real_h/480)*odly_p
                    odleglosci_m = "metry x=" + str(odlx_m) + "  y=" + str(odly_m)
                    # print(odleglosci_m)
                cv2.imshow("predkosc", img_old)
                cv2.waitKey(1)
                # cv2.imshow("okenko",img_new)

        # cv2.imshow("okienko",img_old)
        # cv2.waitKey(0)
            img_old = img_copy
        frame_check=0
    elif frame_check < 10:
        frame_check+=1