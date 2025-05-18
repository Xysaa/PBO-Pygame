import pygame
from abc import ABC, abstractmethod

class Character(ABC):
    def __init__(self, player, x, y, flip, data, sprite_sheet, animation_steps, sound, screen_height, is_bot=False):
        # Encapsulated attributes
        self._player = player
        self._frame_width = data[0]
        self._frame_height = data[1]
        self._image_scale = data[2]
        self._offset = data[3]
        self._flip = flip
        self._sprite_sheet = sprite_sheet
        self._animation_steps = animation_steps
        self._animation_list = self._load_images()
        self._action = 0  # 0:idle, 1:run, 2:jump, 3:attack1, 4:attack2, 5:hit, 6:death
        self._frame_index = 0
        self._image = self._animation_list[self._action][self._frame_index]
        self._update_time = pygame.time.get_ticks()
        self._rect = pygame.Rect((x, y, 80, 180))
        self._rect.bottom = screen_height - 110
        self._vel_y = 0
        self._running = False
        self._jump = False
        self._attacking = False
        self._attack_type = 0
        self._attack_cooldown = 0
        self._attack_sound = sound
        self._hit = False
        self._health = 100
        self._alive = True
        self._is_bot = is_bot
        self._screen_height = screen_height

    @property
    def health(self):
        return self._health

    @property
    def rect(self):
        return self._rect

    @property
    def alive(self):
        return self._alive

    def _load_images(self):
        animation_list = []
        for y, animation in enumerate(self._animation_steps):
            temp_img_list = []
            for x in range(animation):
                img = self._sprite_sheet.subsurface(
                    x * self._frame_width,
                    y * self._frame_height,
                    self._frame_width,
                    self._frame_height
                )
                scaled = pygame.transform.scale(
                    img,
                    (self._frame_width * self._image_scale, self._frame_height * self._image_scale)
                )
                temp_img_list.append(scaled)
            animation_list.append(temp_img_list)
        return animation_list

    def move(self, screen_width, screen_height, surface, target, round_over):
        SPEED = 10
        GRAVITY = 2
        dx, dy = 0, 0
        self._running = False
        self._attack_type = 0

        keys = pygame.key.get_pressed()
        if not self._attacking and self._alive and not round_over:
            # Player 1 controls
            if self._player == 1:
                if keys[pygame.K_a]:
                    dx = -SPEED
                    self._running = True
                if keys[pygame.K_d]:
                    dx = SPEED
                    self._running = True
                if keys[pygame.K_w] and not self._jump:
                    self._vel_y = -30
                    self._jump = True
                if keys[pygame.K_r] or keys[pygame.K_t] or  keys[pygame.K_e]:
                    self.attack(target)
                    if keys[pygame.K_r]:
                        self._attack_type = 1
                    if keys[pygame.K_t]:
                        self._attack_type = 2
                    if keys[pygame.K_e]:
                        self._attack_type = 3
                         
            # Player 2 or Bot controls
            if self._player == 2:
                if self._is_bot:
                    # Simple bot logic
                    if target.rect.centerx < self._rect.centerx:
                        dx = -SPEED
                        self._running = True
                    elif target.rect.centerx > self._rect.centerx:
                        dx = SPEED
                        self._running = True
                    if target.rect.centery < self._rect.centery and not self._jump:
                        self._vel_y = -30
                        self._jump = True
                    if abs(self._rect.centerx - target.rect.centerx) < 100 and self._attack_cooldown == 0:
                        self.attack(target)
                        self._attack_type = 1
                else:
                    if keys[pygame.K_LEFT]:
                        dx = -SPEED
                        self._running = True
                    if keys[pygame.K_RIGHT]:
                        dx = SPEED
                        self._running = True
                    if keys[pygame.K_UP] and not self._jump:
                        self._vel_y = -30
                        self._jump = True
                    if keys[pygame.K_l] or keys[pygame.K_k] or keys[pygame.K_j]:
                        self.attack(target)
                        if keys[pygame.K_l]:
                            self._attack_type = 1
                        if keys[pygame.K_k]:
                            self._attack_type = 2
                        if keys[pygame.K_j]:
                            self._attack_type = 3
        # Apply gravity
        self._vel_y += GRAVITY
        dy += self._vel_y
        # Boundaries
        if self._rect.left + dx < 20:
            dx =20-self._rect.left
        if self._rect.right + dx > screen_width:
            dx = screen_width - self._rect.right
        if self._rect.bottom + dy > screen_height - 110:
            self._vel_y = 0
            self._jump = False
            dy = screen_height - 110 - self._rect.bottom
        # Face each other
        self._flip = target.rect.centerx < self._rect.centerx
        # Cooldown
        if self._attack_cooldown > 0:
            self._attack_cooldown -= 1
        # Update pos
        self._rect.x += dx
        self._rect.y += dy

    def update(self):
        if self._health <= 0:
            self._health = 0
            self._alive = False
            self.update_action(7)
        elif self._hit:
            self.update_action(6)
        elif self._attacking:
            if self._attack_type == 1:
                self.update_action(3)
            elif self._attack_type == 2:
                self.update_action(4)
            elif self._attack_type == 3:
                self.update_action (5)
        elif self._jump:
            self.update_action(2)
        elif self._running:
            self.update_action(1)
        else:
            self.update_action(0)

        animation_cooldown = 50
        self._image = self._animation_list[self._action][self._frame_index]
        if pygame.time.get_ticks() - self._update_time > animation_cooldown:
            self._frame_index += 1
            self._update_time = pygame.time.get_ticks()
        if self._frame_index >= len(self._animation_list[self._action]):
            if not self._alive:
                self._frame_index = len(self._animation_list[self._action]) - 1
            else:
                self._frame_index = 0
                if self._action in (3, 4, 5):
                    self._attacking = False
                    self._attack_cooldown = 20
                if self._action == 6:
                    self._hit = False
                    self._attacking = False
                    self._attack_cooldown = 20

    def update_action(self, new_action):
        if new_action != self._action:
            self._action = new_action
            self._frame_index = 0
            self._update_time = pygame.time.get_ticks()

    @abstractmethod
    def attack(self, target):
        pass

    def draw(self, surface):
        img = pygame.transform.flip(self._image, self._flip, False)
        surface.blit(
            img,
            (self._rect.x - (self._offset[0] * self._image_scale),
             self._rect.y - (self._offset[1] * self._image_scale))
        )


class Warrior(Character):
    def attack(self, target):
        if self._attack_cooldown == 0:
            self._attacking = True
            self._attack_sound.play()
            attacking_rect = pygame.Rect(
                self._rect.centerx - (2 * self._rect.width * self._flip),
                self._rect.y,
                2 * self._rect.width,
                self._rect.height
            )
            if attacking_rect.colliderect(target.rect):
                target._health -= 10
                target._hit = True


class Wizard(Character):
    def attack(self, target):
        if self._attack_cooldown == 0:
            self._attacking = True
            self._attack_sound.play()
            attacking_rect = pygame.Rect(
                self._rect.centerx - (2 * self._rect.width * self._flip),
                self._rect.y,
                2 * self._rect.width,
                self._rect.height
            )
            if attacking_rect.colliderect(target.rect):
                target._health -= 15
                target._hit = True
