from Dependencias import *

# Inicializar Pygame
pygame.init()
# Configuración de la pantalla completa
pygame.display.set_caption("Proyecto Feria de Ciencias")
Pantalla = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
Ancho_Pantalla, Alto_Pantalla = Pantalla.get_size()
Centro_X = Ancho_Pantalla // 2
Centro_Y = Alto_Pantalla // 2

# Colores
Color_Blanco = (225, 225, 225)
Color_Negro = (0, 0, 0)
Color_Gris = (50, 50, 50)
Color_Rojo = (200, 0, 0)
Color_Fondo = (0, 200, 0)
Color_Pared = (0, 150, 0)

# Tamaño de los sprites
Tamaño_Robot = 50
Tamaño_Basura = Tamaño_Robot
Grosor_Pared = Tamaño_Robot // 2

# Configuración del robot
Posicion_Robot = [Centro_X, Centro_Y]
Velocidad_Robot = 5  
Direccion = None

# Configuración de la basura
def Generador_Basura():
    x = random.randint(Grosor_Pared, Ancho_Pantalla - Grosor_Pared - Tamaño_Basura)
    y = random.randint(Grosor_Pared, Alto_Pantalla - Grosor_Pared - Tamaño_Basura)
    return [x, y]

Posicion_Basura = Generador_Basura()
Generar_Basura = True

# Configuración del reloj
Reloj = pygame.time.Clock()

# Fuente para el texto
Fuente_Titulos = pygame.font.SysFont('timesnewroman', 200)
Posicion_Titulos = Centro_X, Centro_Y - 75
Posicion_Texto = Centro_X, Centro_Y + 125
Fuente_Texto = pygame.font.SysFont('timesnewroman', 50)

# Función auxiliar para dibujar texto con borde
def Renderizar_Texto(Texto, Fuente, Color, Grosor_Borde, Color_Borde, X, Y, Pantalla):
    Texto_a_Renderizar = Fuente.render(Texto, True, Color) # Renderizar el texto principal
    
    Ancho_Texto, Alto_Texto = Texto_a_Renderizar.get_size() # Obtener el tamaño del texto
    Borde_Superficie = pygame.Surface((Ancho_Texto + Grosor_Borde * 2, Alto_Texto + Grosor_Borde * 2), pygame.SRCALPHA) # Crear una superficie temporal para dibujar el borde
    Borde_Superficie.fill((0, 0, 0, 0))  # Fondo transparente

    for dx in range(-Grosor_Borde, Grosor_Borde + 1): # Dibujar el texto principal con el color del borde en la superficie temporal
        for dy in range(-Grosor_Borde, Grosor_Borde + 1):
            if dx**2 + dy**2 <= Grosor_Borde**2:
                Borde_Superficie.blit(Fuente.render(Texto, True, Color_Borde), (Grosor_Borde + dx, Grosor_Borde + dy))

    Borde_Superficie.blit(Texto_a_Renderizar, (Grosor_Borde, Grosor_Borde)) # Dibujar el texto principal en la superficie temporal
    
    Pantalla.blit(Borde_Superficie, (X - Ancho_Texto // 2 - Grosor_Borde, Y - Alto_Texto // 2 - Grosor_Borde)) # Dibujar la superficie temporal en la pantalla

# Función para mostrar la pantalla de inicio
def Mostrar_Pantalla_Inicio():
    Pantalla.fill(Color_Gris)
    Renderizar_Texto('Nombre Juego', Fuente_Titulos, Color_Fondo, 10, Color_Negro, *Posicion_Titulos, Pantalla)
    Renderizar_Texto('Presiona "Enter" para Jugar', Fuente_Texto, Color_Blanco, 5, Color_Negro, *Posicion_Texto, Pantalla)
    pygame.display.flip()

# Función para mostrar el mensaje de "Game Over"
def Mostrar_Pantalla_Game_Over():
    # Pantalla.fill((Color_Blanco), 100, pygame.SRCALPHA)
    Renderizar_Texto('¡Perdiste!', Fuente_Titulos, Color_Rojo, 10, Color_Negro, *Posicion_Titulos, Pantalla)
    Renderizar_Texto('Presiona "R" para volver a Jugar', Fuente_Texto, Color_Blanco, 5, Color_Negro, *Posicion_Texto, Pantalla)
    pygame.display.flip()

def Resetear_Juego():
    global Posicion_Robot, Direccion, Posicion_Basura, Generar_Basura
    Posicion_Robot = [Centro_X, Centro_Y]
    Direccion = None  # No se mueve al inicio
    Posicion_Basura = Generador_Basura()
    Generar_Basura = True

# Función principal del juego
def game_loop():
    global Posicion_Robot, Direccion, Posicion_Basura, Generar_Basura
    Game_Over = False
    game_started = False
    bot_moving = False

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    quit()
                if not game_started:
                    if event.key == pygame.K_RETURN:
                        game_started = True
                        bot_moving = False
                    continue
                if Game_Over:
                    if event.key == pygame.K_r:
                        Resetear_Juego()
                        Game_Over = False
                        game_started = True
                        bot_moving = False
                else:
                    if event.key == pygame.K_UP and Direccion != 'DOWN':
                        Direccion = 'UP'
                        bot_moving = True
                    elif event.key == pygame.K_DOWN and Direccion != 'UP':
                        Direccion = 'DOWN'
                        bot_moving = True
                    elif event.key == pygame.K_LEFT and Direccion != 'RIGHT':
                        Direccion = 'LEFT'
                        bot_moving = True
                    elif event.key == pygame.K_RIGHT and Direccion != 'LEFT':
                        Direccion = 'RIGHT'
                        bot_moving = True

        if not game_started:
            Mostrar_Pantalla_Inicio()
        else:
            if not Game_Over:
                # Mover al robot suavemente
                if bot_moving:
                    if Direccion == 'UP':
                        Posicion_Robot[1] -= Velocidad_Robot
                    if Direccion == 'DOWN':
                        Posicion_Robot[1] += Velocidad_Robot
                    if Direccion == 'LEFT':
                        Posicion_Robot[0] -= Velocidad_Robot
                    if Direccion == 'RIGHT':
                        Posicion_Robot[0] += Velocidad_Robot

                # Detectar si el robot toco la basura
                if (Posicion_Robot[0] < Posicion_Basura[0] + Tamaño_Basura and
                    Posicion_Robot[0] + Tamaño_Robot > Posicion_Basura[0] and
                    Posicion_Robot[1] < Posicion_Basura[1] + Tamaño_Basura and
                    Posicion_Robot[1] + Tamaño_Robot > Posicion_Basura[1]):
                    Generar_Basura = False

                if not Generar_Basura:
                    Posicion_Basura = Generador_Basura()
                Generar_Basura = True

                # Pantalla de juego
                Pantalla.fill(Color_Fondo)
                pygame.draw.rect(Pantalla, Color_Blanco, pygame.Rect(Posicion_Robot[0], Posicion_Robot[1], Tamaño_Robot, Tamaño_Robot))
                pygame.draw.rect(Pantalla, Color_Gris, pygame.Rect(Posicion_Basura[0], Posicion_Basura[1], Tamaño_Basura, Tamaño_Basura))

                # Dibujar paredes alrededor de la pantalla
                pygame.draw.rect(Pantalla, Color_Pared, pygame.Rect(0, 0, Ancho_Pantalla, Grosor_Pared))
                pygame.draw.rect(Pantalla, Color_Pared, pygame.Rect(0, 0, Grosor_Pared, Alto_Pantalla))
                pygame.draw.rect(Pantalla, Color_Pared, pygame.Rect(0, Alto_Pantalla - Grosor_Pared, Ancho_Pantalla, Grosor_Pared))
                pygame.draw.rect(Pantalla, Color_Pared, pygame.Rect(Ancho_Pantalla - Grosor_Pared, 0, Grosor_Pared, Alto_Pantalla))

                # Condiciones de fin de juego
                if (Posicion_Robot[0] < Grosor_Pared or
                    Posicion_Robot[0] > Ancho_Pantalla - Grosor_Pared - Tamaño_Robot or
                    Posicion_Robot[1] < Grosor_Pared or
                    Posicion_Robot[1] > Alto_Pantalla - Grosor_Pared - Tamaño_Robot):
                    Game_Over = True

            if Game_Over:
                Mostrar_Pantalla_Game_Over()

        # Actualizar la pantalla y el reloj
        pygame.display.update()
        Reloj.tick(60)

# Ejecutar el juego
if __name__ == "__main__":
    game_loop()