# ============================================================
#  ALGORITMOS DE PLANIFICACIÓN
#  Cada función recibe una lista de procesos (diccionarios)
#  y devuelve: (lista_resultados, lista_gantt, registro_cola)
# ============================================================

import copy

# ------------------------------------------------------------
#  FCFS - First Come, First Served (NO expulsivo)
#  Se ejecuta el que llegó primero.
# ------------------------------------------------------------
def fcfs(procesos):
    proc = sorted(copy.deepcopy(procesos), key=lambda p: p["llegada"])
    tiempo = 0
    gantt = []
    registro_cola = []  # Guarda la cola en cada instante
    cola_espera = []    # Cola de procesos esperando

    for p in proc:
        if tiempo < p["llegada"]:
            tiempo = p["llegada"]  # CPU inactiva

        # Guardar el estado de la cola ANTES de ejecutar
        # En FCFS, la cola son todos los que ya llegaron y no se han ejecutado
        nombres_cola = [x["nombre"] for x in proc if x["llegada"] <= tiempo and x["nombre"] != p["nombre"]]
        # Filtrar solo los que aún no se han ejecutado
        ya_ejecutados = [g[0] for g in gantt]
        nombres_cola = [n for n in nombres_cola if n not in ya_ejecutados]
        registro_cola.append((tiempo, p["nombre"], nombres_cola))

        inicio = tiempo
        tf = tiempo + p["ejecucion"]
        p["tf"] = tf
        p["tr"] = tf - p["llegada"]
        p["te"] = p["tr"] - p["ejecucion"]
        gantt.append((p["nombre"], inicio, tf))
        tiempo = tf

    return proc, gantt, registro_cola

# ------------------------------------------------------------
#  SJF - Shortest Job First (NO expulsivo)
#  Se elige el proceso con menor duración total.
# ------------------------------------------------------------
def sjf(procesos):
    proc = copy.deepcopy(procesos)
    n = len(proc)
    ejecutados = [False] * n
    tiempo = 0
    completados = 0
    gantt = []
    registro_cola = []

    while completados < n:
        disponibles = [i for i in range(n) if not ejecutados[i] and proc[i]["llegada"] <= tiempo]
        if not disponibles:
            tiempo += 1
            continue

        idx = min(disponibles, key=lambda i: proc[i]["ejecucion"])
        p = proc[idx]

        # Guardar la cola antes de ejecutar (los demás disponibles)
        nombres_cola = [proc[i]["nombre"] for i in disponibles if i != idx]
        registro_cola.append((tiempo, p["nombre"], nombres_cola))

        inicio = tiempo
        tf = tiempo + p["ejecucion"]
        p["tf"] = tf
        p["tr"] = tf - p["llegada"]
        p["te"] = p["tr"] - p["ejecucion"]
        gantt.append((p["nombre"], inicio, tf))
        tiempo = tf
        ejecutados[idx] = True
        completados += 1

    return proc, gantt, registro_cola

# ------------------------------------------------------------
#  SRTF - Shortest Remaining Time First (EXPULSIVO)
# ------------------------------------------------------------
def srtf(procesos):
    proc = copy.deepcopy(procesos)
    n = len(proc)
    restante = [p["ejecucion"] for p in proc]
    ejecutados = [False] * n
    tiempo = 0
    completados = 0
    gantt = []
    registro_cola = []

    while completados < n:
        disponibles = [i for i in range(n) if not ejecutados[i] and proc[i]["llegada"] <= tiempo and restante[i] > 0]
        if not disponibles:
            tiempo += 1
            continue

        idx = min(disponibles, key=lambda i: restante[i])
        p = proc[idx]

        # Guardar la cola (los demás disponibles)
        nombres_cola = [proc[i]["nombre"] for i in disponibles if i != idx]
        registro_cola.append((tiempo, p["nombre"], nombres_cola))

        gantt.append((p["nombre"], tiempo, tiempo + 1))
        restante[idx] -= 1
        if restante[idx] == 0:
            tf = tiempo + 1
            p["tf"] = tf
            p["tr"] = tf - p["llegada"]
            p["te"] = p["tr"] - p["ejecucion"]
            ejecutados[idx] = True
            completados += 1
        tiempo += 1

    return proc, gantt, registro_cola

# ------------------------------------------------------------
#  RR - Round Robin (EXPULSIVO)
# ------------------------------------------------------------
def rr(procesos, quantum):
    proc = sorted(copy.deepcopy(procesos), key=lambda p: p["llegada"])
    n = len(proc)
    restante = [p["ejecucion"] for p in proc]
    cola = []
    i = 0
    tiempo = 0
    completados = 0
    gantt = []
    registro_cola = []

    while completados < n:
        while i < n and proc[i]["llegada"] <= tiempo:
            cola.append(i)
            i += 1

        if not cola:
            tiempo += 1
            continue

        idx = cola.pop(0)
        p = proc[idx]
        ejecutar = min(quantum, restante[idx])
        inicio = tiempo
        tiempo += ejecutar
        restante[idx] -= ejecutar
        gantt.append((p["nombre"], inicio, tiempo))

        # Guardar la cola después de la ejecución
        nombres_cola = [proc[j]["nombre"] for j in cola]
        registro_cola.append((inicio, p["nombre"], nombres_cola))

        while i < n and proc[i]["llegada"] <= tiempo:
            cola.append(i)
            i += 1

        if restante[idx] == 0:
            p["tf"] = tiempo
            p["tr"] = tiempo - p["llegada"]
            p["te"] = p["tr"] - p["ejecucion"]
            completados += 1
        else:
            cola.append(idx)

    return proc, gantt, registro_cola

# ------------------------------------------------------------
#  PRIORIDADES (NO expulsivo)
# ------------------------------------------------------------
def prioridades(procesos):
    proc = copy.deepcopy(procesos)
    n = len(proc)
    ejecutados = [False] * n
    tiempo = 0
    completados = 0
    gantt = []
    registro_cola = []

    while completados < n:
        disponibles = [i for i in range(n) if not ejecutados[i] and proc[i]["llegada"] <= tiempo]
        if not disponibles:
            tiempo += 1
            continue

        idx = min(disponibles, key=lambda i: proc[i]["prioridad"])
        p = proc[idx]

        # Guardar la cola (los demás disponibles)
        nombres_cola = [proc[i]["nombre"] for i in disponibles if i != idx]
        registro_cola.append((tiempo, p["nombre"], nombres_cola))

        inicio = tiempo
        tf = tiempo + p["ejecucion"]
        p["tf"] = tf
        p["tr"] = tf - p["llegada"]
        p["te"] = p["tr"] - p["ejecucion"]
        gantt.append((p["nombre"], inicio, tf))
        tiempo = tf
        ejecutados[idx] = True
        completados += 1

    return proc, gantt, registro_cola