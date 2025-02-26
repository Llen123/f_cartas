import pygame
import os
from juego import *
from ordenamiento import *
from datos_globales import *
from utilities import mostrar_texto

pygame.init()

pantalla = pygame.display.set_mode((1280, 720))
pygame.display.set_caption("Juego de Cartas Pokémon")
fuente = pygame.font.Font(None, 36)

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

    ruta_fondo = os.path.join('imagenes', 'fondo_estadio.png')
    if os.path.exists(ruta_fondo):
        fondo_estadio = pygame.image.load(ruta_fondo)
    else:
        print(f"Advertencia: No se encontró la imagen {ruta_fondo}")
        fondo_estadio = None

    return imagenes, fondo_estadio

def dibujar_carta(x, y, carta, imagenes_pokemon):
    pygame.draw.rect(pantalla, BLANCO, (x, y, 300, 400), border_radius=10)
    pygame.draw.rect(pantalla, NEGRO, (x, y, 300, 400), 3, border_radius=10)

    nombre_pokemon = carta.get('nombre', 'Desconocido')
    texto_nombre = fuente.render(nombre_pokemon, True, NEGRO)
    pantalla.blit(texto_nombre, (x + 10, y + 10))  

    pokemon_nombre = carta.get('nombre')  
    if pokemon_nombre and pokemon_nombre.lower() in imagenes_pokemon:
        imagen = imagenes_pokemon[pokemon_nombre.lower()]
        imagen = pygame.transform.scale(imagen, (200, 200))  
        pantalla.blit(imagen, (x + 50, y + 50))  
    else:
        print(f"no se encontro la imagen de {pokemon_nombre}")

    offset_y = 260  
    for atributo, valor in carta.items():
        if atributo != 'nombre':  
            texto = fuente.render(f"{atributo.capitalize()}: {valor}", True, NEGRO)
            pantalla.blit(texto, (x + 10, y + offset_y))
            offset_y += 25  

def dibujar_cuadro_texto(x, y, ancho, alto, texto, activo):
    color = BLANCO if activo else GRIS
    pygame.draw.rect(pantalla, color, (x, y, ancho, alto), 2)
    texto_surface = fuente.render(texto, True, NEGRO)
    pantalla.blit(texto_surface, (x + 10, y + 10))

def pedir_nombres():
    nombres = {"jugador1": "", "jugador2": ""}
    jugador_actual = "jugador1"
    input_activo = True
    max_caracteres = 15  

    cuadro_ancho = 400
    cuadro_alto = 50
    cuadro_x = (ANCHO_PANTALLA - cuadro_ancho) // 2  
    cuadro_y1 = (ALTO_PANTALLA // 2) - 100  
    cuadro_y2 = (ALTO_PANTALLA // 2) + 20  

    boton_continuar = pygame.Rect(cuadro_x, cuadro_y2 + 100, cuadro_ancho, cuadro_alto)  
    boton_menu = pygame.Rect(cuadro_x, cuadro_y2 + 160, cuadro_ancho, cuadro_alto)  

    while input_activo:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return None

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:  
                    if jugador_actual == "jugador1":
                        jugador_actual = "jugador2"
                    else:
                        input_activo = False
                elif event.key == pygame.K_BACKSPACE:  
                    nombres[jugador_actual] = nombres[jugador_actual][:-1]
                else:
                    if len(nombres[jugador_actual]) < max_caracteres:
                        nombres[jugador_actual] += event.unicode

            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                
                if (cuadro_x <= mouse_pos[0] <= cuadro_x + cuadro_ancho and
                    cuadro_y1 <= mouse_pos[1] <= cuadro_y1 + cuadro_alto):
                    jugador_actual = "jugador1"
                
                elif (cuadro_x <= mouse_pos[0] <= cuadro_x + cuadro_ancho and
                      cuadro_y2 <= mouse_pos[1] <= cuadro_y2 + cuadro_alto):
                    jugador_actual = "jugador2"
                
                elif boton_continuar.collidepoint(mouse_pos):
                    if nombres["jugador1"] and nombres["jugador2"]: 
                        input_activo = False

                elif boton_menu.collidepoint(mouse_pos):
                    return "menu"  

        pantalla.fill(VERDE)
        dibujar_cuadro_texto(cuadro_x, cuadro_y1, cuadro_ancho, cuadro_alto, nombres["jugador1"], jugador_actual == "jugador1")
        dibujar_cuadro_texto(cuadro_x, cuadro_y2, cuadro_ancho, cuadro_alto, nombres["jugador2"], jugador_actual == "jugador2")

        pygame.draw.rect(pantalla, COLOR_BOTON, boton_continuar)
        texto_continuar = fuente.render("Continuar", True, BLANCO)
        texto_continuar_rect = texto_continuar.get_rect(center=boton_continuar.center)
        pantalla.blit(texto_continuar, texto_continuar_rect)

        pygame.draw.rect(pantalla, COLOR_BOTON, boton_menu)
        texto_volver = fuente.render("Volver al Menú", True, BLANCO)
        texto_volver_rect = texto_volver.get_rect(center=boton_menu.center)
        pantalla.blit(texto_volver, texto_volver_rect)

        texto_instrucciones = fuente.render("Ingresa los nombres de los jugadores", True, NEGRO)
        texto_instrucciones_rect = texto_instrucciones.get_rect(center=(ANCHO_PANTALLA // 2, cuadro_y1 - 50))
        pantalla.blit(texto_instrucciones, texto_instrucciones_rect)

        texto_limite = fuente.render(f"Máximo {max_caracteres} caracteres", True, NEGRO)
        texto_limite_rect = texto_limite.get_rect(center=(ANCHO_PANTALLA // 2, cuadro_y1 - 20))
        pantalla.blit(texto_limite, texto_limite_rect)

        pygame.display.update()

    return nombres

def mostrar_ventana_ganador(ganador_final, datos_jugadores):
    ventana_ancho = 600
    ventana_alto = 300
    ventana_x = (1280 - ventana_ancho) // 2
    ventana_y = (720 - ventana_alto) // 2

    pygame.draw.rect(pantalla, COLOR_VENTANA, (ventana_x, ventana_y, ventana_ancho, ventana_alto))
    pygame.draw.rect(pantalla, NEGRO, (ventana_x, ventana_y, ventana_ancho, ventana_alto), 3)

    if ganador_final[0]:
        nombre_ganador = datos_jugadores[ganador_final[0]]["nombre"]
        mensaje_ganador = f"El ganador es {nombre_ganador}"
        mensaje_condicion = f"{ganador_final[1]}"
    else:
        mensaje_ganador = "¡Empate!"
        mensaje_condicion = ganador_final[1]

    texto_ganador = fuente.render(mensaje_ganador, True, BLANCO)
    texto_ganador_rect = texto_ganador.get_rect(center=(ventana_x + ventana_ancho // 2, ventana_y + 50))
    pantalla.blit(texto_ganador, texto_ganador_rect)

    texto_condicion = fuente.render(mensaje_condicion, True, BLANCO)
    texto_condicion_rect = texto_condicion.get_rect(center=(ventana_x + ventana_ancho // 2, ventana_y + 100))
    pantalla.blit(texto_condicion, texto_condicion_rect)

    boton_reiniciar = pygame.Rect(ventana_x + 50, ventana_y + 200, 200, 50)
    pygame.draw.rect(pantalla, COLOR_BOTON, boton_reiniciar)
    texto_reiniciar = fuente.render("Volver a jugar", True, BLANCO)
    pantalla.blit(texto_reiniciar, (boton_reiniciar.x + 10, boton_reiniciar.y + 10))

    boton_menu = pygame.Rect(ventana_x + 300, ventana_y + 200, 200, 50)
    pygame.draw.rect(pantalla, COLOR_BOTON, boton_menu)
    texto_menu = fuente.render("Menú principal", True, BLANCO)
    pantalla.blit(texto_menu, (boton_menu.x + 10, boton_menu.y + 10))

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return "salir"
            if event.type == pygame.MOUSEBUTTONDOWN:
                if boton_reiniciar.collidepoint(event.pos):
                    return "reiniciar"
                if boton_menu.collidepoint(event.pos):
                    return "menu"

        pygame.display.update()

def animar_ventana(ventana_x, ventana_y, ventana_ancho, ventana_alto):
    y_inicial = -ventana_alto
    y_final = ventana_y
    velocidad = 10
    for y in range(y_inicial, y_final, velocidad):
        pantalla.fill(VERDE)
        pygame.draw.rect(pantalla, COLOR_VENTANA, (ventana_x, y, ventana_ancho, ventana_alto))
        pygame.draw.rect(pantalla, NEGRO, (ventana_x, y, ventana_ancho, ventana_alto), 3)
        pygame.display.update()
        pygame.time.delay(30)

def mostrar_tabla_posiciones(criterio, orden):
    tabla_pantalla = pygame.display.set_mode((1280, 720))
    pygame.display.set_caption("Tabla de Posiciones")

    fondo_tabla = pygame.image.load("imagenes/fondo_tabla.png")
    fondo_tabla = pygame.transform.scale(fondo_tabla, (1280, 720))

    fuente = pygame.font.Font(None, 36)

    archivo_json = "historial_partidas.json"
    historial_partidas = manejar_archivo_json(archivo_json, "leer")
    jugadores_del_historial = obtener_jugadores_del_historial(historial_partidas)
    jugadores_ordenados = bubble_sort(jugadores_del_historial, criterio, orden)

    boton_menu = pygame.Rect(500, 600, 280, 50)
    pygame.draw.rect(tabla_pantalla, COLOR_BOTON, boton_menu)

    texto_volver = fuente.render("Volver al Menú", True, BLANCO)
    texto_volver_rect = texto_volver.get_rect(center=boton_menu.center)
    tabla_pantalla.blit(texto_volver, texto_volver_rect)

    running = True
    while running:
        tabla_pantalla.blit(fondo_tabla, (0, 0))
        mostrar_texto("Tabla de Posiciones", 500, 50, BLANCO, tabla_pantalla, fuente)

        y = 150
        contador = 0

        for i, jugador in enumerate(jugadores_ordenados):
            if i >= 6:
                break

            texto_fecha = f"Fecha: {jugador['Fecha Partida']}"
            texto_nombre = f"Nombre: {jugador['nombre']}"
            texto_puntuacion = f"Puntuación: {jugador['puntuacion']}"
            texto_victorias = f"Victorias Elementales: {jugador['Victorias Elementales']}"

            if i < 3:
                x = 200
            else:
                x = 800

            mostrar_texto(texto_fecha, x, y, BLANCO, tabla_pantalla, fuente)
            y += 30
            mostrar_texto(texto_nombre, x, y, BLANCO, tabla_pantalla, fuente)
            y += 30
            mostrar_texto(texto_puntuacion, x, y, BLANCO, tabla_pantalla, fuente)
            y += 30
            mostrar_texto(texto_victorias, x, y, BLANCO, tabla_pantalla, fuente)
            y += 40

            contador += 1
            if contador == 3:
                y = 150

        pygame.draw.rect(tabla_pantalla, COLOR_BOTON, boton_menu)
        texto_volver = fuente.render("Volver al Menú", True, BLANCO)
        texto_volver_rect = texto_volver.get_rect(center=boton_menu.center)
        tabla_pantalla.blit(texto_volver, texto_volver_rect)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                if boton_menu.collidepoint(event.pos):
                    running = False

        pygame.display.update()

    pygame.display.set_mode((ANCHO_PANTALLA, ALTO_PANTALLA))

def main():
    imagenes_pokemon, fondo_estadio = cargar_imagenes_pokemon()

    nombres = pedir_nombres()
    if nombres == "menu":
        from menu_pygame import menu_principal
        menu_principal()
        return
    elif not nombres:
        return

    datos_jugadores = {
        "jugador1": {"nombre": nombres["jugador1"], "puntuacion": 0, "Victorias Elementales": 0},
        "jugador2": {"nombre": nombres["jugador2"], "puntuacion": 0, "Victorias Elementales": 0},
    }
    mazo_jugadores = preparar_mazo()
    mesas = []
    max_rondas = 250
    ronda = 1

    estado_juego = "jugando"
    ganador_final = None
    atributo_elegido = None
    resultado_comparacion = None

    AVANZAR_RONDA = pygame.USEREVENT + 1
    pygame.time.set_timer(AVANZAR_RONDA, 1000)

    boton_rapido = pygame.Rect(1000, 10, 120, 40)
    boton_normal = pygame.Rect(1000, 60, 120, 40)
    boton_lento = pygame.Rect(1000, 110, 120, 40)

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                if boton_rapido.collidepoint(mouse_pos):
                    pygame.time.set_timer(AVANZAR_RONDA, 100)
                elif boton_normal.collidepoint(mouse_pos):
                    pygame.time.set_timer(AVANZAR_RONDA, 500)
                elif boton_lento.collidepoint(mouse_pos):
                    pygame.time.set_timer(AVANZAR_RONDA, 1000)

            if event.type == AVANZAR_RONDA and estado_juego == "jugando":
                print(f"Iniciando ronda {ronda}")
                resultado_ronda = jugar_ronda(ronda, datos_jugadores, mazo_jugadores, mesas)

                ganador_ronda = resultado_ronda["ganador"]
                nombre_ganador = resultado_ronda["nombre_ganador"]
                atributo_elegido = resultado_ronda["atributo_elegido"]
                resultado_comparacion = resultado_ronda["resultado_comparacion"]

                print(f"Mazo jugador 1: {mazo_jugadores['jugador1']}")
                print(f"Mazo jugador 2: {mazo_jugadores['jugador2']}")

                ganador_final = verificar_condiciones_de_victoria(datos_jugadores, mazo_jugadores, ronda, max_rondas)
                if ganador_final[0]:
                    print(f"¡Ganador final: {ganador_final[0]}!")
                    estado_juego = "fin"
                    guardar_datos_jugadores(datos_jugadores, ganador_final[0])
                elif ganador_final[0] is None and ganador_final[1]:
                    print("¡Empate!")
                    estado_juego = "fin"
                    guardar_datos_jugadores(datos_jugadores, None)
                else:
                    estado_juego = "resultado"
                    ronda += 1

            if event.type == AVANZAR_RONDA and estado_juego == "resultado":
                estado_juego = "jugando"

        if fondo_estadio:
            pantalla.blit(fondo_estadio, (0, 0))
        else:
            pantalla.fill(VERDE)

        if mazo_jugadores["jugador1"] and mazo_jugadores["jugador2"]:
            carta_jugador1 = mazo_jugadores["jugador1"][0]
            carta_jugador2 = mazo_jugadores["jugador2"][0]

            dibujar_carta(200, 160, carta_jugador1, imagenes_pokemon)
            dibujar_carta(800, 160, carta_jugador2, imagenes_pokemon)

        pygame.draw.rect(pantalla, COLOR_BOTON, boton_rapido)
        pygame.draw.rect(pantalla, COLOR_BOTON, boton_normal)
        pygame.draw.rect(pantalla, COLOR_BOTON, boton_lento)

        mostrar_texto("Rápido", boton_rapido.x + 10, boton_rapido.y + 10, BLANCO, pantalla, fuente)
        mostrar_texto("Normal", boton_normal.x + 10, boton_normal.y + 10, BLANCO, pantalla, fuente)
        mostrar_texto("Lento", boton_lento.x + 10, boton_lento.y + 10, BLANCO, pantalla, fuente)

        mostrar_texto(f"Ronda: {ronda}", 10, 10, BLANCO, pantalla, fuente)
        if atributo_elegido:
            mostrar_texto(f"Atributo elegido: {atributo_elegido}", 10, 50, BLANCO, pantalla, fuente)
        if resultado_comparacion:
            if resultado_ronda["ganador"]:
                mostrar_texto(f"Ganador de la ronda actual: {resultado_ronda['nombre_ganador']}", 10, 90, BLANCO, pantalla, fuente)
            else:
                mostrar_texto(resultado_ronda["resultado_comparacion"], 10, 90, BLANCO, pantalla, fuente)

        if estado_juego == "fin":
            resultado = mostrar_ventana_ganador(ganador_final, datos_jugadores)  

            if resultado == "reiniciar":
                main()  
            elif resultado == "menu":
                from menu_pygame import menu_principal
                menu_principal()  
                running = False  
            elif resultado == "salir":
                running = False  

        pygame.display.update()

    pygame.quit()

if __name__ == "__main__":
    main()