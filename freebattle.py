import pygame
import sys
from pygame import mixer
from fighter import Warrior, Wizard

# Init
pygame.init()
mixer.init()


# Screen
SCREEN_WIDTH, SCREEN_HEIGHT = 1000, 600
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Ascension of the Chosen")

# Colors & Fonts
WHITE = (255, 255, 255)
RED = (255, 0, 0)
YELLOW = (255, 255, 0)
FONT = pygame.font.Font("assets/fonts/turok.ttf", 32)
COUNT_FONT = pygame.font.Font("assets/fonts/turok.ttf", 80)
SCORE_FONT = pygame.font.Font("assets/fonts/turok.ttf", 30)

# Audio
pygame.mixer.music.load("assets/audio/music.mp3")
pygame.mixer.music.set_volume(0.5)
pygame.mixer.music.play(-1, 0.0, 5000)
sword_fx = pygame.mixer.Sound("assets/audio/sword.wav")
sword_fx.set_volume(0.5)
magic_fx = pygame.mixer.Sound("assets/audio/magic.wav")
magic_fx.set_volume(0.75)

# Assets
bg_image = pygame.image.load("assets/images/background/background.jpg").convert_alpha()
victory_img = pygame.image.load("assets/images/icons/victory.png").convert_alpha()
warrior_sheet = pygame.image.load("assets/images/warrior/Sprites/warrior4r.png").convert_alpha()
wizard_sheet = pygame.image.load("assets/images/warrior/Sprites/warrior4r.png").convert_alpha()

# Config
WARRIOR_DATA = [48, 48, 3, [10, -25]]
WIZARD_DATA = [48, 48, 3, [10, -25]]
WARRIOR_ANIM = [10, 8, 1, 7, 7, 3, 7]
WIZARD_ANIM = [10, 8, 1, 7, 7, 3, 7]

# UI funcs
def draw_text(text, x, y, color=WHITE, font=FONT):
    img = font.render(text, True, color)
    screen.blit(img, (x, y))

def draw_bg():
    screen.blit(pygame.transform.scale(bg_image, (SCREEN_WIDTH, SCREEN_HEIGHT)), (0, 0))

def draw_health_bar(health, x, y):
    ratio = health / 100
    pygame.draw.rect(screen, WHITE, (x - 2, y - 2, 404, 34))
    pygame.draw.rect(screen, RED, (x, y, 400, 30))
    pygame.draw.rect(screen, YELLOW, (x, y, 400 * ratio, 30))

def show_dialogue(lines):
    for line in lines:
        screen.fill((0, 0, 0))
        draw_text(line, 50, SCREEN_HEIGHT // 2)
        pygame.display.update()
        wait_for_key()

def wait_for_key():
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                return

# Battle
def start_battle():

    clock = pygame.time.Clock()
    FPS = 60
    intro_count = 3
    last_count_update = pygame.time.get_ticks()
    round_over = False
    ROUND_OVER_COOLDOWN = 2000
    score = [0, 0]

    fighter_1 = Warrior(1, 200, 400, False, WARRIOR_DATA, warrior_sheet, WARRIOR_ANIM, sword_fx, SCREEN_HEIGHT, is_bot=False)
    fighter_2 = Wizard(2, 700, 400, True, WIZARD_DATA, wizard_sheet, WIZARD_ANIM, magic_fx, SCREEN_HEIGHT, is_bot=True)

    run = True
    while run:
        clock.tick(FPS)
        draw_bg()
        draw_health_bar(fighter_1.health, 20, 20)
        draw_health_bar(fighter_2.health, 580, 20)
        draw_text(f"P1: {score[0]}", 20, 60, RED, SCORE_FONT)
        draw_text(f"P2: {score[1]}", 580, 60, RED, SCORE_FONT)

        if intro_count <= 0:
            fighter_1.move(SCREEN_WIDTH, SCREEN_HEIGHT, screen, fighter_2, round_over)
            fighter_2.move(SCREEN_WIDTH, SCREEN_HEIGHT, screen, fighter_1, round_over)
        else:
            draw_text(str(intro_count), SCREEN_WIDTH // 2, SCREEN_HEIGHT // 3, RED, COUNT_FONT)
            if (pygame.time.get_ticks() - last_count_update) >= 1000:
                intro_count -= 1
                last_count_update = pygame.time.get_ticks()

        fighter_1.update()
        fighter_2.update()
        fighter_1.draw(screen)
        fighter_2.draw(screen)

        if not round_over:
            if not fighter_1.alive:
                score[1] += 1
                round_over = True
                round_over_time = pygame.time.get_ticks()
            elif not fighter_2.alive:
                score[0] += 1
                round_over = True
                round_over_time = pygame.time.get_ticks()
        else:
            screen.blit(victory_img, (360, 150))
            if pygame.time.get_ticks() - round_over_time > ROUND_OVER_COOLDOWN:
                run = False

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.mixer.music.stop()
                pygame.quit()
                sys.exit()

        pygame.display.update()

# Story sequence
    
   
if __name__ == "__main__":
    pass

