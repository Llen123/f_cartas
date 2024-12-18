from juego import ejecutar_juego
from ordenamiento import *
import pygame
from boton import *
from constantes import *
import sys

def main():
    while True:
        opcion = input("1: Jugar 2:Ranking 3: Salir: ")
        match opcion:
            case "1":
                ejecutar_juego()
            case "2":
                criterio = input("¿Por qué criterio deseas ordenar? (puntuacion/Victorias Elementales): ")
                orden = input("¿En qué orden deseas ver el ranking? (asc/desc): ")
                ordenar(criterio, orden)  
            case "3":
                print("Saliendo...")
                break
            case _:
                print("Opción inválida")
        
main()



#pygame.init()
#
#ventana = pygame.display.set_mode((ancho_de_pantalla, largo_de_pantalla))
#pygame.display.set_caption("POKEMON CARDS")
#icono = pygame.image.load("pokemon_icono.png")
#pygame.display.set_icon(icono)
#
#
#texto = "Holaaa"
#text_surface = fuente_de_texto.render(texto, True, blanco)
#
#
#flag = True
#while flag:
#    
#    lista_eventos = pygame.event.get()
#    for evento in lista_eventos:
#        if evento.type == pygame.QUIT:
#            flag = False
#
#    ventana.fill(negro)
#    ventana.blit(text_surface, (50,50))
#    pygame.display.flip()
#pygame.quit()


#pygame.init()
#
#
#WIDTH, HEIGHT = 800, 600
#screen = pygame.display.set_mode((WIDTH, HEIGHT))
#pygame.display.set_caption("Cambio de Pantalla con Clic")
#
#
#WHITE = (255, 255, 255)
#RED = (255, 0, 0)
#
#
#def pantalla_principal():
#    screen.fill(WHITE)
#    font = pygame.font.SysFont(None, 55)
#    text = font.render("Clickea para empezar el juego", True, (0, 0, 0))
#    screen.blit(text, (150, 250))
#    pygame.display.flip()
#
#
#def pantalla_secundaria():
#    screen.fill(RED)
#    font = pygame.font.SysFont(None, 55)
#    text = font.render("¡Bienvenido a la segunda pantalla!", True, (255, 255, 255))
#    screen.blit(text, (100, 250))
#    pygame.display.flip()
#
#
#pantalla_actual = "principal"  
#
#
#while True:
#    for event in pygame.event.get():
#        if event.type == pygame.QUIT:
#            pygame.quit()
#            sys.exit()
#
#        if event.type == pygame.MOUSEBUTTONDOWN:
#            
#            if pantalla_actual == "principal":
#                pantalla_actual = "secundaria"
#            else:
#                pantalla_actual = "principal"
#
#    
#    if pantalla_actual == "principal":
#        pantalla_principal()
#    elif pantalla_actual == "secundaria":
#        pantalla_secundaria()
#
#    pygame.display.update()








