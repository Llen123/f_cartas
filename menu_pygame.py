import pygame
import webbrowser
from ordenamiento import *
from main_pygame import *
from utilities import mostrar_texto
from datos_globales import *

pygame.init()

pantalla = pygame.display.set_mode((ANCHO_PANTALLA, ALTO_PANTALLA))
pygame.display.set_caption("Menú Principal")

icono_ventana = pygame.image.load("imagenes/icono.png")
pygame.display.set_icon(icono_ventana)

fuente = pygame.font.Font(None, 50)
fuente_pequena = pygame.font.Font(None, 30)

fondo_menu = pygame.image.load("imagenes/fondo_menu.png")
fondo_menu = pygame.transform.scale(fondo_menu, (ANCHO_PANTALLA, ALTO_PANTALLA))

def menu_principal():
    ejecutando = True
    while ejecutando:
        pantalla.blit(fondo_menu, (0, 0))

        padding = 20
        menu_x = padding
        menu_y = padding
        menu_ancho = 400
        menu_alto = ALTO_PANTALLA - 2 * padding
        pygame.draw.rect(pantalla, GRIS_OSCURO, (menu_x, menu_y, menu_ancho, menu_alto))

        titulo_x = menu_x + padding
        titulo_y = menu_y + padding
        mostrar_texto('Menú Principal', titulo_x, titulo_y, BLANCO, pantalla, fuente)

        mx, my = pygame.mouse.get_pos()

        boton_ancho = menu_ancho - 2 * padding
        boton_alto = 60
        boton_x = menu_x + padding
        boton_y = titulo_y + 100
        espacio_entre_botones = 65

        boton_1 = pygame.Rect(boton_x, boton_y, boton_ancho, boton_alto)
        boton_2 = pygame.Rect(boton_x, boton_y + boton_alto + espacio_entre_botones, boton_ancho, boton_alto)
        boton_3 = pygame.Rect(boton_x, boton_y + 2 * (boton_alto + espacio_entre_botones), boton_ancho, boton_alto)
        boton_4 = pygame.Rect(boton_x, boton_y + 3 * (boton_alto + espacio_entre_botones), boton_ancho, boton_alto)

        pygame.draw.rect(pantalla, GRIS, boton_1)
        texto_jugar = fuente_pequena.render("Jugar", True, NEGRO)
        texto_jugar_rect = texto_jugar.get_rect(center=boton_1.center)
        pantalla.blit(texto_jugar, texto_jugar_rect)

        pygame.draw.rect(pantalla, GRIS, boton_2)
        texto_tabla = fuente_pequena.render("Tabla de Posiciones", True, NEGRO)
        texto_tabla_rect = texto_tabla.get_rect(center=boton_2.center)
        pantalla.blit(texto_tabla, texto_tabla_rect)

        pygame.draw.rect(pantalla, GRIS, boton_3)
        texto_github = fuente_pequena.render("Ver en GitHub", True, NEGRO)
        texto_github_rect = texto_github.get_rect(center=boton_3.center)
        pantalla.blit(texto_github, texto_github_rect)

        pygame.draw.rect(pantalla, GRIS, boton_4)
        texto_salir = fuente_pequena.render("Salir", True, NEGRO)
        texto_salir_rect = texto_salir.get_rect(center=boton_4.center)
        pantalla.blit(texto_salir, texto_salir_rect)

        click = False
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                ejecutando = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    click = True

        if boton_1.collidepoint((mx, my)):
            if click:
                main()
                print("Iniciando juego...")
        if boton_2.collidepoint((mx, my)):
            if click:
                criterio = "puntuacion"
                orden = "desc"
                mostrar_tabla_posiciones(criterio, orden)
        if boton_3.collidepoint((mx, my)):
            if click:
                webbrowser.open("https://github.com/Llen123")
        if boton_4.collidepoint((mx, my)):
            if click:
                ejecutando = False

        pygame.display.update()

    pygame.quit()

if __name__ == "__main__":
    menu_principal()