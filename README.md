# Proyecto Oscilador Armónico

## Entorno de desarrollo

Se utiliza el módulo [https://docs.python.org/3/library/venv.html](venv) para crear un entorno virtual en Python. Gracias a esto, se pueden instalar las dependencias necesarias sin afectar el entorno global de Python.

### Pasos para iniciar el entorno de desarrollo

1. Clonar el repositorio:

    ```bash
    git clone https://github.com/s-becc/proyecto_oscilador_armonico.git
    ```

2. Navegar al directorio del proyecto:

    ```bash
    cd proyecto_oscilador_armonico
    ```

3. Crear y activar el entorno virtual:

    ```bash
    python -m venv .venv
    .venv/Scripts/activate
    ```

4. Instalar dependencias necesarias:

    ```bash
    pip install -r requirements.txt
    ```

5. Ejecutar el script principal:

    ```bash
    python main.py
    ```

## Descripción del Programa

Este script realiza el análisis de un video de un oscilador armónico (por ejemplo, un llavero oscilando) para extraer parámetros físicos del movimiento. El flujo principal es:

1. **Medición de referencia:** El usuario selecciona dos puntos en el video que corresponden a una distancia conocida (10 cm). Esto permite calcular la escala de píxeles a centímetros.
2. **Trackeo del objeto:** El programa detecta y sigue el objeto en movimiento en cada cuadro del video, extrayendo su posición vertical.
3. **Procesamiento de datos:** Convierte las posiciones a centímetros, centra los datos respecto al equilibrio y calcula el tiempo.
4. **Ajuste senoidal:** Ajusta los datos observados a una función coseno para obtener la frecuencia angular y la fase.
5. **Cálculo de derivadas:** Calcula numéricamente la velocidad y aceleración.
6. **Visualización:** Grafica posición, velocidad y aceleración observadas y teóricas.
7. **Parámetros físicos:** Imprime la amplitud, frecuencia angular, frecuencia y período del movimiento.

## Uso del programa

1. Asegúrate de tener el video `oscilador_llaves - Made with Clipchamp.mp4` en el mismo directorio que el script.
2. Ejecuta el script con:

    ```bash
    python main.py
    ```

3. Al iniciar, se mostrará el primer cuadro del video. Haz clic en los dos extremos del objeto de referencia (10 cm) para calibrar la escala. Una vez seleccionados los dos puntos, la ventana se cerrará automáticamente.
4. El programa comenzará a procesar el video automáticamente. Durante el procesamiento, se mostrarán tres ventanas: "ROI" (región de interés), "Video" (el video completo) y "Edges" (bordes detectados). Puedes presionar la tecla ESC en cualquier momento para detener el procesamiento anticipadamente, pero normalmente deja que termine solo.
5. Una vez procesado el video, se mostrarán las gráficas de posición, velocidad y aceleración (observadas y teóricas).
6. Al finalizar, se mostrarán los parámetros físicos calculados en la consola.
