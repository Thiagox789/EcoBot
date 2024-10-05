import pygame
import random
from Assets_Librerias import *



# Función para dibujar texto
def draw_text(text, font, color, surface, x, y):
    text_obj = font.render(text, True, color)
    text_rect = text_obj.get_rect()
    text_rect.topleft = (x, y)
    surface.blit(text_obj, text_rect)




# Fullscreen configuration
pygame.display.set_caption("EcoBot")
screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
Screen_Width, Screen_Height = screen.get_size()  # Changed 'Pantalla' to 'screen'
Centro_Pantalla_X = Screen_Width // 2
Centro_Pantalla_Y = Screen_Height // 2


# Colores
WHITE = (255, 255, 255)
Color_Gris = (192, 192, 192)  # Ejemplo de color gris
Color_Fondo = (0, 128, 0)  # Ejemplo de color fondo
Color_Negro = (0, 0, 0)  # Ejemplo de color negro
Color_Rojo = (255, 0, 0)  # Ejemplo de color rojo

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
tacho_y_position = Screen_Height - 125  # Ajusta esto según el tamaño de tus imágenes

# Inicialización de los tachos (posiciones y sprites)
initial_positions = {
    "plástico": (Screen_Width // 4, tacho_y_position),  # 1/4 de la pantalla
    "vidrio": (Screen_Width // 2, tacho_y_position),    # Centro de la pantalla
    "metal": (Screen_Width * 3 // 4, tacho_y_position)  # 3/4 de la pantalla
}

player_tachos = {
    "plástico": pygame.Rect(initial_positions["plástico"][0], initial_positions["plástico"][1], 100, 100),
    "vidrio": pygame.Rect(initial_positions["vidrio"][0], initial_positions["vidrio"][1], 100, 100),
    "metal": pygame.Rect(initial_positions["metal"][0], initial_positions["metal"][1], 100, 100)
}

# Función para generar un desecho aleatorio
# Función para generar un desecho aleatorio
def generate_random_waste():
    waste_type = random.choice(TYPES_OF_WASTE)
    # Cambiar el rango de generación para que caiga en toda la pantalla
    x_position = random.randint(0, Screen_Width - 30)  # 30 es el ancho del rectángulo de desecho
    waste_rect = pygame.Rect(x_position, 0, 30, 30)  # Un rectángulo que representa el desecho
    return {"type": waste_type, "rect": waste_rect}

# Generar el primer desecho al inicio
current_waste = generate_random_waste()

# Ajustar volumen
Ganar_Tachos.set_volume(0.2)  # Volumen al 20%
Poner_Mal_Tacho.set_volume(0.2)  # Volumen al 20%
Perder_Partida.set_volume(0.3)  # Volumen al 30%

# Configuración de la pantalla completa
Pantalla = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
Ancho_Pantalla, Alto_Pantalla = Pantalla.get_size()
Centro_Pantalla_X = Ancho_Pantalla // 2
Centro_Pantalla_Y = Alto_Pantalla // 2

# Fuente para el texto
Fuente_Titulos = pygame.font.SysFont('timesnewroman', 200)
Fuente_Texto = pygame.font.SysFont('timesnewroman', 50)

# Posiciones del texto
Posicion_Titulos = Centro_Pantalla_X, Centro_Pantalla_Y - 75
Posicion_Texto = Centro_Pantalla_X, Centro_Pantalla_Y + 125
Posicion_Texto2 = Centro_Pantalla_X, Centro_Pantalla_Y + 200

# Función para dibujar texto con borde
def Renderizar_Texto(Texto, Fuente, Color, Grosor_Borde, Color_Borde, X, Y, Pantalla):
    Texto_a_Renderizar = Fuente.render(Texto, True, Color)
    Ancho_Texto, Alto_Texto = Texto_a_Renderizar.get_size()
    Borde_Superficie = pygame.Surface((Ancho_Texto + Grosor_Borde * 2, Alto_Texto + Grosor_Borde * 2), pygame.SRCALPHA)
    Borde_Superficie.fill((0, 0, 0, 0))

    for dx in range(-Grosor_Borde, Grosor_Borde + 1):
        for dy in range(-Grosor_Borde, Grosor_Borde + 1):
            if dx**2 + dy**2 <= Grosor_Borde**2:
                Borde_Superficie.blit(Fuente.render(Texto, True, Color_Borde), (Grosor_Borde + dx, Grosor_Borde + dy))

    Borde_Superficie.blit(Texto_a_Renderizar, (Grosor_Borde, Grosor_Borde))
    Pantalla.blit(Borde_Superficie, (X - Ancho_Texto // 2 - Grosor_Borde, Y - Alto_Texto // 2 - Grosor_Borde))

# Función para mostrar la pantalla de inicio
def mostrar_pantalla_inicio():
    Pantalla.fill(Color_Blanco)
    Renderizar_Texto('Minijuego', Fuente_Titulos, Color_Fondo, 10, Color_Negro, *Posicion_Titulos, Pantalla)
    Renderizar_Texto('Presiona "Enter" para Jugar', Fuente_Texto, Color_Blanco, 5, Color_Negro, *Posicion_Texto, Pantalla)
    Renderizar_Texto('Presiona "R" para salir', Fuente_Texto, Color_Blanco, 5, Color_Negro, *Posicion_Texto2, Pantalla)
    pygame.display.flip()

    # Esperar a que el jugador presione ENTER o R
    waiting = True
    while waiting:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:  # Comienza el minijuego al presionar ENTER
                    Abrir_Menu.play()
                    waiting = False
                if event.key == pygame.K_r:  # Salir del juego al presionar R
                    pygame.quit()
                    quit()

# Muestra el mensaje de "Game Over"
def Mostrar_Pantalla_Game_Over():
    Renderizar_Texto('¡Perdiste!', Fuente_Titulos, Color_Rojo, 10, Color_Negro, *Posicion_Titulos, Pantalla)
    Renderizar_Texto('Presiona "R" para volver a Jugar', Fuente_Texto, Color_Blanco, 5, Color_Negro, *Posicion_Texto, Pantalla)
    pygame.display.flip()
