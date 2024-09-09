from Assets_Librerias import *
import pygame
import random

# Configuración del reloj
Reloj = pygame.time.Clock()

# Configuración de la pantalla completa
pygame.display.set_caption("EcoBot")
Pantalla = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
Ancho_Pantalla, Alto_Pantalla = Pantalla.get_size()
Centro_X = Ancho_Pantalla // 2
Centro_Y = Alto_Pantalla // 2

# Tamaño de los "colliders"
Tamaño_Sprite_Grandes = 125
Tamaño_Basura = 75
Grosor_Pared = 25
Grosor_Pared_Gruesa = 125

# Fuente para el texto
Fuente_Titulos = pygame.font.SysFont('timesnewroman', 200)
Posicion_Titulos = Centro_X, Centro_Y - 75
Fuente_Texto = pygame.font.SysFont('timesnewroman', 50)
Posicion_Texto = Centro_X, Centro_Y + 125

# Configuración inicial del EcoBot
Velocidad_EcoBot = 5
Num_Basuras = 3
Num_Tachos = 3

# Definir la zona de spawn
Zona_Spawn = pygame.Rect(Grosor_Pared + 50, Grosor_Pared + 50, Ancho_Pantalla - 150 , Alto_Pantalla - 275)

# Función auxiliar para dibujar texto con borde
def Renderizar_Texto(Texto, Fuente, Color, Grosor_Borde, Color_Borde, X, Y, Pantalla):
    Texto_a_Renderizar = Fuente.render(Texto, True, Color)
    Ancho_Texto, Alto_Texto = Texto_a_Renderizar.get_size()
    Borde_Superficie = pygame.Surface((Ancho_Texto + Grosor_Borde * 2, Alto_Texto + Grosor_Borde * 2), pygame.SRCALPHA)
    Borde_Superficie.fill((0, 0, 0, 0))

    for dx in range(-Grosor_Borde, Grosor_Borde + 1):
        for dy in range(-Grosor_Borde, Grosor_Borde + 1):
            if dx**2 + dy**2 <= Grosor_Borde**2:
                Borde_Superficie.blit(Fuente.render(Texto, True, Color_Borde), (Grosor_Borde + dx, Grosor_Borde + dy))

    Borde_Superficie.blit(Texto_a_Renderizar, (Grosor_Borde, Grosor_Borde))
    Pantalla.blit(Borde_Superficie, (X - Ancho_Texto // 2 - Grosor_Borde, Y - Alto_Texto // 2 - Grosor_Borde))

# Función para mostrar la pantalla de inicio
def Mostrar_Pantalla_Inicio():
    Pantalla.fill(Color_Gris)
    Renderizar_Texto('EcoBot', Fuente_Titulos, Color_Fondo, 10, Color_Negro, *Posicion_Titulos, Pantalla)
    Renderizar_Texto('Presiona "Enter" para Jugar', Fuente_Texto, Color_Blanco, 5, Color_Negro, *Posicion_Texto, Pantalla)
    pygame.display.flip()

# Función para mostrar el mensaje de "Game Over"
def Mostrar_Pantalla_Game_Over():
    Renderizar_Texto('¡Perdiste!', Fuente_Titulos, Color_Rojo, 10, Color_Negro, *Posicion_Titulos, Pantalla)
    Renderizar_Texto('Presiona "R" para volver a Jugar', Fuente_Texto, Color_Blanco, 5, Color_Negro, *Posicion_Texto, Pantalla)
    pygame.display.flip()

# Función para verificar si dos rectángulos colisionan
def verificar_colision(rect1, rect2):
    return rect1.colliderect(rect2)

# Función para generar una posición dentro de la zona de spawn
def Generador_Posicion(sprite_tamano, objetos_existentes):
    while True:
        x = random.randint(Zona_Spawn.left, Zona_Spawn.right - sprite_tamano)
        y = random.randint(Zona_Spawn.top, Zona_Spawn.bottom - sprite_tamano)
        nueva_posicion = pygame.Rect(x, y, sprite_tamano, sprite_tamano)

        # Verificar que no colisiona con otras posiciones existentes
        if not any(verificar_colision(nueva_posicion, pygame.Rect(o[0], o[1], sprite_tamano, sprite_tamano)) for o in objetos_existentes):
            return [x, y]

# Generar múltiples basuras
def Generar_Basuras(num_basuras, sprite_tamano, posiciones_tachos):
    basuras = []
    while len(basuras) < num_basuras:
        nueva_basura = Generador_Posicion(sprite_tamano, basuras + posiciones_tachos)
        basuras.append(nueva_basura)
    return basuras

# Generar múltiples tachos de basura
def Generar_Tachos(num_tachos, sprite_tamano, posiciones_basura):
    tachos = []
    while len(tachos) < num_tachos:
        nuevo_tacho = Generador_Posicion(sprite_tamano, tachos + posiciones_basura)
        tachos.append(nuevo_tacho)
    return tachos