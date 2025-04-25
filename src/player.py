import pygame

class Player:
    def __init__(self, start_pos):
        self.rect = pygame.Rect(start_pos[0], start_pos[1], 32, 64)

        self.vx = 0
        self.vy = 0

        self.speed = 200
        self.jump_strength = -300

        self.on_ground = False

    def hand_input(self):
        keys = pygame.key.get_pressed()

        self.vx = 0

        if keys[pygame.K_LEFT] or keys[pygame.K_a]:
            self.vx = -self.speed
        elif keys[pygame.K_RIGHT] or keys[pygame.K_d]:
            self.vx = self.speed

        if (keys[pygame.K_SPACE] or keys[pygame.K_w] or keys[pygame.K_UP]) and self.on_ground:
            self.vy = self.jump_strength
            self.on_ground = False

    def apply_gravity(self, gravity, dt):
        self.vy += gravity * dt * 100

    def update(self, dt, platforms):
        self.rect.x += int(self.vx * dt)

        for plat in platforms:
            if self.rect.colliderect(plat):
                if self.vx > 0:
                    self.rect.right = plat.left
                elif self.vx < 0 :
                    self.rect.left = plat.right
                self.vx = 0

        self.rect.y += int(self.vy * dt)

        self.on_ground = False

        for plat in platforms:
            if self.rect.colliderect(plat):
                if self.vy > 0:
                    self.rect.bottom = plat.top
                    self.on_ground = True
                elif self.vy < 0:
                    self.rect.top = plat.bottom
                self.vy = 0

    def draw(self, surface):
        pygame.draw.rect(surface, (255, 0, 0), self.rect)
