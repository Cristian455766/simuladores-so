# ============================================================
#  PROBLEMA: LECTORES - ESCRITORES (CON GRÁFICO Y VELOCIDAD)
# ============================================================

import tkinter as tk
from tkinter import ttk
import threading
import time
import random

class LectoresEscritores:
    def __init__(self, root):
        self.root = root
        self.root.title("Lectores - Escritores")
        self.root.geometry("900x700")

        self.ejecutando = False
        self.pausado = False
        self.velocidad = 1.0
        
        self.lectores_activos = 0
        self.escritor_activo = False
        self.lock = threading.Lock()
        
        # Para el gráfico
        self.recurso = "Base de Datos\n(Datos limpios)"
        self.color_recurso = "#3498DB" # Azul normal

        self.crear_interfaz()

    def crear_interfaz(self):
        # --- Canvas para el gráfico ---
        frame_grafico = tk.LabelFrame(self.root, text="Representación Visual", padx=10, pady=10)
        frame_grafico.pack(fill="both", expand=True, padx=10, pady=10)

        self.canvas = tk.Canvas(frame_grafico, width=850, height=250, bg="#FDFEFE")
        self.canvas.pack()

        # --- Estado ---
        frame_estado = tk.LabelFrame(self.root, text="Estado", padx=10, pady=10)
        frame_estado.pack(fill="x", padx=10, pady=5)

        self.label_lectores = tk.Label(frame_estado, text="Lectores activos: 0", font=("Arial", 12), fg="blue")
        self.label_lectores.pack(anchor="w")

        self.label_escritor = tk.Label(frame_estado, text="Escritor: inactivo", font=("Arial", 12), fg="red")
        self.label_escritor.pack(anchor="w")

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

        tk.Label(frame_botones, text="Velocidad:", font=("Arial", 10)).pack(side="left", padx=(15, 5))
        self.combo_vel = ttk.Combobox(frame_botones, values=["Lento", "Normal", "Rápido"], state="readonly", width=10)
        self.combo_vel.current(1)
        self.combo_vel.pack(side="left")
        self.combo_vel.bind("<<ComboboxSelected>>", self.cambiar_velocidad)

        # --- Log ---
        frame_log = tk.LabelFrame(self.root, text="Registro de eventos", padx=5, pady=5)
        frame_log.pack(fill="both", expand=True, padx=10, pady=5)

        self.texto_log = tk.Text(frame_log, height=8, font=("Courier", 10))
        self.texto_log.pack(fill="both", expand=True)

        self.dibujar_grafico()

    # --------------------------------------------------------
    #  GRÁFICO VISUAL
    # --------------------------------------------------------
    def dibujar_grafico(self):
        self.canvas.delete("all")
        
        # Dibujar la Base de Datos en el centro
        if self.escritor_activo:
            color = "#E74C3C" # Rojo si el escritor está dentro
        elif self.lectores_activos > 0:
            color = "#2ECC71" # Verde si hay lectores
        else:
            color = "#BDC3C7" # Gris si está vacío

        self.canvas.create_rectangle(325, 75, 525, 175, fill=color, outline="black", width=3)
        self.canvas.create_text(425, 125, text=self.recurso, font=("Arial", 12, "bold"), fill="white")

        # Dibujar Lectores (Ojitos azules alrededor)
        for i in range(self.lectores_activos):
            angulo = i * 45 # Separar los ojos
            x = 425 + 200 * random.uniform(0.5, 1.0)
            y = 125 + 80 * random.uniform(-1.0, 1.0)
            self.canvas.create_text(x, y, text="👁️", font=("Arial", 24))

        # Dibujar Escritor (Candado y lápiz)
        if self.escritor_activo:
            self.canvas.create_text(425, 220, text="✍️ ESCRIBIENDO ✍️", font=("Arial", 14, "bold"), fill="red")
            self.canvas.create_text(425, 40, text="🔒 RECURSO BLOQUEADO 🔒", font=("Arial", 14, "bold"), fill="red")
        elif self.lectores_activos > 0:
            self.canvas.create_text(425, 220, text="👀 LEYENDO 👀", font=("Arial", 14, "bold"), fill="green")
        else:
            self.canvas.create_text(425, 125, text="(Vacío)", font=("Arial", 14), fill="black")

    # --------------------------------------------------------
    #  LÓGICA Y HECHOS
    # --------------------------------------------------------
    def esperar(self, segundos):
        tiempo_inicio = time.time()
        while time.time() - tiempo_inicio < segundos * self.velocidad:
            if not self.ejecutando: break
            while self.pausado and self.ejecutando: time.sleep(0.1)
            time.sleep(0.05)

    def cambiar_velocidad(self, event):
        if self.combo_vel.get() == "Lento": self.velocidad = 2.0
        elif self.combo_vel.get() == "Rápido": self.velocidad = 0.5
        else: self.velocidad = 1.0

    def actualizar_interfaz(self, mensaje, color="black"):
        def _actualizar():
            self.label_lectores.config(text=f"Lectores activos: {self.lectores_activos}")
            if self.escritor_activo:
                self.label_escritor.config(text="Escritor: ESCRIBIENDO", fg="red")
            else:
                self.label_escritor.config(text="Escritor: inactivo", fg="gray")
            
            self.dibujar_grafico() # Actualizar el gráfico

            if mensaje:
                self.texto_log.insert(tk.END, mensaje + "\n", color)
                self.texto_log.see(tk.END)
        self.root.after(0, _actualizar)

    def lector(self, id_lector):
        while self.ejecutando:
            with self.lock:
                if self.escritor_activo:
                    self.actualizar_interfaz(f"Lector {id_lector}: esperando (escritor activo)...", "gray")
                else:
                    self.lectores_activos += 1
                    self.actualizar_interfaz(f"Lector {id_lector}: LEYENDO (total: {self.lectores_activos})", "blue")
            self.esperar(random.uniform(1.5, 3.0))
            
            with self.lock:
                if not self.escritor_activo:
                    self.lectores_activos -= 1
                    self.actualizar_interfaz(f"Lector {id_lector}: terminó de leer", "blue")
            self.esperar(random.uniform(1.0, 2.5))

    def escritor(self, id_escritor):
        while self.ejecutando:
            with self.lock:
                if self.lectores_activos > 0 or self.escritor_activo:
                    self.actualizar_interfaz(f"Escritor {id_escritor}: esperando...", "gray")
                else:
                    self.escritor_activo = True
                    self.recurso = f"Modificado por\nEscritor {id_escritor}"
                    self.actualizar_interfaz(f"Escritor {id_escritor}: ESCRIBIENDO", "red")
            self.esperar(random.uniform(2.0, 3.0))
            
            with self.lock:
                if self.escritor_activo:
                    self.escritor_activo = False
                    self.actualizar_interfaz(f"Escritor {id_escritor}: terminó de escribir", "red")
            self.esperar(random.uniform(1.5, 3.0))

    # --------------------------------------------------------
    #  CONTROLES
    # --------------------------------------------------------
    def iniciar(self):
        if self.ejecutando: return
        self.ejecutando = True
        self.pausado = False
        self.lectores_activos = 0
        self.escritor_activo = False
        self.recurso = "Base de Datos\n(Datos limpios)"
        self.texto_log.delete(1.0, tk.END)
        self.texto_log.insert(tk.END, "=== SIMULACIÓN INICIADA ===\n")
        self.actualizar_interfaz("")
        
        for i in range(1, 4):
            threading.Thread(target=self.lector, args=(i,), daemon=True).start()
        for i in range(1, 3):
            threading.Thread(target=self.escritor, args=(i,), daemon=True).start()
            
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
        self.texto_log.insert(tk.END, "=== SIMULACIÓN DETENIDA ===\n")
        self.btn_iniciar.config(state="normal")
        self.btn_pausar.config(state="disabled", text="PAUSAR", bg="#F1C40F")
        self.btn_detener.config(state="disabled")

if __name__ == "__main__":
    root = tk.Tk()
    app = LectoresEscritores(root)
    root.mainloop()