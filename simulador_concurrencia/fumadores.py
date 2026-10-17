# ============================================================
#  PROBLEMA: FUMADORES (CON PAUSA Y VELOCIDAD)
# ============================================================

import tkinter as tk
from tkinter import ttk
import threading
import time
import random

class Fumadores:
    def __init__(self, root):
        self.root = root
        self.root.title("Fumadores")
        self.root.geometry("1000x750")

        # --- Estado ---
        self.ejecutando = False
        self.pausado = False
        self.velocidad = 1.0  # 1.0 es normal, 0.5 es el doble de rápido, 2.0 es la mitad de rápido
        
        self.ingredientes = ["Tabaco", "Papel", "Fósforos"]
        self.fumador_tiene = [0, 1, 2]
        self.mesa = []
        self.estado_fumadores = ["esperando"] * 3
        self.lock = threading.Lock()

        self.semaforo_agente = threading.Semaphore(1)
        self.semaforo_fumadores = [threading.Semaphore(0) for _ in range(3)]

        self.crear_interfaz()

    def crear_interfaz(self):
        # --- Canvas principal ---
        frame_canvas = tk.LabelFrame(self.root, text="Mesa", padx=10, pady=10)
        frame_canvas.pack(fill="both", expand=True, padx=10, pady=10)

        self.canvas = tk.Canvas(frame_canvas, width=950, height=350, bg="#FDFEFE")
        self.canvas.pack()

        # --- Panel de estado ---
        frame_estado = tk.LabelFrame(self.root, text="Estado", padx=10, pady=5)
        frame_estado.pack(fill="x", padx=10, pady=5)

        self.label_agente = tk.Label(frame_estado, text="Agente: esperando...", font=("Arial", 11), fg="blue")
        self.label_agente.pack(anchor="w")

        self.label_fumadores = tk.Label(frame_estado, text="F1: esperando | F2: esperando | F3: esperando",
                                        font=("Arial", 11), fg="green")
        self.label_fumadores.pack(anchor="w")

        # --- Botones y Velocidad ---
        frame_botones = tk.Frame(self.root)
        frame_botones.pack(pady=10)

        self.btn_iniciar = tk.Button(frame_botones, text="INICIAR", command=self.iniciar,
                                     bg="#2ECC71", fg="white", font=("Arial", 11, "bold"), width=10)
        self.btn_iniciar.pack(side="left", padx=5)

        self.btn_pausar = tk.Button(frame_botones, text="PAUSAR", command=self.pausar,
                                    bg="#F1C40F", fg="black", font=("Arial", 11, "bold"), width=10, state="disabled")
        self.btn_pausar.pack(side="left", padx=5)

        self.btn_detener = tk.Button(frame_botones, text="DETENER", command=self.detener,
                                     bg="#E74C3C", fg="white", font=("Arial", 11, "bold"), width=10, state="disabled")
        self.btn_detener.pack(side="left", padx=5)

        # Control de velocidad
        tk.Label(frame_botones, text="Velocidad:", font=("Arial", 10)).pack(side="left", padx=(15, 5))
        self.combo_vel = ttk.Combobox(frame_botones, values=["Lento", "Normal", "Rápido"], state="readonly", width=10)
        self.combo_vel.current(1) # Normal por defecto
        self.combo_vel.pack(side="left")
        self.combo_vel.bind("<<ComboboxSelected>>", self.cambiar_velocidad)

        # --- Log ---
        frame_log = tk.LabelFrame(self.root, text="Registro de eventos", padx=5, pady=5)
        frame_log.pack(fill="both", expand=True, padx=10, pady=5)

        self.texto_log = tk.Text(frame_log, height=8, font=("Courier", 10))
        self.texto_log.pack(fill="both", expand=True)

    # --------------------------------------------------------
    #  FUNCIÓN DE ESPERA QUE RESPETA PAUSA Y VELOCIDAD
    # --------------------------------------------------------
    def esperar(self, segundos):
        """Duerme el hilo, pero se detiene si está pausado."""
        tiempo_inicio = time.time()
        while time.time() - tiempo_inicio < segundos * self.velocidad:
            if not self.ejecutando:
                break
            while self.pausado and self.ejecutando:
                time.sleep(0.1)
            time.sleep(0.05)

    def cambiar_velocidad(self, event):
        if self.combo_vel.get() == "Lento":
            self.velocidad = 2.0
        elif self.combo_vel.get() == "Rápido":
            self.velocidad = 0.5
        else:
            self.velocidad = 1.0

    # --------------------------------------------------------
    #  DIBUJAR
    # --------------------------------------------------------
    def dibujar_mesa(self):
        self.canvas.delete("all")
        for i in range(3):
            x = 150 + i * 300
            y = 250
            color = "#2ECC71" if self.estado_fumadores[i] == "fumando" else "#95A5A6"
            if self.estado_fumadores[i] == "armando":
                color = "#F1C40F"
            
            self.canvas.create_oval(x - 40, y - 40, x + 40, y + 40, fill=color, outline="black", width=2)
            self.canvas.create_text(x, y - 55, text=f"Fumador {i+1}", font=("Arial", 11, "bold"))
            ingr = self.ingredientes[self.fumador_tiene[i]]
            self.canvas.create_text(x, y + 55, text=f"Tiene: {ingr}", font=("Arial", 10))
            
            estado = self.estado_fumadores[i]
            if estado == "fumando":
                self.canvas.create_text(x, y, text="🚬", font=("Arial", 24))
                for j in range(3):
                    self.canvas.create_oval(x + 20 + j*10, y - 60 - j*15, x + 40 + j*10, y - 40 - j*15, outline="gray", width=1)
            elif estado == "armando":
                self.canvas.create_text(x, y, text="🔧", font=("Arial", 20))

        self.canvas.create_rectangle(300, 80, 650, 180, fill="#F9E79F", outline="black", width=3)
        self.canvas.create_text(475, 60, text="Mesa del Agente", font=("Arial", 12, "bold"))

        if not self.mesa:
            self.canvas.create_text(475, 130, text="(mesa vacía)", font=("Arial", 12), fill="gray")
        else:
            for j, ingr in enumerate(self.mesa):
                x = 400 + j * 150
                self.canvas.create_rectangle(x - 60, 100, x + 60, 160, fill="#E67E22", outline="black", width=2)
                self.canvas.create_text(x, 130, text=ingr, font=("Arial", 11, "bold"), fill="white")

        self.label_fumadores.config(text=f"F1: {self.estado_fumadores[0]} | F2: {self.estado_fumadores[1]} | F3: {self.estado_fumadores[2]}")

    def actualizar_log(self, mensaje):
        def _actualizar():
            self.texto_log.insert(tk.END, mensaje + "\n")
            self.texto_log.see(tk.END)
        self.root.after(0, _actualizar)

    def refrescar(self):
        self.root.after(0, self.dibujar_mesa)

    def actualizar_agente(self, mensaje):
        def _actualizar():
            self.label_agente.config(text=f"Agente: {mensaje}")
        self.root.after(0, _actualizar)

    # --------------------------------------------------------
    #  HILOS
    # --------------------------------------------------------
    def agente(self):
        while self.ejecutando:
            self.esperar(1.5)
            if not self.ejecutando: break

            self.semaforo_agente.acquire()
            if not self.ejecutando: break

            ingredientes_disponibles = random.sample([0, 1, 2], 2)
            
            with self.lock:
                self.mesa = [self.ingredientes[i] for i in ingredientes_disponibles]
                self.actualizar_agente(f"puso {self.mesa[0]} y {self.mesa[1]}")
                self.actualizar_log(f"Agente: puso {self.mesa[0]} y {self.mesa[1]} en la mesa")
                self.refrescar()

                for i in range(3):
                    if self.fumador_tiene[i] not in ingredientes_disponibles:
                        self.estado_fumadores[i] = "armando"
                        self.actualizar_log(f"Fumador {i+1}: tiene {self.ingredientes[self.fumador_tiene[i]]}, puede armar")
                        self.refrescar()
                        self.semaforo_fumadores[i].release()
                        break

    def fumador(self, i):
        while self.ejecutando:
            self.semaforo_fumadores[i].acquire()
            if not self.ejecutando: break

            with self.lock:
                self.estado_fumadores[i] = "armando"
                self.actualizar_log(f"Fumador {i+1}: toma los ingredientes de la mesa")
                self.refrescar()
            
            self.esperar(1.0) # Tiempo de armar (más lento para que se vea)

            with self.lock:
                self.estado_fumadores[i] = "fumando"
                self.mesa = []
                self.actualizar_log(f"Fumador {i+1}: 🚬 está FUMANDO")
                self.refrescar()

            self.esperar(3.0) # Tiempo de fumar (más lento para que se vea)

            with self.lock:
                self.estado_fumadores[i] = "esperando"
                self.actualizar_log(f"Fumador {i+1}: terminó de fumar")
                self.refrescar()
            
            self.semaforo_agente.release()

    # --------------------------------------------------------
    #  CONTROLES
    # --------------------------------------------------------
    def iniciar(self):
        if self.ejecutando: return
        
        self.ejecutando = True
        self.pausado = False
        self.mesa = []
        self.estado_fumadores = ["esperando"] * 3
        self.semaforo_agente = threading.Semaphore(1)
        self.semaforo_fumadores = [threading.Semaphore(0) for _ in range(3)]
        
        self.texto_log.delete(1.0, tk.END)
        self.texto_log.insert(tk.END, "=== SIMULACIÓN INICIADA ===\n")
        self.actualizar_agente("esperando...")
        self.refrescar()

        threading.Thread(target=self.agente, daemon=True).start()
        for i in range(3):
            threading.Thread(target=self.fumador, args=(i,), daemon=True).start()

        self.btn_iniciar.config(state="disabled")
        self.btn_pausar.config(state="normal", text="PAUSAR")
        self.btn_detener.config(state="normal")

    def pausar(self):
        if not self.ejecutando: return
        self.pausado = not self.pausado
        if self.pausado:
            self.btn_pausar.config(text="REANUDAR", bg="#3498DB")
            self.texto_log.insert(tk.END, "=== SIMULACIÓN PAUSADA ===\n")
        else:
            self.btn_pausar.config(text="PAUSAR", bg="#F1C40F")
            self.texto_log.insert(tk.END, "=== SIMULACIÓN REANUDADA ===\n")
        self.texto_log.see(tk.END)

    def detener(self):
        self.ejecutando = False
        self.pausado = False
        for s in self.semaforo_fumadores: s.release()
        self.semaforo_agente.release()
        
        self.texto_log.insert(tk.END, "=== SIMULACIÓN DETENIDA ===\n")
        self.texto_log.see(tk.END)
        
        self.btn_iniciar.config(state="normal")
        self.btn_pausar.config(state="disabled", text="PAUSAR", bg="#F1C40F")
        self.btn_detener.config(state="disabled")

if __name__ == "__main__":
    root = tk.Tk()
    app = Fumadores(root)
    root.mainloop()