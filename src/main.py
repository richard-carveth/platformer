import pygame
from settings import SCREEN_WIDTH, SCREEN_HEIGHT, FPS
from player import Player
from level import Level

def draw_main_menu(surface):
    surface.fill((30, 30, 30))
    font = pygame.font.Font(None, 72)
    text = font.render("Press ENTER to Start", True, (255, 255, 255))
    rect = text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2))
    surface.blit(text, rect)

def draw_pause_menu(surface):
    surface.fill((30, 30, 30))
    font = pygame.font.Font(None, 72)
    text = font.render("PAUSED Press ESC to continue", True, (255, 255, 255))
    rect = text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2))
    surface.blit(text, rect)

def main():
    # Initializes pygame and its modules
    pygame.init()

    # Allows for a resizable game window
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.RESIZABLE)

    # Creates the surface for the window
    base_surface = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))

    # Sets the title of the game and the clock to manage frame rate
    pygame.display.set_caption("Platformer")
    clock = pygame.time.Clock()

    # Determines the current game state
    current_state = "menu"

    # Initializes the level and player
    level = Level()
    player = Player(level.player_start_pos)
    level.maybe_generate_more(player)

    running = True  # Game loop flag
    while running:
        dt = clock.tick(FPS) / 1000.0 # Time delta for consistant movement

        # Event handling
        for event in pygame.event.get():
            if event.type == pygame.QUIT: # Check for window closure
                running = False
            if current_state == "menu":
                if event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN:
                    current_state = "playing"
            elif current_state == "playing":
                if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                    current_state = "paused"
                else:
                    player.handle_event(event) # Allows for player inputs
            elif current_state == "paused":
                if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                    current_state = "playing"

        if current_state == "playing":
            player.handle_input() # Continuous player inputs (movement etc)
            player.apply_gravity(dt) # Applies gravity physics
            player.update(dt, level.platforms) # Updates player positon and collision

            # Floor and camera boundries
            floor_y = SCREEN_HEIGHT - 50
            level_height = floor_y + 50

            # Calculates camera positon to follow the player
            cam_x = player.rect.centerx - SCREEN_WIDTH // 2
            cam_y = player.rect.centery - SCREEN_HEIGHT // 2

            # Stops the camera showing areas outside of the level
            cam_x = max(0, cam_x)
            cam_y = min(cam_y, level_height - SCREEN_HEIGHT)

            # Draws the surface of the window
            base_surface.fill((135, 206, 235))
            level.draw(base_surface, cam_x, cam_y)
            player.draw(base_surface, cam_x, cam_y)
        elif current_state == "menu":
            draw_main_menu(base_surface)
        elif current_state == "paused":
            draw_pause_menu(base_surface)

        # Scales everything based on screen size
        window_size = screen.get_size()
        base_surface_scaled = pygame.transform.smoothscale(
            base_surface, window_size
        )
        screen.blit(base_surface_scaled, (0, 0))

        # Updates the display with everything drawn
        pygame.display.flip()

    pygame.quit() # Clean up and close after exiting loop

if __name__ == "__main__":
    main()
