from Minijuego import *

with open("CBM.txt","w") as archivo:
    archivo.write(str(0))
with open("CBP.txt","w") as archivo:
    archivo.write(str(0))
with open("CBV.txt","w") as archivo:
    archivo.write(str(0))

#Poner musica
Reproducir_Musica(Musica_EcoBot, 0.4)
def _Dibujar_Reseteador(screen):
    x, y, width, height = 220, 190, 200, 80
    pygame.draw.rect(screen, Color_Blanco, (x, y, width, height))
    
    button_text = font.render("Resetear", True, Color_Negro)
    screen.blit(button_text, (x + (width - button_text.get_width()) // 2, y + (height - button_text.get_height()) // 2))


# Inicializar el estado del juego 
def Inicializar_Juego():
    global Game_Over, Juego_Iniciado, EcoBot_en_Movimiento, Zona_Reciclaje_Tocada #Contador_Basura_Metal, Contador_Basura_Vidrio, Contador_Basura_Plastico
    global Sprite_Actual_EcoBot, Posicion_EcoBot, Direccion, Posiciones_Basura, Tipos_Basuras_Generada, Posiciones_Tachos, Ultima_Generacion_Tacho, Contador_Tachos_Generados

    Game_Over = False
    Juego_Iniciado = False
    EcoBot_en_Movimiento = False
    Zona_Reciclaje_Tocada = False
    _Dibujar_Reseteador(screen)
    #Contador_Basura_Metal = 0
    #Contador_Basura_Vidrio = 0
    #Contador_Basura_Plastico = 0  

    Sprite_Actual_EcoBot = Sprite_EcoBot_Frente
    Posicion_EcoBot = Centrar_Sprite(Sprite_Actual_EcoBot, [Centro_Pantalla_X, Centro_Pantalla_Y])
    Direccion = None

    # Genera las posiciones y tipos de basura iniciales
    Posiciones_Basura = Generar_Basuras(Num_Basuras, Tamaño_Basura, [])
    Tipos_Basuras_Generada = [random.choice(Tipos_Basuras)() for _ in range(Num_Basuras)]

    Posiciones_Tachos = []
    Ultima_Generacion_Tacho = pygame.time.get_ticks()
    Contador_Tachos_Generados = 0

def Ciclo_Juego():
    global Game_Over, Juego_Iniciado, EcoBot_en_Movimiento, Zona_Reciclaje_Tocada, Contador_Basura_Metal, Contador_Basura_Vidrio, Contador_Basura_Plastico
    global Sprite_Actual_EcoBot, Posicion_EcoBot, Direccion, Posiciones_Basura, Tipos_Basuras_Generada, Posiciones_Tachos, Ultima_Generacion_Tacho, Contador_Tachos_Generados

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
                        Abrir_Menu.play()
                        Juego_Iniciado = True
                        EcoBot_en_Movimiento = False
                    continue

                # Manejo del reinicio del juego
                if Game_Over:
                    
                    if Event.key == pygame.K_r or Event.key == pygame.K_RETURN:  # K_RETURN es la tecla "Enter"
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
                        #Contador_Basura_Metal = 0
                        #Contador_Basura_Vidrio = 0
                        #Contador_Basura_Plastico = 0  
                    continue

                # Manejo de los controles del EcoBot
                if Event.key in [pygame.K_UP, pygame.K_w] and Direccion != 'DOWN':
                    Direccion = 'UP'
                    Sprite_Actual_EcoBot = Sprite_EcoBot_Espalda
                    if not EcoBot_en_Movimiento:
                        EcoBot_en_Movimiento = True
                        Ultima_Generacion_Tacho = pygame.time.get_ticks()  # Inicializa el temporizador al primer movimiento

                elif Event.key in [pygame.K_DOWN, pygame.K_s] and Direccion != 'UP':
                    Direccion = 'DOWN'
                    Sprite_Actual_EcoBot = Sprite_EcoBot_Frente
                    if not EcoBot_en_Movimiento:
                        EcoBot_en_Movimiento = True
                        Ultima_Generacion_Tacho = pygame.time.get_ticks()

                elif Event.key in [pygame.K_LEFT, pygame.K_a] and Direccion != 'RIGHT':
                    Direccion = 'LEFT'
                    Sprite_Actual_EcoBot = Sprite_EcoBot_Izquierda
                    if not EcoBot_en_Movimiento:
                        EcoBot_en_Movimiento = True
                        Ultima_Generacion_Tacho = pygame.time.get_ticks()

                elif Event.key in [pygame.K_RIGHT, pygame.K_d] and Direccion != 'LEFT':
                    Direccion = 'RIGHT'
                    Sprite_Actual_EcoBot = Sprite_EcoBot_Derecha
                    if not EcoBot_en_Movimiento:
                        EcoBot_en_Movimiento = True
                        Ultima_Generacion_Tacho = pygame.time.get_ticks()

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
                    for i, Basura_Pos in enumerate(Posiciones_Basura):
                        if (Posicion_EcoBot[0] < Basura_Pos[0] + Tamaño_Basura and 
                            Posicion_EcoBot[0] + Tamaño_Sprite_Grandes > Basura_Pos[0] and 
                            Posicion_EcoBot[1] < Basura_Pos[1] + Tamaño_Basura and 
                            Posicion_EcoBot[1] + Tamaño_Sprite_Grandes > Basura_Pos[1]):
                            Basura_Recogida = i
                            Tipos_Basuras_Generada[i].Sonido.play()
                            break

                    if Basura_Recogida is not None:
                        # Registrar el tipo de basura recogido antes de cambiar el tipo
                        tipo_basura_recogida = Tipos_Basuras_Generada[Basura_Recogida].Tipo

                        # Incrementar el contador correspondiente usando el tipo de basura recogido
                        if tipo_basura_recogida == "Metal":
                            Contador_Basura_Metal += 1
                        elif tipo_basura_recogida == "Plastico":
                            Contador_Basura_Plastico += 1
                        elif tipo_basura_recogida == "Vidrio":
                            Contador_Basura_Vidrio += 1
                        
                        CBM = Contador_Basura_Metal
                        CBP = Contador_Basura_Plastico
                        CBV = Contador_Basura_Vidrio

                        with open("CBM.txt","w") as archivo:
                            archivo.write(str(CBM))
                        with open("CBP.txt","w") as archivo:
                            archivo.write(str(CBP))
                        with open("CBV.txt","w") as archivo:
                            archivo.write(str(CBV))
                        # Generar una nueva posición y rotación para la basura recogida
                        Posiciones_Basura[Basura_Recogida] = Generador_Posicion(Tamaño_Basura, Posiciones_Basura + Posiciones_Tachos)
                        nueva_rotacion = random.randint(-60, 60)
                        Posiciones_Basura[Basura_Recogida] = (Posiciones_Basura[Basura_Recogida][0], Posiciones_Basura[Basura_Recogida][1], nueva_rotacion)

                        # Generar un nuevo tipo de basura aleatoriamente
                        nuevo_tipo_basura = random.choice(Tipos_Basuras)()
                        Tipos_Basuras_Generada[Basura_Recogida] = nuevo_tipo_basura
                tiempo_actual = pygame.time.get_ticks()
                # Verifica si ha pasado el tiempo para generar un nuevo tacho y si el EcoBot está en movimiento
                if EcoBot_en_Movimiento and tiempo_actual - Ultima_Generacion_Tacho > Tiempo_Para_Generar_Tachos and Contador_Tachos_Generados < Num_Tachos:
                    
                    # Genera un solo nuevo tacho
                    nuevo_tacho = Generar_Tachos(1, Tamaño_Sprite_Grandes, Posiciones_Basura)
                    Posiciones_Tachos.append(nuevo_tacho[0])  # Agrega el nuevo tacho a la lista
                    Contador_Tachos_Generados += 1  # Incrementa el contador de tachos generados
                    Ultima_Generacion_Tacho = tiempo_actual  # Actualiza el tiempo de última generación

                # Si la zona de reciclaje fue tocada, simula entrar al minijuego
                if Zona_Reciclaje_Tocada == True:
                    play_minijuego()
                    
                else:
                    #  Rellena el fondo
                    Pantalla.fill(Color_Fondo)
                  
                    # Dibuja y define las colisiones de EcoBot
                    Pantalla.blit(Sprite_Actual_EcoBot, (Posicion_EcoBot[0], Posicion_EcoBot[1]))
                    Rect_EcoBot = pygame.Rect(Posicion_EcoBot[0], Posicion_EcoBot[1], Tamaño_Sprite_Grandes, Tamaño_Sprite_Grandes)  
                    
                # Dibuja las basuras con la rotación guardada
                for i, Basura in enumerate(Posiciones_Basura):
                    sprite_basura = Tipos_Basuras_Generada[i].Sprite  # Usa el sprite correspondiente al tipo de basura
                    
                    # Usa la rotación almacenada
                    angulo_rotacion = Basura[2]  # El tercer elemento es el ángulo
                    sprite_basura_rotado = pygame.transform.rotate(sprite_basura, angulo_rotacion)  # Rota el sprite
                    
                    # Dibuja la basura rotada
                    Pantalla.blit(sprite_basura_rotado, (Basura[0], Basura[1]))

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
                        Rect_Tacho = pygame.Rect(Tacho[0] + 20, Tacho[1], 90, Tamaño_Sprite_Grandes)
                        
                        if Rect_EcoBot.colliderect(Rect_Tacho):
                            Perder_Partida.play()
                            Game_Over = True

                    # Detectar si el EcoBot está en la zona de reciclaje
                    if Rect_EcoBot.colliderect(Zona_Reciclaje):
                        Zona_Reciclaje_Tocada = True  # Pausa el juego y pone la pantalla en blanco

                    # Dentro de la sección que dibuja la pantalla
                    with open("CC.txt","r") as archivo:
                        CC=archivo.read()
                    CC=int(CC)
                    #print(CC)
                    puntaje=CC
                    Dibujar_Contador_Basura(Pantalla, Fuente_Texto, Ancho_Pantalla, Alto_Pantalla, puntaje, Contador_Basura_Metal, Contador_Basura_Vidrio, Contador_Basura_Plastico)

            if Game_Over:
                Mostrar_Pantalla_Game_Over()

        pygame.display.update()
        Reloj.tick(60)

# Ejecutar el juego
Ciclo_Juego()