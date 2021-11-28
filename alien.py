import pygame
from pygame.sprite import Sprite

class Alien(Sprite):
    """Una clase que representa un solo alien ela flota"""

    def __init__(self, ai_settings, screen):
        """Inicia al alien y establece su posicion inicial"""
        super(Alien, self).__init__()
        self.screen =screen
        self.ai_settings = ai_settings
        
        #Carga la imagen del alien y establece su atibuto rect.
        self.image = pygame.image.load('images/alien.bmp')
        self.rect = self.image.get_rect()

        #Inicia nuevo alien cerca esquina superior izquierda de la pantalla
        self.rect.x =self.rect.width
        self.rect.y = self.rect.height

        #Guarda la posicion exacta del alien.
        self.x = float(self.rect.x)
    
    def blitme(self):
        """Dibuja  al alien en su ubicacion actual"""
        self.screen.blit(self.image, self.rect)

    def check_edges(self):
        """Regresa True si el alien esta al borde de la pantalla."""
        screen_rect = self.screen.get_rect()
        if self.rect.right >= screen_rect.right:
            return True
        elif self.rect.left <= 0:
            return True

    def update(self):
        """Mueve al alien a la derecha o izq."""
        self.x += (self.ai_settings.alien_speed_factor *
                        self.ai_settings.fleet_direction)
        self.rect.x = self.x 