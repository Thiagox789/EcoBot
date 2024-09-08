from Assets_Librerias import *

# Inicializar Pygame
pygame.init()

from Configs import *

def game_loop():
    global Posicion_EcoBot, Direccion, Posiciones_Basura, Posiciones_Tachos, Sprite_Actual
    Game_Over = False
    game_started = False
    bot_moving = False

    # Inicialización
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
                        print("Reiniciando juego...")
                        inicializar_juego()  # Llamada a la función de reinicio
                        Game_Over = False
                        game_started = True
                        bot_moving = False
                        print("Juego reiniciado con valores predeterminados")
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