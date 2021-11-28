class Settings():
    """Una clase para guaradar todas las configuraciones para Alien Invasion"""

    def __init__(self):
        """Inicia las configuraciones del juego."""
        # Configuraciónes de la pantalla.
        self.screen_width = 1200
        self.screen_height = 800
        self.bg_color = (230, 230 ,230)

         #Configuraciones de la Ship
        self.ship_limit = 1

        # Configuracion de las Bullets
        self.bullet_width = 3
        self.bullet_height = 15
        self.bullet_color = (150, 0,230 )
        self.bullets_allowed = 5

        # Configuraciones de los Aliens  
        self.fleet_drop_speed = 5

        # Que tan rapido se acelera el juego.
        self.speedup_scale = 1.1
        # Que tan rapido los valores de los puntos de alien se incrementan.
        self.score_scale = 1.5
        self.initialize_dynamic_settings()


    def initialize_dynamic_settings(self):
        """Inicia las configuaraciones que cambian durante el juego."""
        self.ship_speed_factor = 1.5
        self.bullet_speed_factor = 3
        self.alien_speed_factor = 1
        # La dir. de la flota 1 representa derecha; -1 representa izq.
        self.fleet_direction = 1

        #Puntaje 
        self.alien_points = 50
    
    def increase_speed(self):
        """Incrementa las configuraciones de velocidad y valor de puntos."""
        self.ship_speed_factor *= self.speedup_scale
        self.bullet_speed_factor *= self.speedup_scale
        self.alien_speed_factor *= self.speedup_scale
        
        self.alien_points = int(self.alien_points * self.score_scale)
        