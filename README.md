# Proecyo Oscilador Armónico

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
