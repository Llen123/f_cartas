from utilities import *
from tateti import *

def agregar_a_mesa(pilon_mesa: list, carta1: dict, carta2: dict) -> None:
    
    print("Es un empate, ambas cartas se guardan en el pilón de mesa.")
    agregar_cartas_a_mazo(pilon_mesa, carta1, carta2)

def transferir_cartas(ganador: str, carta1: dict, carta2: dict, mazo_jugadores: dict, datos_jugadores: dict) -> None:
    
    agregar_cartas_a_mazo(mazo_jugadores[ganador], carta1, carta2)
    print(f"{datos_jugadores[ganador]['nombre']} gana la ronda y recibe las cartas")

def resolver_empate(ganador: str, pilon_mesa: list, mazo_jugadores: dict) -> None:
    if ganador == "jugador1":
        mazo_jugadores["jugador1"].extend(pilon_mesa)
    else:
        mazo_jugadores["jugador2"].extend(pilon_mesa)
    
    pilon_mesa.clear()

def verificar_ganador_por_cartas(mazo_jugadores) -> str:
    ganador = None
    if len(mazo_jugadores["jugador1"]) == 0:
        ganador =  "jugador2"
    elif len(mazo_jugadores["jugador2"]) == 0:
        ganador =  "jugador1"
    return ganador

def verificar_ganador_por_rondas(mazo_jugadores: dict, ronda: int, max_ronda: int) -> str:
    
    ganador = None
    if ronda == max_ronda:
        if len(mazo_jugadores["jugador1"]) > len(mazo_jugadores["jugador2"]):
            ganador = "jugador1"
        elif len(mazo_jugadores["jugador2"]) > len(mazo_jugadores["jugador1"]):
            ganador = "jugador2"
        else:
            ganador = "empate"
    return ganador
def verificar_victorias_elementales(datos_jugadores: dict) -> str:
    
    ganador = None
    for jugador in ["jugador1", "jugador2"]:
        if datos_jugadores[jugador]["Victorias Elementales"] >= 10:
            ganador = jugador
    return ganador

def ganador_ronda(resultado: str, carta1: dict, carta2: dict, datos_jugadores: dict, mazo_jugadores: dict, pilon_mesa: list, atributo_elegido: str) -> str:
    
    ganador = None
    
    if atributo_elegido == "elemento":
        resolver_elemento(carta1, carta2, datos_jugadores)
    else:
        
        if resultado == "Empate":
            agregar_a_mesa(pilon_mesa, carta1, carta2)
            
        elif resultado == "carta1":
            ganador = "jugador1"
        elif resultado == "carta2":
            ganador = "jugador2"
        
        if ganador:  
            datos_jugadores[ganador]["puntuacion"] += 1
            transferir_cartas(ganador, carta1, carta2, mazo_jugadores, datos_jugadores)
            resolver_empate(ganador, pilon_mesa, mazo_jugadores)
            

    return ganador




