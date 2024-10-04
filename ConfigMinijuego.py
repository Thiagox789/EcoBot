import pygame
import random

# Función para dibujar texto
def draw_text(text, font, color, surface, x, y):
    text_obj = font.render(text, True, color)
    text_rect = text_obj.get_rect()
    text_rect.topleft = (x, y)
    surface.blit(text_obj, text_rect)

# Tamaño de la pantalla
SCREEN_WIDTH, SCREEN_HEIGHT = 800, 600
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption('Minijuego de Reciclaje')

# Colores
WHITE = (255, 255, 255)

# Variables del juego
clock = pygame.time.Clock()
font = pygame.font.Font(None, 36)
lives = 3
score = 0
game_active = True
selected_tacho = None
previous_tacho = None

# Definimos los tipos de desechos
TYPES_OF_WASTE = ["plástico", "vidrio", "metal"]

# Configuraciones del jugador y los tachos
tacho_y_position = SCREEN_HEIGHT - 125  # Ajusta esto según el tamaño de tus imágenes

# Inicialización de los tachos (posiciones y sprites)
initial_positions = {
    "plástico": (150, tacho_y_position),
    "vidrio": (350, tacho_y_position),
    "metal": (550, tacho_y_position)
}

player_tachos = {
    "plástico": pygame.Rect(initial_positions["plástico"][0], initial_positions["plástico"][1], 100, 100),
    "vidrio": pygame.Rect(initial_positions["vidrio"][0], initial_positions["vidrio"][1], 100, 100),
    "metal": pygame.Rect(initial_positions["metal"][0], initial_positions["metal"][1], 100, 100)
}

# Función para generar un desecho aleatorio
def generate_random_waste():
    waste_type = random.choice(TYPES_OF_WASTE)
    x_position = random.randint(50, SCREEN_WIDTH - 50)
    waste_rect = pygame.Rect(x_position, 0, 30, 30)  # Un rectángulo que representa el desecho
    return {"type": waste_type, "rect": waste_rect}

# Generar el primer desecho al inicio
current_waste = generate_random_waste()
