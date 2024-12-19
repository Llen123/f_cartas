import pygame
from time import sleep
from mazo import *
from jugadores import *
from tateti import jugar_tateti
from juego import *
import os
from botones import crear_boton, checkear_accion_botones
# Create a global dictionary to cache sprites
sprite_cache = {}
from botones import crear_boton, checkear_accion_botones

def mostrar_ganador(pantalla, nombre_ganador, razon_victoria, fuente):
    pantalla.fill((0, 0, 0))

    texto_ganador = fuente.render(f"¡{nombre_ganador} es el ganador!", True, (255, 255, 255))
    texto_razon = fuente.render(f"Razón: {razon_victoria}", True, (255, 255, 255))

    pantalla.blit(texto_ganador, (400 - texto_ganador.get_width() // 2, 200))
    pantalla.blit(texto_razon, (400 - texto_razon.get_width() // 2, 250))

    boton_volver = crear_boton( pantalla, (300, 350), (200, 50), print("eldiablo"), texto="Volver", color_texto=(255, 255, 255), fuente=fuente)
    pygame.display.flip()

    esperando = True
    while esperando:
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                esperando = False

            if evento.type == pygame.MOUSEBUTTONDOWN:
                checkear_accion_botones([boton_volver], evento)

            if boton_volver["estado"] == "activo":
                esperando = False


def cargar_sprite(nombre_pokemon, tamano=(140, 120)):
    nombre_pokemon = nombre_pokemon.lower()

    if nombre_pokemon in sprite_cache:
        return sprite_cache[nombre_pokemon]
    
    try:
        ruta_sprite = f"imagenes/{nombre_pokemon}.png"
        sprite = pygame.image.load(ruta_sprite)
        sprite_escalado = pygame.transform.scale(sprite, tamano)
        sprite_cache[nombre_pokemon] = sprite_escalado
        return sprite_escalado
    
    except FileNotFoundError:
        return None

def limitar_texto(texto, max_caracteres):
    if len(texto) > max_caracteres:
        return texto[:max_caracteres - 3] + "..."
    return texto

def renderizar_carta(pantalla, carta, pos_x, pos_y, fuente, nombre_jugador):
    CARTA_ANCHO = 200
    CARTA_ALTO = 320
    MAX_CARACTERES = 20  

    fuente_detalles = pygame.font.Font(None, 24)  

    pygame.draw.rect(pantalla, (255, 255, 255), (pos_x, pos_y, CARTA_ANCHO, CARTA_ALTO))
    pygame.draw.rect(pantalla, (0, 0, 0), (pos_x, pos_y, CARTA_ANCHO, CARTA_ALTO), 2)

    sprite = cargar_sprite(carta['nombre'], tamano=(140, 120))
    
    if sprite:
        pygame.draw.rect(pantalla, (0, 0, 0), (pos_x + 30, pos_y + 10, 140, 120), 2)
        pantalla.blit(sprite, (pos_x + 30, pos_y + 10))
    else:
        texto_sin_imagen = fuente_detalles.render("Imagen no encontrada", True, (255, 0, 0))
        pantalla.blit(texto_sin_imagen, (pos_x + 30, pos_y + 70))

    
    propiedades = [
        (f"Nombre: {limitar_texto(carta['nombre'], MAX_CARACTERES)}", pos_x + 10, pos_y + 140),
        (f"Velocidad: {carta['velocidad']}", pos_x + 10, pos_y + 165),
        (f"Fuerza: {carta['fuerza']}", pos_x + 10, pos_y + 190),
        (f"Elemento: {limitar_texto(str(carta['elemento']), MAX_CARACTERES)}", pos_x + 10, pos_y + 215),
        (f"Peso: {carta['peso']:.1f}", pos_x + 10, pos_y + 240),
        (f"Altura: {carta['altura']:.1f}", pos_x + 10, pos_y + 265),
    ]

    
    for texto, x, y in propiedades:
        texto_renderizado = fuente_detalles.render(texto, True, (0, 0, 0))
        pantalla.blit(texto_renderizado, (x, y))

   
    nombre_limitado = limitar_texto(nombre_jugador, MAX_CARACTERES)
    renderizar_texto(pantalla, nombre_limitado, pos_x + 10, pos_y - 30, fuente)

def set_fps(fps):
    return 1 / fps

def renderizar_texto(pantalla, texto, pos_x, pos_y, fuente):
    texto_renderizado = fuente.render(texto, True, (0, 0, 0))  
    pantalla.blit(texto_renderizado, (pos_x, pos_y))

def mostrar_tablero_tateti(pantalla, tablero, fuente):
    y_pos = 100
    for fila in tablero:
        fila_texto = " | ".join(fila)
        texto_renderizado = fuente.render(fila_texto, True, (0, 0, 0))
        pantalla.blit(texto_renderizado, (200, y_pos))
        y_pos += 40

def mostrar_cartas_ronda(pantalla, carta1, carta2, fuente, atributo_elegido, nombre_jugador1, nombre_jugador2):
    pantalla.fill((34, 139, 34))  
    renderizar_carta(pantalla, carta1, 100, 150, fuente, nombre_jugador1)  # Cambié pos_y de 200 a 150
    renderizar_carta(pantalla, carta2, 400, 150, fuente, nombre_jugador2)  # Cambié pos_y de 200 a 150
    renderizar_texto(pantalla, f"Atributo elegido: {atributo_elegido}", 250, 50, fuente)
    pygame.display.flip()

def mostrar_resultado_ronda(pantalla, ganador, fuente, timeBetweenFrames):
    texto = f"Ganador de la ronda: {ganador}"
    texto_renderizado = fuente.render(texto, True, (255, 0, 0))
    pantalla.blit(texto_renderizado, (250, 100))  
    pygame.display.flip()
    sleep(timeBetweenFrames)

def jugar_con_pygame(datos_jugadores, mazo_jugadores):
    pygame.init()
    pantalla = pygame.display.set_mode((800, 600))
    pygame.display.set_caption("Cartas - Juego por Rondas")
    fuente = pygame.font.Font(None, 30)
    timeBetweenFrames = set_fps(60)

    running = True
    ronda = 1
    
    # Definir variables para evitar errores
    ganador_final = None
    razon_victoria = ""

    while running:
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                running = False

        if mazo_jugadores["jugador1"] and mazo_jugadores["jugador2"]:
            carta1 = mazo_jugadores["jugador1"].pop(0)
            carta2 = mazo_jugadores["jugador2"].pop(0)
            atributo_elegido = elegir_atributo_aleatorio(atributos)
            mostrar_cartas_ronda(pantalla, carta1, carta2, fuente, atributo_elegido, 
                                 datos_jugadores["jugador1"]["nombre"], 
                                 datos_jugadores["jugador2"]["nombre"])

            if atributo_elegido == "elemento":
                resultado_tateti = jugar_tateti(carta1, carta2, datos_jugadores)
                if resultado_tateti == "jugador1":
                    ganador = datos_jugadores["jugador1"]["nombre"]
                elif resultado_tateti == "jugador2":
                    ganador = datos_jugadores["jugador2"]["nombre"]
                else:
                    ganador = "Empate"
            else:
                resultado_comparacion = comparar_cartas(carta1, carta2, atributo_elegido)
                if resultado_comparacion == "carta1":
                    ganador = datos_jugadores["jugador1"]["nombre"]
                    agregar_cartas_a_mazo(mazo_jugadores["jugador1"], carta1, carta2)
                elif resultado_comparacion == "carta2":
                    ganador = datos_jugadores["jugador2"]["nombre"]
                    agregar_cartas_a_mazo(mazo_jugadores["jugador2"], carta1, carta2)
                else:
                    ganador = "Ninguno (Empate)"

            mostrar_resultado_ronda(pantalla, ganador, fuente, timeBetweenFrames)
            ronda += 1

        else:
            # Determinar ganador y razón
            resultado = verificar_condiciones_de_victoria(datos_jugadores, mazo_jugadores, ronda, 250)
            ganador_final, razon_victoria = resultado

            if ganador_final:
                mostrar_ganador(pantalla, datos_jugadores[ganador_final]['nombre'], razon_victoria, fuente)
            running = False

    pygame.quit()


