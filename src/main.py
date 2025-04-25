import pygame
from settings import SCREEN_WIDTH, SCREEN_HEIGHT, FPS, GRAVITY
from player import Player
from level import Level

def main():
    pygame.init()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
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

        player.handle_input()
        player.apply_gravity(GRAVITY, dt)
        player.update(dt, level.platforms)

        screen.fill((135, 206, 235))
        level.draw(screen)
        player.draw(screen)
        pygame.display.flip()

    pygame.quit()

if __name__ == "__main__":
    main()
