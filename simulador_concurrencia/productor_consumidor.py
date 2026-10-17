# ============================================================
#  PROBLEMA: PRODUCTOR - CONSUMIDOR (CON PAUSA Y VELOCIDAD)
# ============================================================

import tkinter as tk
from tkinter import ttk
import threading
import time

class ProductorConsumidor:
    def __init__(self, root):
        self.root = root
        self.root.title("Productor - Consumidor")
        self.root.geometry("700x600")

        self.buffer = []
        self.capacidad = 5
        self.ejecutando = False
        self.pausado = False
        self.velocidad = 1.0
        self.lock = threading.Lock()

        self.crear_interfaz()

    def crear_interfaz(self):
        frame_buffer = tk.LabelFrame(self.root, text="Buffer (capacidad = 5)", padx=10, pady=10)
        frame_buffer.pack(fill="x", padx=10, pady=10)
        self.canvas_buffer = tk.Canvas(frame_buffer, width=600, height=80, bg="white", highlightthickness=1, highlightbackground="black")
        self.canvas_buffer.pack()

        frame_estado = tk.LabelFrame(self.root, text="Estado", padx=10, pady=10)
        frame_estado.pack(fill="x", padx=10, pady=5)
        self.label_productor = tk.Label(frame_estado, text="Productor: esperando...", font=("Arial", 12), fg="blue")
        self.label_productor.pack(anchor="w")
        self.label_consumidor = tk.Label(frame_estado, text="Consumidor: esperando...", font=("Arial", 12), fg="green")
        self.label_consumidor.pack(anchor="w")
        self.label_buffer = tk.Label(frame_estado, text="Buffer: 0 / 5", font=("Arial", 12), fg="black")
        self.label_buffer.pack(anchor="w")

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
        self.texto_log = tk.Text(frame_log, height=10, font=("Courier", 10))
        self.texto_log.pack(fill="both", expand=True)

    def esperar(self, segundos):
        tiempo_inicio = time.time()
        while time.time() - tiempo_inicio < segundos * self.velocidad:
            if not self.ejecutando: break
            while self.pausado and self.ejecutando:
                time.sleep(0.1)
            time.sleep(0.05)

    def cambiar_velocidad(self, event):
        if self.combo_vel.get() == "Lento": self.velocidad = 2.0
        elif self.combo_vel.get() == "Rápido": self.velocidad = 0.5
        else: self.velocidad = 1.0

    def dibujar_buffer(self):
        self.canvas_buffer.delete("all")
        ancho_celda = 100
        for i in range(self.capacidad):
            x1 = 20 + i * ancho_celda
            y1 = 15
            x2 = x1 + ancho_celda - 10
            y2 = 65
            if i < len(self.buffer):
                self.canvas_buffer.create_rectangle(x1, y1, x2, y2, fill="#3498DB", outline="black")
                self.canvas_buffer.create_text((x1+x2)//2, (y1+y2)//2, text=self.buffer[i], fill="white", font=("Arial", 14, "bold"))
            else:
                self.canvas_buffer.create_rectangle(x1, y1, x2, y2, fill="#ECF0F1", outline="gray", dash=(2,2))
        self.label_buffer.config(text=f"Buffer: {len(self.buffer)} / {self.capacidad}")

    def productor(self):
        contador = 1
        while self.ejecutando:
            with self.lock:
                if len(self.buffer) < self.capacidad:
                    item = f"D{contador}"
                    self.buffer.append(item)
                    contador += 1
                    self.actualizar_estado(f"Productor: agregó {item}", "azul")
                    self.root.after(0, self.dibujar_buffer)
                else:
                    self.actualizar_estado("Productor: buffer lleno, esperando...", "azul")
            self.esperar(1.5)

    def consumidor(self):
        while self.ejecutando:
            with self.lock:
                if len(self.buffer) > 0:
                    item = self.buffer.pop(0)
                    self.actualizar_estado(f"Consumidor: sacó {item}", "verde")
                    self.root.after(0, self.dibujar_buffer)
                else:
                    self.actualizar_estado("Consumidor: buffer vacío, esperando...", "verde")
            self.esperar(2.0)

    def actualizar_estado(self, mensaje, color):
        def _actualizar():
            if color == "azul": self.label_productor.config(text=mensaje)
            else: self.label_consumidor.config(text=mensaje)
            self.texto_log.insert(tk.END, mensaje + "\n")
            self.texto_log.see(tk.END)
        self.root.after(0, _actualizar)

    def iniciar(self):
        if self.ejecutando: return
        self.ejecutando = True
        self.pausado = False
        self.buffer = []
        self.dibujar_buffer()
        self.texto_log.delete(1.0, tk.END)
        self.texto_log.insert(tk.END, "=== SIMULACIÓN INICIADA ===\n")
        threading.Thread(target=self.productor, daemon=True).start()
        threading.Thread(target=self.consumidor, daemon=True).start()
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
    app = ProductorConsumidor(root)
    root.mainloop()