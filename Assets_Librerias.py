# Librerias
import pygame
import random
import os

# Inicializacion Pygame y Pygame Mixer
pygame.init()
pygame.mixer.init()

# Colores
Color_Blanco = (225, 225, 225)
Color_Negro = (0, 0, 0)
Color_Gris = (50, 50, 50)
Color_Rojo = (200, 0, 0)
Color_Fondo = (0, 200, 0)
Color_Pared = (0, 150, 0)

# Funcion para cargar assets
def Cargar_Assets(Carpeta_Asset, Nombre_Asset):
    Ruta_Asset = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'Assets', Carpeta_Asset, Nombre_Asset)
    
    if Carpeta_Asset == 'Sprites':  
        return pygame.image.load(Ruta_Asset)
    
    elif Carpeta_Asset == 'Sonidos':  
        return pygame.mixer.Sound(Ruta_Asset)

# Funcion para centrar assets (actualmente solo se usa para el ecobot)
def Centrar_Sprite(Sprite, Posicion):
    Ancho_Sprite, Alto_Sprite = Sprite.get_size()
    Posicion_Centrada = [Posicion[0] - Ancho_Sprite // 2, Posicion[1] - Alto_Sprite // 2]
    return Posicion_Centrada

# Sprites Cargados
Sprite_EcoBot_Frente = Cargar_Assets('Sprites', 'EcoBot - Frente.png')
Sprite_EcoBot_Espalda = Cargar_Assets('Sprites', 'EcoBot - Espalda.png')
Sprite_EcoBot_Izquierda = Cargar_Assets('Sprites', 'EcoBot - Izquierda.png')
Sprite_EcoBot_Derecha = Cargar_Assets('Sprites', 'EcoBot - Derecha.png')

Sprite_Tacho_de_Basura = Cargar_Assets('Sprites', 'Tacho de Basura.png')
Sprite_Tacho_de_Reciclaje_1 = Cargar_Assets('Sprites', 'Tacho de Reciclaje - 1.png')
Sprite_Tacho_de_Reciclaje_2 = Cargar_Assets('Sprites', 'Tacho de Reciclaje - 2.png')
Sprite_Tacho_de_Reciclaje_3 = Cargar_Assets('Sprites', 'Tacho de Reciclaje - 3.png')

Sprite_Basura_Metal_1 = Cargar_Assets('Sprites', 'Basura - Vidrio 1.png')

# Sonidos Cargados
Agarrar_Papel = Cargar_Assets('Sonidos', 'Agarrar_Papel.mp3')
Agarrar_Papel_Simple = Cargar_Assets('Sonidos', 'Agarrar_Papel_Simple.mp3')
Agarrar_Plastico = Cargar_Assets('Sonidos', 'Agarrar_Plastico.mp3')
Agarrar_Vidrio = Cargar_Assets('Sonidos', 'Agarrar_Vidrio.mp3')
Agarrar_Vidrio2 = Cargar_Assets('Sonidos', 'Agarrar_Vidrio2.mp3')

Abrir_Menu = Cargar_Assets('Sonidos', 'Abrir_Menu.mp3')
Ganar_Tachos = Cargar_Assets('Sonidos', 'Ganar_Tachos.mp3')
Perder_Partida = Cargar_Assets('Sonidos', 'Perder_Partida.mp3')
Poner_Mal_Tacho = Cargar_Assets('Sonidos', 'Poner_Mal_Tacho.mp3')