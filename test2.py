import pygame
from time import sleep
from mazo import *
from jugadores import *
from tateti import jugar_tateti
from juego import *
import os

# Create a global dictionary to cache sprites
sprite_cache = {}

def cargar_sprite(nombre_pokemon, tamano=(180, 150)):
    """
    Función para cargar y escalar un sprite de Pokemon
    
    Args:
        nombre_pokemon (str): Nombre del Pokemon
        tamano (tuple): Tamaño deseado para el sprite
    
    Returns:
        pygame.Surface: Sprite escalado o None si no se encuentra
    """
    # Normalizar el nombre (lowercase)
    nombre_pokemon = nombre_pokemon.lower()
    
    # Verificar si el sprite ya está en caché
    if nombre_pokemon in sprite_cache:
        return sprite_cache[nombre_pokemon]
    
    try:
        # Construir la ruta del archivo
        ruta_sprite = os.path.join("imagenes", f"{nombre_pokemon}.png")
        
        # Cargar y escalar el sprite
        sprite = pygame.image.load(ruta_sprite)
        sprite_escalado = pygame.transform.scale(sprite, tamano)
        
        # Guardar en caché
        sprite_cache[nombre_pokemon] = sprite_escalado
        
        return sprite_escalado
    
    except FileNotFoundError:
        # Retorna None si no se encuentra la imagen
        return None

def renderizar_carta(pantalla, carta, pos_x, pos_y, fuente, nombre_jugador):
    # Aumentar el alto de la carta
    CARTA_ANCHO = 200
    CARTA_ALTO = 350  # Aumentado de 260 a 350

    # Dibujar el fondo blanco de la carta con nuevo alto
    pygame.draw.rect(pantalla, (255, 255, 255), (pos_x, pos_y, CARTA_ANCHO, CARTA_ALTO))
    pygame.draw.rect(pantalla, (0, 0, 0), (pos_x, pos_y, CARTA_ANCHO, CARTA_ALTO), 2)

    # Intentar cargar el sprite
    sprite = cargar_sprite(carta['nombre'], tamano=(180, 200))  # Ajustar tamaño del sprite
    
    if sprite:
        # Dibujar el sprite más arriba
        pantalla.blit(sprite, (pos_x + 10, pos_y + 10))
    else:
        # Mostrar texto de error si no se encuentra el sprite
        texto_sin_imagen = fuente.render("Imagen no encontrada", True, (255, 0, 0))
        pantalla.blit(texto_sin_imagen, (pos_x + 10, pos_y + 10))

    # Propiedades de texto (ajustadas para hacer espacio al sprite y al nuevo alto)
    propiedades = [
        (f"Nombre: {carta['nombre']}", pos_x + 10, pos_y + 220),
        (f"Velocidad: {carta['velocidad']}", pos_x + 10, pos_y + 240),
        (f"Fuerza: {carta['fuerza']}", pos_x + 10, pos_y + 260),
        (f"Elemento: {carta['elemento']}", pos_x + 10, pos_y + 280),
        (f"Peso: {carta['peso']:.1f}", pos_x + 10, pos_y + 300),
        (f"Altura: {carta['altura']:.1f}", pos_x + 10, pos_y + 320),
    ]

    for texto, x, y in propiedades:
        texto_renderizado = fuente.render(texto, True, (0, 0, 0))
        pantalla.blit(texto_renderizado, (x, y))

    renderizar_texto(pantalla, nombre_jugador, pos_x + 10, pos_y - 30, fuente)

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

def mostrar_resultado_ronda(pantalla, ganador, fuente):
    texto = f"Ganador de la ronda: {ganador}"
    texto_renderizado = fuente.render(texto, True, (255, 0, 0))
    pantalla.blit(texto_renderizado, (250, 100))  
    pygame.display.flip()
    sleep(0.2)  

def jugar_con_pygame(datos_jugadores, mazo_jugadores):
    pygame.init()
    pantalla = pygame.display.set_mode((800, 600))
    pygame.display.set_caption("Cartas - Juego por Rondas")
    fuente = pygame.font.Font(None, 30)
    reloj = pygame.time.Clock()

    running = True
    ronda = 1
    
    while running:
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                running = False

        if mazo_jugadores["jugador1"] and mazo_jugadores["jugador2"]:
            carta1 = mazo_jugadores["jugador1"].pop(0)
            carta2 = mazo_jugadores["jugador2"].pop(0)
            #print(f"\nRonda {ronda}:")
            #print(mostrar_carta(carta1, datos_jugadores["jugador1"]["nombre"]))
            #print(mostrar_carta(carta2, datos_jugadores["jugador2"]["nombre"]))
#
            atributo_elegido = elegir_atributo_aleatorio(atributos)
            #print(f"Atributo elegido: {atributo_elegido}")

            mostrar_cartas_ronda(pantalla, carta1, carta2, fuente, atributo_elegido, datos_jugadores["jugador1"]["nombre"], datos_jugadores["jugador2"]["nombre"])

            if atributo_elegido == "elemento":
                resultado_tateti = jugar_tateti(carta1, carta2, datos_jugadores)
                if resultado_tateti == "jugador1":
                    ganador = datos_jugadores["jugador1"]["nombre"]
                elif resultado_tateti == "jugador2":
                    ganador = datos_jugadores["jugador2"]["nombre"]
                else:
                    ganador = "Empate"
                
                
                elementos = [carta1["elemento"], carta2["elemento"]]
                tablero = crear_tablero(elementos, 3, 3)
                mostrar_tablero_tateti(pantalla, tablero, fuente)

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

            mostrar_resultado_ronda(pantalla, ganador, fuente)
            ronda += 1
        else:
            print("No quedan cartas en el mazo de algún jugador.")
            running = False

        reloj.tick(30)

    pygame.quit()


