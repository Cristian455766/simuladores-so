# ============================================================
#  GRÁFICO DEL DIAGRAMA DE GANTT
#  Usa matplotlib para dibujar barras de colores.
# ============================================================

import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

# Lista de colores para los procesos
COLORES = ['#4ECDC4', '#9B59B6', '#A0522D', '#D4A017', '#7F8C8D',
           '#E74C3C', '#3498DB', '#2ECC71', '#F39C12', '#1ABC9C']

def dibujar_gantt(gantt, frame_contenedor, canvas_actual):
    """
    Dibuja el Gantt dentro del frame de Tkinter.
    - gantt: lista de tuplas (nombre, inicio, fin)
    - frame_contenedor: el frame donde se va a poner el gráfico
    - canvas_actual: el canvas anterior (para borrarlo antes de dibujar)
    Devuelve el nuevo canvas.
    """
    # Si ya había un gráfico, lo borramos
    if canvas_actual:
        canvas_actual.get_tk_widget().destroy()

    if not gantt:
        return None

    # Crear la figura
    fig, ax = plt.subplots(figsize=(10, 3))

    # Obtener nombres únicos y asignarles un color
    nombres = list(dict.fromkeys([g[0] for g in gantt]))
    colores_dict = {nombre: COLORES[i % len(COLORES)] for i, nombre in enumerate(nombres)}

    # Dibujar cada bloque como una barra horizontal
    for nombre, inicio, fin in gantt:
        ax.barh(nombre, fin - inicio, left=inicio,
                color=colores_dict[nombre], edgecolor='black', height=0.5)

    # Invertir el eje Y para que los procesos se vean de arriba hacia abajo
    ax.invert_yaxis()
    
    # Configuración del gráfico
    ax.set_xlabel("Tiempo")
    ax.set_ylabel("Proceso")
    ax.set_title("Diagrama de Gantt")
    ax.grid(axis='x', linestyle='--', alpha=0.7)
    

    # Ajustar los límites del eje X
    max_t = max([g[2] for g in gantt]) + 1
    ax.set_xlim(0, max_t)
    ax.set_xticks(range(0, max_t + 1, 1))

    plt.tight_layout()

    # Embeber el gráfico en la ventana
    canvas = FigureCanvasTkAgg(fig, master=frame_contenedor)
    canvas.draw()
    canvas.get_tk_widget().pack(fill="both", expand=True)
    return canvas