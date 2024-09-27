from Assets_Librerias import *

Tipos_Basura = [Sprite_Basura_Metal, Sprite_Basura_Plastico, Sprite_Basura_Vidrio]
# Clase base para las basuras
class Basura:
    def __init__(self, Sprite, Sonido):
        self.Sprite = Sprite
        self.Sonido = Sonido

# Subclase Basura Metal
class Basura_Metal(Basura):
    def __init__(self):
        super().__init__(Sprite_Basura_Metal, Agarrar_Metal)

# Subclase Basura Plastico
class Basura_Plastico(Basura):
    def __init__(self):
        super().__init__(Sprite_Basura_Plastico, Agarrar_Plastico)

# Subclase Basura Vidrio
class Basura_Vidrio(Basura):
    def __init__(self):
        super().__init__(Sprite_Basura_Vidrio, Agarrar_Vidrio)