import pygame
from settings import SCREEN_HEIGHT, SCREEN_WIDTH
from player import Player

class Level:
    def __init__(self):
        self.platforms = [
            pygame.Rect(0, SCREEN_HEIGHT - 50, SCREEN_WIDTH, 50),
            pygame.Rect(200, 400, 100, 20),
            pygame.Rect(400, 300, 150, 20),
        ]

        self.player_start_pos = (50, SCREEN_HEIGHT - 100)

    def maybe_generate_more(self, player):
        if player.rect.right > self.platforms[-1].right - 300:
            self.generate_more()

    def generate_more():
        pass

    def draw(self, surface, cam_x, cam_y):
        for plat in self.platforms:
            shifted_rect = plat.move(-cam_x, -cam_y)
            pygame.draw.rect(surface, (100, 100, 100), shifted_rect)
            #pygame.draw.rect(surface, (100, 100, 100), plat)
