from Assets_Librerias import *

# -------------------------------------------------------------------------------------------------------------
# Configuraciones para el juego
# -------------------------------------------------------------------------------------------------------------

# Configuración de la pantalla completa
pygame.display.set_caption("EcoBot")
Pantalla = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
Ancho_Pantalla, Alto_Pantalla = Pantalla.get_size()
Centro_Pantalla_X = Ancho_Pantalla // 2
Centro_Pantalla_Y = Alto_Pantalla // 2

# Configuración del reloj
Reloj = pygame.time.Clock()

# Tamaños de objetos
Tamaño_Sprite_Grandes = 125
Tamaño_Basura = 75
Grosor_Pared = 25
Grosor_Pared_Gruesa = 150

# Configuraciónes de objetos
Velocidad_EcoBot = 5
Num_Basuras = 3
Num_Tachos = 3
Tiempo_Para_Generar_Tachos = 20000

# Definicion de la zona donde los objetos pueden spawnear y la zona de los Tachos de reciclaje
Zona_Spawneable = pygame.Rect(Grosor_Pared + 50, Grosor_Pared + 50, Ancho_Pantalla - 150 , Alto_Pantalla - 300)
Zona_Reciclaje = pygame.Rect(480, Alto_Pantalla - Grosor_Pared_Gruesa - Grosor_Pared, 405, Grosor_Pared_Gruesa)

# Fuente para el texto
Fuente_Titulos = pygame.font.SysFont('rockwell', 200) 
Posicion_Titulos = Centro_Pantalla_X, Centro_Pantalla_Y - 75
Fuente_Texto = pygame.font.SysFont('rockwell', 50)
Posicion_Texto = Centro_Pantalla_X, Centro_Pantalla_Y + 125

# Función auxiliar para dibujar texto con borde (full ChatGPT)
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

# Función para dibujar los contadores de basura
def Dibujar_Contador_Basura(Pantalla, Fuente_Texto, Ancho_Pantalla, Alto_Pantalla, Contador_Basura_Metal, Contador_Basura_Vidrio, Contador_Basura_Plastico):
    # Espaciado horizontal entre los contadores
    espaciado = 125  # Ajusta este valor según lo que necesites

    # Posición Y del primer contador (basura metálica)
    posicion_y = Alto_Pantalla - 40  # Cambia esto a la altura deseada

    # Contador de Metal
    Renderizar_Texto(str(Contador_Basura_Metal), Fuente_Texto, Color_Blanco, 5, Color_Negro, Ancho_Pantalla - 370, posicion_y, Pantalla)
    Pantalla.blit(Sprite_Basura_Metal, (Ancho_Pantalla - 407.5, Alto_Pantalla - 150))  # Imagen debajo del contador

    # Contador de Vidrio
    Renderizar_Texto(str(Contador_Basura_Vidrio), Fuente_Texto, Color_Blanco, 5, Color_Negro, Ancho_Pantalla - 370 + espaciado, posicion_y, Pantalla)
    Pantalla.blit(Sprite_Basura_Vidrio, (Ancho_Pantalla - 407.5 + espaciado, Alto_Pantalla - 150))  # Imagen debajo del contador

    # Contador de Plástico
    Renderizar_Texto(str(Contador_Basura_Plastico), Fuente_Texto, Color_Blanco, 5, Color_Negro, Ancho_Pantalla - 370 + espaciado * 2, posicion_y, Pantalla)
    Pantalla.blit(Sprite_Basura_Plastico, (Ancho_Pantalla - 407.5 + espaciado * 2, Alto_Pantalla - 150))  # Imagen debajo del contador

# Muestra la pantalla de inicio
def Mostrar_Pantalla_Inicio():
    Pantalla.fill(Color_Gris)
    Renderizar_Texto('EcoBot', Fuente_Titulos, Color_Fondo, 10, Color_Negro, Posicion_Titulos[0] - 250, Posicion_Titulos[1], Pantalla)
    Renderizar_Texto('Presiona "Enter" para Jugar', Fuente_Texto, Color_Blanco, 5, Color_Negro, Posicion_Texto[0] - 250, Posicion_Texto[1], Pantalla)
    Pantalla.blit(Sprite_EcoBot_Menu, (Posicion_Titulos[0] + 125, Posicion_Titulos[1] - 175))
    pygame.display.flip()

# Muestra el mensaje de "Game Over"
def Mostrar_Pantalla_Game_Over():
    Renderizar_Texto('¡Perdiste!', Fuente_Titulos, Color_Rojo, 10, Color_Negro, *Posicion_Titulos, Pantalla)
    Renderizar_Texto('Presiona "R" para volver a Jugar', Fuente_Texto, Color_Blanco, 5, Color_Negro, *Posicion_Texto, Pantalla)
    pygame.display.flip()

# Genera una posición dentro de la zona spawneable
def Generador_Posicion(Sprite_Tamano, Objetos_Existentes):
    while True:
        x = random.randint(Zona_Spawneable.left, Zona_Spawneable.right - Sprite_Tamano)
        y = random.randint(Zona_Spawneable.top, Zona_Spawneable.bottom - Sprite_Tamano)
        Nueva_Posicion = pygame.Rect(x, y, Sprite_Tamano, Sprite_Tamano)

        # Verificar que no colisiona con otras Posiciones existentes (esto esta medio roto)
        if not any(Nueva_Posicion.colliderect(pygame.Rect(o[0], o[1], Sprite_Tamano, Sprite_Tamano)) for o in Objetos_Existentes):
            return [x, y]

# Generar múltiples Basuras con rotación aleatoria
def Generar_Basuras(Num_Basuras, Sprite_Tamano, Posiciones_Tachos):
    Basuras = []
    while len(Basuras) < Num_Basuras:
        Nueva_Basura = Generador_Posicion(Sprite_Tamano, Basuras + Posiciones_Tachos)
        if Nueva_Basura not in Basuras and Nueva_Basura not in Posiciones_Tachos:
            # Añadir también una rotación aleatoria junto con la posición
            angulo_rotacion = random.randint(-60, 60)
            Basuras.append((Nueva_Basura[0], Nueva_Basura[1], angulo_rotacion))  # Incluye la rotación en la lista
    return Basuras

# Generar múltiples Tachos de Basura
def Generar_Tachos(Num_Tachos, Sprite_Tamano, Posiciones_Basura):
    Tachos = []
    while len(Tachos) < Num_Tachos:
        Nuevo_Tacho = Generador_Posicion(Sprite_Tamano, Tachos + Posiciones_Basura)
        Tachos.append(Nuevo_Tacho)
    return Tachos


# -------------------------------------------------------------------------------------------------------------
# Configuraciones para el Minijuego
# -------------------------------------------------------------------------------------------------------------

# Variables del juego
clock = pygame.time.Clock()
font = pygame.font.Font(None, 36)
vida = 3
puntaje = 0
game_active = True
selected_tacho = None
previous_tacho = None

# Definimos los tipos de desechos
tipos_de_basura = ["plástico", "vidrio", "metal"]

# Configuraciones del jugador y los tachos
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

# # Función para dibujar texto (essssssssssssssssssssssssssssssssssssssssssta no deberia existir)
# def draw_text(text, font, color, surface, x, y):
#     text_obj = font.render(text, True, color)
#     text_rect = text_obj.get_rect()
#     text_rect.topleft = (x, y)
#     surface.blit(text_obj, text_rect)
def dibujar_vidas(pantalla, vidas, sprite_corazon, x, y):
    # Dibujar los corazones en la parte superior izquierda de la pantalla
    for i in range(vidas):
        pantalla.blit(sprite_corazon, (10 + i * 40, 10))  # Los corazones se dibujan con un espacio entre ellos

def dibujar_puntaje(pantalla, puntaje):
    # Crear el texto del puntaje
    texto_puntaje = font.render(f"Puntaje: {puntaje}", True, (0, 0, 0))  # Texto en negro
    # Obtener el rectángulo del texto para posicionarlo en la parte inferior derecha
    rect_texto = texto_puntaje.get_rect(bottomright=(Ancho_Pantalla - 10, Alto_Pantalla - 10))
    # Dibujar el texto en la pantalla
    pantalla.blit(texto_puntaje, rect_texto)
# Función para generar un desecho aleatorio
def Generar_Basura_random():
    tipo_basura = random.choice(tipos_de_basura)
    # Cambiar el rango de generación para que caiga en toda la pantalla
    x_position = random.randint(0, Ancho_Pantalla - 30)  # 30 es el ancho del rectángulo de desecho
    waste_rect = pygame.Rect(x_position, 0, 30, 30)  # Un rectángulo que representa el desecho
    return {"type": tipo_basura, "rect": waste_rect}

# Generar el primer desecho al inicio
basura_actual = Generar_Basura_random()


# -------------------------------------------------------------------------------------------------------------
# Clases para las Basuras
# -------------------------------------------------------------------------------------------------------------

# Clase Madre para las basuras
class Basura:
    def __init__(self, Sprite, Sonido, Tipo):
        self.Sprite = Sprite
        self.Sonido = Sonido
        self.Tipo = Tipo

# Subclase Basura Metal
class Basura_Metal(Basura):
    def __init__(self):
        super().__init__(Sprite_Basura_Metal, Agarrar_Metal, "Metal")

# Subclase Basura Plastico
class Basura_Plastico(Basura):
    def __init__(self):
        super().__init__(Sprite_Basura_Plastico, Agarrar_Plastico , "Plastico")

# Subclase Basura Vidrio
class Basura_Vidrio(Basura):
    def __init__(self):
        super().__init__(Sprite_Basura_Vidrio, Agarrar_Vidrio, "Vidrio")

# Define la lista de Tipos_Basura después de definir las clases
Tipos_Basuras = [Basura_Metal, Basura_Plastico, Basura_Vidrio]