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
player_speed = 10
tacho_x_positions = [150, 350, 550]  # Posiciones de los tachos en la parte inferior

# Inicialización de los tachos (posiciones)
player_tachos = {
    "plástico": pygame.Rect(tacho_x_positions[0], SCREEN_HEIGHT - tacho_height - 10, tacho_width, tacho_height),
    "vidrio": pygame.Rect(tacho_x_positions[1], SCREEN_HEIGHT - tacho_height - 10, tacho_width, tacho_height),
    "metal": pygame.Rect(tacho_x_positions[2], SCREEN_HEIGHT - tacho_height - 10, tacho_width, tacho_height)
}

# Configuraciones de los desechos
waste_falling_speed = 5
waste_items = []

# Función para generar un desecho aleatorio
def generate_random_waste():
    waste_type = random.choice(TYPES_OF_WASTE)
    x_position = random.randint(50, SCREEN_WIDTH - 50)
    waste_rect = pygame.Rect(x_position, 0, 30, 30)  # Un rectángulo que representa el desecho
    return {"type": waste_type, "rect": waste_rect}

# Generar algunos desechos al inicio
for _ in range(3):
    waste_items.append(generate_random_waste())

# Variables del juego
clock = pygame.time.Clock()
font = pygame.font.Font(None, 36)
lives = 3
score = 0
game_active = True

# Función principal del minijuego
def play_minigame():
    global lives, score, game_active

    while game_active:
        screen.fill(WHITE)
        
        # Manejo de eventos
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game_active = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:  # Salir del minijuego
                    game_active = False
        
        # Movimiento de los tachos (izquierda/derecha)
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            for tacho in player_tachos.values():
                tacho.x -= player_speed
        if keys[pygame.K_RIGHT]:
            for tacho in player_tachos.values():
                tacho.x += player_speed
        
        # Asegurarse de que los tachos no salgan de la pantalla
        for tacho in player_tachos.values():
            if tacho.x < 0:
                tacho.x = 0
            if tacho.x > SCREEN_WIDTH - tacho_width:
                tacho.x = SCREEN_WIDTH - tacho_width

        # Dibujar los tachos
        for waste_type, tacho in player_tachos.items():
            pygame.draw.rect(screen, TRASH_COLOR[waste_type], tacho)

        # Mover y dibujar los desechos
        for waste in waste_items:
            waste["rect"].y += waste_falling_speed
            pygame.draw.rect(screen, TRASH_COLOR[waste["type"]], waste["rect"])

        # Detectar colisiones entre desechos y tachos
        for waste in waste_items[:]:
            for waste_type, tacho in player_tachos.items():
                if waste["rect"].colliderect(tacho):
                    if waste["type"] == waste_type:
                        score += 1  # Sumar puntos si el desecho cayó en el tacho correcto
                    else:
                        lives -= 1  # Restar vidas si cayó en el tacho incorrecto
                    waste_items.remove(waste)
                    waste_items.append(generate_random_waste())  # Generar nuevo desecho
        
        # Eliminar desechos que caen fuera de la pantalla
        for waste in waste_items[:]:
            if waste["rect"].y > SCREEN_HEIGHT:
                waste_items.remove(waste)
                waste_items.append(generate_random_waste())

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
 