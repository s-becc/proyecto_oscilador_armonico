import os
import glob
import webbrowser
from collections import defaultdict

dir = os.path.dirname(__file__)

carpeta_csv = os.path.join(dir, "Resultados")
carpeta_recursos = os.path.join(dir, "Recursos")

def generar_index():
    html_files = glob.glob(os.path.join(carpeta_csv, "**/*.html"), recursive=True)
    html_files = [f for f in html_files if os.path.basename(f) != "index.html"]

    organized = defaultdict(list)
    for f in html_files:
        rel_path = os.path.relpath(f, carpeta_csv)
        parts = rel_path.split(os.sep)
        if len(parts) >= 3 and "html" in parts[1]:
            category = parts[0]
            sub = parts[1]
            file_name = parts[2]
            organized[(category, sub)].append((file_name, rel_path))

    content = ""
    categories = {
        "Aceleracion Cartesiana": ["Graficos aceX html", "Graficos aceY html"],
        "Aceleracion Intrinsica": ["Graficos Aceleracion Normal html", "Graficos Aceleracion Tangencial html"],
        "Posicion Cartesiana": ["Graficos PosX html", "Graficos PosY html"],
        "Velocidad Cartesiana": ["Graficos velX html", "Graficos velY html"]
    }

    for cat, subs in categories.items():
        content += f"<div class='category'>\n"
        content += f"<h2>{cat}</h2>\n"
        for sub in subs:
            content += f"<h3>{sub.replace(' html', '')}</h3>\n<ul>\n"
            if (cat, sub) in organized:
                for file_name, rel_path in sorted(organized[(cat, sub)]):
                    name = file_name.replace('.html', '')
                    content += f'<li><a href="{rel_path}">{name}</a></li>\n'
            content += "</ul>\n"
        content += "</div>\n"
    with open(os.path.join(carpeta_recursos, "index.template.html"), "r", encoding="utf-8") as f:
        template = f.read()

    html_final = template.replace("{{content}}", content)

    with open(os.path.join(carpeta_csv, "index.html"), "w", encoding="utf-8") as f:
        f.write(html_final)
    
    webbrowser.open("file://" + os.path.join(carpeta_csv, "index.html"))

if __name__ == "__main__":
    generar_index()