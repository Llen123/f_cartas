import pygame
def crear_boton(ventana, dimensiones, posicion, accion, imagen=None, texto="", fuente=None, color_texto=(0, 0, 0)):
    # Comprobamos que 'posicion' y 'dimensiones' sean listas o tuplas de longitud 2
    if not (type(posicion) in [list, tuple] and len(posicion) == 2):
        raise ValueError("La 'posicion' debe ser una lista o tupla con dos elementos (x, y)")

    if not (type(dimensiones) in [list, tuple] and len(dimensiones) == 2):
        raise ValueError("Las 'dimensiones' deben ser una lista o tupla con dos elementos (ancho, alto)")
    
    x, y = posicion
    ancho, alto = dimensiones

    boton = {
        "ventana": ventana,
        "dimensiones": dimensiones,
        "posicion": posicion,
        "accion": accion,
        "imagen": None,
        "texto": texto,
        "fuente": fuente,
        "color_texto": color_texto,
        "estado_hover": False,
        "rectangulo": pygame.Rect(x, y, ancho, alto)
    }
    
    if imagen:
        boton["imagen"] = pygame.image.load(imagen).convert_alpha()
        boton["imagen"] = pygame.transform.scale(boton["imagen"], dimensiones)

    return boton

def dibujar(boton):
    if boton["imagen"]:
        boton["ventana"].blit(boton["imagen"], boton["posicion"])
    else:
        pygame.draw.rect(boton["ventana"], (200, 200, 200), boton["rectangulo"])

    if boton["texto"] and boton["fuente"]:
        texto_renderizado = boton["fuente"].render(boton["texto"], True, boton["color_texto"])
        texto_rect = texto_renderizado.get_rect(center=boton["rectangulo"].center)
        boton["ventana"].blit(texto_renderizado, texto_rect)

def checkear_accion(boton, evento):
    if evento.type == pygame.MOUSEBUTTONDOWN and boton["rectangulo"].collidepoint(evento.pos):
        boton["accion"]()

def actualizar_estado(boton, posicion_mouse):
    boton["estado_hover"] = boton["rectangulo"].collidepoint(posicion_mouse)

def dibujar_botones(lista_botones):
    for boton in lista_botones:
        dibujar(boton)

def checkear_accion_botones(lista_botones, evento):
    for boton in lista_botones:
        checkear_accion(boton, evento)

def actualizar_estados_botones(lista_botones, posicion_mouse):
    for boton in lista_botones:
        actualizar_estado(boton, posicion_mouse)
