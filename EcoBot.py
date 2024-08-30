from Assets_Librerias import *
import pygame
import random
import os

# Inicializar Pygame
pygame.init()

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

# Fuente para el texto
Fuente_Titulos = pygame.font.SysFont('timesnewroman', 200)
Posicion_Titulos = Centro_X, Centro_Y - 75
Fuente_Texto = pygame.font.SysFont('timesnewroman', 50)
Posicion_Texto = Centro_X, Centro_Y + 125

# Función auxiliar para dibujar texto con borde
def Renderizar_Texto(Texto, Fuente, Color, Grosor_Borde, Color_Borde, X, Y, Pantalla):
    Texto_a_Renderizar = Fuente.render(Texto, True, Color) # Renderizar el texto principal
    
    Ancho_Texto, Alto_Texto = Texto_a_Renderizar.get_size() # Obtener el tamaño del texto
    Borde_Superficie = pygame.Surface((Ancho_Texto + Grosor_Borde * 2, Alto_Texto + Grosor_Borde * 2), pygame.SRCALPHA) # Crear una superficie temporal para dibujar el borde
    Borde_Superficie.fill((0, 0, 0, 0))  # Fondo transparente

    for dx in range(-Grosor_Borde, Grosor_Borde + 1): # Dibujar el texto principal con el color del borde en la superficie temporal
        for dy in range(-Grosor_Borde, Grosor_Borde + 1):
            if dx**2 + dy**2 <= Grosor_Borde**2:
                Borde_Superficie.blit(Fuente.render(Texto, True, Color_Borde), (Grosor_Borde + dx, Grosor_Borde + dy))

    Borde_Superficie.blit(Texto_a_Renderizar, (Grosor_Borde, Grosor_Borde)) # Dibujar el texto principal en la superficie temporal
    
    Pantalla.blit(Borde_Superficie, (X - Ancho_Texto // 2 - Grosor_Borde, Y - Alto_Texto // 2 - Grosor_Borde)) # Dibujar la superficie temporal en la pantalla

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

def centrar_sprite(sprite, posicion):
    ancho_sprite, alto_sprite = sprite.get_size()
    posicion_centrada = [posicion[0] - ancho_sprite // 2, posicion[1] - alto_sprite // 2]
    return posicion_centrada

# Configuración del EcoBot
Sprite_Actual = Sprite_EcoBot_Frente
Ancho_Sprite, Alto_Sprite = Sprite_Actual.get_size()
Direccion = None
Velocidad_EcoBot = 5  
Posicion_EcoBot = centrar_sprite(Sprite_Actual, [Centro_X, Centro_Y])

# Función para verificar si dos rectángulos colisionan
def verificar_colision(rect1, rect2):
    return rect1.colliderect(rect2)

# Función para generar una posición que no se superponga y esté dentro del marco
def Generador_Posicion(sprite_tamano, objetos_existentes):
    while True:
        x = random.randint(Grosor_Pared, Ancho_Pantalla - sprite_tamano - Grosor_Pared)
        y = random.randint(Grosor_Pared, Alto_Pantalla - sprite_tamano - Grosor_Pared)
        nueva_posicion = pygame.Rect(x, y, sprite_tamano, sprite_tamano)

        # Verificar si la nueva posición no colisiona con ningún objeto existente
        if not any(verificar_colision(nueva_posicion, pygame.Rect(o[0], o[1], sprite_tamano, sprite_tamano)) for o in objetos_existentes):
            return [x, y]

# Generar múltiples basuras
def Generar_Basuras(num_basuras, sprite_tamano, posiciones_tachos):
    basuras = []
    while len(basuras) < num_basuras:
        nueva_basura = Generador_Posicion(sprite_tamano, basuras + posiciones_tachos)  # Asegura que no colisione con tachos de basura
        basuras.append(nueva_basura)
    return basuras

# Generar múltiples tachos de basura
def Generar_Tachos(num_tachos, sprite_tamano, posiciones_basura):
    tachos = []
    while len(tachos) < num_tachos:
        nuevo_tacho = Generador_Posicion(sprite_tamano, tachos + posiciones_basura)  # Asegura que no colisione con basuras
        tachos.append(nuevo_tacho)
    return tachos

def Resetear_Juego():
    global Posicion_EcoBot, Direccion, Posiciones_Basura, Posiciones_Tachos, Sprite_Actual
    Posicion_EcoBot = centrar_sprite(Sprite_Actual, [Centro_X, Centro_Y])
    Direccion = None  # No se mueve al inicio
    Posiciones_Basura = Generar_Basuras(Num_Basuras, Tamaño_Basura, [])
    Posiciones_Tachos = Generar_Tachos(Num_Tachos, Tamaño_Sprite_Grandes, Posiciones_Basura)
    Sprite_Actual = Sprite_EcoBot_Frente

# Inicializar las basuras y tachos
Num_Basuras = 3
Num_Tachos = 3

Posiciones_Basura = Generar_Basuras(Num_Basuras, Tamaño_Basura, [])
Posiciones_Tachos = Generar_Tachos(Num_Tachos, Tamaño_Sprite_Grandes, Posiciones_Basura)

Posiciones_Basura = [centrar_sprite(Sprite_Basura_Metal_1, pos) for pos in Posiciones_Basura]
Posiciones_Tachos = [centrar_sprite(Sprite_Tacho_de_Basura, pos) for pos in Posiciones_Tachos]

# Pantalla de juego (agregar el dibujo de los tachos)
def game_loop():
    global Posicion_EcoBot, Direccion, Posiciones_Basura, Posiciones_Tachos, Sprite_Actual
    Game_Over = False
    game_started = False
    bot_moving = False

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    quit()
                if not game_started:
                    if event.key == pygame.K_RETURN:
                        game_started = True
                        bot_moving = False
                    continue
                if Game_Over:
                    if event.key == pygame.K_r:
                        Resetear_Juego()
                        Game_Over = False
                        game_started = True
                        bot_moving = False

                else:
                    if event.key in [pygame.K_UP, pygame.K_w] and Direccion != 'DOWN':
                        Direccion = 'UP'
                        Sprite_Actual = Sprite_EcoBot_Espalda
                        bot_moving = True
                    elif event.key in [pygame.K_DOWN, pygame.K_s] and Direccion != 'UP':
                        Direccion = 'DOWN'
                        Sprite_Actual = Sprite_EcoBot_Frente
                        bot_moving = True
                    elif event.key in [pygame.K_LEFT, pygame.K_a] and Direccion != 'RIGHT':
                        Direccion = 'LEFT'
                        Sprite_Actual = Sprite_EcoBot_Izquierda  
                        bot_moving = True
                    elif event.key in [pygame.K_RIGHT, pygame.K_d] and Direccion != 'LEFT':
                        Direccion = 'RIGHT'
                        Sprite_Actual = Sprite_EcoBot_Derecha  
                        bot_moving = True

        if not game_started:
            Mostrar_Pantalla_Inicio()
        else:
            if not Game_Over:
                # Mover al EcoBot suavemente
                if bot_moving:
                    if Direccion == 'UP':
                        Posicion_EcoBot[1] -= Velocidad_EcoBot
                    if Direccion == 'DOWN':
                        Posicion_EcoBot[1] += Velocidad_EcoBot
                    if Direccion == 'LEFT':
                        Posicion_EcoBot[0] -= Velocidad_EcoBot
                    if Direccion == 'RIGHT':
                        Posicion_EcoBot[0] += Velocidad_EcoBot

                # Detectar si el EcoBot tocó alguna basura
                Basura_Recogida = None
                for i, basura in enumerate(Posiciones_Basura):
                    if (Posicion_EcoBot[0] < basura[0] + Tamaño_Basura and
                        Posicion_EcoBot[0] + Tamaño_Sprite_Grandes > basura[0] and
                        Posicion_EcoBot[1] < basura[1] + Tamaño_Basura and
                        Posicion_EcoBot[1] + Tamaño_Sprite_Grandes > basura[1]):
                        Basura_Recogida = i
                        break

                if Basura_Recogida is not None:
                    Posiciones_Basura[Basura_Recogida] = Generador_Posicion(Tamaño_Basura, Posiciones_Basura + Posiciones_Tachos)
                    Posiciones_Basura[Basura_Recogida] = centrar_sprite(Sprite_Basura_Metal_1, Posiciones_Basura[Basura_Recogida])

                # Pantalla de juego
                Pantalla.fill(Color_Fondo)
                
                # Dibuja los sprites
                Pantalla.blit(Sprite_Actual, (Posicion_EcoBot[0], Posicion_EcoBot[1]))
                
                for tacho in Posiciones_Tachos:
                    Pantalla.blit(Sprite_Tacho_de_Basura, (tacho[0], tacho[1]))

                for basura in Posiciones_Basura:
                    Pantalla.blit(Sprite_Basura_Metal_1, (basura[0], basura[1]))

                # Dibuja las paredes
                pygame.draw.rect(Pantalla, Color_Pared, pygame.Rect(0, 0, Ancho_Pantalla, Grosor_Pared))
                pygame.draw.rect(Pantalla, Color_Pared, pygame.Rect(0, Alto_Pantalla - Grosor_Pared, Ancho_Pantalla, Grosor_Pared))
                pygame.draw.rect(Pantalla, Color_Pared, pygame.Rect(0, 0, Grosor_Pared, Alto_Pantalla))
                pygame.draw.rect(Pantalla, Color_Pared, pygame.Rect(Ancho_Pantalla - Grosor_Pared, 0, Grosor_Pared, Alto_Pantalla))

                # Revisa colisión con los bordes
                if (Posicion_EcoBot[0] < Grosor_Pared or
                    Posicion_EcoBot[0] > Ancho_Pantalla - Tamaño_Sprite_Grandes - Grosor_Pared or
                    Posicion_EcoBot[1] < Grosor_Pared or
                    Posicion_EcoBot[1] > Alto_Pantalla - Tamaño_Sprite_Grandes - Grosor_Pared):
                    Game_Over = True

            if Game_Over:
                Mostrar_Pantalla_Game_Over()

            pygame.display.update()
            Reloj.tick(60)

# Ejecutar el juego
game_loop()