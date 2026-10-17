# ============================================================
#  PROBLEMA: FILÓSOFOS COMENSALES (CON PAUSA Y VELOCIDAD)
# ============================================================

import tkinter as tk
from tkinter import ttk
import threading
import time
import random
import math

class Filosofos:
    def __init__(self, root):
        self.root = root
        self.root.title("Filósofos Comensales")
        self.root.geometry("800x800")

        self.ejecutando = False
        self.pausado = False
        self.velocidad = 1.0
        self.N = 5
        self.tenedores = [threading.Lock() for _ in range(self.N)]
        self.estado = ["pensando"] * self.N
        
        self.colores = {"pensando": "#95A5A6", "esperando": "#F1C40F", "comiendo": "#2ECC71"}

        self.crear_interfaz()

    def crear_interfaz(self):
        frame_mesa = tk.LabelFrame(self.root, text="Mesa Redonda", padx=10, pady=10)
        frame_mesa.pack(fill="both", expand=True, padx=10, pady=10)
        self.canvas = tk.Canvas(frame_mesa, width=600, height=500, bg="white")
        self.canvas.pack()

        frame_estado = tk.LabelFrame(self.root, text="Estados", padx=10, pady=5)
        frame_estado.pack(fill="x", padx=10, pady=5)
        self.label_estado = tk.Label(frame_estado, text="Todos pensando...", font=("Arial", 11))
        self.label_estado.pack(anchor="w")

        frame_botones = tk.Frame(self.root)
        frame_botones.pack(pady=10)
        self.btn_iniciar = tk.Button(frame_botones, text="INICIAR", command=self.iniciar, bg="#2ECC71", fg="white", font=("Arial", 11, "bold"), width=10)
        self.btn_iniciar.pack(side="left", padx=5)
        self.btn_pausar = tk.Button(frame_botones, text="PAUSAR", command=self.pausar, bg="#F1C40F", fg="black", font=("Arial", 11, "bold"), width=10, state="disabled")
        self.btn_pausar.pack(side="left", padx=5)
        self.btn_detener = tk.Button(frame_botones, text="DETENER", command=self.detener, bg="#E74C3C", fg="white", font=("Arial", 11, "bold"), width=10, state="disabled")
        self.btn_detener.pack(side="left", padx=5)
        tk.Label(frame_botones, text="Velocidad:", font=("Arial", 10)).pack(side="left", padx=(15, 5))
        self.combo_vel = ttk.Combobox(frame_botones, values=["Lento", "Normal", "Rápido"], state="readonly", width=10)
        self.combo_vel.current(1)
        self.combo_vel.pack(side="left")
        self.combo_vel.bind("<<ComboboxSelected>>", self.cambiar_velocidad)

        frame_log = tk.LabelFrame(self.root, text="Registro de eventos", padx=5, pady=5)
        frame_log.pack(fill="both", expand=True, padx=10, pady=5)
        self.texto_log = tk.Text(frame_log, height=8, font=("Courier", 10))
        self.texto_log.pack(fill="both", expand=True)
        self.dibujar_mesa()

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

    def dibujar_mesa(self):
        self.canvas.delete("all")
        cx, cy = 300, 250
        radio = 150
        self.canvas.create_oval(cx - radio, cy - radio, cx + radio, cy + radio, outline="black", width=2, fill="#FDFEFE")
        for i in range(self.N):
            angulo = math.radians(90 + i * 72)
            x = cx + radio * math.cos(angulo)
            y = cy - radio * math.sin(angulo)
            color = self.colores[self.estado[i]]
            self.canvas.create_oval(x - 30, y - 30, x + 30, y + 30, fill=color, outline="black", width=2)
            self.canvas.create_text(x, y, text=f"F{i+1}", font=("Arial", 14, "bold"), fill="white")
            angulo_tenedor = math.radians(90 + i * 72 + 36)
            tx = cx + (radio - 50) * math.cos(angulo_tenedor)
            ty = cy - (radio - 50) * math.sin(angulo_tenedor)
            color_tenedor = "red" if self.tenedores[i].locked() else "black"
            self.canvas.create_rectangle(tx - 5, ty - 15, tx + 5, ty + 15, fill=color_tenedor, outline="black")
            self.canvas.create_text(tx, ty + 25, text=f"T{i+1}", font=("Arial", 9))
        estados_texto = " | ".join([f"F{i+1}: {self.estado[i]}" for i in range(self.N)])
        self.label_estado.config(text=estados_texto)

    def actualizar_log(self, mensaje):
        def _actualizar():
            self.texto_log.insert(tk.END, mensaje + "\n")
            self.texto_log.see(tk.END)
        self.root.after(0, _actualizar)

    def refrescar_mesa(self):
        self.root.after(0, self.dibujar_mesa)

    def filosofo(self, i):
        izq = i
        der = (i + 1) % self.N
        if i == self.N - 1: primero, segundo = der, izq
        else: primero, segundo = izq, der

        while self.ejecutando:
            self.estado[i] = "pensando"
            self.refrescar_mesa()
            self.esperar(random.uniform(1.0, 2.0))
            if not self.ejecutando: break

            self.estado[i] = "esperando"
            self.refrescar_mesa()
            self.actualizar_log(f"Filósofo {i+1}: quiere comer")
            self.tenedores[primero].acquire()
            self.actualizar_log(f"Filósofo {i+1}: tomó T{primero+1}")
            self.refrescar_mesa()
            self.esperar(0.3)
            self.tenedores[segundo].acquire()
            self.actualizar_log(f"Filósofo {i+1}: tomó T{segundo+1}")
            self.refrescar_mesa()

            self.estado[i] = "comiendo"
            self.refrescar_mesa()
            self.actualizar_log(f"Filósofo {i+1}: COMIENDO")
            self.esperar(random.uniform(1.0, 2.0))

            self.tenedores[segundo].release()
            self.tenedores[primero].release()
            self.actualizar_log(f"Filósofo {i+1}: soltó tenedores")
            self.estado[i] = "pensando"
            self.refrescar_mesa()

    def iniciar(self):
        if self.ejecutando: return
        self.ejecutando = True
        self.pausado = False
        self.estado = ["pensando"] * self.N
        self.tenedores = [threading.Lock() for _ in range(self.N)]
        self.texto_log.delete(1.0, tk.END)
        self.texto_log.insert(tk.END, "=== SIMULACIÓN INICIADA ===\n")
        for i in range(self.N):
            threading.Thread(target=self.filosofo, args=(i,), daemon=True).start()
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
    app = Filosofos(root)
    root.mainloop()