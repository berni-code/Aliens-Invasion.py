import pygame

class Ship():

    def __init__(self, ai_settings, screen):
        """Inicia la nave y establece la posicion de inicio."""
        self.screen = screen
        self.ai_settings = ai_settings

        #Carga la imagen de la nave.
        self.image = pygame.image.load('images/ship.bmp')
        self.rect = self.image.get_rect()
        self.screen_rect = screen.get_rect()

        # Inicia cada nueva nave al fondo y centro de la pantalla.
        self.rect.centerx = self.screen_rect.centerx
        self.rect.bottom = self.screen_rect.bottom

        # Guarda un valor decimal para el centro de la nave
        self.center = float(self.rect.centerx)

        # Bandera de movimiento 
        self.moving_right = False
        self.moving_left = False

    def update(self):
        """Actualiza la posicion de la nave basado en el movimiento de la bandera"""
        #Actualiza el valor del centro de la nave, no el rect.
        if self.moving_right and self.rect.right < self.screen_rect.right:
            self.center += self.ai_settings.ship_speed_factor
        if self.moving_left and self.rect.left > 0:
            self.center -= self.ai_settings.ship_speed_factor
        # Actualiza objeto rect de self.center
        self.rect.centerx = self.center
            
    def blitme(self):
        """Dibuja la nave en su ubicacion actual"""
        self.screen.blit(self.image, self.rect)

    def center_ship(self):
        """Centra la nave en la pantalla."""
        self.center = self.screen_rect.centerx

    