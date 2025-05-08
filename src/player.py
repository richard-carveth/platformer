import pygame
import settings
class Player:
    def __init__(self, start_pos):
        # Initialize player positon
        self.pos_x = float(start_pos[0])
        self.pos_y = float(start_pos[1])

        # Collision box and sprite
        self.rect = pygame.Rect(int(self.pos_x), int(self.pos_y), 32, 64)
        self.image = pygame.image.load("assets/player.png").convert_alpha()
        self.image = pygame.transform.scale(self.image, (self.rect.width, self.rect.height))

        # Physics properties
        self.vx = 0 # Horizontal velocity
        self.vy = 0 # Vertical velocity
        self.speed = 200 # Movement speed
        self.jump_strength = -700 # Jump velocity
        self.max_fall_speed = settings.MAX_FALL_SPEED

        # Direction detection (1 = right, -1 = left)
        self.facing = 1

        # Jump mechanics
        self.jump_count = 0
        self.is_gliding = False

        # Dash mechanics
        self.is_dashing = False
        self.dash_timer = 0.0
        self.can_dash = True
        self.dash_direction = 0

        # Ground state and advanced jump logic
        self.on_ground = True
        self.coyote_timer = 0.0
        self.jump_buffer_timer = 0.0

    # Handles input events such as jumping and dashing
    def handle_event(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key in (pygame.K_SPACE, pygame.K_w, pygame.K_UP):
                # Jump buffer timer
                self.jump_buffer_timer = settings.JUMP_BUFFER_TIME

            # Initiate dash
            if event.key == pygame.K_c and (not self.is_dashing and self.can_dash):
                self.dash_direction = self.facing
                self.is_dashing = True
                self.dash_timer = settings.DASH_TIME
                self.can_dash = False

    # Handles continuous keyboard input for movement
    def handle_input(self):
        keys = pygame.key.get_pressed()
        self.vx = 0

        # Determins if gliding should happen
        self.is_gliding = (
            (keys[pygame.K_SPACE] or keys[pygame.K_w] or keys[pygame.K_UP]) and
            not self.on_ground and
            self.jump_count >= 2
        )

        # Movement
        if keys[pygame.K_LEFT] or keys[pygame.K_a]:
            self.vx = -self.speed
            self.facing = -1
        elif keys[pygame.K_RIGHT] or keys[pygame.K_d]:
            self.vx = self.speed
            self.facing = 1

    # Handles gravity physics based on dt, also changes if gliding
    def apply_gravity(self, dt):
        self.vy = min(self.vy, self.max_fall_speed)
        if self.is_gliding and self.vy > 0:
            self.vy += (settings.GRAVITY * 0.3) * dt
        else:
            self.vy += settings.GRAVITY * dt

    # Handles player state, movement, collisions, and actions
    def update(self, dt, platforms):

        # Timers for advanced jumping and dashing
        if not self.on_ground and self.coyote_timer > 0.0:
            self.coyote_timer = max(0.0, self.coyote_timer - dt)
        if self.jump_buffer_timer > 0.0:
            self.jump_buffer_timer = max(0.0, self.jump_buffer_timer - dt)
        if self.is_dashing:
            self.dash_timer -= dt
            if self.dash_timer <= 0:
                self.is_dashing = False

        # Switches to dash movement, defaults to right
        effective_vx = settings.DASH_SPEED * self.dash_direction if self.is_dashing else self.vx

        # Horizontal movement and collision
        self.pos_x += effective_vx * dt
        self.rect.x = int(self.pos_x)
        for plat in platforms:
            if self.rect.colliderect(plat):
                if effective_vx > 0:
                    self.rect.right = plat.left
                elif effective_vx < 0:
                    self.rect.left = plat.right
                self.pos_x = float(self.rect.x)
                effective_vx = 0

        # Vertical movement and collision
        self.pos_y += self.vy * dt
        self.rect.y = int(self.pos_y)
        self.on_ground = False

        for plat in platforms:
            if self.rect.colliderect(plat):
                if self.vy > 0:
                    self.rect.bottom = plat.top
                    self.on_ground = True
                    self.can_dash = True
                    self.coyote_timer = settings.COYOTE_TIME
                    self.jump_count = 0
                elif self.vy < 0:
                    self.rect.top = plat.bottom
                self.pos_y = float(self.rect.y)
                self.vy = 0.0

        # Jumping logic to facilitate double jump, gliding and buffered jumps
        if self.jump_count == 0 and (self.on_ground or self.coyote_timer > 0) and self.jump_buffer_timer > 0:
            self.vy = self.jump_strength
            self.on_ground = False
            self.coyote_timer = 0
            self.jump_buffer_timer = 0
            self.jump_count = 1
        elif self.jump_count == 1 and self.jump_buffer_timer > 0:
            self.vy = self.jump_strength * 0.50
            self.jump_buffer_timer = 0
            self.jump_count = 2

    # Draws the player and other visual effects
    def draw(self, surface, cam_x, cam_y):

        local_x = self.rect.x - cam_x
        local_y = self.rect.y - cam_y

        surface.blit(self.image, (local_x, local_y))

        # Gliding visuals
        if self.is_gliding:
            w, h = 52, 8
            x, y = self.rect.topleft
            spinning_ears = pygame.Rect(local_x - 10, local_y + 6, w, h)
            pygame.draw.rect(surface, (255, 200, 0), spinning_ears)
