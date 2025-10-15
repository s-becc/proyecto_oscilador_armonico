import cv2
import numpy as np

# Una función vacía que necesitamos para los trackbars
def nada(x):
    pass

# Carga una imagen de tu video donde se vea bien el objeto
# Puedes sacar una captura de pantalla del video
frame = cv2.imread('Calibre.png') 
# Opcional: redimensiona si es muy grande para tu pantalla
#frame = cv2.resize(frame, (600, 400)) 

# Crea una ventana para los controles
cv2.namedWindow("Controles")

# Crea los deslizadores para los valores HSV MÍNIMOS y MÁXIMOS
# H (Hue/Tono), S (Saturation/Saturación), V (Value/Brillo)
cv2.createTrackbar("H Min", "Controles", 0, 179, nada) # El Hue va de 0 a 179 en OpenCV
cv2.createTrackbar("S Min", "Controles", 0, 255, nada)
cv2.createTrackbar("V Min", "Controles", 0, 255, nada)
cv2.createTrackbar("H Max", "Controles", 179, 179, nada)
cv2.createTrackbar("S Max", "Controles", 255, 255, nada)
cv2.createTrackbar("V Max", "Controles", 255, 255, nada)

while True:
    # Convierte la imagen a HSV
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

    # Lee los valores actuales de los deslizadores
    h_min = cv2.getTrackbarPos("H Min", "Controles")
    s_min = cv2.getTrackbarPos("S Min", "Controles")
    v_min = cv2.getTrackbarPos("V Min", "Controles")
    h_max = cv2.getTrackbarPos("H Max", "Controles")
    s_max = cv2.getTrackbarPos("S Max", "Controles")
    v_max = cv2.getTrackbarPos("V Max", "Controles")

    # Crea los arrays con los valores de los deslizadores
    lower_range = np.array([h_min, s_min, v_min])
    upper_range = np.array([h_max, s_max, v_max])

    # Crea la máscara con el rango actual
    mask = cv2.inRange(hsv, lower_range, upper_range)
    
    # Opcional: Muestra el resultado aplicando la máscara a la imagen original
    resultado = cv2.bitwise_and(frame, frame, mask=mask)

    # Muestra las ventanas
    cv2.imshow("Imagen Original", frame)
    cv2.imshow("Mascara", mask)
    cv2.imshow("Resultado", resultado)

    # Termina el bucle si se presiona la tecla 'esc'
    if cv2.waitKey(1) & 0xFF == 27:
        break

cv2.destroyAllWindows()

# Imprime los valores finales para que los copies en tu script principal
print(f"lower_range = np.array([{h_min}, {s_min}, {v_min}])")
print(f"upper_range = np.array([{h_max}, {s_max}, {v_max}])")