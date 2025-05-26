import pygame
from pygame import mixer
from fighter import Warrior, Mobs
from character_data import CHARACTER_DATA
from character_assets import load_character_assets
from start_battle import start_battle as run_battle
from char_sel import select_characters

mixer.init()
pygame.init()

# Create game window
SCREEN_WIDTH = 1000
SCREEN_HEIGHT = 600
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("THe Choosen")

# Colors
RED = (255, 0, 0)
YELLOW = (255, 255, 0)
WHITE = (255, 255, 255)
GREY = (200, 200, 200)
BLACK = (0, 0, 0)
GREEN = (0, 180, 0)
DARK_RED = (180, 0, 0)
DARK_BlUE = (74,84,98)

# Fighter config
assets = load_character_assets()

bg_image = pygame.image.load("assets/images/background/background.jpeg").convert_alpha()
victory_img = pygame.image.load("assets/images/icons/victory.png").convert_alpha()

# Text funcs
font_large = pygame.font.Font("assets/fonts/turok.ttf", 80)
font_med = pygame.font.Font("assets/fonts/turok.ttf", 40)
font_small = pygame.font.Font("assets/fonts/turok.ttf", 30)

def draw_text(text, font, color, x, y):
    img = font.render(text, True, color)
    screen.blit(img, (x, y))

def draw_bg():
    screen.blit(pygame.transform.scale(bg_image, (SCREEN_WIDTH, SCREEN_HEIGHT)), (0, 0))

def draw_health_bar(health, x, y):
    ratio = health / 100
    pygame.draw.rect(screen, WHITE, (x - 2, y - 2, 404, 34))
    pygame.draw.rect(screen, RED, (x, y, 400, 30))
    pygame.draw.rect(screen, DARK_BlUE, (x, y, 400 * ratio, 30))
    
def start_battle():
    fighter_1_selected, fighter_2_selected = select_characters(screen, font_small, font_med, assets, SCREEN_WIDTH, SCREEN_HEIGHT)
    if fighter_1_selected is None or fighter_2_selected is None:
        print("Character selection was cancelled or quit.")
        return True
    return_to_main_menu = run_battle(
        SCREEN_WIDTH, SCREEN_HEIGHT, screen,
        draw_bg, font_small, font_med, font_large,
        draw_health_bar, draw_text,
        fighter_1_selected, fighter_2_selected,
        victory_img,
        is_story=False)
    return return_to_main_menu
if __name__ == "__main__":
    pass


