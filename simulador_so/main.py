# ============================================================
#  PUNTO DE ENTRADA DEL PROGRAMA
#  Ejecuta este archivo para abrir el simulador.
# ============================================================

import tkinter as tk
from interfaz import SimuladorSO

if __name__ == "__main__":
    root = tk.Tk()
    app = SimuladorSO(root)
    root.mainloop()