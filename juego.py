from utilities import *
from mazo import *
from jugadores import *
from funciones import *
from tateti import *
import time


def obtener_jugadores() -> dict:
    
    datos_jugadores = obtener_nombres_jugadores()
    return datos_jugadores

def preparar_mazo() -> dict:

    mazo = cargar_mazo("cartas.csv")
    mazo_jugadores = mezclar_mazo(mazo)
    mazo_mezclado = repartir_cartas(mazo_jugadores)
    return mazo_mezclado

def mostrar_carta(carta: dict, nombre: str) -> str:
    resultado = f"\nCarta del jugador {nombre}:\n"

    for atributo, valor in carta.items():
        resultado += f"{atributo}: {valor}\n"

    return resultado

def sacar_carta_de_cada_jugador(mazo_jugadores: dict):
    cartas_sacadas = []
    for jugador, mazo in mazo_jugadores.items():
        carta = mazo.pop(0)  
        cartas_sacadas.append(carta)
    return tuple(cartas_sacadas)


def mostrar_carta_jugadores(carta1: dict, carta2: dict, datos_jugadores: dict) -> None:
    cartas = {"jugador1": carta1, "jugador2": carta2}
    for jugador, carta in cartas.items():
        mostrar_carta(carta, datos_jugadores[jugador]["nombre"])


def jugar_ronda(ronda: int, datos_jugadores: dict, mazo_jugadores: dict, mesas: list) -> str:
    
    print(f"\nRonda: {ronda}")
    
    carta1, carta2 = sacar_carta_de_cada_jugador(mazo_jugadores)
    
    atributo_elegido = elegir_atributo_aleatorio(atributos)
    print(f"Atributo elegido: {atributo_elegido}")
    
    resultado_comparacion = comparar_cartas(carta1, carta2, atributo_elegido)
    
    mostrar_carta_jugadores(carta1, carta2, datos_jugadores)

    ganador = ganador_ronda(resultado_comparacion, carta1, carta2, datos_jugadores, mazo_jugadores, mesas, atributo_elegido)
    return ganador


def verificar_condiciones_de_victoria(datos_jugadores, mazo_jugadores, ronda, max_rondas):
    ganador_final = None
    razon_victoria = ""

    ganador_por_cartas = verificar_ganador_por_cartas(mazo_jugadores)
    ganador_por_rondas = verificar_ganador_por_rondas(mazo_jugadores, ronda, max_rondas)
    ganador_por_victorias_elementales = verificar_victorias_elementales(datos_jugadores)

    if ganador_por_cartas:
        razon_victoria = "Se quedó con todas las cartas."
        ganador_final = ganador_por_cartas

    elif ganador_por_rondas:
        razon_victoria = f"Tiene más cartas tras {max_rondas} rondas."
        ganador_final = ganador_por_rondas

    elif ganador_por_victorias_elementales:
        razon_victoria = "Logró 10 victorias elementales."
        ganador_final = ganador_por_victorias_elementales

    resultado = (ganador_final, razon_victoria)
    return resultado


def ejecutar_juego():
   
    datos_jugadores = obtener_jugadores()
    mazo_jugadores = preparar_mazo()
    mesas = []
    max_rondas =250
    ronda = 1
    
    while ronda <= max_rondas:
        jugar_ronda(ronda, datos_jugadores, mazo_jugadores, mesas)
        ganador_final = verificar_condiciones_de_victoria(datos_jugadores, mazo_jugadores, ronda, max_rondas)
        if ganador_final:
            guardar_datos_jugadores(datos_jugadores,ganador_final)
            break
        ronda += 1
        
    
   