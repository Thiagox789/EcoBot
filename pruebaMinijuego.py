import pygame
import random

# Inicializamos pygame
pygame.init()

# Tamaño de la pantalla
SCREEN_WIDTH, SCREEN_HEIGHT = 800, 600
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption('Minijuego de Reciclaje')

# Colores
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)

# Definimos los tipos de desechos y colores
TYPES_OF_WASTE = ["plástico", "vidrio", "metal"]
TRASH_COLOR = {"plástico": GREEN, "vidrio": BLUE, "metal": RED}

# Configuraciones del jugador y los tachos
tacho_width = 100
tacho_height = 50
tacho_y_position = SCREEN_HEIGHT - tacho_height - 10

# Inicialización de los tachos (posiciones)
initial_positions = {
    "plástico": (150, tacho_y_position),
    "vidrio": (350, tacho_y_position),
    "metal": (550, tacho_y_position)
}

player_tachos = {
    "plástico": pygame.Rect(initial_positions["plástico"][0], initial_positions["plástico"][1], tacho_width, tacho_height),
    "vidrio": pygame.Rect(initial_positions["vidrio"][0], initial_positions["vidrio"][1], tacho_width, tacho_height),
    "metal": pygame.Rect(initial_positions["metal"][0], initial_positions["metal"][1], tacho_width, tacho_height)
}

# Inicialización de los desechos
current_waste = None

# Función para generar un desecho aleatorio
def generate_random_waste():
    waste_type = random.choice(TYPES_OF_WASTE)
    x_position = random.randint(50, SCREEN_WIDTH - 50)
    waste_rect = pygame.Rect(x_position, 0, 30, 30)  # Un rectángulo que representa el desecho
    return {"type": waste_type, "rect": waste_rect}

# Generar el primer desecho al inicio
current_waste = generate_random_waste()

# Variables del juego
clock = pygame.time.Clock()
font = pygame.font.Font(None, 36)
lives = 3
score = 0
game_active = True
selected_tacho = None  # Variable para controlar el tacho seleccionado
previous_tacho = None  # Variable para recordar el tacho anterior

# Función principal del minijuego
def play_minigame():
    global lives, score, game_active, current_waste, selected_tacho, previous_tacho

    while game_active:
        screen.fill(WHITE)
        
        # Manejo de eventos
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game_active = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:  # Salir del minijuego
                    game_active = False
                if event.key == pygame.K_1:  # Seleccionar tacho plástico
                    previous_tacho = selected_tacho  # Guardar el tacho anterior
                    selected_tacho = "plástico"
                if event.key == pygame.K_2:  # Seleccionar tacho vidrio
                    previous_tacho = selected_tacho  # Guardar el tacho anterior
                    selected_tacho = "vidrio"
                if event.key == pygame.K_3:  # Seleccionar tacho metal
                    previous_tacho = selected_tacho  # Guardar el tacho anterior
                    selected_tacho = "metal"

        # Movimiento de los tachos con el teclado
        keys = pygame.key.get_pressed()
        
        # Mover el tacho seleccionado
        if selected_tacho:
            if keys[pygame.K_a] and player_tachos[selected_tacho].x > 0:
                player_tachos[selected_tacho].x -= 5  # Mover a la izquierda
            if keys[pygame.K_d] and player_tachos[selected_tacho].x < SCREEN_WIDTH - tacho_width:
                player_tachos[selected_tacho].x += 5  # Mover a la derecha

        # Elevar el tacho seleccionado y volver el anterior a su posición inicial
        if previous_tacho and previous_tacho != selected_tacho:
            player_tachos[previous_tacho].x, player_tachos[previous_tacho].y = initial_positions[previous_tacho]  # Volver a la posición inicial
        if selected_tacho:
            player_tachos[selected_tacho].y = tacho_y_position - 20  # Elevar el tacho seleccionado más

        # Dibujar los tachos
        for waste_type, tacho in player_tachos.items():
            pygame.draw.rect(screen, TRASH_COLOR[waste_type], tacho)

        # Mover y dibujar el desecho
        current_waste["rect"].y += 5  # Velocidad de caída del desecho
        pygame.draw.rect(screen, TRASH_COLOR[current_waste["type"]], current_waste["rect"])

        # Detectar colisiones entre el desecho y los tachos
        for waste_type, tacho in player_tachos.items():
            if current_waste["rect"].colliderect(tacho):
                if current_waste["type"] == waste_type:
                    score += 1  # Sumar puntos si el desecho cayó en el tacho correcto
                else:
                    lives -= 1  # Restar vidas si cayó en el tacho incorrecto
                current_waste = generate_random_waste()  # Generar nuevo desecho
                break  # Salir del bucle tras detectar colisión

        # Eliminar desechos que caen fuera de la pantalla
        if current_waste["rect"].y > SCREEN_HEIGHT:
            current_waste = generate_random_waste()  # Generar nuevo desecho si se cae fuera

        # Dibujar la interfaz (puntuación y vidas)
        draw_text(f"Score: {score}", font, BLACK, screen, 10, 10)
        draw_text(f"Lives: {lives}", font, BLACK, screen, 10, 50)

        # Fin del juego si se quedan sin vidas
        if lives <= 0:
            draw_text("Game Over", font, RED, screen, SCREEN_WIDTH // 2 - 100, SCREEN_HEIGHT // 2)
            pygame.display.flip()
            pygame.time.delay(2000)
            game_active = False

        pygame.display.flip()
        clock.tick(60)

# Función para dibujar texto
def draw_text(text, font, color, surface, x, y):
    text_obj = font.render(text, True, color)
    text_rect = text_obj.get_rect()
    text_rect.topleft = (x, y)
    surface.blit(text_obj, text_rect)

# Correr el minijuego
play_minigame()
pygame.quit()
