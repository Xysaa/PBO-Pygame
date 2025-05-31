import pygame
from abc import ABC, abstractmethod
import random

# Gamepad Button Constants (assuming they might be used, or for future reference)
JUMP_BUTTON = 0
ATTACK1_BUTTON = 2
ATTACK2_BUTTON = 1
ATTACK3_BUTTON = 3


class Character(ABC):
    def __init__(self, player, x, y, flip, data, sprite_sheet, animation_steps, sound, screen_height, is_bot=False, joystick=None): #
        self._player = player
        self.initial_x=x 
        self.initial_y=y 
        self._frame_width = data[0]
        self._frame_height = data[1]
        self._image_scale = data[2]
        self._offset = data[3]
        self._flip = flip
        self._sprite_sheet = sprite_sheet
        self._animation_steps = animation_steps # e.g., Warrior: [8, 8, 26, 11, 19, 18, 6, 13]
        self._animation_list = self._load_images()
        self._action = 0 # Current animation set (0:idle, 1:run, 3:attack1, 4:attack2, 5:attack3 for Warrior)
        self._frame_index = 0
        self._image = self._animation_list[self._action][self._frame_index]
        self._update_time = pygame.time.get_ticks()
        self._rect = pygame.Rect((x, y, 80, 180))
        self._rect.bottom = screen_height - 110
        self._vel_y = 0
        self._running = False
        self._jump = False
        self._attacking = False
        self._attack_type = 0 # 1, 2, or 3
        self._attack_cooldown = 0
        self._attack_sound = sound
        self._hit = False
        self._health = 100
        self._alive = True
        self._is_bot = is_bot
        self._screen_height = screen_height
        self._joystick = joystick

        # NEW: Flags for managing damage application per attack execution
        self._attack_damage_applied_count = 0 # Used to track hits for multi-hit or delayed attacks


    @property
    def health(self):
        return self._health

    @property
    def rect(self):
        return self._rect

    @property
    def alive(self):
        return self._alive

    def _load_images(self): #
        animation_list = []
        for y_idx, animation_length in enumerate(self._animation_steps): 
            temp_img_list = []
            for x_idx in range(animation_length):
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
    
    def reset(self): #
        # ... (reset logic remains the same)
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
        self._attack_damage_applied_count = 0 # Reset this too

    def move(self, screen_width, screen_height, surface, target, round_over): #
        # ... (movement input logic remains the same as per previous joystick update) ...
        SPEED = 10
        GRAVITY = 2
        dx, dy = 0, 0
        self._running = False
        keys = pygame.key.get_pressed()
        joy_dx, joy_jump, joy_attack1, joy_attack2, joy_attack3 = 0, False, False, False, False
        if self._joystick:
            if self._joystick.get_numhats() > 0:
                hat_x, _ = self._joystick.get_hat(0); joy_dx = hat_x * SPEED
            joy_jump = self._joystick.get_button(JUMP_BUTTON)
            joy_attack1 = self._joystick.get_button(ATTACK1_BUTTON)
            joy_attack2 = self._joystick.get_button(ATTACK2_BUTTON)
            joy_attack3 = self._joystick.get_button(ATTACK3_BUTTON)

        if not self._attacking and self._alive and not round_over:
            if self._player == 1:
                if keys[pygame.K_a]: dx = -SPEED; self._running = True
                if keys[pygame.K_d]: dx = SPEED; self._running = True
                if keys[pygame.K_w] and not self._jump: self._vel_y = -30; self._jump = True
                if joy_dx != 0: dx = joy_dx; self._running = True
                if joy_jump and not self._jump: self._vel_y = -30; self._jump = True
                perform_attack = False
                if keys[pygame.K_r] or joy_attack1: self._attack_type = 1; perform_attack = True
                elif keys[pygame.K_t] or joy_attack2: self._attack_type = 2; perform_attack = True
                elif keys[pygame.K_e] or joy_attack3: self._attack_type = 3; perform_attack = True
                if perform_attack: self.attack(target) # attack() now mostly initiates
                         
            elif self._player == 2 and not self._is_bot :
                if keys[pygame.K_LEFT]: dx = -SPEED; self._running = True
                if keys[pygame.K_RIGHT]: dx = SPEED; self._running = True
                if keys[pygame.K_UP] and not self._jump: self._vel_y = -30; self._jump = True
                if joy_dx != 0: dx = joy_dx; self._running = True
                if joy_jump and not self._jump: self._vel_y = -30; self._jump = True
                perform_attack = False
                if keys[pygame.K_l] or joy_attack1: self._attack_type = 1; perform_attack = True
                elif keys[pygame.K_k] or joy_attack2: self._attack_type = 2; perform_attack = True
                elif keys[pygame.K_j] or joy_attack3: self._attack_type = 3; perform_attack = True
                if perform_attack: self.attack(target)

            elif self._is_bot: #
                # ... (Bot AI remains the same) ...
                BOT_ATTACK_RANGE = 100; BOT_MIN_ENGAGE_DISTANCE = BOT_ATTACK_RANGE * 0.7
                BOT_JUMP_CHANCE = 0.015; BOT_JUMP_IF_TARGET_HIGHER_BONUS = 0.12 
                BOT_REPOSITION_CHANCE_WHEN_CLOSE_COOLDOWN = 0.15; BOT_HESITATION_CHANCE = 0.25 
                distance_to_target_x = target.rect.centerx - self._rect.centerx
                abs_distance_to_target_x = abs(distance_to_target_x)
                if abs_distance_to_target_x < BOT_ATTACK_RANGE and self._attack_cooldown == 0 and target.alive:
                    if not (random.random() < BOT_HESITATION_CHANCE): 
                        # Bot chooses an attack type
                        if isinstance(self, Warrior): self._attack_type = random.choice([1, 2, 3]) 
                        elif isinstance(self, Mobs): self._attack_type = 1
                        else: self._attack_type = 1
                        self.attack(target) # Bot initiates attack
                if abs_distance_to_target_x > BOT_MIN_ENGAGE_DISTANCE:
                    dx = -SPEED if distance_to_target_x < 0 else SPEED; self._running = True
                elif abs_distance_to_target_x < BOT_ATTACK_RANGE / 2 and self._attack_cooldown > 0:
                    if random.random() < BOT_REPOSITION_CHANCE_WHEN_CLOSE_COOLDOWN: 
                        dx = random.choice([-SPEED / 2, SPEED / 2]); self._running = True
                    else: self._running = False
                else: self._running = False
                if not self._jump and target.alive:
                    current_jump_chance = BOT_JUMP_CHANCE
                    if target.rect.bottom < self._rect.bottom - self._rect.height * 0.6 :
                         current_jump_chance += BOT_JUMP_IF_TARGET_HIGHER_BONUS
                    if random.random() < current_jump_chance: self._vel_y = -30; self._jump = True
        # ... (rest of move physics remains same) ...
        self._vel_y += GRAVITY; dy += self._vel_y
        if self._rect.left + dx < 0: dx = -self._rect.left
        if self._rect.right + dx > screen_width: dx = screen_width - self._rect.right
        if self._rect.bottom + dy > screen_height - 110:
            self._vel_y = 0; self._jump = False; dy = screen_height - 110 - self._rect.bottom
        if target.alive: self._flip = target.rect.centerx < self._rect.centerx
        if self._attack_cooldown > 0: self._attack_cooldown -= 1
        self._rect.x += dx; self._rect.y += dy

    @abstractmethod
    def update(self): pass
    @abstractmethod
    def update_action(self, new_action): pass
    
    # The attack method is now mostly for initiating the attack state
    # and handling instant damage for simple attacks (like Mobs or Warrior's AttackType1).
    # Warrior's AttackType2 and AttackType3 damage will be handled in its specific update method.
    @abstractmethod
    def attack(self, target): pass

    def draw(self, surface): #
        img = pygame.transform.flip(self._image, self._flip, False)
        surface.blit(img, (self._rect.x - (self._offset[0] * self._image_scale),
                           self._rect.y - (self._offset[1] * self._image_scale)))


class Warrior(Character): #
    def __init__(self, player, x, y, flip, data, sprite_sheet, animation_steps, sound, screen_height, is_bot=False, joystick=None):
        super().__init__(player, x, y, flip, data, sprite_sheet, animation_steps, sound, screen_height, is_bot, joystick)
        # Define frames for damage application for specific attacks
        # These are 0-indexed frame numbers within their respective attack animations
        # Warrior animation_steps: [Idle, Run, Jump, Attack1, Attack2, Attack3, Hit, Death]
        # Example: Attack2 (self._action == 4) has 19 frames (indices 0-18)
        # Example: Attack3 (self._action == 5) has 18 frames (indices 0-17)
        self.attack2_damage_frames = [5, 12] # Example: Apply damage on 6th and 13th frame of Attack2 animation
        self.attack3_damage_frame = 1        # Example: Apply damage on 2nd frame of Attack3 animation

    def attack(self, target): #
        if self._attack_cooldown == 0:
            self._attacking = True
            self._attack_sound.play() #
            self._attack_damage_applied_count = 0 # Reset for current attack sequence

            # Attack Type 1 still applies damage instantly here (or could be moved to update too for consistency)
            if self._attack_type == 1:
                attack_width = self._rect.width * 1.8 # Standard attack range
                if self._flip: attacking_rect = pygame.Rect(self._rect.left - attack_width, self._rect.y, attack_width, self._rect.height)
                else: attacking_rect = pygame.Rect(self._rect.right, self._rect.y, attack_width, self._rect.height)
                
                if attacking_rect.colliderect(target.rect) and target.alive:
                    damage = 12 
                    if self._is_bot: damage = int(damage * 0.8)
                    target._health -= damage
                    target._hit = True
                    self._attack_damage_applied_count = 1 # Mark as damage dealt for this attack

            # For Attack Types 2 and 3, damage is handled in update based on animation frames
            # This method just sets the state.

    def _apply_damage(self, target, damage_value):
        """Helper to apply damage and create attacking rect."""
        attack_width = self._rect.width * 1.8 # Standard attack range for Warrior
        if self._flip:
            attacking_rect = pygame.Rect(self._rect.left - attack_width, self._rect.y, attack_width, self._rect.height)
        else:
            attacking_rect = pygame.Rect(self._rect.right, self._rect.y, attack_width, self._rect.height)

        if attacking_rect.colliderect(target.rect) and target.alive:
            base_damage = damage_value
            if self._is_bot:
                base_damage = int(base_damage * 0.8)
            target._health -= base_damage
            target._hit = True
            return True # Damage applied
        return False # No hit

    def update(self, target=None): # Added target for damage application context
        if self._health <= 0:
            self._health = 0; self._alive = False
            self.update_action(7) # Death animation index
        elif self._hit: self.update_action(6) # Hit animation index
        elif self._attacking:
            current_attack_action = 0
            if self._attack_type == 1: current_attack_action = 3 # Animation for attack1
            elif self._attack_type == 2: current_attack_action = 4 # Animation for attack2
            elif self._attack_type == 3: current_attack_action = 5 # Animation for attack3
            self.update_action(current_attack_action)

            # --- Damage application based on animation frame ---
            if target: # Ensure target is passed to update if attacking
                if self._attack_type == 2 and self._action == 4: # Attack2 animation
                    # Hit 1
                    if self._frame_index == self.attack2_damage_frames[0] and self._attack_damage_applied_count == 0:
                        if self._apply_damage(target, 14): # Damage value for attack 2
                            self._attack_damage_applied_count = 1
                    # Hit 2
                    elif self._frame_index == self.attack2_damage_frames[1] and self._attack_damage_applied_count == 1:
                        if self._apply_damage(target, 14): # Damage value for attack 2
                            self._attack_damage_applied_count = 2
                
                elif self._attack_type == 3 and self._action == 5: # Attack3 animation
                    if self._frame_index == self.attack3_damage_frame and self._attack_damage_applied_count == 0:
                        if self._apply_damage(target, 20): # Damage value for attack 3
                            self._attack_damage_applied_count = 1
        
        elif self._jump: self.update_action(2) # Jump animation index
        elif self._running: self.update_action(1) # Run animation index
        else: self.update_action(0) # Idle animation index

        animation_cooldown = 60 # ms per frame
        self._image = self._animation_list[self._action][self._frame_index]
        
        if pygame.time.get_ticks() - self._update_time > animation_cooldown:
            self._frame_index += 1
            self._update_time = pygame.time.get_ticks()
        
        if self._frame_index >= len(self._animation_list[self._action]):
            if not self._alive: # If dead, stay on last death frame
                self._frame_index = len(self._animation_list[self._action]) - 1
            else:
                self._frame_index = 0 # Loop animation
                if self._action in (3, 4, 5): # If an attack animation finished
                    self._attacking = False
                    self._attack_cooldown = 25 
                    if self._is_bot: self._attack_cooldown += 15 
                    self._attack_damage_applied_count = 0 # Reset for next attack sequence
                if self._action == 6: # If hit animation finished
                    self._hit = False
                    self._attack_cooldown = 10 # Small cooldown after being hit

    def update_action(self, new_action): #
        if new_action != self._action:
            self._action = new_action
            self._frame_index = 0
            self._update_time = pygame.time.get_ticks()


class Mobs(Character): #
    # Mobs class remains unchanged as the request was specific to Warrior and its subclasses
    def attack(self, target): #
        if self._attack_cooldown == 0:
            self._attacking = True
            self._attack_sound.play() #
            attack_width = self._rect.width * 1.5 
            if self._flip: attacking_rect = pygame.Rect(self._rect.left - attack_width, self._rect.y, attack_width, self._rect.height)
            else: attacking_rect = pygame.Rect(self._rect.right, self._rect.y, attack_width, self._rect.height)

            if attacking_rect.colliderect(target.rect) and target.alive:
                damage = 9
                if self._is_bot: damage = int(damage * 0.8) # Mobs are always bots
                target._health -= damage
                target._hit = True
    
    def update(self, target=None): # Added target for consistency, though Mobs don't use it here
        if self._health <= 0:
            self._health = 0; self._alive = False
            self.update_action(4) # Death
        elif self._hit: self.update_action(3) # Hit
        elif self._attacking: self.update_action(2) # Attack
        elif self._running: self.update_action(1) # Run
        else: self.update_action(0) # Idle

        animation_cooldown = 80 #
        self._image = self._animation_list[self._action][self._frame_index]
        if pygame.time.get_ticks() - self._update_time > animation_cooldown:
            self._frame_index += 1
            self._update_time = pygame.time.get_ticks()
        if self._frame_index >= len(self._animation_list[self._action]):
            if not self._alive: self._frame_index = len(self._animation_list[self._action]) - 1
            else:
                self._frame_index = 0
                if self._action == 2: # Attack finished
                    self._attacking = False; self._attack_cooldown = 35
                    if self._is_bot: self._attack_cooldown += 25
                if self._action == 3: # Hit finished
                    self._hit = False; self._attacking = False; self._attack_cooldown = 20

    def update_action(self, new_action): #
        if new_action != self._action:
            self._action = new_action
            self._frame_index = 0
            self._update_time = pygame.time.get_ticks()
