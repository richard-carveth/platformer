import pygame
import random
from settings import SCREEN_HEIGHT, SCREEN_WIDTH

class Level:
    def __init__(self):
        self.platforms = [
            pygame.Rect(0, SCREEN_HEIGHT - 50, SCREEN_WIDTH, 50),
            pygame.Rect(200, 600, 100, 20),
            pygame.Rect(400, 500, 150, 20),
            pygame.Rect(900, 500, 150, 20),
            pygame.Rect(1200, 500, 150, 20)
        ]

        self.player_start_pos = (50, SCREEN_HEIGHT - 100)

    def maybe_generate_more(self, player):
        if player.rect.right > self.platforms[-1].right - 800:
            self.generate_more()

    def generate_more(self):
        last_platform = self.platforms[-1]
        start = last_platform.right + random.randint(100, 400)
        min_y = max(0, last_platform.y - 200)
        max_y = min(SCREEN_HEIGHT - 100, last_platform.y + 200)

        width = random.randint(60, 120)
        height = 20
        y = random.randint(min_y, max_y)

        new_platform = pygame.Rect(start, y, width, height)
        self.platforms.append(new_platform)

    def draw(self, surface, cam_x, cam_y):
        for plat in self.platforms:
            shifted_rect = plat.move(-cam_x, -cam_y)
            pygame.draw.rect(surface, (100, 100, 100), shifted_rect)
