from Assets_Librerias import *
from Configs import *
from Basuras import tipos_basura
import random

# Inicializar el estado del juego 
def Inicializar_Juego():
    global Game_Over, Juego_Iniciado, EcoBot_en_Movimiento, Zona_Reciclaje_Tocada
    global Posicion_EcoBot, Direccion, Posiciones_Basura, Posiciones_Tachos, Sprite_Actual_EcoBot

    Game_Over = False
    Juego_Iniciado = False
    EcoBot_en_Movimiento = False
    Zona_Reciclaje_Tocada = False

    Sprite_Actual_EcoBot = Sprite_EcoBot_Frente
    Posicion_EcoBot = Centrar_Sprite(Sprite_Actual_EcoBot, [Centro_Pantalla_X, Centro_Pantalla_Y])
    Direccion = None

    # Generar basuras inicialmente
    Posiciones_Basura = Generar_Basuras(Num_Basuras, Tamaño_Basura, [])
    Posiciones_Tachos = Generar_Tachos(Num_Tachos, Tamaño_Sprite_Grandes, Posiciones_Basura)

def Ciclo_Juego():
    global Game_Over, Juego_Iniciado, EcoBot_en_Movimiento, Zona_Reciclaje_Tocada
    global Posicion_EcoBot, Direccion, Posiciones_Basura, Posiciones_Tachos, Sprite_Actual_EcoBot

    Inicializar_Juego()

    while True:
        for Event in pygame.event.get():
            if Event.type == pygame.QUIT:
                pygame.quit()
                quit()

            elif Event.type == pygame.KEYDOWN:
                if Event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    quit()

                # Manejo del inicio del juego
                if not Juego_Iniciado:
                    if Event.key == pygame.K_RETURN:
                        Juego_Iniciado = True
                        EcoBot_en_Movimiento = False
                    continue

                # Manejo del reinicio del juego
                if Game_Over:
                    if Event.key == pygame.K_r:
                        Inicializar_Juego()
                        Juego_Iniciado = True
                    continue

                # Si la zona de reciclaje fue tocada, el juego se pausa y entra al minijuego
                if Zona_Reciclaje_Tocada:
                    if Event.key == pygame.K_RETURN:
                        Zona_Reciclaje_Tocada = False
                        Direccion = 'UP'
                        Sprite_Actual_EcoBot = Sprite_EcoBot_Espalda
                        EcoBot_en_Movimiento = True
                    continue

                # Manejo de los controles del EcoBot
                if Event.key in [pygame.K_UP, pygame.K_w] and Direccion != 'DOWN':
                    Direccion = 'UP'
                    Sprite_Actual_EcoBot = Sprite_EcoBot_Espalda
                    EcoBot_en_Movimiento = True

                elif Event.key in [pygame.K_DOWN, pygame.K_s] and Direccion != 'UP':
                    Direccion = 'DOWN'
                    Sprite_Actual_EcoBot = Sprite_EcoBot_Frente
                    EcoBot_en_Movimiento = True

                elif Event.key in [pygame.K_LEFT, pygame.K_a] and Direccion != 'RIGHT':
                    Direccion = 'LEFT'
                    Sprite_Actual_EcoBot = Sprite_EcoBot_Izquierda  
                    EcoBot_en_Movimiento = True

                elif Event.key in [pygame.K_RIGHT, pygame.K_d] and Direccion != 'LEFT':
                    Direccion = 'RIGHT'
                    Sprite_Actual_EcoBot = Sprite_EcoBot_Derecha  
                    EcoBot_en_Movimiento = True

        if not Juego_Iniciado:
            Mostrar_Pantalla_Inicio()
        else:
            if not Game_Over:
                if EcoBot_en_Movimiento and not Zona_Reciclaje_Tocada:
                    if Direccion == 'UP':
                        Posicion_EcoBot[1] -= Velocidad_EcoBot
                    if Direccion == 'DOWN':
                        Posicion_EcoBot[1] += Velocidad_EcoBot
                    if Direccion == 'LEFT':
                        Posicion_EcoBot[0] -= Velocidad_EcoBot
                    if Direccion == 'RIGHT':
                        Posicion_EcoBot[0] += Velocidad_EcoBot

                # Detectar si el EcoBot colisionó con alguna Basura
                Basura_Recogida = None
                for i, Basura in enumerate(Posiciones_Basura):
                    if (Posicion_EcoBot[0] < Basura[0] + Tamaño_Basura and 
                        Posicion_EcoBot[0] + Tamaño_Sprite_Grandes > Basura[0] and 
                        Posicion_EcoBot[1] < Basura[1] + Tamaño_Basura and 
                        Posicion_EcoBot[1] + Tamaño_Sprite_Grandes > Basura[1]): 
                        Basura_Recogida = i
                        Agarrar_Metal.play()
                        break

                if Basura_Recogida is not None:
                    # Reemplazar la basura recogida con una nueva en una posición aleatoria
                    Posiciones_Basura[Basura_Recogida] = Generador_Posicion(Tamaño_Basura, Posiciones_Basura + Posiciones_Tachos)

                # Si la zona de reciclaje fue tocada, simula entrar al minijuego
                if Zona_Reciclaje_Tocada:
                    Abrir_Menu.play()
                    Pantalla.fill(Color_Pared)
                else:
                    # Rellena el fondo
                    Pantalla.fill(Color_Fondo)

                    # Dibuja y define las colisiones de EcoBot
                    Pantalla.blit(Sprite_Actual_EcoBot, (Posicion_EcoBot[0], Posicion_EcoBot[1]))
                    Rect_EcoBot = pygame.Rect(Posicion_EcoBot[0], Posicion_EcoBot[1], Tamaño_Sprite_Grandes, Tamaño_Sprite_Grandes)

                    # Dibuja las Basuras
                    for Basura in Posiciones_Basura:
                        sprite_basura = random.choice(tipos_basura)
                        Pantalla.blit(sprite_basura, (Basura[0], Basura[1]))  # Dibuja la basura en su posición

                    # Dibuja los Tachos
                    for Tacho in Posiciones_Tachos:
                        Pantalla.blit(Sprite_Tacho_de_Basura, (Tacho[0], Tacho[1]))

                    # Dibuja los Tachos de reciclaje
                    Pantalla.blit(Sprite_Tacho_de_Reciclaje_1, (Centro_Pantalla_X - 62.5 - 125, Centro_Pantalla_Y + 215))
                    Pantalla.blit(Sprite_Tacho_de_Reciclaje_2, (Centro_Pantalla_X - 62.5, Centro_Pantalla_Y + 215))
                    Pantalla.blit(Sprite_Tacho_de_Reciclaje_3, (Centro_Pantalla_X - 62.5 + 125, Centro_Pantalla_Y + 215))

                    # Dibuja y define las colisiones de las Paredes
                    Pared_Arriba = pygame.draw.rect(Pantalla, Color_Pared, pygame.Rect(0, 0, Ancho_Pantalla, Grosor_Pared))
                    Pared_Abajo = pygame.draw.rect(Pantalla, Color_Pared, pygame.Rect(0, Alto_Pantalla - Grosor_Pared, Ancho_Pantalla, Grosor_Pared))
                    Pared_Izquierda = pygame.draw.rect(Pantalla, Color_Pared, pygame.Rect(0, 0, Grosor_Pared, Alto_Pantalla))
                    Pared_Derecha = pygame.draw.rect(Pantalla, Color_Pared, pygame.Rect(Ancho_Pantalla - Grosor_Pared, 0, Grosor_Pared, Alto_Pantalla))

                    Pared_Gruesa_Izquierda = pygame.draw.rect(Pantalla, Color_Pared, pygame.Rect(0, Alto_Pantalla - Grosor_Pared_Gruesa - Grosor_Pared, 480, Grosor_Pared_Gruesa))
                    Pared_Gruesa_Derecha = pygame.draw.rect(Pantalla, Color_Pared, pygame.Rect(Ancho_Pantalla - 480, Alto_Pantalla - Grosor_Pared_Gruesa - Grosor_Pared, 480, Grosor_Pared_Gruesa))

                    # Revisa la colisión con los Paredes
                    if (Rect_EcoBot.colliderect(Pared_Arriba) or Rect_EcoBot.colliderect(Pared_Abajo) or Rect_EcoBot.colliderect(Pared_Izquierda) or Rect_EcoBot.colliderect(Pared_Derecha) or Rect_EcoBot.colliderect(Pared_Gruesa_Izquierda) or Rect_EcoBot.colliderect(Pared_Gruesa_Derecha)):
                        Perder_Partida.play()
                        Game_Over = True

                    # Verificar colisiones con los Tachos de Basura
                    for Tacho in Posiciones_Tachos:
                        Rect_Tacho = pygame.Rect(Tacho[0], Tacho[1], Tamaño_Sprite_Grandes, Tamaño_Sprite_Grandes)
                        if Rect_EcoBot.colliderect(Rect_Tacho):
                            Zona_Reciclaje_Tocada = True
                            break

            else:
                # Mostrar el mensaje de Game Over
                Mostrar_Mensaje_Game_Over()

        pygame.display.flip()
        Reloj.tick(FPS)

def Mostrar_Pantalla_Inicio():
    Pantalla.fill(Color_Fondo)
    Pantalla.blit(Sprite_Titulo, (Centro_Pantalla_X - 125, Centro_Pantalla_Y - 200))
    Pantalla.blit(Sprite_Instrucciones, (Centro_Pantalla_X - 150, Centro_Pantalla_Y))
    pygame.display.flip()

def Mostrar_Mensaje_Game_Over():
    Pantalla.fill(Color_Fondo)
    Pantalla.blit(Sprite_Game_Over, (Centro_Pantalla_X - 150, Centro_Pantalla_Y - 100))
    pygame.display.flip()

# Función para generar basuras en posiciones aleatorias
def Generar_Basuras(cantidad, tamaño, posiciones_existentes):
    posiciones = []
    for _ in range(cantidad):
        while True:
            nueva_posicion = Generador_Posicion(tamaño, posiciones + posiciones_existentes)
            if nueva_posicion not in posiciones:  # Asegurarse de que no haya colisiones
                posiciones.append(nueva_posicion)
                break
    return posiciones

# Función para generar una posición aleatoria para las basuras
def Generador_Posicion(tamaño, posiciones_excluidas):
    while True:
        x = random.randint(0, Ancho_Pantalla - tamaño)
        y = random.randint(0, Alto_Pantalla - tamaño)
        nueva_posicion = (x, y)
        if nueva_posicion not in posiciones_excluidas:
            return nueva_posicion

# Función para generar los tachos
def Generar_Tachos(cantidad, tamaño, posiciones_excluidas):
    posiciones = []
    for _ in range(cantidad):
        while True:
            nueva_posicion = Generador_Posicion(tamaño, posiciones + posiciones_excluidas)
            if nueva_posicion not in posiciones:  # Asegurarse de que no haya colisiones
                posiciones.append(nueva_posicion)
                break
    return posiciones

# Llamar a la función de ciclo de juego
Ciclo_Juego()
