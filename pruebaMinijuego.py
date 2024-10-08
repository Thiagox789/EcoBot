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
cuadro_y = 100  # Espacio superior
cuadro_ancho = Ancho_Pantalla - cuadro_x - margen_derecha  # Desde cuadro_x hasta el borde derecho
cuadro_alto = 600  # Altura total del cuadro

# Función para dibujar las vidas fuera del área del minijuego
def dibujar_vidas(Pantalla, vida, Sprite_Corazon, x, y):
    for i in range(vida):
        Pantalla.blit(Sprite_Corazon, (x + i * 40, y))  # Dibujar cada corazón con un pequeño espacio entre ellos

def play_minigame():
    global vida, puntaje, game_active, basura_actual, selected_tacho, previous_tacho

    while game_active:
        Pantalla.fill(Color_Gris)  # Color de fondo fuera del área del minijuego

        # Dibujar el área de juego (cuadro)
        pygame.draw.rect(Pantalla, Color_Blanco, (cuadro_x, cuadro_y, cuadro_ancho, cuadro_alto + espacio_abajo))

        # Manejo de eventos
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game_active = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:  # Salir del minijuego
                    pygame.quit()
                    quit()  
                    game_active = False
                if event.key in (pygame.K_1, pygame.K_2, pygame.K_3):
                    previous_tacho = selected_tacho  # Guardar el tacho anterior
                    selected_tacho = tipos_de_basura[event.key - pygame.K_1]  # Selecciona el tacho correspondiente

        # Movimiento de los tachos con el teclado
        tecla = pygame.key.get_pressed()
        if selected_tacho:
            # Movimiento con las teclas A y D
            if tecla[pygame.K_a] and tachos_jugadores[selected_tacho].x > cuadro_x:
                tachos_jugadores[selected_tacho].x -= 5  # Mover a la izquierda
            if tecla[pygame.K_d] and tachos_jugadores[selected_tacho].x < cuadro_x + cuadro_ancho - 100:
                tachos_jugadores[selected_tacho].x += 5  # Mover a la derecha
            # Movimiento con las teclas de flecha izquierda y derecha
            if tecla[pygame.K_LEFT] and tachos_jugadores[selected_tacho].x > cuadro_x:
                tachos_jugadores[selected_tacho].x -= 5  # Mover a la izquierda
            if tecla[pygame.K_RIGHT] and tachos_jugadores[selected_tacho].x < cuadro_x + cuadro_ancho - 100:
                tachos_jugadores[selected_tacho].x += 5  # Mover a la derecha

        # Elevar el tacho seleccionado
        if previous_tacho and previous_tacho != selected_tacho:
            tachos_jugadores[previous_tacho].topleft = posicion_inicial[previous_tacho]  # Volver a la posición inicial
        if selected_tacho:
            tachos_jugadores[selected_tacho].y = cuadro_y + cuadro_alto - 150  # Ajustar la elevación del tacho

        # Dibujar los tachos
        for tipo_basura in tachos_jugadores:
            if tipo_basura == "vidrio":
                Pantalla.blit(Sprite_Tacho_de_Reciclaje_1, tachos_jugadores[tipo_basura].topleft)
            elif tipo_basura == "metal":
                Pantalla.blit(Sprite_Tacho_de_Reciclaje_2, tachos_jugadores[tipo_basura].topleft)
            elif tipo_basura == "plástico":
                Pantalla.blit(Sprite_Tacho_de_Reciclaje_3, tachos_jugadores[tipo_basura].topleft)

        # Mover y dibujar el desecho
        if basura_actual["type"] == "plástico":
            waste_sprite = Sprite_Basura_Plastico
        elif basura_actual["type"] == "vidrio":
            waste_sprite = Sprite_Basura_Vidrio
        else:
            waste_sprite = Sprite_Basura_Metal

        basura_actual["rect"].y += 3  # Velocidad de caída del desecho
        Pantalla.blit(waste_sprite, basura_actual["rect"].topleft)  # Dibuja el sprite del desecho

        # Detectar colisiones entre el desecho y los tachos
        for tipo_basura, tacho in tachos_jugadores.items():
            if basura_actual["rect"].colliderect(tacho):
                if basura_actual["type"] == tipo_basura:
                    Ganar_Tachos.play()
                    puntaje += 1  # Sumar puntos si el desecho cayó en el tacho correcto
                else:
                    Poner_Mal_Tacho.play()
                    vida -= 1  # Restar vidas si cayó en el tacho incorrecto
                basura_actual = Generar_Basura_random()  # Generar nuevo desecho
                break  # Salir del bucle tras detectar colisión

        # Eliminar desechos que caen fuera de la pantalla
        if basura_actual["rect"].y > cuadro_y + cuadro_alto + espacio_abajo:
            basura_actual = Generar_Basura_random()  # Generar nuevo desecho si se cae fuera

        # Dibujar las vidas en la pantalla (fuera del área de juego)
        dibujar_vidas(Pantalla, vida, Sprite_Corazon, cuadro_x, cuadro_y - 50)  # Mostrar arriba del cuadro

        # Fin del juego si se quedan sin vidas
        if vida <= 0:
            Perder_Partida.play()
            Mostrar_Pantalla_Game_Over()  # Llama a la función para mostrar la pantalla de Game Over
            pygame.time.delay(2000)
            game_active = False

        pygame.display.flip()
        clock.tick(60)

# Mostrar la pantalla de inicio antes de comenzar el minijuego
# Correr el minijuego
play_minigame()
pygame.quit()
