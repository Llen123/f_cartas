import random
from mazo import *
from jugadores import *
from tateti import jugar_tateti
atributos = ["velocidad", "fuerza", "elemento", "peso", "altura"]

def elegir_atributo_aleatorio(atributos: list) -> str:
    
    return random.choice(atributos)

def comparar_cartas(carta1: dict, carta2: dict, atributo: str) -> str:
    
    retorno = "Empate"
    if carta1[atributo] > carta2[atributo]:
            retorno =  "carta1"  
    elif carta2[atributo] > carta1[atributo]:
            retorno =  "carta2"  
    return retorno

def resolver_elemento(carta1: dict, carta2: dict, datos_jugadores: dict) -> str:
    
    resultado_tateti = jugar_tateti(carta1, carta2, datos_jugadores)
    retorno = "Empate"
    
    if resultado_tateti == "jugador1":
        datos_jugadores["jugador1"]["Victorias Elementales"] += 1
        retorno = "jugador1"
    elif resultado_tateti == "jugador2":
        datos_jugadores["jugador2"]["Victorias Elementales"] += 1
        retorno = "jugador2"
    return retorno

def agregar_cartas_a_mazo(mazo: list, carta1: dict, carta2: dict) -> None:
    mazo.extend([carta1, carta2])