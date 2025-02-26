import random
import pygame
from mazo import *
from jugadores import *
from tateti import jugar_tateti


def elegir_atributo_aleatorio(carta):
    atributos = ["velocidad", "fuerza", "elemento", "peso", "altura"]

    atributo_elegido = random.choice(atributos)

    return atributo_elegido

def comparar_cartas(carta_jugador1, carta_jugador2, atributo_elegido):
    valor_jugador1 = carta_jugador1.get(atributo_elegido, 0)
    valor_jugador2 = carta_jugador2.get(atributo_elegido, 0)

    if valor_jugador1 > valor_jugador2:
        retorno = "jugador1"
    elif valor_jugador2 > valor_jugador1:
        retorno = "jugador2"
    else:
        retorno = None
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


pygame.init()
font = pygame.font.Font(None, 36)
pantalla = pygame.display.set_mode((1280, 720))

def mostrar_texto(texto, x, y, color, screen, font):
    texto_renderizado = font.render(texto, True, color)
    screen.blit(texto_renderizado, (x, y))