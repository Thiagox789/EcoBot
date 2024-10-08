# Librerias
import pygame
import random
import os
import time


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
def Cargar_Asset(Carpeta_Asset, Nombre_Asset):
    Ruta_Asset = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'Assets', Carpeta_Asset, Nombre_Asset)
    
    if Carpeta_Asset == 'Sprites':  
        return pygame.image.load(Ruta_Asset)
    
    elif Carpeta_Asset == 'Sonidos':  
        return pygame.mixer.Sound(Ruta_Asset)
    
    elif Carpeta_Asset == 'Musica':
        return Ruta_Asset


# Funcion para centrar sprites (actualmente solo se usa para el EcoBot)
def Centrar_Sprite(Sprite, Posicion):
    Ancho_Sprite, Alto_Sprite = Sprite.get_size()
    Posicion_Centrada = [Posicion[0] - Ancho_Sprite // 2, Posicion[1] - Alto_Sprite // 2]
    return Posicion_Centrada


# Función para reproducir música
def Reproducir_Musica(Ruta_Musica, Volumen):
    pygame.mixer.music.load(Ruta_Musica)
    pygame.mixer.music.set_volume(Volumen)
    pygame.mixer.music.play(-1)


# Sprites Cargados
Sprite_EcoBot_Menu = Cargar_Asset('Sprites', 'EcoBot - Menu.png')

Sprite_EcoBot_Frente = Cargar_Asset('Sprites', 'EcoBot - Frente.png')
Sprite_EcoBot_Espalda = Cargar_Asset('Sprites', 'EcoBot - Espalda.png')
Sprite_EcoBot_Izquierda = Cargar_Asset('Sprites', 'EcoBot - Izquierda.png')
Sprite_EcoBot_Derecha = Cargar_Asset('Sprites', 'EcoBot - Derecha.png')

Sprite_Tacho_de_Basura = Cargar_Asset('Sprites', 'Tacho de Basura.png')
Sprite_Tacho_de_Reciclaje_1 = Cargar_Asset('Sprites', 'Tacho de Reciclaje - 1.png')
Sprite_Tacho_de_Reciclaje_2 = Cargar_Asset('Sprites', 'Tacho de Reciclaje - 2.png')
Sprite_Tacho_de_Reciclaje_3 = Cargar_Asset('Sprites', 'Tacho de Reciclaje - 3.png')

Sprite_Basura_Metal = Cargar_Asset('Sprites', 'Basura - Metal.png')
Sprite_Basura_Plastico = Cargar_Asset('Sprites', 'Basura - Plastico.png')
Sprite_Basura_Vidrio = Cargar_Asset('Sprites', 'Basura - Vidrio.png')

Sprite_Reloj = Cargar_Asset('Sprites', 'Reloj.png')
Sprite_Corazon = Cargar_Asset('Sprites', 'Corazon.png')
Sprite_Cartel_Peligro = Cargar_Asset('Sprites', 'Cartel Peligro.png')
Sprite_Corona = Cargar_Asset('Sprites', 'Corona.png') 


# Sonidos Cargados
Agarrar_Plastico = Cargar_Asset('Sonidos', 'Agarrar_Plastico.mp3')
Agarrar_Vidrio = Cargar_Asset('Sonidos', 'Agarrar_Vidrio.mp3')
Agarrar_Metal= Cargar_Asset('Sonidos', 'Agarrar_Metal.mp3')

Abrir_Menu = Cargar_Asset('Sonidos', 'Abrir_Menu.mp3')
Perder_Partida = Cargar_Asset('Sonidos', 'Perder_Partida.mp3')
Ganar_Tachos = Cargar_Asset('Sonidos', 'Ganar_Tachos.mp3')
Poner_Mal_Tacho = Cargar_Asset('Sonidos', 'Poner_Mal_Tacho.mp3')


# Musica Cargada
Musica_EcoBot = Cargar_Asset('Musica', 'Musica_EcoBot.mp3')
Musica_Minijuego = Cargar_Asset('Musica', 'Musica_Minijuego.mp3')


# Ajustar Volumen Sonidos
Agarrar_Plastico.set_volume(0.2)  
Agarrar_Vidrio.set_volume(0.2)
Agarrar_Metal.set_volume(0.1) 

Perder_Partida.set_volume(0.3)
Ganar_Tachos.set_volume(0.2)  
Poner_Mal_Tacho.set_volume(0.2) 