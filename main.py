from juego import ejecutar_juego
from ordenamiento import *
import pygame
from boton import *
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



