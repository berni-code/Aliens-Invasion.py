import pygame
from pygame.sprite import Sprite

class Bullet(Sprite):
    """Una clase que dispara balas de la nave"""

    def __init__(self, ai_settings, screen, ship):
        """Crea una objeto de bala en la posiscion actual de la nave."""
        super(Bullet, self).__init__()
        self.screen = screen

        #Crea una bala rect en (0, 0) y establece la posicion correcta.
        self.rect = pygame.Rect(0 , 0 , ai_settings.bullet_width,
            ai_settings.bullet_height) 
        self.rect.centerx = ship.rect.centerx
        self.rect.top = ship.rect.top

        # Guarda la posicion de la bala en un valor decimal.
        self.y = float(self.rect.y)

        self.color = ai_settings.bullet_color
        self.speed_factor = ai_settings.bullet_speed_factor

    def update(self):
        """"Mueve la bala hacie arriba en la pantalla."""
        #Actualiza el valor decimal de la bala.
        self.y -= self.speed_factor
        #Actualiza la posicion rect.
        self.rect.y = self.y

    def draw_bullet(self):
        """Dibuja una bala en la pantalla."""
        pygame.draw.rect(self.screen, self.color, self.rect)
