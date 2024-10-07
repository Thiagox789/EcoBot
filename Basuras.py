from Assets_Librerias import *

# Clase base para las basuras
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