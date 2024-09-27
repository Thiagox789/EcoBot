from Assets_Librerias import *
from Configs import *
from Basuras import Tipos_Basura

# Inicializar el estado del juego 
def Inicializar_Juego():
    global Game_Over, Juego_Iniciado, EcoBot_en_Movimiento, Zona_Reciclaje_Tocada, Contador_Basura
    global Posicion_EcoBot, Direccion, Posiciones_Basura, Posiciones_Tachos, Sprite_Actual_EcoBot

    Game_Over = False
    Juego_Iniciado = False
    EcoBot_en_Movimiento = False
    Zona_Reciclaje_Tocada = False

    Contador_Basura = 0  # Inicializa el contador de basura

    Sprite_Actual_EcoBot = Sprite_EcoBot_Frente
    Posicion_EcoBot = Centrar_Sprite(Sprite_Actual_EcoBot, [Centro_Pantalla_X, Centro_Pantalla_Y])
    Direccion = None

    Posiciones_Basura = Generar_Basuras(Num_Basuras, Tamaño_Basura, [])
    Posiciones_Tachos = Generar_Tachos(Num_Tachos, Tamaño_Sprite_Grandes, Posiciones_Basura)

# (la idea es despues hacer lo de inicializacio con todas las partes del Ciclo_Juego() para fragmentarlo, por ejemplo con manejar_Eventos(), actualizar_juego(), etc.)
def Ciclo_Juego():
    global Game_Over, Juego_Iniciado, EcoBot_en_Movimiento, Zona_Reciclaje_Tocada, Contador_Basura
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
                        Contador_Basura = 0
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

                # Detectar si el EcoBot colisiono con alguna Basura
                Basura_Recogida = None
                for i, Basura in enumerate(Posiciones_Basura):
                    
                    if (Posicion_EcoBot[0] < Basura[0] + Tamaño_Basura and Posicion_EcoBot[0] + Tamaño_Sprite_Grandes > Basura[0] and Posicion_EcoBot[1] < Basura[1] + Tamaño_Basura and Posicion_EcoBot[1] + Tamaño_Sprite_Grandes > Basura[1]): 
                        Basura_Recogida = i
                        Agarrar_Metal.play()
                        break

                if Basura_Recogida is not None:
                    Posiciones_Basura[Basura_Recogida] = Generador_Posicion(Tamaño_Basura, Posiciones_Basura + Posiciones_Tachos)
                    Contador_Basura += 1  # Incrementa el contador de basura

                # Si la zona de reciclaje fue tocada, simula entrar al minijuego
                if Zona_Reciclaje_Tocada:
                    # Abrir_Menu.play()
                    Pantalla.fill(Color_Pared)

                else:
                    #  Rellena el fondo
                    Pantalla.fill(Color_Fondo)
                  
                    # Dibuja y define las colisiones de EcoBot
                    Pantalla.blit(Sprite_Actual_EcoBot, (Posicion_EcoBot[0], Posicion_EcoBot[1]))
                    Rect_EcoBot = pygame.Rect(Posicion_EcoBot[0], Posicion_EcoBot[1], Tamaño_Sprite_Grandes, Tamaño_Sprite_Grandes)  
                    
                    #  Dibuja las Basuras
                    for Basura in Posiciones_Basura:
                        sprite_basura = Sprite_Basura_Metal #random.choice(tipos_basura)
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

                    # Revisa la colision con los Paredes
                    if (Rect_EcoBot.colliderect(Pared_Arriba) or Rect_EcoBot.colliderect(Pared_Abajo) or Rect_EcoBot.colliderect(Pared_Izquierda) or Rect_EcoBot.colliderect(Pared_Derecha) or Rect_EcoBot.colliderect(Pared_Gruesa_Izquierda) or Rect_EcoBot.colliderect(Pared_Gruesa_Derecha)):
                        Perder_Partida.play()
                        Game_Over = True
                    
                    # Verificar colisiones con los Tachos de Basura
                    for Tacho in Posiciones_Tachos:
                        Rect_Tacho = pygame.Rect(Tacho[0], Tacho[1], Tamaño_Sprite_Grandes, Tamaño_Sprite_Grandes)
                        
                        if Rect_EcoBot.colliderect(Rect_Tacho):
                            Perder_Partida.play()
                            Game_Over = True

                    # Detectar si el EcoBot está en la zona de reciclaje
                    if Rect_EcoBot.colliderect(Zona_Reciclaje):
                        Zona_Reciclaje_Tocada = True  # Pausa el juego y pone la pantalla en blanco

                    Dibujar_Contador_Basura(Contador_Basura, Pantalla, Fuente_Texto, Sprite_Basura_Metal, Ancho_Pantalla, Alto_Pantalla)

            if Game_Over:
                Mostrar_Pantalla_Game_Over()

        pygame.display.update()
        Reloj.tick(60)

# Ejecutar el juego
Ciclo_Juego()