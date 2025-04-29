import pygame
from settings import SCREEN_WIDTH, SCREEN_HEIGHT, FPS
from player import Player
from level import Level

def main():
    pygame.init()
    #screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.RESIZABLE)
    base_surface = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("Platformer")
    clock = pygame.time.Clock()

    level = Level()
    player = Player(level.player_start_pos)

    running = True
    while running:
        dt = clock.tick(FPS) / 1000.0

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            player.handle_event(event)

        player.handle_input()
        player.apply_gravity(dt)
        player.update(dt, level.platforms)
        floor_y = SCREEN_HEIGHT - 50
        level_height = floor_y + 50
        cam_x = player.rect.centerx - SCREEN_WIDTH // 2
        cam_y = player.rect.centery - SCREEN_HEIGHT // 2
        cam_x = max(0, cam_x)
        cam_y = min(cam_y, level_height - SCREEN_HEIGHT)

        base_surface.fill((135, 206, 235))
        level.draw(base_surface, cam_x, cam_y)
        player.draw(base_surface, cam_x, cam_y)
        window_size = screen.get_size()
        scaled = pygame.transform.smoothscale(base_surface, window_size)
        screen.blit(scaled, (0, 0))
        pygame.display.flip()

    pygame.quit()

if __name__ == "__main__":
    main()
