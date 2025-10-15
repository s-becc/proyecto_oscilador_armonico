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
            px_to_cm = altura / dist
            print(f"Escala calculada: {px_to_cm:.5f} cm/px")
            params['px_to_cm'] = px_to_cm

altura = 1.6 #Altura en cm del objeto de referencia, en este caso el clavo

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
        cv2.imshow("Medir", frame)
        cv2.setMouseCallback("Medir", click_event, params)
        print("Haz clic en los dos extremos del objeto de referencia.")
        cv2.waitKey(0)
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

        lower_range = np.array([39, 95, 0])
        upper_range = np.array([133, 255, 255]) 

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
        results_matrix = np.column_stack((time_index, x, y))
        header = "Tiempo (s),PosX (cm),PosY (cm)"

        np.savetxt(
            rutaSalida,
            results_matrix,
            delimiter=",",
            header=header,
            comments="",
            fmt="%.4f"
        )
    
    # # 3️⃣ Procesar posiciones
    # positions = np.array(positions, dtype=float)

    # if positions.shape[0] == 0:
    #     print("No se detectaron posiciones. Verifica el video o los parámetros de detección.")
    #     exit()

    # y_positions = positions[:, 1]  # solo componente vertical

    # # Convertir a centímetros
    # y_positions = y_positions * px_to_cm

    # # Amplitud y equilibrio
    # A = (np.max(y_positions) - np.min(y_positions)) / 2
    # y_equilibrium = (np.max(y_positions) + np.min(y_positions)) / 2
    # y_positions = y_positions - y_equilibrium  # centrar en el equilibrio

    # # Tiempo
    # t = np.arange(len(positions)) * dt

    # # 4️⃣ Ajuste senoidal
    # def sine_wave(t, omega, phase):
    #     return A * np.cos(omega * t + phase)

    # popt, _ = curve_fit(sine_wave, t, y_positions, p0=[2*np.pi, 0])
    # omega, phase = popt

    # # Curvas teóricas
    # y_theoretical = A * np.cos(omega * t + phase)
    # v_theoretical = -A * omega * np.sin(omega * t + phase)
    # a_theoretical = -A * omega**2 * np.cos(omega * t + phase)

    # # 5️⃣ Derivadas numéricas
    # v_numeric = np.gradient(y_positions, dt)      # cm/s
    # a_numeric = np.gradient(v_numeric, dt)        # cm/s²

    # # 6️⃣ Gráficas
    # plt.figure(figsize=(12, 10))

    # # Posición
    # plt.subplot(3,1,1)
    # plt.plot(t, y_positions, 'b.', label='Datos obsservados', alpha=0.6)
    # plt.plot(t, y_theoretical, 'r-', label='Posicion teórica')
    # plt.ylabel('Posición [cm]')
    # plt.title('Movimiento Armónico Simple')
    # plt.legend()
    # plt.grid(True)

    # # Velocidad
    # plt.subplot(3,1,2)
    # plt.plot(t, v_numeric, 'b.', alpha=0.6, label='Datos observados')
    # plt.plot(t, v_theoretical, 'g-', label='Velocidad teórica')
    # plt.ylabel('Velocidad [cm/s]')
    # plt.legend()
    # plt.grid(True)

    # # Aceleración
    # plt.subplot(3,1,3)
    # plt.plot(t, a_numeric, 'b.', alpha=0.6, label='Datos observados')
    # plt.plot(t, a_theoretical, 'm-', label='Aceleración teórica')
    # plt.xlabel('Tiempo [s]')
    # plt.ylabel('Aceleración [cm/s²]')
    # plt.legend()
    # plt.grid(True)

    # plt.tight_layout()
    # plt.show()

    # # 7️⃣ Parámetros
    # print(f"Amplitud: {A:.2f} cm")
    # print(f"Frecuencia angular ω: {omega:.2f} rad/s")
    # print(f"Frecuencia f: {omega/(2*np.pi):.2f} Hz")
    # print(f"Período T: {2*np.pi/omega:.2f} s")