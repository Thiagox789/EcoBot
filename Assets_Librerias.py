# Librerias
import pygame
import random
import os

# Inicializar el mixer
pygame.mixer.init()

# Colores
Color_Blanco = (225, 225, 225)
Color_Negro = (0, 0, 0)
Color_Gris = (50, 50, 50)
Color_Rojo = (200, 0, 0)
Color_Fondo = (0, 200, 0)
Color_Pared = (0, 150, 0)

# Función para cargar assets
def cargar_asset(Carpeta_Asset, Nombre_Asset):
    Ruta_Asset = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'Assets', Carpeta_Asset, Nombre_Asset)
    
    if Carpeta_Asset == 'Sprites':  
        return pygame.image.load(Ruta_Asset)
    
    elif Carpeta_Asset == 'Sonidos':  
        return pygame.mixer.Sound(Ruta_Asset)
    
# Cargar sprites
Sprite_EcoBot_Frente = cargar_asset('Sprites', 'EcoBot - Frente.png')
Sprite_EcoBot_Espalda = cargar_asset('Sprites', 'EcoBot - Espalda.png')
Sprite_EcoBot_Izquierda = cargar_asset('Sprites', 'EcoBot - Izquierda.png')
Sprite_EcoBot_Derecha = cargar_asset('Sprites', 'EcoBot - Derecha.png')
# Cargar sonidos
Agarrar_Papel = cargar_asset('Sonidos', 'Agarrar_Papel.mp3')
Agarrar_Papel_Simple = cargar_asset('Sonidos', 'Agarrar_Papel_Simple.mp3')
Agarrar_Plastico = cargar_asset('Sonidos', 'Agarrar_Plastico.mp3')
Agarrar_Vidrio = cargar_asset('Sonidos', 'Agarrar_Vidrio.mp3')
Agarrar_Vidrio2 = cargar_asset('Sonidos', 'Agarrar_Vidrio2.mp3')

Abrir_Menu = cargar_asset('Sonidos', 'Abrir_Menu.mp3')
Ganar_Tachos = cargar_asset('Sonidos', 'Ganar_Tachos.mp3')
Perder_Partida = cargar_asset('Sonidos', 'Perder_Partida.mp3')
Poner_Mal_Tacho = cargar_asset('Sonidos', 'Poner_Mal_Tacho.mp3')
