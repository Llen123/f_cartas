import pygame
import sys
from botones import (
    crear_boton,
    dibujar_botones,
    checkear_accion_botones,
    actualizar_estados_botones
)
from test2 import jugar_con_pygame, preparar_mazo
from jugadores import manejar_archivo_json

def crear_caja_texto(x, y, ancho, alto):
    return {
        "rect": pygame.Rect(x, y, ancho, alto),
        "texto": "",
        "activo": False,
        "color_inactivo": pygame.Color('lightskyblue3'),
        "color_activo": pygame.Color('dodgerblue2'),
        "color": pygame.Color('lightskyblue3')
    }

def manejar_evento_caja(caja, evento):
    if evento.type == pygame.MOUSEBUTTONDOWN:
        if caja["rect"].collidepoint(evento.pos):
            caja["activo"] = True
            caja["color"] = caja["color_activo"]
        else:
            caja["activo"] = False
            caja["color"] = caja["color_inactivo"]
    
    if evento.type == pygame.KEYDOWN and caja["activo"]:
        if evento.key == pygame.K_RETURN:
            return caja["texto"]
        elif evento.key == pygame.K_BACKSPACE:
            caja["texto"] = caja["texto"][:-1]
        else:
            caja["texto"] += evento.unicode
            
    if len(caja["texto"]) > 15:
        caja["texto"] = caja["texto"][:15]
    return None

def dibujar_caja_texto(pantalla, caja, fuente):
    txt_surface = fuente.render(caja["texto"], True, caja["color"])
    width = max(200, txt_surface.get_width()+10)
    caja["rect"].w = width
    pygame.draw.rect(pantalla, caja["color"], caja["rect"], 2)
    pantalla.blit(txt_surface, (caja["rect"].x+5, caja["rect"].y+5))

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


def mostrar_scoreboard():
    pygame.init()
    ANCHO, ALTO = 800, 600
    pantalla = pygame.display.set_mode((ANCHO, ALTO))
    pygame.display.set_caption("Scoreboard")
    
    fuente_titulo = pygame.font.Font(None, 74)
    fuente_texto = pygame.font.Font(None, 32)
    fuente_boton = pygame.font.Font(None, 50)
    VERDE = (34, 139, 34)
    BLANCO = (255, 255, 255)
    
    archivo_json = "historial_partidas.json"
    historial_partidas = manejar_archivo_json(archivo_json, "leer")
    jugadores_del_historial = obtener_jugadores_del_historial(historial_partidas)
    jugadores_ordenados = bubble_sort(jugadores_del_historial, "puntuacion", "desc")
    
    boton_volver = crear_boton(
        pantalla,
        (300, 80),
        (ANCHO//2 - 150, 500),
        crear_menu,
        texto="Volver",
        fuente=fuente_boton,
        color_texto=BLANCO
    )
    
    lista_botones = [boton_volver]
    
    while True:
        pantalla.fill(VERDE)
        texto_titulo = fuente_titulo.render("SCOREBOARD", True, BLANCO)
        pantalla.blit(texto_titulo, (ANCHO//2 - texto_titulo.get_width()//2, 20))
        
        y_pos = 160
        for i, jugador in enumerate(jugadores_ordenados[:5]):
            texto_jugador = fuente_texto.render(
                f"{i+1}. {jugador['nombre']} - Puntos: {jugador['puntuacion']} - "
                f"Fecha: {jugador['Fecha Partida']}", 
                True, 
                BLANCO
            )
            pantalla.blit(texto_jugador, (50, y_pos))
            y_pos += 40
        
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            checkear_accion_botones(lista_botones, evento)
        
        actualizar_estados_botones(lista_botones, pygame.mouse.get_pos())
        dibujar_botones(lista_botones)
        pygame.display.flip()

def continuar_juego(datos):
    caja_jugador1, caja_jugador2 = datos
    nombre_jugador1 = caja_jugador1["texto"]
    nombre_jugador2 = caja_jugador2["texto"]
    
    if nombre_jugador1 and nombre_jugador2:
        datos_jugadores = {
            "jugador1": {"nombre": nombre_jugador1, "puntuacion": 0, "Victorias Elementales": 0},
            "jugador2": {"nombre": nombre_jugador2, "puntuacion": 0, "Victorias Elementales": 0}
        }
        mazo_jugadores = preparar_mazo()
        jugar_con_pygame(datos_jugadores, mazo_jugadores)

def iniciar_juego():
    pygame.init()
    ANCHO, ALTO = 800, 600
    pantalla = pygame.display.set_mode((ANCHO, ALTO))
    pygame.display.set_caption("Ingreso de Nombres")
    
    caja_jugador1 = crear_caja_texto(ANCHO//2 - 100, 200, 200, 32)
    caja_jugador2 = crear_caja_texto(ANCHO//2 - 100, 300, 200, 32)
    
    fuente = pygame.font.Font(None, 32)
    fuente_boton = pygame.font.Font(None, 50)
    VERDE = (34, 139, 34)
    BLANCO = (255, 255, 255)
    
    boton_continuar = crear_boton(
        pantalla,
        (300, 80),
        (ANCHO//2 - 150, 400),
        lambda: continuar_juego((caja_jugador1, caja_jugador2)),
        texto="Continuar",
        fuente=fuente_boton,
        color_texto=BLANCO
    )
    
    boton_volver = crear_boton(
        pantalla,
        (300, 80),
        (ANCHO//2 - 150, 500),
        crear_menu,
        texto="Volver",
        fuente=fuente_boton,
        color_texto=BLANCO
    )
    
    lista_botones = [boton_continuar, boton_volver]
    
    while True:
        pantalla.fill(VERDE)
        
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            
            manejar_evento_caja(caja_jugador1, evento)
            manejar_evento_caja(caja_jugador2, evento)
            checkear_accion_botones(lista_botones, evento)
        
        texto1 = fuente.render("Nombre Jugador 1:", True, BLANCO)
        texto2 = fuente.render("Nombre Jugador 2:", True, BLANCO)
        
        pantalla.blit(texto1, (ANCHO//2 - 100, 170))
        pantalla.blit(texto2, (ANCHO//2 - 100, 270))
        
        dibujar_caja_texto(pantalla, caja_jugador1, fuente)
        dibujar_caja_texto(pantalla, caja_jugador2, fuente)
        
        actualizar_estados_botones(lista_botones, pygame.mouse.get_pos())
        dibujar_botones(lista_botones)
        pygame.display.flip()

def salir():
    pygame.quit()
    sys.exit()

def crear_menu():
    pygame.init()
    ANCHO, ALTO = 800, 600
    pantalla = pygame.display.set_mode((ANCHO, ALTO))
    pygame.display.set_caption("Menú del Juego")
    
    fuente_titulo = pygame.font.Font(None, 74)
    fuente_boton = pygame.font.Font(None, 50)
    VERDE = (34, 139, 34)
    BLANCO = (255, 255, 255)
    
    boton_jugar = crear_boton(
        pantalla,
        (300, 80),
        (ANCHO//2 - 150, 200),
        iniciar_juego,
        texto="Jugar",
        fuente=fuente_boton,
        color_texto=BLANCO
    )
    
    boton_scoreboard = crear_boton(
        pantalla,
        (300, 80),
        (ANCHO//2 - 150, 300),
        mostrar_scoreboard,
        texto="Scoreboard",
        fuente=fuente_boton,
        color_texto=BLANCO
    )
    
    boton_salir = crear_boton(
        pantalla,
        (300, 80),
        (ANCHO//2 - 150, 400),
        salir,
        texto="Salir",
        fuente=fuente_boton,
        color_texto=BLANCO
    )
    
    lista_botones = [boton_jugar, boton_scoreboard, boton_salir]
    
    ejecutando = True
    while ejecutando:
        pantalla.fill(VERDE)
        texto_titulo = fuente_titulo.render("MENÚ DEL JUEGO", True, BLANCO)
        pantalla.blit(texto_titulo, (ANCHO//2 - texto_titulo.get_width()//2, 100))
        
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                ejecutando = False
            checkear_accion_botones(lista_botones, evento)
        
        actualizar_estados_botones(lista_botones, pygame.mouse.get_pos())
        dibujar_botones(lista_botones)
        pygame.display.flip()
    
    salir()

if __name__ == "__main__":
    crear_menu()