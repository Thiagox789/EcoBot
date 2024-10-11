from Configs import *
import EcoBot
with open("CC.txt","w") as archivo:
    archivo.write(str(0))


# Configurar música
Reproducir_Musica(Musica_Minijuego, 0.1)

# Definimos los tipos de desechos
tipos_de_basura = ["plástico", "vidrio", "metal"]

# # Configuraciones del jugador y los tachos
tacho_y_position = Alto_Pantalla - 125  # Ajusta esto según el tamaño de tus imágenes

# Inicialización de los tachos (posiciones y sprites)
posicion_inicial = {
    "plástico": (Ancho_Pantalla // 4, tacho_y_position),  # 1/4 de la pantalla
    "vidrio": (Ancho_Pantalla // 2, tacho_y_position),    # Centro de la pantalla
    "metal": (Ancho_Pantalla * 3 // 4, tacho_y_position)  # 3/4 de la pantalla
}

tachos_jugadores = {
    "plástico": pygame.Rect(posicion_inicial["plástico"][0], posicion_inicial["plástico"][1], 100, 100),
    "vidrio": pygame.Rect(posicion_inicial["vidrio"][0], posicion_inicial["vidrio"][1], 100, 100),
    "metal": pygame.Rect(posicion_inicial["metal"][0], posicion_inicial["metal"][1], 100, 100)
}

# Definir márgenes y área de juego
margen_derecha = 50
espacio_abajo = 50
primer_tacho_x = min(tacho.x for tacho in tachos_jugadores.values())

cuadro_x = primer_tacho_x - 50
cuadro_y = 0
cuadro_ancho = Ancho_Pantalla - cuadro_x - margen_derecha
cuadro_alto = 600

# Fuente para el puntaje
fuente_puntaje = pygame.font.Font(None, 50)

# Contadores de basura reciclada

with open("CBP.txt","r") as archivo:
    contador_plastico=archivo.read()
with open("CBV.txt","r") as archivo:
    contador_vidrio=archivo.read()
with open("CBM.txt","r") as archivo:
    contador_metal=archivo.read()

contador_plastico=int(contador_plastico)
contador_metal=int(contador_metal)
contador_vidrio=int(contador_vidrio)


# Función para dibujar vidas
def dibujar_vidas(Pantalla, vida, Sprite_Corazon, x, y):
    for i in range(vida):
        Pantalla.blit(Sprite_Corazon, (x + i * 40, y))

# Función para reiniciar el juego
def reiniciar_juego():
    global vida, game_active, basura_actual, selected_tacho, previous_tacho
    #global contador_plastico, contador_vidrio, contador_metal
    vida= 3 
    game_active = True
    basura_actual = Generar_Basura_random()
    selected_tacho = previous_tacho = None
    #contador_plastico, contador_vidrio, contador_metal = 0, 0, 0

# Dibujar la corona con puntaje
def dibujar_corona_con_puntaje(Pantalla, puntaje, Sprite_Corona, x, y):
    Pantalla.blit(Sprite_Corona, (x, y))
    texto_puntaje = fuente_puntaje.render(str(puntaje), True, (0, 0, 0))
    Pantalla.blit(texto_puntaje, (x + Sprite_Corona.get_width() + 10, y + 10))

# Función para dibujar los contadores de basura reciclada con sprites
def dibujar_contadores(Pantalla, contador_plastico, contador_vidrio, contador_metal, x, y):
    # Dibujar el sprite de plástico y su puntaje
    Pantalla.blit(Sprite_Basura_Plastico, (x, y))
    texto_plastico = fuente_puntaje.render(f"{contador_plastico}", True, (0, 0, 0))
    Pantalla.blit(texto_plastico, (x + Sprite_Basura_Plastico.get_width() + 10, y + 10))

    # Dibujar el sprite de vidrio y su puntaje
    Pantalla.blit(Sprite_Basura_Vidrio, (x, y + 100))  # Aumenta y en 60 para dejar espacio
    texto_vidrio = fuente_puntaje.render(f"{contador_vidrio}", True, (0, 0, 0))
    Pantalla.blit(texto_vidrio, (x + Sprite_Basura_Vidrio.get_width() + 10, y + 120 + 10))

    # Dibujar el sprite de metal y su puntaje
    Pantalla.blit(Sprite_Basura_Metal, (x, y + 200))  # Aumenta y en 120 para dejar espacio
    texto_metal = fuente_puntaje.render(f"{contador_metal}", True, (0, 0, 0))
    Pantalla.blit(texto_metal, (x + Sprite_Basura_Metal.get_width() + 10, y + 220 + 10))

# Generar basura aleatoria
def Generar_Basura_random():
    tipos = ["plástico", "vidrio", "metal"]
    tipo_basura = random.choice(tipos)
    rect = pygame.Rect(random.randint(cuadro_x + 10, cuadro_x + cuadro_ancho - 10), cuadro_y + 10, 30, 30)
    return {"type": tipo_basura, "rect": rect}

# Obtener el sprite correspondiente al tipo de basura
def obtener_sprite_basura(tipo):
    if tipo == "plástico":
        return Sprite_Basura_Plastico
    elif tipo == "vidrio":
        return Sprite_Basura_Vidrio
    elif tipo == "metal":
        return Sprite_Basura_Metal

# Función principal del minijuego
def play_minijuego():
    global vida,puntaje, game_active, basura_actual, selected_tacho, previous_tacho
    
    with open("CBP.txt","r") as archivo:
        contador_plastico=archivo.read()
    with open("CBV.txt","r") as archivo:
        contador_vidrio=archivo.read()
    with open("CBM.txt","r") as archivo:
        contador_metal=archivo.read()
    contador_plastico=int(contador_plastico)
    contador_metal=int(contador_metal)
    contador_vidrio=int(contador_vidrio)


    reiniciar_juego()

    while True:
        while game_active:
            Pantalla.fill((Color_Pared))  # Fondo fuera del área de juego

            # Dibujar el área de juego
            pygame.draw.rect(Pantalla, (Color_Fondo), (cuadro_x, cuadro_y, cuadro_ancho, cuadro_alto + espacio_abajo))  # Verde oscuro

            # Eventos
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    quit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        pygame.quit()
                        quit()
                    if event.key in (pygame.K_1, pygame.K_2, pygame.K_3):
                        previous_tacho = selected_tacho
                        selected_tacho = tipos_de_basura[event.key - pygame.K_1]
                    if event.key == pygame.K_r and vida <= 0:
                        reiniciar_juego()

            # Movimiento de tachos con el teclado
            tecla = pygame.key.get_pressed()
            if selected_tacho:
                if tecla[pygame.K_a] and tachos_jugadores[selected_tacho].x > cuadro_x:
                    tachos_jugadores[selected_tacho].x -= 7
                if tecla[pygame.K_d] and tachos_jugadores[selected_tacho].x < cuadro_x + cuadro_ancho - 100:
                    tachos_jugadores[selected_tacho].x += 7
                if tecla[pygame.K_LEFT] and tachos_jugadores[selected_tacho].x > cuadro_x:
                    tachos_jugadores[selected_tacho].x -= 7
                if tecla[pygame.K_RIGHT] and tachos_jugadores[selected_tacho].x < cuadro_x + cuadro_ancho - 100:
                    tachos_jugadores[selected_tacho].x += 7

            # Ajustar elevación del tacho seleccionado
            if previous_tacho and previous_tacho != selected_tacho:
                tachos_jugadores[previous_tacho].topleft = posicion_inicial[previous_tacho]
            if selected_tacho:
                tachos_jugadores[selected_tacho].y = cuadro_y + cuadro_alto - 110

            # Dibujar los tachos
            for tipo_basura, tacho in tachos_jugadores.items():
                sprite_tacho = (
                    Sprite_Tacho_de_Reciclaje_1 if tipo_basura == "vidrio" else
                    Sprite_Tacho_de_Reciclaje_2 if tipo_basura == "metal" else
                    Sprite_Tacho_de_Reciclaje_3
                )
                Pantalla.blit(sprite_tacho, (tacho.x, cuadro_y + cuadro_alto - 80))
                waste_sprite = obtener_sprite_basura(tipo_basura)
                Pantalla.blit(waste_sprite, (tacho.x + 25, cuadro_y + cuadro_alto + 75))

            # Caída de la basura
            basura_actual["rect"].y += 3

            if contador_vidrio == 0 and basura_actual["type"] == "vidrio":
                basura_actual = Generar_Basura_random()
                Pantalla.blit(obtener_sprite_basura(basura_actual["type"]), basura_actual["rect"].topleft)
                
            elif contador_metal == 0 and basura_actual["type"] == "metal":
                basura_actual = Generar_Basura_random()
                Pantalla.blit(obtener_sprite_basura(basura_actual["type"]), basura_actual["rect"].topleft)

            elif contador_plastico == 0 and basura_actual["type"] == "plástico":
                basura_actual = Generar_Basura_random()
                Pantalla.blit(obtener_sprite_basura(basura_actual["type"]), basura_actual["rect"].topleft)

            Pantalla.blit(obtener_sprite_basura(basura_actual["type"]), basura_actual["rect"].topleft)

            
            # Colisiones
            for tipo_basura, tacho in tachos_jugadores.items():
                if basura_actual["rect"].colliderect(tacho):
                    if basura_actual["type"] == tipo_basura:
                        Ganar_Tachos.play()
                        puntaje += 1
                        if tipo_basura == "plástico":
                            contador_plastico = max(0, contador_plastico - 1)
                        elif tipo_basura == "vidrio":
                            contador_vidrio = max(0, contador_vidrio - 1)
                        elif tipo_basura == "metal":
                            contador_metal = max(0, contador_metal - 1)
                    else:
                        Poner_Mal_Tacho.play()
                        vida -= 1
                    basura_actual = Generar_Basura_random()
                    break

            CC = puntaje
            with open("CC.txt","w") as archivo:
                            archivo.write(str(CC))

            # Basura fuera del cuadro
            if basura_actual["rect"].y > cuadro_y + cuadro_alto + espacio_abajo:
                basura_actual = Generar_Basura_random()

            # Dibujar vidas y puntaje
            dibujar_vidas(Pantalla, vida, Sprite_Corazon, 50, cuadro_y + 50)
            dibujar_corona_con_puntaje(Pantalla, puntaje, Sprite_Corona, 50, cuadro_y + 250)

            # Dibujar los contadores con sprites debajo del puntaje
            dibujar_contadores(Pantalla, contador_plastico, contador_vidrio, contador_metal, 50, cuadro_y + 350)

            # Fin del juego
            if vida <= 0:
                Perder_Partida.play()
                Mostrar_Pantalla_Game_Over()
                pygame.time.delay(2000)
                game_active = False
                
            if contador_metal == 0 and contador_plastico == 0 and contador_vidrio == 0:
                EcoBot.Ciclo_Juego()
                return
            pygame.display.flip()
            
        # Reiniciar al presionar 'R'
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            if event.type == pygame.KEYDOWN and event.key == pygame.K_r:
                EcoBot.Ciclo_Juego()
                return
                #reiniciar_juego()
                #break