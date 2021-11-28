import sys
from time import sleep

import pygame
from bullet import Bullet
from alien import Alien

def check_keydown_events(event, ai_settings, screen, ship, bullets):
    """Respond to keypresses."""
    if event.key == pygame.K_RIGHT:
        ship.moving_right = True
    elif event.key == pygame.K_LEFT:
                ship.moving_left = True
    elif event.key == pygame.K_SPACE:
        fire_bullet(ai_settings, screen, ship, bullets)
    elif event.key == pygame.K_q:
        sys.exit()
        
def fire_bullet(ai_settings, screen, ship, bullets):
    """Dispara una bala si el limite aun no se ha alcanzado"""
    # Crea una nueva bala y agregala al grupo de las balas.   
    if len(bullets) < ai_settings.bullets_allowed:
        new_bullet = Bullet(ai_settings, screen, ship)
        bullets.add(new_bullet)

def check_keyup_events(event, ship):
    """Respond to key relases."""
    if event.key == pygame.K_RIGHT:
        ship.moving_right = False
    elif event.key == pygame.K_LEFT:
        ship.moving_left = False

def check_events(ai_settings, screen, stats, sb, play_button, ship, aliens,
        bullets):
    """Responde al presionar teclas y mover el mouse"""
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()

        elif event.type == pygame.KEYDOWN:
            check_keydown_events(event,ai_settings, screen, ship, bullets)
        elif event.type == pygame.KEYUP:
            check_keyup_events(event, ship)   
        elif event.type == pygame.MOUSEBUTTONDOWN:
            mouse_x, mouse_y = pygame.mouse.get_pos()
            check_play_button(ai_settings, screen, stats, sb, play_button,
                ship, aliens, bullets, mouse_x, mouse_y)

def check_play_button(ai_settings, screen, stats, sb, play_button, ship,
        aliens,bullets, mouse_x, mouse_y):
    """Empieza un nuevo juego cuando el jugador da click en Play."""
    button_clicked = play_button.rect.collidepoint(mouse_x, mouse_y)
    if button_clicked and not stats.game_active:
        #Resetea las configuraciones del juego.
        ai_settings.initialize_dynamic_settings()

        # Esconde el cursor del mouse.
        pygame.mouse.set_visible(False)
        #Resetea las estadisticas del juego.
        stats.reset_stats()
        stats.game_active = True

        # Resetea las imagenes de los puntajes.
        sb.prep_score()
        sb.prep_high_score()
        sb.prep_level()
        sb.prep_ships()

        # Vacia la lista de aliens y balas.
        aliens.empty()
        bullets.empty()

        # Crea una nueva flota y centra la nave.
        create_fleet(ai_settings, screen , ship, aliens)
        ship.center_ship()
    
def update_bullets(ai_settings, screen, stats, sb, ship, aliens, bullets):
    """Actualiza la posicion de las balas y desaste de las viejas"""
    #Actualiza la posicion de la balas.
    bullets.update()

    #Desaste de las balas que han desaparecido.
    for bullet in bullets.copy():
        if bullet.rect.bottom <= 0:
            bullets.remove(bullet)
    check_bullet_alien_collisions(ai_settings, screen, stats, sb, ship,
        aliens, bullets)

def check_bullet_alien_collisions(ai_settings, screen, stats, sb, ship,
        aliens, bullets):
    """Responde a bullet-alien colisiones."""
    # Remueve cualquier bala y alien que colisionen.
    collisions = pygame.sprite.groupcollide(bullets, aliens ,True ,True)
    if collisions:
        for aliens in collisions.values():
            stats.score += ai_settings.alien_points * len(aliens)
            sb.prep_score()
        check_high_score(stats, sb)

    if len(aliens) == 0:
        # Si la flota entera es destruida empieza otro nivel.
        bullets.empty()
        ai_settings.increase_speed()

        #Incrementa un nivel.
        stats.level += 1
        sb.prep_level()

        create_fleet(ai_settings, screen, ship, aliens)


def get_number_aliens_x(ai_settings, alien_width):
    """Determine the number of aliens that fit in a row."""
    available_space_x = ai_settings.screen_width - 2 * alien_width
    number_aliens_x = int(available_space_x / (2 * alien_width))
    return number_aliens_x

def get_number_rows(ai_settings, ship_height, alien_height):
    """Determina el numero de filas de aliens que caben en la pantalla."""
    available_space_y = (ai_settings.screen_height -
                            (3 * alien_height) - ship_height)
    number_rows = int(available_space_y / (2 * alien_height))
    return number_rows

def create_alien(ai_settings, screen, aliens, alien_number,row_number):
    """Crea un alien y lo coloca en un lugar de la fila."""
    #Espacia entre cada alien es igual al ancho de cada alien.
    alien = Alien(ai_settings, screen)
    alien_width = alien.rect.width
    alien.x = alien_width + 2 * alien_width * alien_number
    alien.rect.x = alien.x
    alien.rect.y = alien.rect.height + 2 * alien.rect.height * row_number
    aliens.add(alien)

def create_fleet(ai_settings, screen, ship, aliens):
    """Crea una flota completa de aliens."""
    #Crea un alien y encuentra el numero en una fila.
    alien = Alien(ai_settings, screen)
    number_aliens_x = get_number_aliens_x(ai_settings, alien.rect.width)
    number_rows = get_number_rows(ai_settings, ship.rect.height,
         alien.rect.height)
   
    #Crea la flota de aliens.
    for row_number in range(number_rows):
        for alien_number in range(number_aliens_x):
            create_alien(ai_settings, screen, aliens, alien_number,
                row_number)

def check_fleet_edges(ai_settings, aliens):
    """Responde apropiadamente si cualquier alien a alcanzado el borde."""
    for alien in aliens.sprites():
        if alien.check_edges():
            change_fleet_direction(ai_settings, aliens)
            break

def change_fleet_direction(ai_settings, aliens):
    """Baja la flota entera y cambia la direccion."""
    for alien in aliens.sprites():
        alien.rect.y += ai_settings.fleet_drop_speed
    ai_settings.fleet_direction *= -1     


def check_aliens_bottom(ai_settings, stats, screen, ship, aliens, bullets):
    """Revisa si algun alien alcanzo la base de la pantalla."""
    screen_rect = screen.get_rect()
    for alien in aliens.sprites():
        if alien.rect.bottom >= screen_rect.bottom:
            # Trata esto como si la nave fuera golpeada.
            ship_hit(ai_settings, stats, screen, ship, aliens, bullets)
            break

def update_aliens(ai_settings,screen, stats, sb, ship, aliens, bullets):
    """
    Revisa si la flota esta en el borde
    Actualiza la posicion de todos los aliens de la flota.
    """
    check_fleet_edges(ai_settings, aliens)
    aliens.update()

    # Busca las colisiones alien-ship.
    if pygame.sprite.spritecollideany(ship, aliens):
        ship_hit (ai_settings, screen, stats, sb, ship, aliens, bullets)
        print("Me dieron , aaahhhhaaaaa me dieron !!!")
        # Busca aliens que toquen la base de la pantalla.
        check_aliens_bottom(ai_settings, screen, stats, sb, ship, aliens, bullets)

def ship_hit(ai_settings, screen, stats, sb, ship, aliens, bullets):
    """Respuesta de la anave al ser golpeada por un alien"""
    if stats.ships_left > 0:
        # Reduce las naves que quedan.
        stats.ships_left -= 1

        # Actualiza el puntaje.
        sb.prep_ships()

        # Vacia las lista de aliens y balas.
        aliens.empty()
        bullets.empty()

        #Crea una flot ay centa la nave.
        create_fleet(ai_settings, screen, ship, aliens)
        ship.center_ship()

        # Pausar.
        sleep(0.5)

    else:
        stats.game_active = False
        pygame.mouse.set_visible(True)

def check_aliens_bottom(ai_settings, screen, stats, sb, ship, aliens, bullets):
    """Revisa si algun alien alcanzo la base de la pantalla."""
    screen_rect = screen.get_rect()
    for alien in aliens.sprites():
        if alien.rect.bottom >= screen_rect.bottom:
            # Trata esto como si la nave fuera golpeada.
            ship_hit(ai_settings, screen, stats, sb, ship, aliens, bullets)
            break

def check_high_score(stats, sb):
    """Revisa si hay un nievo puntaje alto."""
    if stats.score > stats.high_score:
        stats.high_score = stats.score
        sb.prep_high_score()


def update_screen(ai_settings, screen, stats, sb, ship, aliens, bullets,
        play_button):
    """Actualiza las imagenes en la pantalla y gira a una nueva pantalla"""
    #Redibuja la pantalla durante cada paso del loop
    screen.fill(ai_settings.bg_color)
    ship.blitme()
    aliens.draw(screen)
    
    #Redibuja todas las balas detras de la nave y aliens.
    for bullet in bullets:
        bullet.draw_bullet()
    ship.blitme()

    # Dibuja la informacion del puntaje.
    sb.show_score()

    # Dibuja el boton jugar si el juego esta inactivo.
    if not stats.game_active:
        play_button.draw_button()

    # Hace visible la pantalla dibujada mas reciente
    pygame.display.flip()
