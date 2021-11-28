import pygame
from pygame.sprite import Group
from settings import Settings
from game_stats import GameStats
from scoreboard import Scoreboard
from button import Button
from ship import Ship
import game_functions as gf

def run_game():
    #Inicia el juego y crea el objeto de la pantalla.  
    pygame.init()
    ai_settings = Settings()
    screen = pygame.display.set_mode(
        (ai_settings.screen_width, ai_settings.screen_height))
    pygame.display.set_caption("Alien Invasion")

    # Crea el boton jugar.
    play_button = Button(ai_settings, screen, "Jugar")

    #Crea una instancia para guardar las estadisticas y crear el marcador.
    stats = GameStats(ai_settings)
    sb = Scoreboard(ai_settings, screen, stats)

    # Crea una nave, un grupo de balas, y un grupo de aliens.
    ship = Ship(ai_settings,screen)
    bullets = Group()
    aliens = Group()

    #Crea una flota de aliens.
    gf.create_fleet(ai_settings, screen,ship, aliens)

    #Inicia el loop principal del juego.
    while True:
        gf.check_events(ai_settings, screen, stats, sb, play_button, ship,
            aliens, bullets)

        if stats.game_active:
            ship.update()
            gf.update_bullets(ai_settings, screen, stats, sb, ship, aliens,
                bullets)
            gf.update_aliens(ai_settings, screen,stats,sb, ship, aliens, bullets)
            
        gf.update_screen(ai_settings, screen, stats, sb, ship, aliens,bullets, play_button)

run_game()




