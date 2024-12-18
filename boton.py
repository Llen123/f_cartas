import pygame
def crear_boton(dimensiones, posicion, ventana, accion,  imagen = None):
    boton = {}
    boton["Ventana"] = ventana
    boton["Dimensiones"] = dimensiones
    boton["Posicion"] = posicion
    boton["Presionado"] = False
    boton["Accion"] = accion

    
    if imagen != None:
        img = pygame.image.load(imagen)
        boton["Contenido"] = pygame.transform.scale(img, boton["Dimensiones"]) 

    boton["Rectangulo"] = boton["Contenido"].get_rect()
    boton["Rectangulo"].topleft = boton["Posicion"]

    return boton

def dibujar(boton):
    boton["Ventana"].blit(boton["Contenido"], boton["Posicion"])

def dibujar_botones(lista):
    for boton in lista:
        dibujar(boton)

def checkear_accion_botones(lista_botones, evento):
    for boton in lista_botones:
        if boton["Rectangulo"].collidepoint(evento.pos):
            boton["Accion"]()
