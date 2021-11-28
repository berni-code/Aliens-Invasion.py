class GameStats():
    """Registra las estadisticas para Aliens Invasion."""

    def __init__(self, ai_settings):
        """Inicia las estadisticas."""
        self.ai_settings = ai_settings
        self.reset_stats()
         # El puntaje mas alto no debe ser borrado.
        self.high_score = 0

        # Inicia Aliens Invasion en un estado Inactivo.
        self.game_active = False

    def reset_stats(self):
        """Inicia estadisticas que han cambiado durante el juego."""
        self.ships_left = self.ai_settings.ship_limit
        self.score = 0
        self.level = 1

    def show_score(self):
        """Dibuja el puntaje en la pantalla."""
        self.screen.blit(self.score_image, self.score_rect)
