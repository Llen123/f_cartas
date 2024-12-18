import pygame
import sys
from test2 import jugar_con_pygame, preparar_mazo, obtener_jugadores

def crear_menu():
    pygame.init()
    
    # Configuración de la pantalla
    ANCHO = 800
    ALTO = 600
    pantalla = pygame.display.set_mode((ANCHO, ALTO))
    pygame.display.set_caption("Menú del Juego")
    
    # Colores
    VERDE = (34, 139, 34)
    BLANCO = (255, 255, 255)
    
    # Fuentes
    fuente_titulo = pygame.font.Font(None, 74)
    fuente_menu = pygame.font.Font(None, 50)
    
    # Bucle principal del menú
    running = True
    while running:
        pantalla.fill(VERDE)
        
        # Eventos
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                running = False
            
            if evento.type == pygame.KEYDOWN:
                if evento.key == pygame.K_1:
                    # Preparar datos de jugadores y mazo
                    datos_jugadores = {
                        "jugador1": {"nombre": "Jugador 1", "puntuacion": 0, "Victorias Elementales": 0},
                        "jugador2": {"nombre": "Jugador 2", "puntuacion": 0, "Victorias Elementales": 0}
                    }
                    mazo_jugadores = preparar_mazo()
                    
                    # Cerrar ventana de menú
                    pygame.quit()
                    
                    # Iniciar juego
                    jugar_con_pygame(datos_jugadores, mazo_jugadores)
                    
                    # Reiniciar Pygame para el menú
                    pygame.init()
                    pantalla = pygame.display.set_mode((ANCHO, ALTO))
                    pygame.display.set_caption("Menú del Juego")
                
                elif evento.key == pygame.K_2:
                    running = False
        
        # Renderizar título
        texto_titulo = fuente_titulo.render("MENÚ DEL JUEGO", True, BLANCO)
        pantalla.blit(texto_titulo, (ANCHO//2 - texto_titulo.get_width()//2, 100))
        
        # Renderizar opciones
        texto_jugar = fuente_menu.render("1. Jugar", True, BLANCO)
        texto_salir = fuente_menu.render("2. Salir", True, BLANCO)
        
        pantalla.blit(texto_jugar, (ANCHO//2 - texto_jugar.get_width()//2, 250))
        pantalla.blit(texto_salir, (ANCHO//2 - texto_salir.get_width()//2, 300))
        
        # Actualizar pantalla
        pygame.display.flip()
    
    pygame.quit()
    sys.exit()

# Ejecutar el menú
if __name__ == "__main__":
    crear_menu()