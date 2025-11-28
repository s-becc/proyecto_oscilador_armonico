import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import pandas as pd
import os
import glob
import shutil
from GenerarIndex import generar_index

# Obtener la ruta del script actual
dir = os.path.dirname(__file__)

# Subir al directorio raíz del repositorio
carpeta_csv = os.path.join(dir, "Resultados")

# Archivos
files = glob.glob(carpeta_csv + "/**/*.csv", recursive=True)

videos = os.path.join(dir, "Videos")

print(videos)

for video in os.listdir(videos):
    nombre = os.path.splitext(video)[0]
    figX = make_subplots(
        rows = 3,
        cols = 1,
        subplot_titles = ("Posicion X (m)", "Velocidad X (m/s)", "Aceleracion X (m/s^2)"),
        shared_xaxes = True
    )

    figY = make_subplots(
        rows = 3,
        cols = 1,
        subplot_titles = ("Posicion Y (m)", "Velocidad Y (m/s)", "Aceleracion Y (m/s^2)"),
        shared_xaxes = True
    )

    figFuerzas = make_subplots(
        rows = 2,
        cols = 1,
        subplot_titles= ("Fuerzas X", "Fuerzas Y"),
        shared_xaxes= True
    )

    figEnergiaTrabajo = make_subplots(
        rows = 2,
        cols = 1,
        subplot_titles = ("Energia", "Trabajo"),
        shared_xaxes= True
    )

    for file in files:
        if nombre in file:
            if "Sin Filtrar" in file:
                if "Posicion Cartesiana" in file:
                    # Posicion Sin Filtrar de cada video
                    df = pd.read_csv(file)
                    tiempo = df.iloc[:,0]
                    posX = df.iloc[:,1]
                    posY = df.iloc[:,2]

                    figX.add_trace(go.Scatter(
                        x = tiempo,
                        y = posX,
                        mode = 'markers',
                        name = 'Posicion Sin Filtrar'
                    ), row = 1, col = 1)

                    figY.add_trace(go.Scatter(
                        x = tiempo,
                        y = posY,
                        mode = 'markers',
                        name = 'Posicion Sin Filtrar'
                    ), row = 1, col = 1)
                elif "Velocidad Cartesiana" in file:
                    # Velocidad Sin Filtrar de cada video
                    df = pd.read_csv(file)
                    tiempo = df.iloc[:, 0]
                    posX = df.iloc[:, 1]
                    posY = df.iloc[:, 2]

                    figX.add_trace(go.Scatter(
                        x = tiempo,
                        y = posX,
                        mode = 'markers',
                        name = 'Velocidad Sin Filtrar'
                    ), row = 2, col = 1)
                    
                    figY.add_trace(go.Scatter(
                        x = tiempo,
                        y = posY,
                        mode = 'markers',
                        name = 'Aceleracion Sin Filtrar'
                    ), row = 2, col = 1)
                elif "Aceleracion Cartesiana" in file:
                    # Aceleracion Sin Filtrar de cada video
                    df = pd.read_csv(file)
                    tiempo = df.iloc[:, 0]
                    posX = df.iloc[:, 1]
                    posY = df.iloc[:, 2]

                    figX.add_trace(go.Scatter(
                        x = tiempo,
                        y = posX,
                        mode = 'markers',
                        name = 'Posicion Sin Filtrar'
                    ), row = 3, col = 1)
                    
                    figY.add_trace(go.Scatter(
                        x = tiempo,
                        y = posY,
                        mode = 'markers',
                        name = 'Posicion Sin Filtrar'
                    ), row = 3, col = 1)
            elif "Filtrado" in file:
                if "Posicion Cartesiana" in file:
                    # Posicion Filtrada de cada video
                    df = pd.read_csv(file)
                    tiempo = df.iloc[:, 0]
                    posX = df.iloc[:, 1]
                    posY = df.iloc[:, 2]

                    figX.add_trace(go.Scatter(
                        x = tiempo,
                        y = posX,
                        mode = 'lines',
                        name = 'Posicion Filtrada'
                    ), row = 1, col = 1)

                    figY.add_trace(go.Scatter(
                        x = tiempo,
                        y = posY,
                        mode = 'lines',
                        name = 'Posicion Filtrada'
                    ), row = 1, col = 1)
                elif "Velocidad Cartesiana" in file:
                    # Velocidad Filtrada de cada video
                    df = pd.read_csv(file)
                    tiempo = df.iloc[:, 0]
                    posX = df.iloc[:, 1]
                    posY = df.iloc[:, 2]

                    figX.add_trace(go.Scatter(
                        x = tiempo,
                        y = posX,
                        mode = 'lines',
                        name = 'Velocidad Filtrada'
                    ), row = 2, col = 1)
                    
                    figY.add_trace(go.Scatter(
                        x = tiempo,
                        y = posY,
                        mode = 'lines',
                        name = 'Aceleracion Filtrada'
                    ), row = 2, col = 1)

                elif "Aceleracion Cartesiana" in file:
                    # Aceleracion Filtrada de cada video
                    df = pd.read_csv(file)
                    tiempo = df.iloc[:, 0]
                    posX = df.iloc[:, 1]
                    posY = df.iloc[:, 2]

                    figX.add_trace(go.Scatter(
                        x = tiempo,
                        y = posX,
                        mode = 'lines',
                        name = 'Aceleracion Filtrada'
                    ), row = 3, col = 1)
                    
                    figY.add_trace(go.Scatter(
                        x = tiempo,
                        y = posY,
                        mode = 'lines',
                        name = 'Aceleracion Filtrada'
                    ), row = 3, col = 1)
                elif "Fuerzas" in file:
                    df = pd.read_csv(file)
                    tiempo = df.iloc[:, 0]

                    # Datos para Ejes
                    FuerzaX = df["FuerzaX (N)"]
                    FuerzaElastica = df["FuerzaElastica (N)"]
                    FuerzaRozamiento = df["FuerzaRozamiento (N)"]
                    FuerzaY = df["FuerzaY (N)"]
                    FuerzaNormal = df["FuerzaNormal (N)"]

                    # --- FILA 1: FUERZAS EN EJE X (OVERLAY) ---

                    # 1. Fuerza Resultante X (Resalta la resultante)
                    figFuerzas.add_trace(go.Scatter(
                        x = tiempo,
                        y = FuerzaX,
                        mode = 'lines',
                        name = 'Fuerza X',
                        line = dict(color='darkred', width=3) # Línea más gruesa
                    ), row = 1, col = 1)

                    # 2. Fuerza Elástica
                    figFuerzas.add_trace(go.Scatter(
                        x = tiempo,
                        y = FuerzaElastica,
                        mode = 'lines',
                        name = 'F. Elástica'
                    ), row = 1, col = 1)

                    # 3. Fuerza de Fricción (Rozamiento)
                    figFuerzas.add_trace(go.Scatter(
                        x = tiempo,
                        y = FuerzaRozamiento,
                        mode = 'lines',
                        name = 'F. Rozamiento'
                    ), row = 1, col = 1)

                    # --- FILA 2: FUERZAS EN EJE Y (OVERLAY) ---

                    # 4. Fuerza Resultante Y (Resalta la resultante)
                    figFuerzas.add_trace(go.Scatter(
                        x = tiempo,
                        y = FuerzaY,
                        mode = 'lines',
                        name = 'Fuerza Y',
                        line = dict(color='darkblue', width=3)
                    ), row = 2, col = 1)

                    # 5. Fuerza Normal (constante)
                    figFuerzas.add_trace(go.Scatter(
                        x = tiempo,
                        y = FuerzaNormal,
                        mode = 'lines',
                        name = 'F. Normal',
                        line = dict(dash='dot')
                    ), row = 2, col = 1)
                elif "Trabajo y energia" in file:
                    if "E_" in file:
                        # Archivo de energia
                        df = pd.read_csv(file)
                        tiempo = df.iloc[:, 0]

                        # Datos para Ejes
                        ECinetica = df["Energia Cinetica (J)"]
                        EPE = df["Energia Potencial Elastica (J)"]
                        EM = df["Energia Mecanica Total (J)"]
                        dK = df["Delta K (J)"]

                        figEnergiaTrabajo.add_trace(go.Scatter(
                            x = tiempo,
                            y = ECinetica,
                            mode = 'lines',
                            name = 'Energica Cinetica'
                        ), row = 1, col = 1)

                        figEnergiaTrabajo.add_trace(go.Scatter(
                            x = tiempo,
                            y = EPE,
                            mode = 'lines',
                            name = 'Energica Potencial Elastica'
                        ), row = 1, col = 1)

                        figEnergiaTrabajo.add_trace(go.Scatter(
                            x = tiempo,
                            y = EM,
                            mode = 'lines',
                            name = 'Energica Mecanica'
                        ), row = 1, col = 1)

                    
                    elif "T_" in file:
                        df = pd.read_csv(file)
                        tiempo = df.iloc[:, 0]

                        # Datos para Ejes
                        TrabajoNeto = df["Trabajo Neto (J)"]
                        TrabajoElastico = df["Trabajo Elastico (J)"]
                        TrabajoRozamiento = df["Trabajo Rozamiento (J)"]

                        figEnergiaTrabajo.add_trace(go.Scatter(
                            x = tiempo,
                            y = TrabajoNeto,
                            mode = 'lines',
                            name = 'Trabajo Neto Acumulado'
                        ), row = 2, col = 1)

                        figEnergiaTrabajo.add_trace(go.Scatter(
                            x = tiempo,
                            y = TrabajoElastico,
                            mode = 'lines',
                            name = 'Trabajo Elastico Acumulado'
                        ), row = 2, col = 1)

                        figEnergiaTrabajo.add_trace(go.Scatter(
                            x = tiempo,
                            y = TrabajoRozamiento,
                            mode = 'lines',
                            name = 'Trabajo Rozamiento Acumulado'
                        ), row = 2, col = 1)

    carpeta_graficos = os.path.join(dir, "Resultados", "Graficos")
    os.makedirs(carpeta_graficos, exist_ok = True)
    ruta_salida = os.path.join(carpeta_graficos, f'{nombre}')
    figX.write_html(f"{ruta_salida}X.html")
    figX.write_image(f"{ruta_salida}X.png")
    figY.write_html(f"{ruta_salida}Y.html")
    figY.write_image(f"{ruta_salida}Y.png")
    figFuerzas.write_html(f"{ruta_salida}Fuerzas.html")
    figFuerzas.write_image(f"{ruta_salida}Fuerzas.png")
    figEnergiaTrabajo.write_html(f"{ruta_salida}EnergiaTrabajo.html")
    figEnergiaTrabajo.write_image(f"{ruta_salida}EnergiaTrabajo.png")

    