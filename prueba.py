from EcoBot import *
def Inicializar_Juego():
    global Game_Over, Juego_Iniciado, EcoBot_en_Movimiento, Zona_Reciclaje_Tocada #Contador_Basura_Metal, Contador_Basura_Vidrio, Contador_Basura_Plastico
    global Sprite_Actual_EcoBot, Posicion_EcoBot, Direccion, Posiciones_Basura, Tipos_Basuras_Generada, Posiciones_Tachos, Ultima_Generacion_Tacho, Contador_Tachos_Generados

    Game_Over = False
    Juego_Iniciado = False
    EcoBot_en_Movimiento = False
    Zona_Reciclaje_Tocada = False

    #Contador_Basura_Metal = 0
    #Contador_Basura_Vidrio = 0
    #Contador_Basura_Plastico = 0  

    Sprite_Actual_EcoBot = Sprite_EcoBot_Frente
    Posicion_EcoBot = Centrar_Sprite(Sprite_Actual_EcoBot, [Centro_Pantalla_X, Centro_Pantalla_Y])
    Direccion = None

    # Genera las posiciones y tipos de basura iniciales
    Posiciones_Basura = Generar_Basuras(Num_Basuras, Tamaño_Basura, [])
    Tipos_Basuras_Generada = [random.choice(Tipos_Basuras)() for _ in range(Num_Basuras)]

    Posiciones_Tachos = []
    Ultima_Generacion_Tacho = pygame.time.get_ticks()
    Contador_Tachos_Generados = 0
Ciclo_Juego()