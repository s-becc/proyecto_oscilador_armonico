import subprocess
import sys
import os

def run_script(script_name):
    try:
        print(f"Ejecutando {script_name}...")
        result = subprocess.run([sys.executable, script_name], check=True, cwd=os.path.dirname(__file__))
        print(f"{script_name} completado exitosamente.")
    except subprocess.CalledProcessError as e:
        print(f"Error al ejecutar {script_name}: {e}")
        sys.exit(1)

if __name__ == "__main__":
    scripts = [
        "ProcesarVideos.py",
        "ProcesarDatos.py",
        #"Graficador.py",
        "Graficador2.py",
        "GenerarIndex.py"
    ]

    print("Iniciando pipeline de procesamiento...")
    
    for script in scripts:
        run_script(script)
    
    print("Pipeline completado.")
