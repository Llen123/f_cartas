import pygame
from datetime import datetime
from jugadores import *
from utilities import mostrar_texto  
from datos_globales import *

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

def mostrar_jugadores_ordenados(jugadores_ordenados, pantalla, fuente):
    y = 100  
    contador = 0

    for jugador in jugadores_ordenados:
        texto_fecha = f"Fecha: {jugador['Fecha Partida']}"
        texto_nombre = f"Nombre: {jugador['nombre']}"
        texto_puntuacion = f"Puntuación: {jugador['puntuacion']}"
        texto_victorias = f"Victorias Elementales: {jugador['Victorias Elementales']}"

        mostrar_texto(texto_fecha, 50, y, NEGRO, pantalla, fuente)
        y += 30 
        mostrar_texto(texto_nombre, 50, y, NEGRO, pantalla, fuente)
        y += 30
        mostrar_texto(texto_puntuacion, 50, y, NEGRO, pantalla, fuente)
        y += 30
        mostrar_texto(texto_victorias, 50, y, NEGRO, pantalla, fuente)
        y += 40  

        contador += 1
        if contador >= 10:  
            break

def ordenar(criterio, orden, pantalla, fuente):
    archivo_json = "historial_partidas.json"
    historial_partidas = manejar_archivo_json(archivo_json, "leer") 
    jugadores_del_historial = obtener_jugadores_del_historial(historial_partidas)
    jugadores_ordenados = bubble_sort(jugadores_del_historial, criterio, orden)

    pantalla.fill(BLANCO)
    mostrar_texto("Tabla de Posiciones", 500, 50, NEGRO, pantalla, fuente)  
    
    mostrar_jugadores_ordenados(jugadores_ordenados, pantalla, fuente)

    pygame.display.update()