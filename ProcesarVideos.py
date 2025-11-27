import cv2
import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit
import os

# 1️⃣ Medir referencia en píxeles (haz clic en los extremos del objeto de 10 cm)
def click_event(event, x, y, flags, params):
    if event == cv2.EVENT_LBUTTONDOWN:
        print(f"Coordenada: ({x}, {y})")
        points.append((x, y))
        if len(points) == 2:
            cv2.line(frame, points[0], points[1], (255, 0, 0), 2)
            cv2.imshow("Medir", frame)
            dist = np.linalg.norm(np.array(points[0]) - np.array(points[1]))
            print(f"Distancia en píxeles: {dist}")
            # Calcula la escala y muestra
            px_to_cm = referencia / dist
            print(f"Escala calculada: {px_to_cm:.5f} cm/px")
            params['px_to_cm'] = px_to_cm

referencia = 0.3 #Largo en metros de la tabla que se usa de base

#Definir directorios
dir = os.path.dirname(__file__)
carpetaVideos = os.path.join(dir, "Videos")
carpetaResultados = os.path.join(dir, "Resultados")
os.makedirs(carpetaResultados, exist_ok=True)

videos = [f for f in os.listdir(carpetaVideos) if f.endswith(".mp4")]

for v in videos:
    # --- Medición de referencia ---
    video = os.path.join(carpetaVideos, v)
    cap = cv2.VideoCapture(video)
    ret, frame = cap.read()
    points = []
    params = {}
    if ret:
        cv2.namedWindow("Medir", cv2.WINDOW_NORMAL)
        cv2.imshow("Medir", frame)
        cv2.setMouseCallback("Medir", click_event, params)
        print("Haz clic en los dos extremos del objeto de referencia.")
        while len(points) < 2:
            cv2.waitKey(1)
        cv2.destroyAllWindows()
    cap.release()

    # Si no se midió, usa un valor por defecto
    px_to_cm = params.get('px_to_cm', 0.05)  # Cambia este valor si tienes otra referencia
    print("cm: ", px_to_cm)
    # 2️⃣ Trackeo
    cap = cv2.VideoCapture(video)
    fps = cap.get(cv2.CAP_PROP_FPS)
    if fps == 0:
        fps = 30
    dt = 1 / fps
    print("FPS detectado:", fps)

    object_detector = cv2.createBackgroundSubtractorMOG2(history=100, varThreshold=40)
    tracking_data = []
    frame_index = 0

    while True:
        ret, frame = cap.read()
        if not ret:
            break

        hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

        lower_range = np.array([0, 203, 76])
        upper_range = np.array([55, 255, 255])

        mask = cv2.inRange(hsv, lower_range, upper_range)

        contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

        if contours:
            cnt = max(contours, key=cv2.contourArea)
            if cv2.contourArea(cnt) > 100:
                M = cv2.moments(cnt)
                if M["m00"] != 0:
                    cx = int(M["m10"] / M["m00"])
                    cy = int(M["m01"] / M["m00"])
                    cv2.circle(frame, (cx, cy), 10, (0, 250, 0), -1)
                    time = frame_index/fps
                    posX = cx * px_to_cm
                    posY = cy * px_to_cm
                    tracking_data.append((time, posX, posY))

        cv2.imshow("Video", frame)
        cv2.imshow("Mascara de color", mask)

        if cv2.waitKey(30) & 0xFF == 27:
            break

        frame_index += 1

    cap.release()
    cv2.destroyAllWindows()

    # Guardar Datos
    nombreSinExtension = os.path.splitext(v)[0]
    carpetaPosiciones = os.path.join(carpetaResultados, "Posicion Cartesiana", "Sin Filtrar")
    os.makedirs(carpetaPosiciones, exist_ok = True)
    rutaSalida = os.path.join(carpetaPosiciones, f"P_{nombreSinExtension}.csv")
    results = np.array(tracking_data, dtype = float)
    if results.size == 0:
        print("No se detectaron posiciones para guardar.")
    else:
        time_index = results[:, 0]
        x = results[:, 1]
        y = results[:, 2]
        x_final = x[0]
        y_final = y[0]
        x_centrado = x - x_final
        y_centrado = y - y_final
        results_matrix = np.column_stack((time_index, x_centrado, y_centrado))
        header = "Tiempo (s),PosX (m),PosY (m)"

        np.savetxt(
            rutaSalida,
            results_matrix,
            delimiter=",",
            header=header,
            comments="",
            fmt="%.4f"
        )