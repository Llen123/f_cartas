import random
from mazo import *

def obtener_cartas_jugadores(carta1: dict, carta2: dict) -> list:
    '''Obtiene los elementos de las cartas de cada jugador y lo devuelve'''
    elementos_ronda_actual = [carta1["elemento"], carta2["elemento"]]                                                             
    return elementos_ronda_actual

def crear_fila(elementos: list, columnas: int) -> list:
    fila = []
    for i in range(columnas):
        fila.append(random.choice(elementos))  
    return fila

def agregar_fila(tablero: list, fila: list) -> list:
    tablero.append(fila)
    return tablero

def validar_tablero(tablero, filas_restantes):
    if tablero == None:
        tablero = []
    return tablero

def crear_tablero(elementos: list, filas_restantes: int, columnas: int, tablero=None) -> list:
    tablero = validar_tablero(tablero, filas_restantes)
    resultado = tablero
    if filas_restantes > 0:
        fila_actual = crear_fila(elementos, columnas)
        resultado.append(fila_actual)
        resultado = crear_tablero(elementos, filas_restantes - 1, columnas, resultado)
    return resultado 

def imprimir_tablero(tablero: list) -> None:
    for fila in tablero:
        print(" | ".join(fila))
        print("-" * 5)

def incrementar_si_valido(condicion: bool, contador: int) -> int:
    if condicion:
        contador += 1
    return contador

def verificar_columnas(tablero: list, elemento: str) -> int:
    n = len(tablero)
    combinaciones = 0

    for j in range(n):
        columna_valida = True
        for i in range(n):
            if tablero[i][j] != elemento:
                columna_valida = False
                break
        
        if columna_valida:
            combinaciones += 1

    return combinaciones
    
def verificar_filas_y_diagonales(tablero: list, elemento: str) -> int:
    combinaciones = 0
    n = len(tablero)
    diagonal_principal = True
    diagonal_secundaria = True

    for i in range(n):
        fila_valida = True
        for j in range(n):
            if tablero[i][j] != elemento:
                fila_valida = False
                break
        combinaciones = incrementar_si_valido(fila_valida, combinaciones)
        if tablero[i][i] != elemento:
            diagonal_principal = False

        if tablero[i][n - 1 - i] != elemento:
            diagonal_secundaria = False
    combinaciones = incrementar_si_valido(diagonal_principal, combinaciones)
    combinaciones = incrementar_si_valido(diagonal_secundaria, combinaciones)

    return combinaciones

def verificar_combinaciones_totales(tablero: list, elemento: str) -> int:
    combinaciones_totales = 0
    combinaciones_totales += verificar_filas_y_diagonales(tablero, elemento)
    combinaciones_totales += verificar_columnas(tablero, elemento)
    return combinaciones_totales




def bubble_sort(combinaciones: list) -> list:
   
    for i in range(len(combinaciones) - 1):
        for j in range(i + 1, len(combinaciones)):
            if combinaciones[i][2] < combinaciones[j][2]:  
                combinaciones[i], combinaciones[j] = combinaciones[j], combinaciones[i]
    return combinaciones

def mostrar_combinaciones(combinaciones_ordenadas: list) -> None:
    
    print(f"{combinaciones_ordenadas[0][0]} ({combinaciones_ordenadas[0][1]}) tiene {combinaciones_ordenadas[0][2]} combinaciones ganadoras.")
    print(f"{combinaciones_ordenadas[1][0]} ({combinaciones_ordenadas[1][1]}) tiene {combinaciones_ordenadas[1][2]} combinaciones ganadoras.")

def determinar_resultado_final(combinaciones_jugador1: int, combinaciones_jugador2: int) -> str:
  
    ganador = None
    if combinaciones_jugador1 > combinaciones_jugador2:
        ganador =  "jugador1"
    elif combinaciones_jugador2 > combinaciones_jugador1:
        ganador =  "jugador2"
    else:
        ganador= "empate"
    return ganador

def determinar_ganador(combinaciones_ordenadas: list, combinaciones_jugador1: int, combinaciones_jugador2: int) -> str:

    mostrar_combinaciones(combinaciones_ordenadas)
    ganador = determinar_resultado_final(combinaciones_jugador1, combinaciones_jugador2)
    return ganador

def jugar_tateti(carta1: list, carta2: list, datos_jugadores: dict) -> str:

    elementos = obtener_cartas_jugadores(carta1, carta2)
    
    
    tablero = crear_tablero(elementos, filas_restantes=3, columnas=3)
    
   
    jugador1 = elementos[0]
    jugador2 = elementos[1]
    
    
    nombre_jugador1 = datos_jugadores["jugador1"]["nombre"]
    nombre_jugador2 = datos_jugadores["jugador2"]["nombre"] 
    
    
    combinaciones_jugador1 = verificar_combinaciones_totales(tablero, jugador1)
    combinaciones_jugador2 = verificar_combinaciones_totales(tablero, jugador2)
    
    
    print("Tablero:")
    imprimir_tablero(tablero)
    
    
    combinaciones = [
        (nombre_jugador1, jugador1, combinaciones_jugador1),
        (nombre_jugador2, jugador2, combinaciones_jugador2)
    ] 
    
   
    combinaciones_ordenadas = bubble_sort(combinaciones)
    

    resultado = determinar_ganador(combinaciones_ordenadas, combinaciones_jugador1, combinaciones_jugador2)
    return resultado