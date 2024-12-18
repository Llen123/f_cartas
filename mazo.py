import random

def crear_carta(valores):
    carta = {
                "nombre": valores[0],
                "velocidad": int(valores[1]),
                "fuerza": int(valores[2]),
                "elemento": valores[3],
                "peso": float(valores[4]),
                "altura": float(valores[5])
            }
    return carta


def cargar_mazo(path):
    mazo = []
    with open(path, "r") as archivo:
        contenido = archivo.readlines()
        contenido.pop(0)
        for linea in contenido:
            valores = linea.strip().split(",")
            carta = crear_carta(valores)
            mazo.append(carta)
    return mazo


    
def mezclar_mazo(mazo: list) -> list:
    for i in range(len(mazo) - 1, 0, -1):
        j = random.randint(0, i)  
        mazo[i], mazo[j] = mazo[j], mazo[i]  
    return mazo

def repartir_cartas(mazo: list) -> dict:
    mazos = {
        "jugador1": [],
        "jugador2": []
    }

    for i in range(len(mazo)):
        if i % 2 == 0:
            mazos["jugador1"].append(mazo[i])  
        else:
            mazos["jugador2"].append(mazo[i])  

    return mazos