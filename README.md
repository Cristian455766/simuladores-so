# 🖥️ Simuladores de Sistemas Operativos

Este repositorio contiene el código fuente de dos simuladores interactivos desarrollados en **Python** como parte del curso de **Sistemas Operativos**. El objetivo principal es modelar y visualizar de forma gráfica el comportamiento de la CPU y la concurrencia de hilos.

## 📂 Estructura del Proyecto

El repositorio está dividido en dos carpetas principales:

### 1. `/simulador_so` (Gestión de Procesos)
Simulador de planificación de CPU que permite ingresar procesos y visualizar su ejecución.
*   **Políticas incluidas:** FCFS, SJF, SRTF, Round Robin (con quantum configurable) y Prioridades.
*   **Características:**
    *   Diagrama de Gantt generado con Matplotlib.
    *   Cálculo de métricas (Tiempo de Retorno, Tiempo de Espera, Varianza, Uso de CPU).
    *   Cola de espera en tiempo real.
    *   Simulación paso a paso con velocidad ajustable.
    *   Importación de procesos desde archivos `.txt`.

### 2. `/simulador_concurrencia` (Problemas Clásicos)
Simulador visual de los 5 problemas clásicos de sincronización de hilos, resueltos mediante semáforos y mutex.
*   **Problemas incluidos:**
    1.  Productor - Consumidor (Buffer limitado).
    2.  Lectores - Escritores.
    3.  Filósofos Comensales (Prevención de Deadlocks).
    4.  Barbero Dormilón.
    5.  Fumadores.
*   **Características:**
    *   Interfaz animada en tiempo real (Canvas).
    *   Uso de hilos (`threading`).
    *   Controles de Pausa, Inicio, Detener y selección de velocidad.

## 🛠️ Tecnologías Utilizadas
*   **Lenguaje:** Python 3.13
*   **Interfaz Gráfica:** Tkinter (incluido en Python).
*   **Gráficos:** Matplotlib (para el Diagrama de Gantt).
*   **Concurrencia:** Librería nativa `threading` (Hilos, Locks, Semáforos).

## ⚙️ Instalación y Ejecución

Para ejecutar cualquiera de los dos simuladores, sigue estos pasos:

1.  Asegúrate de tener Python instalado.
2.  Instala la librería de gráficos:
    ```bash
    pip install matplotlib
