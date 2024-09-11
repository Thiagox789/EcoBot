from Assets_Librerias import *
from Configs import *

# Inicializar el estado del juego
def inicializar_juego():
    global Game_Over, game_started, bot_moving, Zona_Reciclaje_Tocada
    global Posicion_EcoBot, Direccion, Posiciones_Basura, Posiciones_Tachos, Sprite_Actual

    Game_Over = False
    game_started = False
    bot_moving = False
    Zona_Reciclaje_Tocada = False  # Variable para detectar si la zona de reciclaje fue tocada

    Sprite_Actual = Sprite_EcoBot_Frente
    Posicion_EcoBot = centrar_sprite(Sprite_Actual, [Centro_X, Centro_Y])
    Direccion = None

    Posiciones_Basura = Generar_Basuras(Num_Basuras, Tamaño_Basura, [])
    Posiciones_Tachos = Generar_Tachos(Num_Tachos, Tamaño_Sprite_Grandes, Posiciones_Basura)

def game_loop():
    global Game_Over, game_started, bot_moving, Zona_Reciclaje_Tocada
    global Posicion_EcoBot, Direccion, Posiciones_Basura, Posiciones_Tachos, Sprite_Actual

    # Inicialización del juego
    inicializar_juego()

    while True:

        for event in pygame.event.get():

            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
                
            elif event.type == pygame.KEYDOWN:

                if event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    quit()

                # Manejo del inicio del juego
                if not game_started:

                    if event.key == pygame.K_RETURN:
                        game_started = True
                        bot_moving = False
                    continue

                # Manejo del reinicio del juego
                if Game_Over:

                    if event.key == pygame.K_r:
                        inicializar_juego()
                        game_started = True
                    continue

                # Si la zona de reciclaje fue tocada, el juego está pausado
                if Zona_Reciclaje_Tocada:
                    if event.key == pygame.K_RETURN:  # Reanudar el juego al presionar "Enter"
                        Zona_Reciclaje_Tocada = False
                        Direccion = 'UP'  # El EcoBot ahora apunta hacia arriba
                        Sprite_Actual = Sprite_EcoBot_Espalda
                        bot_moving = True
                    continue

                # Manejo de los controles del EcoBot
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

                if bot_moving and not Zona_Reciclaje_Tocada:  # Solo mover si el juego no está pausado
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

                # Si la zona de reciclaje fue tocada, pantalla completamente blanca
                if Zona_Reciclaje_Tocada:
                    Pantalla.fill((255, 255, 255))  # Pantalla completamente blanca
                else:
                    Pantalla.fill(Color_Fondo)

                    # Dibuja los sprites
                    Pantalla.blit(Sprite_Actual, (Posicion_EcoBot[0], Posicion_EcoBot[1]))
                    
                    for tacho in Posiciones_Tachos:
                        Pantalla.blit(Sprite_Tacho_de_Basura, (tacho[0], tacho[1]))

                    for basura in Posiciones_Basura:
                        Pantalla.blit(Sprite_Basura_Metal_1, (basura[0], basura[1]))

                    # Define áreas de colisión para las paredes
                    Pared_superior = pygame.draw.rect(Pantalla, Color_Pared, pygame.Rect(0, 0, Ancho_Pantalla, Grosor_Pared))
                    Pared_inferior = pygame.draw.rect(Pantalla, Color_Pared, pygame.Rect(0, Alto_Pantalla - Grosor_Pared, Ancho_Pantalla, Grosor_Pared))
                    Pared_izquierdo = pygame.draw.rect(Pantalla, Color_Pared, pygame.Rect(0, 0, Grosor_Pared, Alto_Pantalla))
                    Pared_derecho = pygame.draw.rect(Pantalla, Color_Pared, pygame.Rect(Ancho_Pantalla - Grosor_Pared, 0, Grosor_Pared, Alto_Pantalla))

                    pared_gruesa_izquierda = pygame.draw.rect(Pantalla, Color_Pared, pygame.Rect(0, Alto_Pantalla - Grosor_Pared_Gruesa - Grosor_Pared, (Ancho_Pantalla - 450) // 2, Grosor_Pared_Gruesa))
                    pared_gruesa_derecha = pygame.draw.rect(Pantalla, Color_Pared, pygame.Rect(Ancho_Pantalla - (Ancho_Pantalla - 450) // 2, Alto_Pantalla - Grosor_Pared_Gruesa - Grosor_Pared, (Ancho_Pantalla - 450) // 2, Grosor_Pared_Gruesa))

                    # Definir la zona de los tachos de reciclaje
                    Zona_Reciclaje = pygame.Rect(0, Alto_Pantalla - Grosor_Pared_Gruesa - Grosor_Pared, Ancho_Pantalla // 2, Grosor_Pared_Gruesa)

                    rect_ecobot = pygame.Rect(Posicion_EcoBot[0], Posicion_EcoBot[1], Tamaño_Sprite_Grandes, Tamaño_Sprite_Grandes)

                    # Revisa colisión con los Pareds y las paredes gruesas
                    if (rect_ecobot.colliderect(Pared_superior) or rect_ecobot.colliderect(Pared_inferior) or rect_ecobot.colliderect(Pared_izquierdo) or rect_ecobot.colliderect(Pared_derecho) or rect_ecobot.colliderect(pared_gruesa_izquierda) or rect_ecobot.colliderect(pared_gruesa_derecha)):
                        Game_Over = True
                    
                    # Verificar colisiones con los tachos de basura
                    for tacho in Posiciones_Tachos:
                        rect_tacho = pygame.Rect(tacho[0], tacho[1], Tamaño_Sprite_Grandes, Tamaño_Sprite_Grandes)
                        
                        if rect_ecobot.colliderect(rect_tacho):
                            Game_Over = True

                    # Detectar si el EcoBot está en la zona de reciclaje
                    if rect_ecobot.colliderect(Zona_Reciclaje):
                        Zona_Reciclaje_Tocada = True  # Pausa el juego y pone la pantalla en blanco

            if Game_Over:
                Mostrar_Pantalla_Game_Over()

        pygame.display.update()
        Reloj.tick(60)

# Ejecutar el juego
game_loop()