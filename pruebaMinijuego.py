import pygame
import random
from Assets_Librerias import *
from Configs import *

# Inicializamos pygame
pygame.init()

# Configuración de la pantalla
Ancho_Pantalla = 800
Alto_Pantalla = 600
Pantalla = pygame.display.set_mode((Ancho_Pantalla, Alto_Pantalla))
Color_Blanco = (255, 255, 255)

# Configuración del rectángulo central para la caída de basura
rect_area = pygame.Rect(Ancho_Pantalla // 2 - 100, Alto_Pantalla // 2, 200, 400)  # (x, y, width, height)

# Cargar música
pygame.mixer.music.load('Assets/Sonidos/Minijuego_Musica.mp3')
pygame.mixer.music.play(-1)
pygame.mixer.music.set_volume(0.1)

def generate_random_waste():
    # Generar un tipo de basura aleatorio y establecer su rectángulo inicial dentro del área definida
    waste_types = ["plástico", "vidrio", "metal"]
    waste_type = random.choice(waste_types)
    waste_rect = pygame.Rect(random.randint(rect_area.x, rect_area.x + rect_area.width - 50),  # 50 es el ancho del sprite
                             rect_area.y,  # Comienza en la parte superior del área
                             50,  # Ancho del sprite de basura
                             50)  # Alto del sprite de basura
    return {"type": waste_type, "rect": waste_rect}

def play_minigame():
    global lives, score, game_active, current_waste, selected_tacho, previous_tacho

    current_waste = generate_random_waste()  # Inicializa la basura
    while game_active:
        Pantalla.fill(Color_Blanco)

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
                    selected_tacho = TYPES_OF_WASTE[event.key - pygame.K_1]  # Selecciona el tacho correspondiente

        # Movimiento de los tachos con el teclado
        keys = pygame.key.get_pressed()
        if selected_tacho:
            if keys[pygame.K_a] and player_tachos[selected_tacho].x > 0:
                player_tachos[selected_tacho].x -= 5  # Mover a la izquierda
            if keys[pygame.K_d] and player_tachos[selected_tacho].x < Ancho_Pantalla - 100:
                player_tachos[selected_tacho].x += 5  # Mover a la derecha

        # Elevar el tacho seleccionado
        if previous_tacho and previous_tacho != selected_tacho:
            player_tachos[previous_tacho].topleft = initial_positions[previous_tacho]  # Volver a la posición inicial
        if selected_tacho:
            player_tachos[selected_tacho].y = tacho_y_position - 150  # Elevar el tacho seleccionado

        # Dibujar los tachos
        for waste_type in player_tachos:
            if waste_type == "vidrio":
                Pantalla.blit(Sprite_Tacho_de_Reciclaje_1, player_tachos[waste_type].topleft)
            elif waste_type == "metal":
                Pantalla.blit(Sprite_Tacho_de_Reciclaje_2, player_tachos[waste_type].topleft)
            elif waste_type == "plástico":
                Pantalla.blit(Sprite_Tacho_de_Reciclaje_3, player_tachos[waste_type].topleft)

        # Mover y dibujar el desecho
        if current_waste["type"] == "plástico":
            waste_sprite = Sprite_Basura_Plastico
        elif current_waste["type"] == "vidrio":
            waste_sprite = Sprite_Basura_Vidrio
        else:
            waste_sprite = Sprite_Basura_Metal

        current_waste["rect"].y += 3  # Velocidad de caída del desecho
        Pantalla.blit(waste_sprite, current_waste["rect"].topleft)  # Dibuja el sprite del desecho

        # Detectar colisiones entre el desecho y los tachos
        for waste_type, tacho in player_tachos.items():
            if current_waste["rect"].colliderect(tacho):
                if current_waste["type"] == waste_type:
                    Ganar_Tachos.play()
                    score += 1  # Sumar puntos si el desecho cayó en el tacho correcto
                else:
                    Poner_Mal_Tacho.play()
                    lives -= 1  # Restar vidas si cayó en el tacho incorrecto
                current_waste = generate_random_waste()  # Generar nuevo desecho
                break  # Salir del bucle tras detectar colisión

        # Eliminar desechos que caen fuera del área definida
        if current_waste["rect"].y > rect_area.y + rect_area.height:
            current_waste = generate_random_waste()  # Generar nuevo desecho si se cae fuera

        # Dibujar el rectángulo donde caen las basuras
        pygame.draw.rect(Pantalla, (0, 0, 255, 50), rect_area, 2)  # Rectángulo azul de contorno

        # Dibujar las vidas en la pantalla
        dibujar_vidas(Pantalla, lives, Sprite_Corazon)

        # Fin del juego si se quedan sin vidas
        if lives <= 0:
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
