# ============================================================
#  INTERFAZ GRÁFICA (Tkinter)
#  Contiene la clase SimuladorSO que crea la ventana.
# ============================================================

import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import statistics

from datos_ejemplo import DATOS_EJERCICIOS
from algoritmos import fcfs, sjf, srtf, rr, prioridades
from grafico import dibujar_gantt

class SimuladorSO:
    def __init__(self, root):
        self.root = root
        self.root.title("Simulador de Planificación de Procesos - SO")
        self.root.geometry("1100x900")

        self.procesos = []
        self.canvas = None
        self.paso_actual = -1  # Para la simulación paso a paso
        self.retardo = 800     # Retardo por defecto (Normal)

        self.crear_interfaz()

    # --------------------------------------------------------
    #  CREAR TODOS LOS WIDGETS
    # --------------------------------------------------------
    def crear_interfaz(self):
        # --- Carga rápida del PDF ---
        frame_carga = tk.LabelFrame(self.root, text="Cargar datos de ejemplo (PDF)", padx=5, pady=5)
        frame_carga.pack(fill="x", padx=10, pady=5)

        tk.Label(frame_carga, text="Ejercicio:").pack(side="left", padx=5)
        self.combo_ejercicio = ttk.Combobox(frame_carga,
                                            values=list(DATOS_EJERCICIOS.keys()),
                                            state="readonly", width=15)
        self.combo_ejercicio.pack(side="left", padx=5)
        self.combo_ejercicio.current(0)
        tk.Button(frame_carga, text="Cargar", command=self.cargar_ejercicio,
                  bg="#3498DB", fg="white").pack(side="left", padx=5)

        # --- Entrada manual ---
        frame_input = tk.LabelFrame(self.root, text="Registrar Proceso (Manual)", padx=5, pady=5)
        frame_input.pack(fill="x", padx=10, pady=5)

        tk.Label(frame_input, text="Nombre:").grid(row=0, column=0, padx=2)
        self.entry_nombre = tk.Entry(frame_input, width=8)
        self.entry_nombre.grid(row=0, column=1, padx=2)

        tk.Label(frame_input, text="Llegada:").grid(row=0, column=2, padx=2)
        self.entry_llegada = tk.Entry(frame_input, width=5)
        self.entry_llegada.grid(row=0, column=3, padx=2)

        tk.Label(frame_input, text="Ejecución:").grid(row=0, column=4, padx=2)
        self.entry_ejecucion = tk.Entry(frame_input, width=5)
        self.entry_ejecucion.grid(row=0, column=5, padx=2)

        tk.Label(frame_input, text="Prioridad:").grid(row=0, column=6, padx=2)
        self.entry_prioridad = tk.Entry(frame_input, width=5)
        self.entry_prioridad.grid(row=0, column=7, padx=2)

        tk.Button(frame_input, text="Agregar", command=self.agregar_proceso,
                  bg="#2ECC71", fg="white").grid(row=0, column=8, padx=5)
        tk.Button(frame_input, text="Limpiar Todo", command=self.limpiar_todo,
                  bg="#E74C3C", fg="white").grid(row=0, column=9, padx=5)
        tk.Button(frame_input, text="Importar TXT", command=self.importar_txt,
                  bg="#F39C12", fg="white").grid(row=0, column=10, padx=5)

        # --- Tabla de procesos ---
        frame_tabla = tk.LabelFrame(self.root, text="Procesos Registrados", padx=5, pady=5)
        frame_tabla.pack(fill="x", padx=10, pady=5)

        self.tabla = ttk.Treeview(frame_tabla,
                                  columns=("Nombre", "Llegada", "Ejecución", "Prioridad"),
                                  show="headings", height=5)
        for col in ("Nombre", "Llegada", "Ejecución", "Prioridad"):
            self.tabla.heading(col, text=col)
            self.tabla.column(col, width=100)
        self.tabla.pack(fill="x")

        self.label_contador = tk.Label(frame_tabla, text="Total de procesos: 0", font=("Arial", 10, "bold"))
        self.label_contador.pack(anchor="e", padx=5)

        # --- Simulación ---
        frame_sim = tk.LabelFrame(self.root, text="Simulación", padx=5, pady=5)
        frame_sim.pack(fill="x", padx=10, pady=5)

        tk.Label(frame_sim, text="Política:").grid(row=0, column=0, padx=5)
        self.combo_politica = ttk.Combobox(frame_sim,
                                           values=["FCFS", "SJF", "SRTF", "RR", "Prioridades"],
                                           state="readonly", width=12)
        self.combo_politica.grid(row=0, column=1, padx=5)
        self.combo_politica.current(0)
        self.combo_politica.bind("<<ComboboxSelected>>", self.actualizar_quantum)

        tk.Label(frame_sim, text="Quantum:").grid(row=0, column=2, padx=5)
        self.entry_quantum = tk.Entry(frame_sim, width=5)
        self.entry_quantum.grid(row=0, column=3, padx=5)
        self.entry_quantum.insert(0, "2")
        self.entry_quantum.config(state="disabled")

        tk.Button(frame_sim, text="SIMULAR", command=self.simular,
                  bg="#F1E60F", fg="black", font=("Arial", 10, "bold")).grid(row=0, column=4, padx=15)
        tk.Button(frame_sim, text="PASO A PASO", command=self.simular_paso_a_paso,
                  bg="#9B59B6", fg="white", font=("Arial", 10, "bold")).grid(row=0, column=5, padx=15)

        # --- Selector de velocidad ---
        tk.Label(frame_sim, text="Velocidad:").grid(row=0, column=6, padx=5)
        self.combo_velocidad = ttk.Combobox(frame_sim,
                                            values=["Lento (1.5s)", "Normal (0.8s)",
                                                    "Rápido (0.4s)", "Muy rápido (0.1s)"],
                                            state="readonly", width=15)
        self.combo_velocidad.grid(row=0, column=7, padx=5)
        self.combo_velocidad.current(1)  # Normal por defecto

        # --- Resultados ---
        frame_resultados = tk.LabelFrame(self.root, text="Resultados / Estado Actual", padx=5, pady=5)
        frame_resultados.pack(fill="both", expand=True, padx=10, pady=5)

        self.texto_resultados = tk.Text(frame_resultados, height=6, font=("Courier", 10))
        self.texto_resultados.pack(fill="both", expand=True)

        # --- Cola de Espera ---
        frame_cola = tk.LabelFrame(self.root, text="Cola de Espera", padx=5, pady=5)
        frame_cola.pack(fill="x", padx=10, pady=5)

        self.texto_cola = tk.Text(frame_cola, height=8, font=("Courier", 10), bg="#F0F0F0")
        self.texto_cola.pack(fill="x")

        # --- Frame para el Gantt ---
        self.frame_grafico = tk.Frame(self.root)
        self.frame_grafico.pack(fill="both", expand=True, padx=10, pady=5)

    # --------------------------------------------------------
    #  FUNCIONES DE LA INTERFAZ
    # --------------------------------------------------------
    def actualizar_contador(self):
        """Actualiza el label que muestra el total de procesos."""
        total = len(self.procesos)
        self.label_contador.config(text=f"Total de procesos: {total}")

    def actualizar_quantum(self, event):
        """Activa el campo quantum solo si la política es RR."""
        if self.combo_politica.get() == "RR":
            self.entry_quantum.config(state="normal")
        else:
            self.entry_quantum.config(state="disabled")

    def cargar_ejercicio(self):
        """Carga los datos del PDF seleccionado."""
        self.limpiar_todo()
        for p in DATOS_EJERCICIOS[self.combo_ejercicio.get()]:
            self.procesos.append(p)
            self.tabla.insert("", "end", values=(p["nombre"], p["llegada"], p["ejecucion"], p["prioridad"]))
        self.actualizar_contador()

    def agregar_proceso(self):
        """Agrega un proceso ingresado manualmente."""
        nombre = self.entry_nombre.get().strip()
        try:
            llegada = int(self.entry_llegada.get())
            ejecucion = int(self.entry_ejecucion.get())
            prioridad = int(self.entry_prioridad.get()) if self.entry_prioridad.get() else 0
        except ValueError:
            messagebox.showerror("Error", "Ingrese valores numéricos válidos")
            return
        if not nombre:
            messagebox.showerror("Error", "Ingrese un nombre")
            return
        p = {"nombre": nombre, "llegada": llegada, "ejecucion": ejecucion, "prioridad": prioridad}
        self.procesos.append(p)
        self.tabla.insert("", "end", values=(nombre, llegada, ejecucion, prioridad))
        self.actualizar_contador()
        self.entry_nombre.delete(0, tk.END)
        self.entry_llegada.delete(0, tk.END)
        self.entry_ejecucion.delete(0, tk.END)
        self.entry_prioridad.delete(0, tk.END)

    def importar_txt(self):
        """Abre un archivo TXT y carga los procesos desde ahí."""
        archivo = filedialog.askopenfilename(
            title="Seleccionar archivo de procesos",
            filetypes=[("Archivos de texto", "*.txt"), ("Todos los archivos", "*.*")]
        )
        if not archivo:
            return
        try:
            with open(archivo, "r", encoding="utf-8") as f:
                for linea in f:
                    partes = linea.strip().split(",")
                    if len(partes) == 4:
                        nombre = partes[0].strip()
                        llegada = int(partes[1].strip())
                        ejecucion = int(partes[2].strip())
                        prioridad = int(partes[3].strip())
                        p = {"nombre": nombre, "llegada": llegada,
                             "ejecucion": ejecucion, "prioridad": prioridad}
                        self.procesos.append(p)
                        self.tabla.insert("", "end", values=(nombre, llegada, ejecucion, prioridad))
            self.actualizar_contador()
            messagebox.showinfo("Éxito", "Procesos importados correctamente.")
        except Exception as e:
            messagebox.showerror("Error", f"No se pudo leer el archivo:\n{e}")

    def limpiar_todo(self):
        """Borra todos los procesos y resultados."""
        self.procesos = []
        self.paso_actual = -1  # Detener la animación
        for i in self.tabla.get_children():
            self.tabla.delete(i)
        self.texto_resultados.delete(1.0, tk.END)
        self.texto_cola.delete(1.0, tk.END)
        if self.canvas:
            self.canvas.get_tk_widget().destroy()
            self.canvas = None
        self.actualizar_contador()

    def simular(self):
        """Ejecuta la política seleccionada (resultado final de golpe)."""
        if not self.procesos:
            messagebox.showwarning("Advertencia", "No hay procesos registrados")
            return

        self.paso_actual = -1  # Detener cualquier animación previa
        politica = self.combo_politica.get()
        try:
            if politica == "FCFS":
                res, gantt, registro_cola = fcfs(self.procesos)
            elif politica == "SJF":
                res, gantt, registro_cola = sjf(self.procesos)
            elif politica == "SRTF":
                res, gantt, registro_cola = srtf(self.procesos)
            elif politica == "RR":
                q = int(self.entry_quantum.get())
                res, gantt, registro_cola = rr(self.procesos, q)
            elif politica == "Prioridades":
                res, gantt, registro_cola = prioridades(self.procesos)
            else:
                return
        except Exception as e:
            messagebox.showerror("Error", f"Error en la simulación: {e}")
            return

        self.mostrar_resultados(res, politica)
        self.canvas = dibujar_gantt(gantt, self.frame_grafico, self.canvas)
        self.mostrar_cola(registro_cola)

    def simular_paso_a_paso(self):
        """Ejecuta la simulación paso a paso (animada)."""
        if not self.procesos:
            messagebox.showwarning("Advertencia", "No hay procesos registrados")
            return

        politica = self.combo_politica.get()
        try:
            if politica == "FCFS":
                res, gantt, registro_cola = fcfs(self.procesos)
            elif politica == "SJF":
                res, gantt, registro_cola = sjf(self.procesos)
            elif politica == "SRTF":
                res, gantt, registro_cola = srtf(self.procesos)
            elif politica == "RR":
                q = int(self.entry_quantum.get())
                res, gantt, registro_cola = rr(self.procesos, q)
            elif politica == "Prioridades":
                res, gantt, registro_cola = prioridades(self.procesos)
            else:
                return
        except Exception as e:
            messagebox.showerror("Error", f"Error en la simulación: {e}")
            return

        # Guardar los datos para la animación
        self.gantt_completo = gantt
        self.registro_cola_completo = registro_cola
        self.resultados_completos = res
        self.politica_actual = politica
        self.paso_actual = 0

        # Leer la velocidad seleccionada
        velocidad = self.combo_velocidad.get()
        if "1.5s" in velocidad:
            self.retardo = 1500
        elif "0.8s" in velocidad:
            self.retardo = 800
        elif "0.4s" in velocidad:
            self.retardo = 400
        else:
            self.retardo = 100

        # Limpiar la interfaz
        self.texto_resultados.delete(1.0, tk.END)
        self.texto_cola.delete(1.0, tk.END)
        if self.canvas:
            self.canvas.get_tk_widget().destroy()
            self.canvas = None

        # Iniciar la animación
        self.animar_paso()

    def animar_paso(self):
        """Muestra un paso de la simulación y programa el siguiente."""
        if self.paso_actual < 0:
            return

        if self.paso_actual >= len(self.registro_cola_completo):
            # Terminar la animación y mostrar los resultados finales
            self.mostrar_resultados(self.resultados_completos, self.politica_actual)
            self.canvas = dibujar_gantt(self.gantt_completo, self.frame_grafico, self.canvas)
            return

        # Obtener el estado actual
        instante, en_cpu, cola = self.registro_cola_completo[self.paso_actual]

        # Mostrar el estado actual en el panel de resultados
        self.texto_resultados.delete(1.0, tk.END)
        texto = f"=== SIMULACIÓN PASO A PASO ===\n"
        texto += f"Política: {self.politica_actual}\n"
        texto += f"Instante actual: t = {instante}\n"
        texto += f"Proceso en CPU: {en_cpu}\n"
        texto += f"Paso: {self.paso_actual + 1} de {len(self.registro_cola_completo)}\n"
        self.texto_resultados.insert(tk.END, texto)

        # --- MOSTRAR LA COLA DE ESPERA PASO A PASO ---
        self.texto_cola.delete(1.0, tk.END)
        cola_texto = "Instante | CPU ejecutando | Cola de espera\n"
        cola_texto += "-" * 55 + "\n"
        for i in range(self.paso_actual + 1):
            t, cpu, c = self.registro_cola_completo[i]
            cola_str = "[" + ", ".join(c) + "]" if c else "[vacía]"
            cola_texto += f"   t={t:<3} | {cpu:<13} | {cola_str}\n"
        self.texto_cola.insert(tk.END, cola_texto)

        # AUTO-SCROLL: desplazar automáticamente hacia abajo
        self.texto_cola.see(tk.END)

        # Dibujar el Gantt parcial
        gantt_parcial = self.gantt_completo[:self.paso_actual + 1]
        self.canvas = dibujar_gantt(gantt_parcial, self.frame_grafico, self.canvas)

        # Programar el siguiente paso con la velocidad elegida
        self.paso_actual += 1
        self.root.after(self.retardo, self.animar_paso)

    def mostrar_resultados(self, resultados, politica):
        """Muestra la tabla de resultados y las métricas globales."""
        self.texto_resultados.delete(1.0, tk.END)
        texto = f"POLÍTICA: {politica}\n"
        texto += f"{'Proceso':<10} {'Llegada':<10} {'Ejecución':<10} {'TF':<8} {'TR':<8} {'TE':<8}\n"
        texto += "-" * 65 + "\n"

        sum_tr = 0
        sum_te = 0
        lista_te = []
        for r in resultados:
            texto += f"{r['nombre']:<10} {r['llegada']:<10} {r['ejecucion']:<10} {r['tf']:<8} {r['tr']:<8} {r['te']:<8}\n"
            sum_tr += r["tr"]
            sum_te += r["te"]
            lista_te.append(r["te"])

        n = len(resultados)
        texto += "-" * 65 + "\n"
        texto += f"Tiempo de Retorno Medio: {sum_tr/n:.2f}\n"
        texto += f"Tiempo de Espera Medio:  {sum_te/n:.2f}\n"
        if n > 1:
            texto += f"Varianza del Tiempo de Espera: {statistics.variance(lista_te):.2f}\n"

        # --- MÉTRICAS GLOBALES ---
        tiempo_total = max(r["tf"] for r in resultados)
        tiempo_ocupado = sum(r["ejecucion"] for r in resultados)
        uso_cpu = (tiempo_ocupado / tiempo_total) * 100 if tiempo_total > 0 else 0
        throughput = n / tiempo_total if tiempo_total > 0 else 0

        texto += "-" * 65 + "\n"
        texto += f"--- MÉTRICAS GLOBALES ---\n"
        texto += f"Total de procesos:          {n}\n"
        texto += f"Tiempo total de simulación: {tiempo_total}\n"
        texto += f"Tiempo de CPU ocupado:      {tiempo_ocupado}\n"
        texto += f"Tiempo de CPU inactivo:     {tiempo_total - tiempo_ocupado}\n"
        texto += f"Uso de CPU:                 {uso_cpu:.2f}%\n"
        texto += f"Throughput:                 {throughput:.4f} procesos/unidad\n"

        self.texto_resultados.insert(tk.END, texto)

    def mostrar_cola(self, registro_cola):
        """Muestra el registro completo de la cola de espera."""
        self.texto_cola.delete(1.0, tk.END)
        texto = "Instante | CPU ejecutando | Cola de espera\n"
        texto += "-" * 55 + "\n"
        for instante, en_cpu, cola in registro_cola:
            cola_str = "[" + ", ".join(cola) + "]" if cola else "[vacía]"
            texto += f"   t={instante:<3} | {en_cpu:<13} | {cola_str}\n"
        self.texto_cola.insert(tk.END, texto)