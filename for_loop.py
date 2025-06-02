import numpy as np
import matplotlib.pyplot as plt
import csv
import os
from matplotlib.collections import LineCollection

# Crear el archivo CSV si no existe
def crear_csv_hidrogeno(archivo):
    datos = [
        {'nivel_principal': 1, 'energia': -13.60, 'symbol': 'K'},
        {'nivel_principal': 2, 'energia': -3.40, 'symbol': 'L'},
        {'nivel_principal': 3, 'energia': -1.51, 'symbol': 'M'},
        {'nivel_principal': 4, 'energia': -0.85, 'symbol': 'N'},
        {'nivel_principal': 5, 'energia': -0.54, 'symbol': 'O'},
        {'nivel_principal': 6, 'energia': -0.38, 'symbol': 'P'},
        {'nivel_principal': 7, 'energia': -0.28, 'symbol': 'Q'}
    ]
    
    with open(archivo, 'w', newline='') as f:
        campos = ['nivel_principal', 'energia', 'symbol']
        writer = csv.DictWriter(f, fieldnames=campos)
        writer.writeheader()
        writer.writerows(datos)

# Leer niveles de energía desde CSV
def leer_niveles_energia(archivo_csv):
    niveles = {}
    with open(archivo_csv, 'r') as f:
        reader = csv.DictReader(f)
        for fila in reader:
            nivel = int(fila['nivel_principal'])
            energia = float(fila['energia'])
            niveles[nivel] = energia
    return niveles

# Calcular todas las transiciones posibles
def calcular_transiciones(niveles):
    transiciones = []
    for ni in niveles:
        for nf in niveles:
            if ni > nf:  # Solo transiciones a niveles inferiores
                delta_e = abs(niveles[nf] - niveles[ni])
                longitud_onda = 1240 / delta_e  # en nm (E = hc/λ)
                transiciones.append({
                    'inicial': ni,
                    'final': nf,
                    'energia_eV': round(delta_e, 2),
                    'longitud_onda_nm': round(longitud_onda, 1)
                })
    return transiciones

# Generar espectro de líneas
def generar_espectro(transiciones, archivo_salida):
    # Filtrar solo el rango visible
    visibles = [t for t in transiciones if 380 < t['longitud_onda_nm'] < 750]
    
    # Configurar gráfico
    fig, ax = plt.subplots(figsize=(12, 6))
    
    # Crear segmentos de líneas
    segmentos = []
    intensidades = []
    for t in visibles:
        wl = t['longitud_onda_nm']
        segmentos.append([(wl, 0), (wl, 1)])
        intensidades.append(t['energia_eV'])
    
    # Normalizar intensidades para colorear
    max_intensidad = max(intensidades)
    colores = plt.cm.plasma(np.array(intensidades)/max_intensidad)
    
    lc = LineCollection(segmentos, linewidths=2, colors=colores)
    ax.add_collection(lc)
    
    # Configurar ejes
    ax.set_xlim(380, 750)
    ax.set_ylim(0, 1.2)
    ax.set_title('Espectro Atómico del Hidrógeno', fontsize=14)
    ax.set_xlabel('Longitud de onda (nm)', fontsize=12)
    ax.set_ylabel('Intensidad relativa', fontsize=12)
    ax.grid(True, alpha=0.3)
    
    # Anotar transiciones importantes
    lineas_balmer = {
        656.3: r'H$\alpha$ (n=3→2)',
        486.1: r'H$\beta$ (n=4→2)',
        434.0: r'H$\gamma$ (n=5→2)',
        410.2: r'H$\delta$ (n=6→2)'
    }
    
    for wl, label in lineas_balmer.items():
        ax.text(wl, 1.05, label, ha='center', fontsize=9, rotation=90)
    
    # Añadir barra de color
    sm = plt.cm.ScalarMappable(cmap='plasma', 
                              norm=plt.Normalize(0, max_intensidad))
    sm.set_array([])
    cbar = plt.colorbar(sm, ax=ax)
    cbar.set_label('Energía (eV)', fontsize=10)
    
    plt.tight_layout()
    plt.savefig(archivo_salida, dpi=150)
    plt.show()
    
    return visibles

# Guardar transiciones en CSV
def guardar_transiciones(transiciones, archivo_salida):
    with open(archivo_salida, 'w', newline='') as f:
        campos = ['inicial', 'final', 'energia_eV', 'longitud_onda_nm']
        writer = csv.DictWriter(f, fieldnames=campos)
        writer.writeheader()
        writer.writerows(transiciones)

# Programa principal
if __name__ == "__main__":
    # Crear archivo CSV si no existe
    archivo_csv = 'niveles_hidrogeno.csv'
    if not os.path.exists(archivo_csv):
        crear_csv_hidrogeno(archivo_csv)
        print(f"Archivo {archivo_csv} creado exitosamente!")
    
    # 1. Leer datos desde CSV
    niveles = leer_niveles_energia(archivo_csv)
    print("Niveles de energía cargados:", niveles)
    
    # 2. Calcular transiciones
    transiciones = calcular_transiciones(niveles)
    print(f"Se calcularon {len(transiciones)} transiciones posibles")
    
    # 3. Generar espectro y obtener transiciones visibles
    transiciones_visibles = generar_espectro(transiciones, 'espectro_hidrogeno.png')
    
    # 4. Guardar resultados
    guardar_transiciones(transiciones_visibles, 'transiciones_visibles.csv')
    print("Resultados guardados en 'transiciones_visibles.csv'")
