from warnings import filterwarnings
import pygame
import random

#definición de colores
NEGRO = (0 ,0 ,0)
BLANCO = (255, 255, 255)
AZUL = (0, 0, 255)
VERDE = (0, 255, 0)
ROJO = (255, 0, 0)
AMARILLO = (255, 255, 0)
NARANJA = (255, 165, 0)
MORADO = (128, 0, 128)
CYAN = (0, 255, 255)

#definición de la anchura y  altura d ecada bloque del juego
ANCHURA_BLOQUE = 30
ALTURA_BLOQUE = 30

#definición de las formas de las piezas del tetris
FORMAS = [
    [[1, 1, 1, 1]],  # I
    [[1, 1, 0],
     [0, 1, 1]],     # Z
    [[0, 1, 1],
     [1, 1, 0]],     # S
    [[1, 1],
     [1, 1]],        # O
    [[1, 1, 1],
     [0, 1, 0]],     # T
    [[1, 1, 1],
     [0, 0, 1]],     # L
    [[1, 1, 1],
     [1, 0, 0]]      # J
]

def crear_tablero_vacio():
    return [[NEGRO for _ in range(10)] for _ in range(20)]

def dibujar_bloque(superficie, fila,columna, color):
    pygame.draw.rect(superficie, color, (columna * ANCHURA_BLOQUE, fila * ALTURA_BLOQUE, ANCHURA_BLOQUE, ALTURA_BLOQUE), 0)
    pygame.draw.rect(superficie, BLANCO, (columna * ANCHURA_BLOQUE, fila * ALTURA_BLOQUE, ANCHURA_BLOQUE, ALTURA_BLOQUE), 1)

def dibujar_tablero(superficie, tablero):
    for fila in range(len(tablero)):
        for columna in range(len(tablero[0])):
            dibujar_bloque(superficie, fila, columna, tablero[fila][columna])

def crear_pieza():
    forma = random.choice(FORMAS)
    pieza = {
        'forma': forma,
        'color': random.choice([AZUL, VERDE, ROJO, AMARILLO, NARANJA, MORADO, CYAN]),
        'fila': 0,
        'columna': 3
    }
    return pieza

def mover_pieza(pieza, fila, columna):
    pieza['fila'] = fila
    pieza['columna'] = columna

def agregar_pieza_al_tablero(tablero, pieza):
    for fila in range(len(pieza['forma'])):
        for columna in range(len(pieza['forma'][0])):
            if pieza['forma'][fila][columna]:
                tablero[fila + pieza['fila']][columna + pieza['columna']] = pieza['color']

def rotar_pieza(pieza):
    pieza['forma'] = [list(reversed(columna)) for columna in zip(*pieza['forma'])]

def es_valido_el_movimiento(tablero, pieza, fila, columna):
    for f in range(len(pieza['forma'])):
        for c in range(len(pieza['forma'][0])):
            if pieza['forma'][f][c]:
                nueva_fila, nueva_columna = fila + f, columna + c
                if not (0 <= nueva_fila <20 and 0 <= nueva_columna < 10) or tablero[nueva_fila][nueva_columna] != NEGRO:
                    return False
    return True

def eliminar_fila(tablero, fila):
    del tablero[fila]
    tablero.insert(0, [NEGRO for _ in range(10)])

def eliminar_filas_completas(tablero):
    filas_completas = [i for i, fila in enumerate(tablero) if NEGRO not in fila]
    for fila in filas_completas:
        eliminar_fila(tablero, fila)

def main():
    pygame.init()
    pantalla = pygame.display.set_mode((300, 600))
    pygame.display.set_caption("Tetris")

    reloj = pygame.time.Clock()
    pieza_actual = crear_pieza()
    tablero = crear_tablero_vacio()

    tiempo_antes_de_caer = 0
    tiempo_de_caida = 1000 #tiempo en milisegundos antes que la pieza caigan en un bloque

    terminado = False
    while not terminado:
        pantalla.fill(NEGRO)
        tiempo_actual = pygame.time.get_ticks()

        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                terminado = True
            elif evento.type == pygame.KEYDOWN:
                if evento.key == pygame.K_LEFT and es_valido_el_movimiento(tablero, pieza_actual, pieza_actual['fila'], pieza_actual['columna'] - 1):
                    pieza_actual['columna'] -= 1
                elif evento.key == pygame.K_RIGHT and es_valido_el_movimiento(tablero, pieza_actual, pieza_actual['fila'], pieza_actual['columna'] + 1):
                    pieza_actual['columna'] += 1
                elif evento.key == pygame.K_DOWN:
                    if es_valido_el_movimiento(tablero, pieza_actual, pieza_actual['fila'] + 1, pieza_actual['columna']):
                        pieza_actual['fila'] += 1
                    else:
                        agregar_pieza_al_tablero(tablero, pieza_actual)
                        eliminar_filas_completas(tablero)
                        pieza_actual = crear_pieza()
                elif evento.key == pygame.K_UP:
                    rotar_pieza(pieza_actual)
                    if not es_valido_el_movimiento(tablero, pieza_actual, pieza_actual['fila'], pieza_actual['columna']):
                        rotar_pieza(pieza_actual)

        if tiempo_actual - tiempo_antes_de_caer > tiempo_de_caida or (evento.type == pygame.KEYDOWN and evento.key == pygame.K_SPACE):
            if es_valido_el_movimiento(tablero, pieza_actual, pieza_actual['fila'] + 1, pieza_actual['columna']):
                pieza_actual['fila'] += 1
            else:
                agregar_pieza_al_tablero(tablero, pieza_actual)
                eliminar_filas_completas(tablero)
                pieza_actual = crear_pieza()
            tiempo_antes_de_caer = tiempo_actual

        dibujar_tablero(pantalla, tablero)
        for fila in range(len(pieza_actual['forma'])):
            for columna in range(len(pieza_actual['forma'][0])):
                if pieza_actual['forma'][fila][columna]:
                    dibujar_bloque(pantalla, fila + pieza_actual['fila'], columna + pieza_actual['columna'], pieza_actual['color'])

        pygame.display.update()
        reloj.tick(30)

    pygame.quit()

if __name__ == "__main__":
    main()   