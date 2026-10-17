# ============================================================
#  PROBLEMA: BARBERO DORMILÓN (CON PAUSA Y VELOCIDAD)
# ============================================================

import tkinter as tk
from tkinter import ttk
import threading
import time
import random

class BarberoDormilon:
    def __init__(self, root):
        self.root = root
        self.root.title("Barbero Dormilón")
        self.root.geometry("1000x700")

        self.ejecutando = False
        self.pausado = False
        self.velocidad = 1.0
        self.N_SILLAS = 3
        self.sillas_espera = []
        self.silla_barbero = None
        self.barbero_durmiendo = True
        self.barbero_ocupado = False
        self.total_atendidos = 0
        self.total_perdidos = 0

        self.semaforo_clientes = threading.Semaphore(0)
        self.mutex = threading.Lock()

        self.crear_interfaz()

    def crear_interfaz(self):
        frame_canvas = tk.LabelFrame(self.root, text="Barbería", padx=10, pady=10)
        frame_canvas.pack(fill="both", expand=True, padx=10, pady=10)
        self.canvas = tk.Canvas(frame_canvas, width=950, height=300, bg="#FDFEFE")
        self.canvas.pack()

        frame_estado = tk.LabelFrame(self.root, text="Estado", padx=10, pady=5)
        frame_estado.pack(fill="x", padx=10, pady=5)
        self.label_barbero = tk.Label(frame_estado, text="Barbero: durmiendo 😴", font=("Arial", 12), fg="gray")
        self.label_barbero.pack(anchor="w")
        self.label_estadisticas = tk.Label(frame_estado, text="Atendidos: 0 | Perdidos: 0 | En espera: 0", font=("Arial", 11))
        self.label_estadisticas.pack(anchor="w")

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

    def dibujar_barberia(self):
        self.canvas.delete("all")
        self.canvas.create_rectangle(30, 100, 180, 300, fill="#D5DBDB", outline="black", width=2)
        self.canvas.create_text(105, 80, text="Silla del Barbero", font=("Arial", 10, "bold"))

        if self.barbero_durmiendo:
            self.canvas.create_oval(70, 150, 140, 220, fill="#95A5A6", outline="black", width=2)
            self.canvas.create_text(105, 185, text="😴", font=("Arial", 20))
        elif self.barbero_ocupado:
            self.canvas.create_oval(70, 150, 140, 220, fill="#E74C3C", outline="black", width=2)
            self.canvas.create_text(105, 185, text="✂️", font=("Arial", 20))
        else:
            self.canvas.create_oval(70, 150, 140, 220, fill="#F1C40F", outline="black", width=2)
            self.canvas.create_text(105, 185, text="🧔", font=("Arial", 20))

        if self.silla_barbero:
            self.canvas.create_text(105, 260, text=f"Cliente {self.silla_barbero}", font=("Arial", 11, "bold"))

        self.canvas.create_text(560, 50, text=f"Sillas de Espera ({self.N_SILLAS})", font=("Arial", 12, "bold"))
        espacio_inicio, espacio_fin = 220, 940
        ancho_total = espacio_fin - espacio_inicio
        ancho_silla = min(90, ancho_total // self.N_SILLAS - 5)
        margen = max(2, (ancho_total - (ancho_silla * self.N_SILLAS)) // (self.N_SILLAS + 1))

        for i in range(self.N_SILLAS):
            x1 = espacio_inicio + margen + i * (ancho_silla + margen)
            y1, y2 = 100, 200
            x2 = x1 + ancho_silla
            self.canvas.create_rectangle(x1, y1, x2, y2, fill="#ECF0F1", outline="black", width=2)
            if i < len(self.sillas_espera):
                tam = max(15, ancho_silla // 3)
                self.canvas.create_oval(x1 + tam, y1 + 20, x2 - tam, y1 + 20 + tam * 2, fill="#3498DB", outline="black")
                self.canvas.create_text((x1+x2)//2, y1 + 95, text=f"C{self.sillas_espera[i]}", font=("Arial", 9, "bold"))

        if self.barbero_durmiendo: self.label_barbero.config(text="Barbero: durmiendo 😴", fg="gray")
        elif self.barbero_ocupado: self.label_barbero.config(text=f"Barbero: cortando a Cliente {self.silla_barbero} ✂️", fg="red")
        else: self.label_barbero.config(text="Barbero: despierto, esperando...", fg="orange")

        self.label_estadisticas.config(text=f"Atendidos: {self.total_atendidos} | Perdidos: {self.total_perdidos} | En espera: {len(self.sillas_espera)}")

    def actualizar_log(self, mensaje):
        def _actualizar():
            self.texto_log.insert(tk.END, mensaje + "\n")
            self.texto_log.see(tk.END)
        self.root.after(0, _actualizar)

    def refrescar(self): self.root.after(0, self.dibujar_barberia)

    def barbero(self):
        while self.ejecutando:
            if self.silla_barbero is None:
                self.barbero_durmiendo = True
                self.refrescar()
                self.actualizar_log("Barbero: durmiendo...")
                self.semaforo_clientes.acquire()
            if not self.ejecutando: break
            with self.mutex:
                if self.silla_barbero is None and self.sillas_espera:
                    self.silla_barbero = self.sillas_espera.pop(0)
                    self.actualizar_log(f"Barbero: toma al Cliente {self.silla_barbero}")
                if self.silla_barbero is None: continue
                self.barbero_durmiendo = False
                self.barbero_ocupado = True
                self.actualizar_log(f"Barbero: atendiendo al Cliente {self.silla_barbero}")
                self.refrescar()
            self.esperar(random.uniform(2.0, 3.0))
            with self.mutex:
                self.total_atendidos += 1
                self.actualizar_log(f"Barbero: terminó con Cliente {self.silla_barbero}")
                self.silla_barbero = None
                self.barbero_ocupado = False
                self.refrescar()

    def cliente(self, id_cliente):
        self.esperar(random.uniform(0.5, 2.0))
        if not self.ejecutando: return
        with self.mutex:
            if self.barbero_durmiendo:
                self.silla_barbero = id_cliente
                self.barbero_durmiendo = False
                self.actualizar_log(f"Cliente {id_cliente}: despertó al barbero y se sienta")
                self.refrescar()
                self.semaforo_clientes.release()
                return
            if len(self.sillas_espera) < self.N_SILLAS:
                self.sillas_espera.append(id_cliente)
                self.actualizar_log(f"Cliente {id_cliente}: se sentó (espera: {len(self.sillas_espera)})")
                self.refrescar()
                self.semaforo_clientes.release()
            else:
                self.total_perdidos += 1
                self.actualizar_log(f"Cliente {id_cliente}: NO había sillas, se fue 😢")
                self.refrescar()

    def generador_clientes(self):
        id_cliente = 1
        while self.ejecutando:
            threading.Thread(target=self.cliente, args=(id_cliente,), daemon=True).start()
            id_cliente += 1
            self.esperar(random.uniform(0.8, 2.0))

    def iniciar(self):
        if self.ejecutando: return
        self.ejecutando = True
        self.pausado = False
        self.sillas_espera = []
        self.silla_barbero = None
        self.barbero_durmiendo = True
        self.barbero_ocupado = False
        self.total_atendidos = 0
        self.total_perdidos = 0
        self.semaforo_clientes = threading.Semaphore(0)
        self.texto_log.delete(1.0, tk.END)
        self.texto_log.insert(tk.END, "=== SIMULACIÓN INICIADA ===\n")
        self.refrescar()
        threading.Thread(target=self.barbero, daemon=True).start()
        threading.Thread(target=self.generador_clientes, daemon=True).start()
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
        self.semaforo_clientes.release()
        self.texto_log.insert(tk.END, "=== SIMULACIÓN DETENIDA ===\n")
        self.btn_iniciar.config(state="normal")
        self.btn_pausar.config(state="disabled", text="PAUSAR", bg="#F1C40F")
        self.btn_detener.config(state="disabled")

if __name__ == "__main__":
    root = tk.Tk()
    app = BarberoDormilon(root)
    root.mainloop()