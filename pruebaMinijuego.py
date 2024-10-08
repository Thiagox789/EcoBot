import pygame
import random
from Assets_Librerias import *
from Configs import *

# Inicializamos pygame
pygame.init()

# Configurar música
pygame.mixer.music.load('Assets/Musica/Musica_Minijuego.mp3')
pygame.mixer.music.play(-1)
pygame.mixer.music.set_volume(0.1)

# Definir márgenes
margen_derecha = 50  # Espacio a la derecha del último tacho
espacio_abajo = 50    # Espacio debajo de los tachos
primer_tacho_x = min(tacho.x for tacho in tachos_jugadores.values())  # Posición del primer tacho (a la izquierda)

# Definir las dimensiones del cuadro del área de juego
cuadro_x = primer_tacho_x - 50  # Un poco más a la izquierda que el primer tacho
cuadro_y = 0  # Pegado al borde superior de la pantalla
cuadro_ancho = Ancho_Pantalla - cuadro_x - margen_derecha  # Desde cuadro_x hasta el borde derecho
cuadro_alto = 600  # Altura total del cuadro

# Definir la fuente para el puntaje
fuente_puntaje = pygame.font.Font(None, 50)  # Tamaño 50 para el número

# Función para dibujar las vidas fuera del área del minijuego
def dibujar_vidas(Pantalla, vida, Sprite_Corazon, x, y):
    for i in range(vida):
        Pantalla.blit(Sprite_Corazon, (x + i * 40, y))  # Dibujar cada corazón con un pequeño espacio entre ellos

def reiniciar_minijuego():
    global vida, puntaje, game_active, basura_actual, selected_tacho, previous_tacho

    vida = 3  # Reiniciar las vidas
    puntaje = 0  # Reiniciar el puntaje
    game_active = True  # Activar el juego
    basura_actual = Generar_Basura_random()  # Generar el primer desecho nuevamente
    selected_tacho = None  # Reiniciar el tacho seleccionado
    previous_tacho = None  # Reiniciar el tacho anterior
# Función para dibujar la corona con el puntaje al lado
def dibujar_corona_con_puntaje(Pantalla, puntaje, Sprite_Corona, x, y):
    Pantalla.blit(Sprite_Corona, (x, y))  # Dibujar la corona
    texto_puntaje = fuente_puntaje.render(str(puntaje), True, (0, 0, 0))  # Dibujar el puntaje en negro
    Pantalla.blit(texto_puntaje, (x + Sprite_Corona.get_width() + 10, y + 10))  # Colocar el número al lado de la corona

def Generar_Basura_random():
    tipos = ["plástico", "vidrio", "metal"]
    tipo_basura = random.choice(tipos)
    rect = pygame.Rect(random.randint(cuadro_x + 10, cuadro_x + cuadro_ancho - 10), cuadro_y + 10, 30, 30)  # Generar en el cuadro
    return {"type": tipo_basura, "rect": rect}

def obtener_sprite_basura(tipo):
    """ Devuelve el sprite correspondiente según el tipo de basura """
    if tipo == "plástico":
        return Sprite_Basura_Plastico
    elif tipo == "vidrio":
        return Sprite_Basura_Vidrio
    elif tipo == "metal":
        return Sprite_Basura_Metal

def play_minijuego():
    global vida, puntaje, game_active, basura_actual, selected_tacho, previous_tacho

    # Inicializar variables para el juego
    vida = 3  # Por ejemplo, puedes ajustar la cantidad de vidas iniciales
    puntaje = 0
    game_active = True
    basura_actual = Generar_Basura_random()  # Generar el primer desecho

    while True:  # Bucle principal
        while game_active:
            Pantalla.fill((0, 200, 0))   # Color de fondo fuera del área del minijuego

            # Dibujar el área de juego (cuadro)
            pygame.draw.rect(Pantalla, Color_Blanco, (cuadro_x, cuadro_y, cuadro_ancho, cuadro_alto + espacio_abajo))

            # Manejo de eventos
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    quit()  
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:  # Salir del minijuego
                        pygame.quit()
                        quit()  
                        game_active = False
                    if event.key in (pygame.K_1, pygame.K_2, pygame.K_3):
                        previous_tacho = selected_tacho  # Guardar el tacho anterior
                        selected_tacho = tipos_de_basura[event.key - pygame.K_1]  # Selecciona el tacho correspondiente
                    if event.key == pygame.K_r and vida <= 0:  # Reiniciar el juego si se presiona 'R'
                        vida = 3  # Reiniciar vidas
                        puntaje = 0  # Reiniciar puntaje
                        game_active = True  # Reiniciar el estado del juego
                        basura_actual = Generar_Basura_random()  # Generar el primer desecho
                        continue  # Volver al inicio del bucle

            # Movimiento de los tachos con el teclado
            tecla = pygame.key.get_pressed()
            if selected_tacho:
                # Movimiento con las teclas A y D
                if tecla[pygame.K_a] and tachos_jugadores[selected_tacho].x > cuadro_x:
                    tachos_jugadores[selected_tacho].x -= 7  # Aumentar la velocidad de movimiento
                if tecla[pygame.K_d] and tachos_jugadores[selected_tacho].x < cuadro_x + cuadro_ancho - 100:
                    tachos_jugadores[selected_tacho].x += 7  # Aumentar la velocidad de movimiento
                # Movimiento con las teclas de flecha izquierda y derecha
                if tecla[pygame.K_LEFT] and tachos_jugadores[selected_tacho].x > cuadro_x:
                    tachos_jugadores[selected_tacho].x -= 7  # Aumentar la velocidad de movimiento
                if tecla[pygame.K_RIGHT] and tachos_jugadores[selected_tacho].x < cuadro_x + cuadro_ancho - 100:
                    tachos_jugadores[selected_tacho].x += 7  # Aumentar la velocidad de movimiento

            # Elevar el tacho seleccionado
            if previous_tacho and previous_tacho != selected_tacho:
                tachos_jugadores[previous_tacho].topleft = posicion_inicial[previous_tacho]  # Volver a la posición inicial
            if selected_tacho:
                tachos_jugadores[selected_tacho].y = cuadro_y + cuadro_alto - 110  # Ajustar la elevación del tacho (subir más)

            # Dibujar los tachos dentro del cuadro
            for tipo_basura, tacho in tachos_jugadores.items():
                Pantalla.blit(Sprite_Tacho_de_Reciclaje_1 if tipo_basura == "vidrio" else
                              Sprite_Tacho_de_Reciclaje_2 if tipo_basura == "metal" else
                              Sprite_Tacho_de_Reciclaje_3, (tacho.x, cuadro_y + cuadro_alto - 50))  # Tachoes pegados al cuadro

                # Dibujar el sprite del desecho correspondiente debajo de cada tacho
                waste_sprite = obtener_sprite_basura(tipo_basura)  # Obtener el sprite del desecho correspondiente
                Pantalla.blit(waste_sprite, (tacho.x + 25, cuadro_y + cuadro_alto + 75))  # Dibuja el sprite del desecho

            # Mover y dibujar el desecho que cae
            basura_actual["rect"].y += 3  # Velocidad de caída del desecho
            Pantalla.blit(obtener_sprite_basura(basura_actual["type"]), basura_actual["rect"].topleft)  # Dibuja el sprite del desecho

            # Detectar colisiones entre el desecho que cae y los tachos
            for tipo_basura, tacho in tachos_jugadores.items():
               if basura_actual["rect"].colliderect(tacho):
                    if basura_actual["type"] == tipo_basura:
                        Ganar_Tachos.play()
                        puntaje += 1  # Sumar puntos si el desecho cayó en el tacho correcto
                        # Hacer que el tacho se suba al recoger la basura
                        tachos_jugadores[tipo_basura].y -= 10  # Subir el tacho 10 píxeles
                    else:
                        Poner_Mal_Tacho.play()
                        vida -= 1  # Restar vidas si cayó en el tacho incorrecto
                    basura_actual = Generar_Basura_random()  # Generar nuevo desecho
                    break  # Salir del bucle tras detectar colisión


            # Eliminar desechos que caen fuera del cuadro
            if basura_actual["rect"].y > cuadro_y + cuadro_alto + espacio_abajo:
                basura_actual = Generar_Basura_random()  # Generar nuevo desecho si se cae fuera

            # Dibujar las vidas en la pantalla (fuera del área de juego)
            dibujar_vidas(Pantalla, vida, Sprite_Corazon, 50, cuadro_y + 50)  # Mostrar en el centro del espacio fuera del cuadro

            # Dibujar la corona con el puntaje
            dibujar_corona_con_puntaje(Pantalla, puntaje, Sprite_Corona, 50, cuadro_y + 250)  # Mostrar una corona con el puntaje al lado

            # Fin del juego si se quedan sin vidas
            if vida <= 0:
                Perder_Partida.play()
                Mostrar_Pantalla_Game_Over()  # Llama a la función para mostrar la pantalla de Game Over
                pygame.time.delay(2000)
                game_active = False  # Cambiar el estado del juego a inactivo

            pygame.display.flip()
            clock.tick(60)

        # Esperar a que se presione 'R' para reiniciar el juego
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r:  # Reiniciar el juego si se presiona 'R'
                    vida = 3  # Reiniciar vidas
                    puntaje = 0  # Reiniciar puntaje
                    game_active = True  # Reiniciar el estado del juego
                    basura_actual = Generar_Basura_random()  # Generar el primer desecho
                    break  # Volver al inicio del bucle principal del juego

# Correr el minijuego
play_minijuego()
pygame.quit()
