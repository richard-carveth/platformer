import pygame
from settings import GRAVITY, MAX_FALL_SPEED, COYOTE_TIME, JUMP_BUFFER_TIME

class Player:
    def __init__(self, start_pos):
        self.pos_x = float(start_pos[0])
        self.pos_y = float(start_pos[1])
        self.rect = pygame.Rect(int(self.pos_x), int(self.pos_y), 32, 64)

        self.vx = 0
        self.vy = 0
        self.speed = 200
        self.jump_strength = -700
        self.max_fall_speed = MAX_FALL_SPEED

        self.on_ground = True
        self.coyote_timer = 0.0
        self.jump_buffer_timer = 0.0

    def handle_event(self, event):
        if event.type == pygame.KEYDOWN and event.key in (pygame.K_SPACE, pygame.K_w, pygame.K_UP):
            self.jump_buffer_timer = JUMP_BUFFER_TIME


    def handle_input(self):
        keys = pygame.key.get_pressed()
        self.vx = 0
        if keys[pygame.K_LEFT] or keys[pygame.K_a]:
            self.vx = -self.speed
        elif keys[pygame.K_RIGHT] or keys[pygame.K_d]:
            self.vx = self.speed

    def apply_gravity(self, dt):
        self.vy += GRAVITY * dt
        self.vy = min(self.vy, self.max_fall_speed)

    def update(self, dt, platforms):
        if not self.on_ground and self.coyote_timer > 0.0:
            self.coyote_timer = max(0.0, self.coyote_timer - dt)
        if self.jump_buffer_timer > 0.0:
            self.jump_buffer_timer = max(0.0, self.jump_buffer_timer - dt)

        self.pos_x += self.vx * dt
        self.rect.x = int(self.pos_x)
        for plat in platforms:
            if self.rect.colliderect(plat):
                if self.vx > 0:
                    self.rect.right = plat.left
                elif self.vx < 0:
                    self.rect.left = plat.right
                self.pos_x = float(self.rect.x)
                self.vx = 0.0

        self.pos_y += self.vy * dt
        self.rect.y = int(self.pos_y)
        self.on_ground = False

        for plat in platforms:
            if self.rect.colliderect(plat):
                if self.vy > 0:
                    self.rect.bottom = plat.top
                    self.on_ground = True
                    self.coyote_timer = COYOTE_TIME
                elif self.vy < 0:
                    self.rect.top = plat.bottom
                self.pos_y = float(self.rect.y)
                self.vy = 0.0

        if (self.on_ground or self.coyote_timer > 0.0) and self.jump_buffer_timer > 0.0:
            self.vy = self.jump_strength
            self.on_ground = False
            self.coyote_timer = 0.0
            self.jump_buffer_timer = 0.0

    def draw(self, surface):
        pygame.draw.rect(surface, (255, 0, 0), self.rect)
