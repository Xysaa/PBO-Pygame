import pygame
from abc import ABC, abstractmethod
import random

class Character(ABC):
    def __init__(self, player, x, y, flip, data, sprite_sheet, animation_steps, sound, screen_height, is_bot=False):
        self._player = player
        self.initial_x=x 
        self.initial_y=y 
        self._frame_width = data[0]
        self._frame_height = data[1]
        self._image_scale = data[2]
        self._offset = data[3]
        self._flip = flip
        self._sprite_sheet = sprite_sheet
        self._animation_steps = animation_steps
        self._animation_list = self._load_images()
        self._action = 0
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
        for y_idx, animation in enumerate(self._animation_steps): # Renamed y to y_idx
            temp_img_list = []
            for x_idx in range(animation):
                img = self._sprite_sheet.subsurface(
                    x_idx * self._frame_width,
                    y_idx * self._frame_height,
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
    
    def reset(self):
        self._rect.x = self.initial_x
        self._rect.bottom = self._screen_height - 110
        self._health = 100
        self._alive = True
        self._action = 0
        self._frame_index = 0
        self._update_time = pygame.time.get_ticks()
        self._attacking = False
        self._attack_type = 0
        self._attack_cooldown = 0
        self._jump = False
        self._vel_y = 0
        self._hit = False

    def move(self, screen_width, screen_height, surface, target, round_over):
        SPEED = 10
        GRAVITY = 2
        dx, dy = 0, 0
        self._running = False

        keys = pygame.key.get_pressed()
        if not self._attacking and self._alive and not round_over:
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
                         
            if self._player == 2:
                if self._is_bot:
                    # --- Penyesuaian Parameter Bot ---
                    BOT_ATTACK_RANGE = 100  
                    BOT_MIN_ENGAGE_DISTANCE = BOT_ATTACK_RANGE * 0.7
                    BOT_JUMP_CHANCE = 0.015
                    BOT_JUMP_IF_TARGET_HIGHER_BONUS = 0.12 
                    BOT_REPOSITION_CHANCE_WHEN_CLOSE_COOLDOWN = 0.15
                    BOT_HESITATION_CHANCE = 0.25 

                    distance_to_target_x = target.rect.centerx - self._rect.centerx
                    abs_distance_to_target_x = abs(distance_to_target_x)

                    if abs_distance_to_target_x < BOT_ATTACK_RANGE and self._attack_cooldown == 0 and target.alive:
                        if not (random.random() < BOT_HESITATION_CHANCE): 
                            self.attack(target)
                            if isinstance(self, Warrior):
                                self._attack_type = random.choice([1, 2, 3]) 
                            elif isinstance(self, Mobs):
                                self._attack_type = 1
                            else:
                                self._attack_type = 1
                    
                    
                    if abs_distance_to_target_x > BOT_MIN_ENGAGE_DISTANCE:
                        if distance_to_target_x < 0:
                            dx = -SPEED
                        else:
                            dx = SPEED
                        self._running = True
                    elif abs_distance_to_target_x < BOT_ATTACK_RANGE / 2 and self._attack_cooldown > 0:
                        if random.random() < BOT_REPOSITION_CHANCE_WHEN_CLOSE_COOLDOWN: 
                            dx = random.choice([-SPEED / 2, SPEED / 2])
                            self._running = True
                        else:
                            self._running = False
                    else:
                        self._running = False
                    
                    if not self._jump and target.alive:
                        current_jump_chance = BOT_JUMP_CHANCE
                        if target.rect.bottom < self._rect.bottom - self._rect.height * 0.6 :
                             current_jump_chance += BOT_JUMP_IF_TARGET_HIGHER_BONUS

                        if random.random() < current_jump_chance:
                            self._vel_y = -30 
                            self._jump = True
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

        self._vel_y += GRAVITY
        dy += self._vel_y
        if self._rect.left + dx < 0:
            dx = -self._rect.left
        if self._rect.right + dx > screen_width:
            dx = screen_width - self._rect.right
        if self._rect.bottom + dy > screen_height - 110:
            self._vel_y = 0
            self._jump = False
            dy = screen_height - 110 - self._rect.bottom
        if target.alive:
          self._flip = target.rect.centerx < self._rect.centerx
        if self._attack_cooldown > 0:
            self._attack_cooldown -= 1
        self._rect.x += dx
        self._rect.y += dy

    @abstractmethod
    def update(self):
        pass 
    @abstractmethod
    def update_action(self, new_action):
        pass
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

        animation_cooldown = 60
        self._image = self._animation_list[self._action][self._frame_index]
        if pygame.time.get_ticks() - self._update_time > animation_cooldown:
            self._frame_index += 1
            self._update_time = pygame.time.get_ticks()
        if self._frame_index >= len(self._animation_list[self._action]):
            if not self._alive:
                self._frame_index = len(self._animation_list[self._action]) - 1
            else:
                self._frame_index = 0
                if self._action in (3, 4, 5): # Jika selesai serangan
                    self._attacking = False
                    self._attack_cooldown = 25 # Cooldown dasar
                    if self._is_bot:
                        self._attack_cooldown += 15 # Cooldown tambahan untuk bot 
                if self._action == 6: # Jika selesai kena hit
                    self._hit = False
                    self._attack_cooldown = 10


    def update_action(self, new_action):
        if new_action != self._action:
            self._action = new_action
            self._frame_index = 0
            self._update_time = pygame.time.get_ticks()

    def attack(self, target):
        if self._attack_cooldown == 0:
            self._attacking = True
            self._attack_sound.play()
            attack_width = self._rect.width * 1.8
            if self._flip:
                attacking_rect = pygame.Rect(
                    self._rect.left - attack_width, self._rect.y,
                    attack_width, self._rect.height
                )
            else:
                attacking_rect = pygame.Rect(
                    self._rect.right, self._rect.y,
                    attack_width, self._rect.height
                )

            if attacking_rect.colliderect(target.rect) and target.alive:
                damage = 12 
                if self._attack_type == 2: damage = 14
                if self._attack_type == 3: damage = 20
                
                if self._is_bot:
                    damage *= 0.8 
                    damage = int(damage)
                
                target._health -= damage
                target._hit = True


class Mobs(Character):
    def update(self):
        if self._health <= 0:
            self._health = 0
            self._alive = False
            self.update_action(4)
        elif self._hit:
            self.update_action(3)
        elif self._attacking:
            self.update_action(2)
        elif self._running:
            self.update_action(1)
        else:
            self.update_action(0)

        animation_cooldown = 80
        self._image = self._animation_list[self._action][self._frame_index]
        if pygame.time.get_ticks() - self._update_time > animation_cooldown:
            self._frame_index += 1
            self._update_time = pygame.time.get_ticks()
        if self._frame_index >= len(self._animation_list[self._action]):
            if not self._alive:
                self._frame_index = len(self._animation_list[self._action]) - 1
            else:
                self._frame_index = 0
                if self._action == 2: # Jika selesai serangan
                    self._attacking = False
                    self._attack_cooldown = 35 # Cooldown dasar
                    if self._is_bot:
                        self._attack_cooldown += 25 # Cooldown tambahan untuk bot
                if self._action == 3: # Jika selesai kena hit
                    self._hit = False
                    self._attacking = False
                    self._attack_cooldown = 20

    def update_action(self, new_action):
        if new_action != self._action:
            self._action = new_action
            self._frame_index = 0
            self._update_time = pygame.time.get_ticks()

    def attack(self, target):
        if self._attack_cooldown == 0:
            self._attacking = True
            self._attack_sound.play()
            attack_width = self._rect.width * 1.5 
            if self._flip:
                attacking_rect = pygame.Rect(self._rect.left - attack_width, self._rect.y, attack_width, self._rect.height)
            else:
                attacking_rect = pygame.Rect(self._rect.right, self._rect.y, attack_width, self._rect.height)

            if attacking_rect.colliderect(target.rect) and target.alive:
                damage = 9
                
                if self._is_bot:
                    damage *= 0.8 
                    damage = int(damage)

                target._health -= damage
                target._hit = True
