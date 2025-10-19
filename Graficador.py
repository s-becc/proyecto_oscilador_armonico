import plotly.express as px
import plotly.graph_objects as go
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
files = glob.glob(carpeta_csv + "/**/* Filtrado.csv", recursive=True)

# Recorrer archivos CSV
for ruta_csv in files:
    print("Procesando:", ruta_csv)
    
    parent_dir = os.path.dirname(os.path.dirname(ruta_csv))
    nombre_archivo = os.path.basename(ruta_csv).replace(" Filtrado", "")
    nombre_base = nombre_archivo.replace(".csv", "")    
    
    print("  Leyendo datos...")
    dfFiltrado = pd.read_csv(ruta_csv)
    dfSinFiltrar = pd.read_csv(os.path.join(parent_dir, "Sin Filtrar", nombre_archivo))

    tiempo = dfFiltrado.columns[0]
    colx = dfFiltrado.columns[1]
    coly = dfFiltrado.columns[2]

    print(f"  Graficando {colx} y {coly}...")
    dfFiltrado[tiempo] = pd.to_numeric(dfFiltrado[tiempo], errors='coerce')
    dfSinFiltrar[tiempo] = pd.to_numeric(dfSinFiltrar[tiempo], errors='coerce')

    figx = px.line(dfFiltrado, x = tiempo, y = colx, title = f"{colx} en {nombre_base}(t)")
    figy = px.line(dfFiltrado, x = tiempo, y = coly, title = f"{coly} en {nombre_base}(t)")

    #Forzar eje X a comenzar en 0 si hay datos válidos
    if dfFiltrado[tiempo].notna().any():
        figx.update_layout(xaxis_range=[0, dfFiltrado[tiempo].max()])
        figy.update_layout(xaxis_range=[0, dfFiltrado[tiempo].max()])


    print("  Agregando datos sin filtrar...")
    figx.add_trace(go.Scatter(x = dfSinFiltrar[tiempo], y = dfSinFiltrar[colx], mode = 'markers', name = 'Sin filtrar'))
    figy.add_trace(go.Scatter(x = dfSinFiltrar[tiempo], y = dfSinFiltrar[coly], mode = 'markers', name = 'Sin filtrar'))


    nombre_x = f"Graficos {colx}".split(" (", 1)[0]
    nombre_y = f"Graficos {coly}".split(" (", 1)[0]
    
    dir_html = os.path.join(parent_dir, f"{nombre_x} html")
    dir_img = os.path.join(parent_dir, f"{nombre_x} png")

    print("  Guardando gráficos...")
    os.makedirs(dir_html, exist_ok=True)
    os.makedirs(dir_img, exist_ok=True)

    figx.write_html(os.path.join(dir_html, f"{nombre_base}.html"))
    figx.write_image(os.path.join(dir_img, f"{nombre_base}.png"))
    
    dir_html = os.path.join(parent_dir, f"{nombre_y} html")
    dir_img = os.path.join(parent_dir, f"{nombre_y} png")
    
    os.makedirs(dir_html, exist_ok=True)
    os.makedirs(dir_img, exist_ok=True)

    figy.write_html(os.path.join(dir_html, f"{nombre_base}.html"))
    figy.write_image(os.path.join(dir_img, f"{nombre_base}.png"))

    print("  Finalizado")