from Assets_Librerias import *
import pygame
tipos_basura = [Sprite_Basura_Metal, Sprite_Basura_Plastico, Sprite_Basura_Vidrio]
# Clase base para las basuras
class Basura:
    def __init__(self, sprite, sonido):
        self.sprite = sprite
        self.sonido = sonido

# Subclase BasuraMetal
class BasuraMetal(Basura):
    def __init__(self):
        super().__init__(Sprite_Basura_Metal, Agarrar_Metal)

# Subclase BasuraPlastico
class BasuraPlastico(Basura):
    def __init__(self):
        super().__init__(Sprite_Basura_Plastico, Agarrar_Plastico)

# Subclase BasuraVidrio
class BasuraVidrio(Basura):
    def __init__(self):
        super().__init__(Sprite_Basura_Vidrio, Agarrar_Vidrio)
