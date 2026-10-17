# ============================================================
#  MENÚ PRINCIPAL - SIMULADOR DE CONCURRENCIA
#  Ejecuta este archivo para abrir el menú.
# ============================================================

import tkinter as tk
from tkinter import messagebox

# Importar las clases de cada problema
from productor_consumidor import ProductorConsumidor
from lectores_escritores import LectoresEscritores
from filosofos import Filosofos
from barbero import BarberoDormilon
from fumadores import Fumadores

class MenuPrincipal:
    def __init__(self, root):
        self.root = root
        self.root.title("Simulador de Concurrencia - Sistemas Operativos")
        self.root.geometry("600x550")
        self.root.configure(bg="#2C3E50")

        # --- Título ---
        titulo = tk.Label(self.root,
                          text="SIMULADOR DE CONCURRENCIA",
                          font=("Arial", 20, "bold"),
                          bg="#2C3E50", fg="white")
        titulo.pack(pady=20)

        subtitulo = tk.Label(self.root,
                             text="Problemas Clásicos de Sistemas Operativos",
                             font=("Arial", 12),
                             bg="#2C3E50", fg="#BDC3C7")
        subtitulo.pack(pady=5)

        # --- Botones de los problemas ---
        frame_botones = tk.Frame(self.root, bg="#2C3E50")
        frame_botones.pack(pady=20)

        problemas = [
            ("1. Productor - Consumidor", self.abrir_productor, "#3498DB"),
            ("2. Lectores - Escritores", self.abrir_lectores, "#9B59B6"),
            ("3. Filósofos Comensales", self.abrir_filosofos, "#E67E22"),
            ("4. Barbero Dormilón", self.abrir_barbero, "#E74C3C"),
            ("5. Fumadores", self.abrir_fumadores, "#2ECC71"),
        ]

        for texto, comando, color in problemas:
            btn = tk.Button(frame_botones,
                            text=texto,
                            command=comando,
                            bg=color, fg="white",
                            font=("Arial", 13, "bold"),
                            width=30, height=2,
                            relief="raised", bd=3,
                            cursor="hand2")
            btn.pack(pady=8)

        # --- Botón Salir ---
        btn_salir = tk.Button(self.root,
                              text="Salir",
                              command=self.root.quit,
                              bg="#7F8C8D", fg="white",
                              font=("Arial", 11, "bold"),
                              width=15)
        btn_salir.pack(pady=15)

        # --- Pie de página ---
        pie = tk.Label(self.root,
                       text="Sistemas Operativos 2026 II",
                       font=("Arial", 9),
                       bg="#2C3E50", fg="#7F8C8D")
        pie.pack(side="bottom", pady=10)

    # --------------------------------------------------------
    #  ABRIR CADA SIMULACIÓN EN UNA VENTANA NUEVA
    # --------------------------------------------------------
    def abrir_ventana(self, clase):
        """Abre una simulación en una ventana nueva."""
        ventana = tk.Toplevel(self.root)
        app = clase(ventana)

    def abrir_productor(self):
        self.abrir_ventana(ProductorConsumidor)

    def abrir_lectores(self):
        self.abrir_ventana(LectoresEscritores)

    def abrir_filosofos(self):
        self.abrir_ventana(Filosofos)

    def abrir_barbero(self):
        self.abrir_ventana(BarberoDormilon)

    def abrir_fumadores(self):
        self.abrir_ventana(Fumadores)


# ============================================================
#  PUNTO DE ENTRADA
# ============================================================
if __name__ == "__main__":
    root = tk.Tk()
    app = MenuPrincipal(root)
    root.mainloop()