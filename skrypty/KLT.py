import cv2
import numpy as np
import time

# Inicjalizacja kamery lub pliku wideo
video_capture = cv2.VideoCapture('/Users/Kochan/PycharmProjects/edge_navigation/data/1.mp4')
# video_capture = cv2.VideoCapture(0)


# Inicjalizacja parametrów algorytmu KLT
feature_params = dict(maxCorners=50,
                       qualityLevel=0.2,
                       minDistance=5,
                       blockSize=7)
lk_params = dict(winSize=(15, 15),
                 maxLevel=2,
                 criteria=(cv2.TERM_CRITERIA_EPS | cv2.TERM_CRITERIA_COUNT, 10, 0.03))

# Inicjalizacja początkowych punktów kluczowych i ich historii
previous_frame = None
previous_points = None
point_history = []
last_clear_time = time.time()
frame_counter = 0

# Inicjalizacja zmiennych przesunięcia
average_dx = 0
average_dy = 0

while True:
    ret, frame = video_capture.read()

    if not ret:
        break

    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    if previous_frame is not None:
        if previous_points is not None:
            # Śledzenie punktów kluczowych za pomocą algorytmu KLT
            new_points, status, _ = cv2.calcOpticalFlowPyrLK(previous_frame, gray, previous_points, None, **lk_params)

            # Obliczenie przesunięcia na podstawie punktów kluczowych
            total_dx = 0
            total_dy = 0
            num_points = 0

            for i in range(len(new_points)):
                if status[i] == 1:
                    x, y = new_points[i][0]
                    x, y = int(x), int(y)  # Konwersja współrzędnych na liczby całkowite
                    dx = new_points[i][0][0] - previous_points[i][0][0]
                    dy = new_points[i][0][1] - previous_points[i][0][1]

                    # Obliczenie średniego przesunięcia
                    total_dx += dx
                    total_dy += dy
                    num_points += 1

                    # Obliczenie współrzędnych punktu kluczowego
                    x, y = int(x), int(y)

                    # Zaznaczenie punktu czerwonym kółkiem
                    cv2.circle(frame, (x, y), 5, (0, 0, 255), -1)

                    # Dodanie bieżącego położenia punktu do historii
                    point_history.append((x, y))

            # Obliczenie średniego przesunięcia punktów kluczowych w klatce
            if num_points > 0:
                average_dx = total_dx / num_points
                average_dy = total_dy / num_points
                print(f'Średnie przesunięcie w klatce (x, y): ({average_dx:.2f}, {average_dy:.2f}) pikseli')

            previous_points = new_points

            # Sprawdzenie, czy minęły dwie sekundy od ostatniego czyszczenia śladów
            current_time = time.time()
            if current_time - last_clear_time >= 2:
                point_history = []  # Usunięcie śladów punktów
                last_clear_time = current_time

        frame_counter += 1

        # Co kilka klatek (np. co 20 klatek) ponownie wykrywamy punkty kluczowe
        if frame_counter % 20 == 0:
            previous_points = cv2.goodFeaturesToTrack(gray, mask=None, **feature_params).reshape(-1, 1, 2)

    else:
        # Pierwsza klatka - znajdź punkty kluczowe
        previous_points = cv2.goodFeaturesToTrack(gray, mask=None, **feature_params).reshape(-1, 1, 2)

    previous_frame = gray.copy()

    # Rysowanie śladu punktów na obrazie
    for point in point_history:
        cv2.circle(frame, point, 1, (0, 255, 0), -1)

    # Dodanie strzałki w lewym górnym rogu
    arrow_length = 50
    arrow_color = (0, 0, 255)  # Kolor strzałki (zielony)
    cv2.arrowedLine(frame, (200, 200), (20 + int(average_dx * arrow_length), 20 + int(average_dy * arrow_length)),
                    arrow_color, 2)

    cv2.imshow('Śledzenie punktów kluczowych', frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

video_capture.release()
cv2.destroyAllWindows()
