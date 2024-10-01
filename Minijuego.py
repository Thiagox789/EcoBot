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

# Cargar los assets (reemplazar con los nombres de tus archivos)
# Por ejemplo:
# plastic_image = pygame.image.load("assets/imagenes/plastico.png")
# glass_image = pygame.image.load("assets/imagenes/vidrio.png")
# metal_image = pygame.image.load("assets/imagenes/metal.png")

# Configuraciones del jugador y los tachos
tacho_width = 100
tacho_height = 50
tacho_y_position = SCREEN_HEIGHT - tacho_height - 10

# Inicialización de los tachos (posiciones)
player_tachos = {
    "plástico": pygame.Rect(150, tacho_y_position, tacho_width, tacho_height),
    "vidrio": pygame.Rect(350, tacho_y_position, tacho_width, tacho_height),
    "metal": pygame.Rect(550, tacho_y_position, tacho_width, tacho_height)
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

# Función principal del minijuego
def play_minigame():
    global lives, score, game_active, current_waste

    while game_active:
        screen.fill(WHITE)
        
        # Manejo de eventos
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game_active = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:  # Salir del minijuego
                    game_active = False

        # Movimiento de los tachos con el mouse
        mouse_x, _ = pygame.mouse.get_pos()
        
        # Controlar cada tacho de forma independiente
        if pygame.mouse.get_pressed()[0]:  # Si se presiona el botón izquierdo del mouse
            # Mover el tacho correspondiente al mouse según el área
            if player_tachos["plástico"].collidepoint(mouse_x, tacho_y_position + tacho_height // 2):
                player_tachos["plástico"].x = mouse_x - player_tachos["plástico"].width // 2
            elif player_tachos["vidrio"].collidepoint(mouse_x, tacho_y_position + tacho_height // 2):
                player_tachos["vidrio"].x = mouse_x - player_tachos["vidrio"].width // 2
            elif player_tachos["metal"].collidepoint(mouse_x, tacho_y_position + tacho_height // 2):
                player_tachos["metal"].x = mouse_x - player_tachos["metal"].width // 2

        # Asegurarse de que los tachos no salgan de la pantalla
        for tacho in player_tachos.values():
            if tacho.x < 0:
                tacho.x = 0
            if tacho.x > SCREEN_WIDTH - tacho_width:
                tacho.x = SCREEN_WIDTH - tacho_width

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
