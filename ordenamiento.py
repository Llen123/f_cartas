from datetime import datetime
from jugadores import *

def obtener_jugadores_del_historial(historial_partidas):

    jugadores = []
    for partida in historial_partidas:
        ganador = partida["Ganador"]
        jugadores.append({
            "Fecha Partida": ganador["Fecha De partida"],
            "nombre": ganador["Nombre"],
            "puntuacion": ganador["Puntuacion"],
            "Victorias Elementales": ganador["Victorias Elementales"]
        })
    return jugadores

def bubble_sort(jugadores, criterio, orden):

    for i in range(len(jugadores) - 1):
        for j in range(i + 1, len(jugadores)):
            valor_1 = jugadores[i][criterio]
            valor_2 = jugadores[j][criterio]

            if orden == "asc" and valor_1 > valor_2:
                jugadores[i], jugadores[j] = jugadores[j], jugadores[i]
            elif orden == "desc" and valor_1 < valor_2:
                jugadores[i], jugadores[j] = jugadores[j], jugadores[i]

    return jugadores

def mostrar_jugadores_ordenados(jugadores_ordenados):
    print("\nJugadores ordenados:")
    contador = 0 
    for jugador in jugadores_ordenados:
        print(f"Fecha de partida: {jugador['Fecha Partida']}")
        print(f"Nombre: {jugador['nombre']}")
        print(f"Puntuacion: {jugador['puntuacion']}")
        print(f"Victorias Elementales: {jugador['Victorias Elementales']}\n")
        contador += 1
        if contador >= 5:
            break 

def ordenar(criterio, orden):

    archivo_json = "historial_partidas.json"
    historial_partidas = manejar_archivo_json(archivo_json, "leer") 
    jugadores_del_historial = obtener_jugadores_del_historial(historial_partidas)
    jugadores_ordenados = bubble_sort(jugadores_del_historial, criterio, orden)
    mostrar_jugadores_ordenados(jugadores_ordenados)