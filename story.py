
import pygame
from pygame import mixer
from fighter import Warrior, Wizard
import start_battle
from character_data import CHARACTER_DATA
from character_assets import load_character_assets
from start_battle import start_battle as run_battle

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

# Fighter config
assets = load_character_assets()
warrior_data = CHARACTER_DATA["warrior"]
warrior_assets = assets["warrior"]
wizard_data = CHARACTER_DATA["wizard"]
wizard_assets = assets["wizard"]
#
bg_image = pygame.image.load("assets/images/background/background.jpg").convert_alpha()
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
    pygame.draw.rect(screen, YELLOW, (x, y, 400 * ratio, 30))

def show_dialogue(lines):
    try:
        pygame.mixer.music.load("assets/audio/story.wav")
        pygame.mixer.music.set_volume(0.5)
        pygame.mixer.music.play(-1, 0.0, 5000)
    except pygame.error as e:
        print(f"Error loading battle music: {e}")
    for line in lines:
        screen.fill((0, 0, 0))
        draw_text(line, font_small,WHITE,20,SCREEN_HEIGHT // 2)
        pygame.display.update()
        if not wait_for_key():
            return False
    return True

def wait_for_key():
    waiting = True
    while waiting:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False
            if event.type == pygame.KEYDOWN:
                return True

    return True

# fighter1_data = Warrior(1, 200, SCREEN_HEIGHT, False, [*warrior_data["size"], warrior_data["scale"], warrior_data["offset"]], warrior_assets["image"], warrior_data["animation_steps"], warrior_assets["sound"], SCREEN_HEIGHT,is_bot=False)    
# fighter2_data = Wizard(2, 700, SCREEN_HEIGHT, True, [*wizard_data["size"],wizard_data["scale"], wizard_data["offset"]],wizard_assets["image"],wizard_data["animation_steps"],wizard_assets["sound"],SCREEN_HEIGHT, is_bot=False)
#

# run_battle(screen, draw_bg, font_small, font_med, font_large, draw_health_bar, draw_text, Warrior, Wizard, [*warrior_data["size"], warrior_data["scale"], warrior_data["offset"]], [*wizard_data["size"], wizard_data["scale"], wizard_data["offset"]], warrior_assets, wizard_assets, victory_img, "assets/audio/music.mp3")
# start_battle.start_battle(screen, draw_bg, font_small, font_med, font_large, draw_health_bar, draw_text,Warrior, Wizard, fighter1_data, fighter2_data, victory_img)
#
fighter_1 = Warrior(1, 200, SCREEN_HEIGHT, False, [*warrior_data["size"], warrior_data["scale"], warrior_data["offset"]], warrior_assets["image"], warrior_data["animation_steps"], warrior_assets["sound"], SCREEN_HEIGHT,is_bot=False)    
fighter_2 = Wizard(2, 700, SCREEN_HEIGHT, True, [*wizard_data["size"],wizard_data["scale"], wizard_data["offset"]],wizard_assets["image"],wizard_data["animation_steps"],wizard_assets["sound"],SCREEN_HEIGHT, is_bot=False)
def start_battle():
    return_to_main_menu = run_battle(SCREEN_WIDTH,SCREEN_HEIGHT,screen, draw_bg, font_small, font_med, font_large,draw_health_bar, draw_text,fighter_1,fighter_2,victory_img,is_story=True)
    return return_to_main_menu
lore_chapters = [

    [
        "Bab 1: Awal Kebangkitan",
        "Dunia Aetherion pernah damai, hingga Celestial Seal rusak...",
        "Makhluk jahat dari Void menyusup ke dunia nyata.",
        "Kamu dipanggil sebagai salah satu The Chosen..."
    ],
    [
        "Bab 2: Ujian Para Penjaga",
        "Ujian pertama: Crumbling Citadel."
    ],
    [
        "Bab 3: Kebenaran yang Terungkap",
        "Penjaga dulunya pejuang yang jatuh dalam kegelapan...",
        "Satu-satunya yang tersisa adalah Stevanus. Tapi ia menghilang..."
    ],
    [
        "Bab 4: Pertemuan Takdir",
        "Stevanus muncul di Skyhold, menantangmu dalam duel akhir."
    ]
]


def main_story():
    for i, chapter in enumerate (lore_chapters):
        if not show_dialogue(chapter):
            return 
        
        play_menu = start_battle()
        #mengembalikan ke main menu ketika main menu di klik
        if play_menu:
            return
        #reset kondisi karakter ketika memasuki chapter baru
        fighter_1.reset()
        fighter_2.reset()
    show_dialogue([
        "Kamu menang! Stevanus kini menjadi karakter baru di Free Battle.",
        "Tapi... celah ke Void belum sepenuhnya tertutup..."
    ])
if __name__ == "__main__":
    pass


