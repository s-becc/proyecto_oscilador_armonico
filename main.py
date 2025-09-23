import cv2
import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit


# 1 Cargar video y preparar detector

cap = cv2.VideoCapture(r"C:\Users\santi\OneDrive\Desktop\proyecto py\oscilador_llaves - Made with Clipchamp.mp4")
fps = cap.get(cv2.CAP_PROP_FPS)
if fps == 0:   # fallback si no detecta bien
    fps = 30
dt = 1 / fps
print("FPS detectado:", fps)

object_detector = cv2.createBackgroundSubtractorMOG2(history=100, varThreshold=40)
positions = []

# 2️ Trackeo
while True:
    ret, frame = cap.read()
    if not ret:
        break
    
    frame = cv2.resize(frame, (360, 640))  # esto cambia la escala
    roi = frame[200:500, 100:300]
    
    gray = cv2.cvtColor(roi, cv2.COLOR_BGR2GRAY)
    blur = cv2.GaussianBlur(gray, (7, 7), 0)
    edges = cv2.Canny(blur, 50, 150)
    
    contours, _ = cv2.findContours(edges, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    
    if contours:
        cnt = max(contours, key=cv2.contourArea)
        if cv2.contourArea(cnt) > 100:
            M = cv2.moments(cnt)
            if M["m00"] != 0:
                cx = int(M["m10"] / M["m00"])
                cy = int(M["m01"] / M["m00"])
                
                cv2.circle(roi, (cx, cy), 5, (0, 0, 255), -1)
                cv2.circle(roi, (cx, cy), 20, (255, 0, 0), 2)
                cv2.drawContours(roi, [cnt], -1, (0, 255, 0), 2)
                
                positions.append((cx, cy))

    cv2.imshow("ROI", roi)
    cv2.imshow("Video", frame)
    cv2.imshow("Edges", edges)

    if cv2.waitKey(30) & 0xFF == 27:
        break

cap.release()
cv2.destroyAllWindows()

# 3️ Procesar posiciones
positions = np.array(positions, dtype=float)
y_positions = positions[:, 1]  # solo componente vertical

# Amplitud y equilibrio
A = (np.max(y_positions) - np.min(y_positions)) / 2
y_equilibrium = (np.max(y_positions) + np.min(y_positions)) / 2
y_positions = y_positions - y_equilibrium  # centrar en el equilibrio

# Tiempo
t = np.arange(len(positions)) * dt

# 4️ Ajuste senoidal
def sine_wave(t, omega, phase):
    return A * np.cos(omega * t + phase)

popt, _ = curve_fit(sine_wave, t, y_positions, p0=[2*np.pi, 0])
omega, phase = popt

# Curvas teóricas
y_theoretical = A * np.cos(omega * t + phase)
v_theoretical = -A * omega * np.sin(omega * t + phase)
a_theoretical = -A * omega**2 * np.cos(omega * t + phase)

# 5️ Derivadas numéricas
v_numeric = np.gradient(y_positions, dt)
a_numeric = np.gradient(v_numeric, dt)


# 6️ Gráficas
plt.figure(figsize=(12, 10))

# Posición
plt.subplot(3,1,1)
plt.plot(t, y_positions, 'b.', label='Datos obsservados', alpha=0.6)
plt.plot(t, y_theoretical, 'r-', label='Posicion teórica')
plt.ylabel('Posición [px]')
plt.title('Movimiento Armónico Simple')
plt.legend()
plt.grid(True)

# Velocidad
plt.subplot(3,1,2)
plt.plot(t, v_numeric, 'b.', alpha=0.6, label='Datos observados')
plt.plot(t, v_theoretical, 'g-', label='Velocidad teórica')
plt.ylabel('Velocidad [px/s]')
plt.legend()
plt.grid(True)

# Aceleración
plt.subplot(3,1,3)
plt.plot(t, a_numeric, 'b.', alpha=0.6, label='Datos observados')
plt.plot(t, a_theoretical, 'm-', label='Aceleración teórica')
plt.xlabel('Tiempo [s]')
plt.ylabel('Aceleración [px/s²]')
plt.legend()
plt.grid(True)

plt.tight_layout()
plt.show()

# 7️ Parámetros
print(f"Amplitud: {A:.2f} px")
print(f"Frecuencia angular ω: {omega:.2f} rad/s")
print(f"Frecuencia f: {omega/(2*np.pi):.2f} Hz")
print(f"Período T: {2*np.pi/omega:.2f} s")

