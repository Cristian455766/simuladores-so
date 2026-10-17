# ============================================================
#  DATOS DE EJEMPLO (los del PDF del taller)
#  Cada proceso tiene: nombre, llegada, ejecucion, prioridad
# ============================================================

DATOS_EJERCICIOS = {
    "Ejercicio 1": [
        {"nombre": "P0", "llegada": 0, "ejecucion": 6, "prioridad": 0},
        {"nombre": "P1", "llegada": 1, "ejecucion": 3, "prioridad": 0},
        {"nombre": "P2", "llegada": 3, "ejecucion": 2, "prioridad": 0},
        {"nombre": "P3", "llegada": 5, "ejecucion": 4, "prioridad": 0},
    ],
    "Ejercicio 2": [
        {"nombre": "A", "llegada": 0, "ejecucion": 2, "prioridad": 0},
        {"nombre": "B", "llegada": 0, "ejecucion": 1, "prioridad": 0},
        {"nombre": "C", "llegada": 0, "ejecucion": 8, "prioridad": 0},
        {"nombre": "D", "llegada": 0, "ejecucion": 3, "prioridad": 0},
        {"nombre": "E", "llegada": 0, "ejecucion": 5, "prioridad": 0},
    ],
    "Ejercicio 3": [
        {"nombre": "A", "llegada": 0, "ejecucion": 3, "prioridad": 0},
        {"nombre": "B", "llegada": 1, "ejecucion": 5, "prioridad": 0},
        {"nombre": "C", "llegada": 3, "ejecucion": 2, "prioridad": 0},
        {"nombre": "D", "llegada": 9, "ejecucion": 5, "prioridad": 0},
        {"nombre": "E", "llegada": 12, "ejecucion": 5, "prioridad": 0},
    ],
    #"Ejercicio 4 (Teórico)": [
        # Este ejercicio NO tiene datos de procesos.
        # Es una pregunta de análisis sobre Round Robin.
        # La respuesta está en el PDF: un proceso recibe 5% de CPU
        # porque tiene una ráfaga muy larga o hace muchas E/S.
        # (No se puede simular, solo es informativo)
    #],
    "Ejercicio 5": [
        {"nombre": "P0", "llegada": 0, "ejecucion": 6, "prioridad": 0},
        {"nombre": "P1", "llegada": 1, "ejecucion": 3, "prioridad": 0},
        {"nombre": "P2", "llegada": 3, "ejecucion": 2, "prioridad": 0},
        {"nombre": "P3", "llegada": 5, "ejecucion": 4, "prioridad": 0},
    ],
    "Ejercicio 6": [
        {"nombre": "A", "llegada": 0, "ejecucion": 5, "prioridad": 0},
        {"nombre": "B", "llegada": 1, "ejecucion": 2, "prioridad": 0},
        {"nombre": "C", "llegada": 2, "ejecucion": 6, "prioridad": 0},
        {"nombre": "D", "llegada": 3, "ejecucion": 4, "prioridad": 0},
        {"nombre": "E", "llegada": 4, "ejecucion": 3, "prioridad": 0},
    ],
    "Ejercicio 7": [
        {"nombre": "P1", "llegada": 0, "ejecucion": 10, "prioridad": 3},
        {"nombre": "P2", "llegada": 0, "ejecucion": 1, "prioridad": 1},
        {"nombre": "P3", "llegada": 0, "ejecucion": 2, "prioridad": 3},
        {"nombre": "P4", "llegada": 0, "ejecucion": 1, "prioridad": 4},
        {"nombre": "P5", "llegada": 0, "ejecucion": 5, "prioridad": 2},
    ],
}