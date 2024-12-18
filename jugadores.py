import json
from datetime import datetime

fecha = datetime.now()
fecha_completa = fecha.strftime("%d/%m/%Y, %H:%M:%S")

def manejar_archivo_json(archivo: str, modo: str, datos: dict = None) -> dict:
    resultado = []
    if modo == "leer":
        try:
            with open(archivo, "r") as archivo_json:
                resultado =  json.load(archivo_json)
        except:
            resultado = []
    elif modo == "escribir":
        if datos:
            with open(archivo, "w") as archivo_json:
                json.dump(datos, archivo_json, indent=4)
    return resultado

def validar_nombres(nombre_jugador: str) -> str:

    nombre = input(f"Ingrese el nombre del jugador {nombre_jugador}: ")
    while len(nombre.strip()) == 0:
        nombre = input(
            f"El campo está vacío. Ingrese el nombre del jugador {nombre_jugador}: ").strip()
    return nombre

def obtener_nombres_jugadores() -> dict:

    datos_jugadores = {}
    for nombres_jugadores in range(1, 3):
        nombre = validar_nombres(nombres_jugadores)
        datos_jugadores[f"jugador{nombres_jugadores}"] = {
            "nombre": nombre, "puntuacion": 0, "Victorias Elementales": 0}
    return datos_jugadores

def guardar_datos_jugadores(datos_jugadores: dict, ganador_final: str) -> None:
    
    archivo_json = "historial_partidas.json"


    datos_partida = {
        "Ganador": {
            "Nombre": datos_jugadores[ganador_final]["nombre"],
            "Puntuacion": datos_jugadores[ganador_final]["puntuacion"],
            "Victorias Elementales": datos_jugadores[ganador_final]["Victorias Elementales"],
            "Fecha De partida": fecha_completa,
        }
    }

    historial_partidas = manejar_archivo_json(archivo_json, "leer")


    historial_partidas.append(datos_partida)
    manejar_archivo_json(archivo_json, "escribir", historial_partidas)