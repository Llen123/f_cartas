import pygame
import os
from juego import *

# Inicializar Pygame
pygame.init()

# Configuración de la ventana
screen = pygame.display.set_mode((1280, 720))
pygame.display.set_caption("Juego de Cartas Pokémon")

# Colores
GREEN = (34, 139, 34)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY = (200, 200, 200)
COLOR_VENTANA = (50, 50, 50)  # Gris oscuro
COLOR_BORDE = (0, 0, 0)       # Negro
COLOR_BOTON = (0, 128, 0)     # Verde
COLOR_BOTON_HOVER = (0, 200, 0)  # Verde más claro
COLOR_TEXTO = (255, 255, 255) # Blanco

# Fuente
font = pygame.font.Font(None, 36)

# Cargar imágenes de los Pokémon
def cargar_imagenes_pokemon():
    imagenes = {}
    nombres_pokemon = [
        "aerodactyl", "arcanine", "blastoise", "charizard", "charmander",
        "dragonite", "dugtrio", "electabuzz", "fearow", "flareon",
        "geodude", "golem", "gyarados", "jolteon", "lapras",
        "moltres", "onix", "pidgeot", "pidgeotto", "pikachu",
        "raichu", "sandslash", "squirtle", "vaporeon", "zapdos"
    ]
    for nombre in nombres_pokemon:
        ruta_imagen = os.path.join('imagenes', f"{nombre}.png")
        if os.path.exists(ruta_imagen):
            imagenes[nombre.lower()] = pygame.image.load(ruta_imagen)
        else:
            print(f"Advertencia: No se encontró la imagen {ruta_imagen}")
    return imagenes

# Función para dibujar una carta en pantalla
def draw_card(x, y, carta, imagenes_pokemon):
    # Dibujar el rectángulo de la carta
    pygame.draw.rect(screen, WHITE, (x, y, 300, 400), border_radius=10)
    pygame.draw.rect(screen, BLACK, (x, y, 300, 400), 3, border_radius=10)

    # Mostrar el nombre de la carta en la parte superior
    nombre_pokemon = carta.get('nombre', 'Desconocido')
    texto_nombre = font.render(nombre_pokemon, True, BLACK)
    screen.blit(texto_nombre, (x + 10, y + 10))  # Posición del nombre

    # Mostrar la imagen del Pokémon
    pokemon_nombre = carta.get('nombre')  # Obtener el nombre del Pokémon
    if pokemon_nombre and pokemon_nombre.lower() in imagenes_pokemon:
        imagen = imagenes_pokemon[pokemon_nombre.lower()]
        imagen = pygame.transform.scale(imagen, (200, 200))  # Reducir el tamaño de la imagen
        screen.blit(imagen, (x + 50, y + 50))  # Posición de la imagen
    else:
        print(f"Advertencia: No se encontró la imagen para el Pokémon {pokemon_nombre}")

    # Mostrar atributos de la carta
    offset_y = 260  # Empezar a mostrar los atributos debajo de la imagen
    for atributo, valor in carta.items():
        if atributo != 'nombre':  # Excluir el campo 'nombre' de los atributos mostrados
            texto = font.render(f"{atributo.capitalize()}: {valor}", True, BLACK)
            screen.blit(texto, (x + 10, y + offset_y))
            offset_y += 25  # Espacio entre atributos

# Función para mostrar texto en la pantalla
def mostrar_texto(texto, x, y, color=BLACK):
    texto_renderizado = font.render(texto, True, color)
    screen.blit(texto_renderizado, (x, y))

# Función para dibujar un cuadro de texto
def dibujar_cuadro_texto(x, y, ancho, alto, texto, activo):
    color = WHITE if activo else GRAY
    pygame.draw.rect(screen, color, (x, y, ancho, alto), 2)
    texto_surface = font.render(texto, True, BLACK)
    screen.blit(texto_surface, (x + 10, y + 10))

# Función para pedir nombres de los jugadores
def pedir_nombres():
    nombres = {"jugador1": "", "jugador2": ""}
    jugador_actual = "jugador1"
    input_activo = True
    max_caracteres = 15  # Límite de caracteres

    # Coordenadas y dimensiones de los cuadros de texto
    cuadro_ancho = 480
    cuadro_alto = 50
    cuadro_x = 400
    cuadro_y1 = 200  # Posición del primer cuadro
    cuadro_y2 = 300  # Posición del segundo cuadro

    while input_activo:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return None

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:  # Presionar Enter para confirmar
                    if jugador_actual == "jugador1":
                        jugador_actual = "jugador2"
                    else:
                        input_activo = False
                elif event.key == pygame.K_BACKSPACE:  # Borrar caracteres
                    nombres[jugador_actual] = nombres[jugador_actual][:-1]
                else:
                    # Añadir caracteres si no se supera el límite
                    if len(nombres[jugador_actual]) < max_caracteres:
                        nombres[jugador_actual] += event.unicode

            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                # Verificar si se hizo clic en el primer cuadro de texto
                if (cuadro_x <= mouse_pos[0] <= cuadro_x + cuadro_ancho and
                    cuadro_y1 <= mouse_pos[1] <= cuadro_y1 + cuadro_alto):
                    jugador_actual = "jugador1"
                # Verificar si se hizo clic en el segundo cuadro de texto
                elif (cuadro_x <= mouse_pos[0] <= cuadro_x + cuadro_ancho and
                      cuadro_y2 <= mouse_pos[1] <= cuadro_y2 + cuadro_alto):
                    jugador_actual = "jugador2"

        # Fondo
        screen.fill(GREEN)

        # Dibujar cuadros de texto
        dibujar_cuadro_texto(cuadro_x, cuadro_y1, cuadro_ancho, cuadro_alto, nombres["jugador1"], jugador_actual == "jugador1")
        dibujar_cuadro_texto(cuadro_x, cuadro_y2, cuadro_ancho, cuadro_alto, nombres["jugador2"], jugador_actual == "jugador2")

        # Mostrar instrucciones
        mostrar_texto("Ingresa los nombres de los jugadores", 200, 100)
        mostrar_texto(f"Máximo {max_caracteres} caracteres", 200, 130)
        mostrar_texto("Haz clic en un cuadro para seleccionarlo", 200, 160)

        # Actualizar pantalla
        pygame.display.update()

    return nombres

def mostrar_ventana_ganador(ganador_final, datos_jugadores):
    # Configuración de la ventana emergente
    ventana_ancho = 600
    ventana_alto = 300
    ventana_x = (1280 - ventana_ancho) // 2
    ventana_y = (720 - ventana_alto) // 2

    # Animación de la ventana
    animar_ventana(ventana_x, ventana_y, ventana_ancho, ventana_alto)

    # Dibujar la ventana emergente
    pygame.draw.rect(screen, COLOR_VENTANA, (ventana_x, ventana_y, ventana_ancho, ventana_alto))
    pygame.draw.rect(screen, COLOR_BORDE, (ventana_x, ventana_y, ventana_ancho, ventana_alto), 3)  # Borde negro

    # Obtener el nombre del ganador
    nombre_ganador = datos_jugadores[ganador_final[0]]["nombre"]

    # Mostrar el nombre del ganador en el primer renglón
    mensaje_ganador = f"El ganador es {nombre_ganador}"
    texto_ganador = font.render(mensaje_ganador, True, COLOR_TEXTO)
    texto_ganador_rect = texto_ganador.get_rect(center=(ventana_x + ventana_ancho // 2, ventana_y + 50))
    screen.blit(texto_ganador, texto_ganador_rect)

    # Mostrar la condición de victoria en el segundo renglón
    mensaje_condicion = f"{ganador_final[1]}"
    texto_condicion = font.render(mensaje_condicion, True, COLOR_TEXTO)
    texto_condicion_rect = texto_condicion.get_rect(center=(ventana_x + ventana_ancho // 2, ventana_y + 100))
    screen.blit(texto_condicion, texto_condicion_rect)

    # Dibujar el botón para reiniciar
    boton_ancho = 200
    boton_alto = 50
    boton_x = ventana_x + (ventana_ancho - boton_ancho) // 2
    boton_y = ventana_y + 200
    boton_rect = pygame.Rect(boton_x, boton_y, boton_ancho, boton_alto)

    # Bucle para esperar la interacción del usuario
    while True:
        # Obtener la posición del mouse
        mouse_pos = pygame.mouse.get_pos()

        # Dibujar el botón con el efecto hover
        if boton_rect.collidepoint(mouse_pos):
            pygame.draw.rect(screen, COLOR_BOTON_HOVER, boton_rect)  # Botón hover
        else:
            pygame.draw.rect(screen, COLOR_BOTON, boton_rect)  # Botón normal

        # Mostrar el texto "Volver a jugar" centrado en el botón
        texto_boton = font.render("Volver a jugar", True, COLOR_TEXTO)
        texto_boton_rect = texto_boton.get_rect(center=(boton_x + boton_ancho // 2, boton_y + boton_alto // 2))
        screen.blit(texto_boton, texto_boton_rect)

        # Actualizar pantalla
        pygame.display.update()

        # Manejar eventos
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return False  # Salir del juego
            if event.type == pygame.MOUSEBUTTONDOWN:
                if boton_rect.collidepoint(event.pos):
                    return True  # Reiniciar el juego

# Función principal del juego
def animar_ventana(ventana_x, ventana_y, ventana_ancho, ventana_alto):
    # Posición inicial (fuera de la pantalla)
    y_inicial = -ventana_alto
    y_final = ventana_y
    velocidad = 10  # Velocidad de la animación
    # Mover la ventana gradualmente
    for y in range(y_inicial, y_final, velocidad):
        screen.fill(GREEN)  # Limpiar la pantalla
        pygame.draw.rect(screen, COLOR_VENTANA, (ventana_x, y, ventana_ancho, ventana_alto))
        pygame.draw.rect(screen, COLOR_BORDE, (ventana_x, y, ventana_ancho, ventana_alto), 3)
        pygame.display.update()
        pygame.time.delay(30)  # Controlar la velocidad de la animación

# Definir botones de velocidad
boton_rapido = pygame.Rect(1000, 10, 80, 40)  # (x, y, ancho, alto)
boton_normal = pygame.Rect(1000, 60, 80, 40)
boton_lento = pygame.Rect(1000, 110, 80, 40)



def main():
    # Cargar imágenes de los Pokémon
    imagenes_pokemon = cargar_imagenes_pokemon()

    # Pedir nombres de los jugadores
    nombres = pedir_nombres()
    if not nombres:
        return

    # Inicializar el juego con los nombres ingresados
    datos_jugadores = {
        "jugador1": {"nombre": nombres["jugador1"], "puntuacion": 0, "Victorias Elementales": 0},
        "jugador2": {"nombre": nombres["jugador2"], "puntuacion": 0, "Victorias Elementales": 0},
    }
    mazo_jugadores = preparar_mazo()
    mesas = []
    max_rondas = 250
    ronda = 1

    # Variables para controlar el estado del juego
    estado_juego = "jugando"
    ganador_final = None
    atributo_elegido = None
    resultado_comparacion = None

    # Configurar temporizador para avanzar las rondas automáticamente
    AVANZAR_RONDA = pygame.USEREVENT + 1
    pygame.time.set_timer(AVANZAR_RONDA, 1000)  # Avanzar cada 1000 ms (1 segundo)

    # Definir botones de velocidad
    boton_rapido = pygame.Rect(1000, 10, 80, 40)  # (x, y, ancho, alto)
    boton_normal = pygame.Rect(1000, 60, 80, 40)
    boton_lento = pygame.Rect(1000, 110, 80, 40)

    # Bucle principal del juego
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            # Detectar clics en los botones de velocidad
            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                if boton_rapido.collidepoint(mouse_pos):
                    pygame.time.set_timer(AVANZAR_RONDA, 100)  # 100 ms
                elif boton_normal.collidepoint(mouse_pos):
                    pygame.time.set_timer(AVANZAR_RONDA, 500)  # 500 ms
                elif boton_lento.collidepoint(mouse_pos):
                    pygame.time.set_timer(AVANZAR_RONDA, 1000)  # 1000 ms

            # Avanzar automáticamente las rondas
            if event.type == AVANZAR_RONDA and estado_juego == "jugando":
                print(f"Iniciando ronda {ronda}")  # Depuración
                resultado_ronda = jugar_ronda(ronda, datos_jugadores, mazo_jugadores, mesas)
    
                # Acceder a los valores del diccionario
                ganador_ronda = resultado_ronda["ganador"]
                nombre_ganador = resultado_ronda["nombre_ganador"]  # Nombre del ganador
                atributo_elegido = resultado_ronda["atributo_elegido"]
                resultado_comparacion = resultado_ronda["resultado_comparacion"]

                # Depuración: Verificar el estado del mazo
                print(f"Mazo jugador 1: {mazo_jugadores['jugador1']}")
                print(f"Mazo jugador 2: {mazo_jugadores['jugador2']}")

                # Verificar condiciones de victoria
                ganador_final = verificar_condiciones_de_victoria(datos_jugadores, mazo_jugadores, ronda, max_rondas)
                if ganador_final[0]:
                    print(f"¡Ganador final: {ganador_final[0]}!")  # Depuración
                    estado_juego = "fin"
                    guardar_datos_jugadores(datos_jugadores, ganador_final[0])  # Guardar datos del ganador
                else:
                    estado_juego = "resultado"
                    ronda += 1

            # Volver automáticamente al estado "jugando" después de mostrar el resultado
            if event.type == AVANZAR_RONDA and estado_juego == "resultado":
                estado_juego = "jugando"

        # Fondo
        screen.fill(GREEN)

        # Dibujar cartas de cada jugador
        if mazo_jugadores["jugador1"] and mazo_jugadores["jugador2"]:
            carta_jugador1 = mazo_jugadores["jugador1"][0]
            carta_jugador2 = mazo_jugadores["jugador2"][0]

            # Dibujar las cartas
            draw_card(200, 160, carta_jugador1, imagenes_pokemon)  # Carta del jugador 1
            draw_card(800, 160, carta_jugador2, imagenes_pokemon)  # Carta del jugador 2

        # Dibujar botones de velocidad
        pygame.draw.rect(screen, COLOR_BOTON, boton_rapido)
        pygame.draw.rect(screen, COLOR_BOTON, boton_normal)
        pygame.draw.rect(screen, COLOR_BOTON, boton_lento)

        # Mostrar etiquetas de los botones
        mostrar_texto("Rápido", boton_rapido.x + 10, boton_rapido.y + 10, COLOR_TEXTO)
        mostrar_texto("Normal", boton_normal.x + 10, boton_normal.y + 10, COLOR_TEXTO)
        mostrar_texto("Lento", boton_lento.x + 10, boton_lento.y + 10, COLOR_TEXTO)

        # Mostrar información de la ronda
        mostrar_texto(f"Ronda: {ronda}", 10, 10)
        if atributo_elegido:
            mostrar_texto(f"Atributo elegido: {atributo_elegido}", 10, 50)
        if resultado_comparacion:
            mostrar_texto(f"Ganador de la ronda actual: {resultado_ronda['nombre_ganador']}", 10, 90)

        # Mostrar ventana emergente si el juego termina
        if estado_juego == "fin":
            if mostrar_ventana_ganador(ganador_final, datos_jugadores):  # Pasar datos_jugadores aquí
                main()  # Reiniciar el juego
            else:
                running = False  # Salir del juego

        # Actualizar pantalla
        pygame.display.update()

    # Salir de Pygame
    pygame.quit()

# Ejecutar el juego
if __name__ == "__main__":
    main()