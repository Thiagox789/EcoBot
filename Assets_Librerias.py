# Librerias
import pygame
import random
import os

# Función para cargar assets
def cargar_asset(Carpeta_Asset, Nombre_Asset):
    Ruta_Asset = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'Assets', Carpeta_Asset, Nombre_Asset)
    
    if Carpeta_Asset == 'Sprites':  
        return pygame.image.load(Ruta_Asset)
    
    elif Carpeta_Asset == 'Audios':  
        return pygame.mixer.Sound(Ruta_Asset)
    
# Cargar sprites
Sprite_EcoBot_Frente = cargar_asset('Sprites', 'EcoBot - Frente.png')
Sprite_EcoBot_Espalda = cargar_asset('Sprites', 'EcoBot - Espalda.png')
Sprite_EcoBot_Izquierda = cargar_asset('Sprites', 'EcoBot - Izquierda.png')
Sprite_EcoBot_Derecha = cargar_asset('Sprites', 'EcoBot - Derecha.png')

#  Sonidos
# Efectos de sonido - Agarrar
Agarrar_Papel = r"Efectos_De_Sonido\Agarrar\Agarrar_Papel.mp3"
Agarrar_Papel_Simple = r"Efectos_De_Sonido\Agarrar\Agarrar_Papel_Simple.mp3"
Agarrar_Plastico = r"Efectos_De_Sonido\Agarrar\Agarrar_Plastico.mp3"
Agarrar_Vidrio = r"Efectos_De_Sonido\Agarrar\Agarrar_Vidrio.mp3"
Agarrar_Vidrio2 = r"Efectos_De_Sonido\Agarrar\Agarrar_Vidrio2.mp3"

# Efectos de sonido - Menu
Abrir_Menu = r"Efectos_De_Sonido\Menu\Abrir_Menu.mp3"
Ganar_Tachos = r"Efectos_De_Sonido\Menu\Ganar_Tachos.mp3"
Perder_Partida = r"Efectos_De_Sonido\Menu\Perder_Partida.mp3"
Poner_Mal_Tacho = r"Efectos_De_Sonido\Menu\Poner_Mal_Tacho.mp3"