import pandas as pd
from scipy.signal import savgol_filter
import numpy as np
import os

def calculate_derivative(x, t):
    """
    Calcula la velocidad derivando en base a posición x y tiempo t, luego suaviza.
    Maneja casos donde delta_t es demasiado pequeño para evitar infinitos.
    """

    x = pd.Series(x)
    t = pd.Series(t)

    # Derivar posición suavizada para obtener velocidad
    delta_x = x.diff(periods=2)
    delta_t = t.diff(periods=2)
    
    derivative = delta_x / delta_t

    return derivative

# Definir carpeta base
dir = os.path.dirname(__file__)
carpeta_resultados = os.path.join(dir, "Resultados")
carpeta_posicion = os.path.join(carpeta_resultados, "Posicion Cartesiana")
carpeta_pos_sin_filtrar = os.path.join(carpeta_posicion, "Sin Filtrar")
carpeta_pos_filtrado = os.path.join(carpeta_posicion, "Filtrado")

os.makedirs(carpeta_pos_filtrado, exist_ok=True)

window_size = 4
order = 2

#Suavizar posición
for archivo_csv in os.listdir(carpeta_pos_sin_filtrar):
    ruta_csv = os.path.join(carpeta_pos_sin_filtrar, archivo_csv)
    nombre_base = os.path.splitext(archivo_csv)[0]
    try:
        df = pd.read_csv(ruta_csv)
        if df.empty:
            print(f"Archivo sin datos: {archivo_csv}")
            continue

        df_aux = pd.DataFrame({
            "Tiempo (s)": df["Tiempo (s)"]
        })
        
        if len(df["PosX (cm)"] >= window_size):
            df_aux["PosX (cm)"] = savgol_filter(df["PosX (cm)"], window_length=window_size, polyorder=order)

        if len(df["PosY (cm)"] >= window_size):
            df_aux["PosY (cm)"] = savgol_filter(df["PosY (cm)"], window_length=window_size, polyorder=order)

        df_export = df_aux[["Tiempo (s)", "PosX (cm)", "PosY (cm)"]]
        salida_csv = os.path.join(carpeta_pos_filtrado, f"{nombre_base} Filtrado.csv")
        df_export.to_csv(salida_csv, index = False)
        print(f"Generado: {salida_csv}")
    except Exception as e:
        print(f"Error suavizando el archivo: {archivo_csv}: {e}")
        continue

# Crear carpeta para las velocidades si no existen
carpeta_velocidad = os.path.join(carpeta_resultados, "Velocidad Cartesiana")
carpeta_vel_sin_filtrar = os.path.join(carpeta_velocidad, "Sin Filtrar")
carpeta_vel_filtrado = os.path.join(carpeta_velocidad, "Filtrado")

os.makedirs(carpeta_vel_sin_filtrar, exist_ok=True)
os.makedirs(carpeta_vel_filtrado, exist_ok=True)

# Calcular velocidad para todos los archivos de posicion filtrados
for archivo_csv in os.listdir(carpeta_pos_filtrado):
    ruta_csv = os.path.join(carpeta_pos_filtrado, archivo_csv)
    nombre_base = os.path.splitext(archivo_csv)[0]
    try:
        # Leer archivo original
        df = pd.read_csv(ruta_csv)

        if df.empty:
            print(f"Archivo sin datos: {archivo_csv}")
            continue

        df_aux = pd.DataFrame({
            "Tiempo (s)": df["Tiempo (s)"]
        })

        # Calcular velocidades
        df_aux["velX (m/s)"] = calculate_derivative(df["PosX (cm)"], df["Tiempo (s)"])
        df_aux["velY (m/s)"] = calculate_derivative(df["PosY (cm)"], df["Tiempo (s)"])

        # Crear nuevo DataFrame para exportar
        df_export = df_aux[["Tiempo (s)", "velX (m/s)", "velY (m/s)"]]
        
        #Eliminar los NaN del dataframe
        df_export = df_export.bfill()

        # Guardar como nuevo archivo
        nombre_limpio = nombre_base.replace(" Filtrado", "").replace("P_", "V_")
        salida_csv = os.path.join(carpeta_vel_sin_filtrar, f"{nombre_limpio}.csv")
        df_export.to_csv(salida_csv, index=False)

        print(f"Generado: {salida_csv}")

    except Exception as e:
        print(f"Error procesando {archivo_csv}: {e}")
        continue

#Suavizar velocidad
for archivo_csv in os.listdir(carpeta_vel_sin_filtrar):
    ruta_csv = os.path.join(carpeta_vel_sin_filtrar, archivo_csv)
    nombre_base = os.path.splitext(archivo_csv)[0]
    try:
        df = pd.read_csv(ruta_csv)
        if df.empty:
            print(f"Archivo sin datos: {archivo_csv}")
            continue

        df_aux = pd.DataFrame({
            "Tiempo (s)": df["Tiempo (s)"]
        })

        if len(df["velX (m/s)"] >= window_size):
            df_aux["velX (m/s)"] = savgol_filter(df["velX (m/s)"], window_length=window_size, polyorder=order)

        if len(df["velY (m/s)"] >= window_size):
            df_aux["velY (m/s)"] = savgol_filter(df["velY (m/s)"], window_length=window_size, polyorder=order)

        df_export = df_aux[["Tiempo (s)", "velX (m/s)", "velY (m/s)"]]
        salida_csv = os.path.join(carpeta_vel_filtrado, f"{nombre_base} Filtrado.csv")
        df_export.to_csv(salida_csv, index = False)

        print(f"Generado: {salida_csv}")

    except Exception as e:
        print(f"Error suavizando el archivo: {archivo_csv}: {e}")
        continue

#Crear carpetas para la aceleracion
carpeta_aceleracion = os.path.join(carpeta_resultados, "Aceleracion Cartesiana")
carpeta_ace_sin_filtrar = os.path.join(carpeta_aceleracion, "Sin Filtrar")
carpeta_ace_filtrado = os.path.join(carpeta_aceleracion, "Filtrado")

os.makedirs(carpeta_ace_sin_filtrar, exist_ok=True)
os.makedirs(carpeta_ace_filtrado, exist_ok=True)

#Calcular aceleracion para todos los archivos de velocidad filtrados
for archivo_csv in os.listdir(carpeta_vel_filtrado):
    ruta_csv = os.path.join(carpeta_vel_filtrado, archivo_csv)
    nombre_base = os.path.splitext(archivo_csv)[0]
    try:
        # Leer archivo original
        df = pd.read_csv(ruta_csv)

        if df.empty:
            print(f"Archivo sin datos: {archivo_csv}")
            continue

        df_aux = pd.DataFrame({
            "Tiempo (s)": df["Tiempo (s)"]
        })

        # Calcular velocidades
        df_aux["aceX (m/s^2)"] = calculate_derivative(df["velX (m/s)"], df["Tiempo (s)"])
        df_aux["aceY (m/s^2)"] = calculate_derivative(df["velY (m/s)"], df["Tiempo (s)"])

        # Crear nuevo DataFrame para exportar
        df_export = df_aux[["Tiempo (s)", "aceX (m/s^2)", "aceY (m/s^2)"]]
        
        #Eliminar los NaN del dataframe
        df_export = df_export.bfill()

        # Guardar como nuevo archivo
        nombre_limpio = nombre_base.replace(" Filtrado", "").replace("V_", "A_")
        salida_csv = os.path.join(carpeta_ace_sin_filtrar, f"{nombre_limpio}.csv")
        df_export.to_csv(salida_csv, index=False)

        print(f"Generado: {salida_csv}")

    except Exception as e:
        print(f"Error procesando {archivo_csv}: {e}")
        continue

#Suavizar aceleracion
for archivo_csv in os.listdir(carpeta_ace_sin_filtrar):
    ruta_csv = os.path.join(carpeta_ace_sin_filtrar, archivo_csv)
    nombre_base = os.path.splitext(archivo_csv)[0]
    try:
        df = pd.read_csv(ruta_csv)
        if df.empty:
            print(f"Archivo sin datos: {archivo_csv}")
            continue
        
        df_aux = pd.DataFrame({
            "Tiempo (s)": df["Tiempo (s)"]
        })

        if len(df["aceX (m/s^2)"] >= window_size):
            df_aux["aceX (m/s^2)"] = savgol_filter(df["aceX (m/s^2)"], window_length=window_size, polyorder=order)

        if len(df["aceY (m/s^2)"] >= window_size):
            df_aux["aceY (m/s^2)"] = savgol_filter(df["aceY (m/s^2)"], window_length=window_size, polyorder=order)

        df_export = df_aux[["Tiempo (s)", "aceX (m/s^2)", "aceY (m/s^2)"]]
        salida_csv = os.path.join(carpeta_ace_filtrado, f"{nombre_base} Filtrado.csv")
        df_export.to_csv(salida_csv, index = False)

        print(f"Generado: {salida_csv}")

    except Exception as e:
        print(f"Error suavizando el archivo: {archivo_csv}: {e}")
        continue

#-----------------------------------------------------------
#    Calcular aceleracion en intrinsicas
#-----------------------------------------------------------

carpeta_intrinsicas = os.path.join(carpeta_resultados, "Aceleracion Intrinsica")
carpeta_int_sin_filtrar = os.path.join(carpeta_intrinsicas, "Sin Filtrar")
carpeta_int_filtrado = os.path.join(carpeta_intrinsicas, "Filtrado")

os.makedirs(carpeta_int_filtrado, exist_ok=True)
os.makedirs(carpeta_int_sin_filtrar, exist_ok=True)

for archivo_ace in os.listdir(carpeta_ace_filtrado):
    #Calcular la aceleración normal
    
    archivo_vel = archivo_ace.replace("A_", "V_")

    ruta_ace = os.path.join(carpeta_ace_filtrado, archivo_ace)
    ruta_vel = os.path.join(carpeta_vel_filtrado, archivo_vel)
    
    df_acel = pd.read_csv(ruta_ace)
    df_vel = pd.read_csv(ruta_vel)

    v_mod = np.sqrt(df_vel["velX (m/s)"]**2 + df_vel["velY (m/s)"]**2)

    prod_cruz = df_vel["velX (m/s)"] * df_acel["aceY (m/s^2)"] - df_vel["velY (m/s)"] * df_acel["aceX (m/s^2)"]

    a_normal = np.where(v_mod > 0, np.abs(prod_cruz) / v_mod, 0)

    #Calcular la aceleracion tangencial

    a_tangencial = calculate_derivative(v_mod, df_vel["Tiempo (s)"])

    df_export = pd.DataFrame({
        "Tiempo (s)": df_vel["Tiempo (s)"],
        "Aceleracion Normal (m/s^2)": a_normal,
        "Aceleracion Tangencial (m/s^2)": a_tangencial
    })
    
    df_export = df_export.bfill()

    nombre_limpio = os.path.splitext(archivo_ace)[0].replace(" Filtrado", "").replace("A_", "AI_")
    salida_csv = os.path.join(carpeta_int_sin_filtrar, f"{nombre_limpio}.csv")
    df_export.to_csv(salida_csv, index = False)

    print(f"Generado: {salida_csv}")

#Suavizar aceleracion intrisica
for archivo_csv in os.listdir(carpeta_int_sin_filtrar):
    ruta_csv = os.path.join(carpeta_int_sin_filtrar, archivo_csv)
    nombre_base = os.path.splitext(archivo_csv)[0]
    try:
        df = pd.read_csv(ruta_csv)
        if df.empty:
            print(f"Archivo sin datos: {archivo_csv}")
            continue

        df_aux = pd.DataFrame({
            "Tiempo (s)": df["Tiempo (s)"]
        })
        
        if len(df["Aceleracion Normal (m/s^2)"] >= window_size):
            df_aux["Aceleracion Normal (m/s^2)"] = savgol_filter(df["Aceleracion Normal (m/s^2)"], window_length=window_size, polyorder=order)

        if len(df["Aceleracion Tangencial (m/s^2)"] >= window_size):
            df_aux["Aceleracion Tangencial (m/s^2)"] = savgol_filter(df["Aceleracion Tangencial (m/s^2)"], window_length=window_size, polyorder=order)

        df_export = df_aux[["Tiempo (s)", "Aceleracion Normal (m/s^2)", "Aceleracion Tangencial (m/s^2)"]]
        salida_csv = os.path.join(carpeta_int_filtrado, f"{nombre_base} Filtrado.csv")
        df_export.to_csv(salida_csv, index = False)

        print(f"Generado: {salida_csv}")

    except Exception as e:
        print(f"Error suavizando el archivo: {archivo_csv}: {e}")
        continue