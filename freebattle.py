import pygame
from pygame import mixer
from fighter import Warrior, Wizard
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
    
# fighter1_data = Warrior(1, 200, SCREEN_HEIGHT, False, [*warrior_data["size"], warrior_data["scale"], warrior_data["offset"]], warrior_assets["image"], warrior_data["animation_steps"], warrior_assets["sound"], SCREEN_HEIGHT,is_bot=False)    
# fighter2_data = Wizard(2, 700, SCREEN_HEIGHT, True, [*wizard_data["size"],wizard_data["scale"], wizard_data["offset"]],wizard_assets["image"],wizard_data["animation_steps"],wizard_assets["sound"],SCREEN_HEIGHT, is_bot=False)
#

# run_battle(screen, draw_bg, font_small, font_med, font_large, draw_health_bar, draw_text, Warrior, Wizard, [*warrior_data["size"], warrior_data["scale"], warrior_data["offset"]], [*wizard_data["size"], wizard_data["scale"], wizard_data["offset"]], warrior_assets, wizard_assets, victory_img, "assets/audio/music.mp3")
# start_battle.start_battle(screen, draw_bg, font_small, font_med, font_large, draw_health_bar, draw_text,Warrior, Wizard, fighter1_data, fighter2_data, victory_img)
#
fighter_1 = Warrior(1, 200, SCREEN_HEIGHT, False, [*warrior_data["size"], warrior_data["scale"], warrior_data["offset"]], warrior_assets["image"], warrior_data["animation_steps"], warrior_assets["sound"], SCREEN_HEIGHT,is_bot=False)    
fighter_2 = Wizard(2, 700, SCREEN_HEIGHT, True, [*wizard_data["size"],wizard_data["scale"], wizard_data["offset"]],wizard_assets["image"],wizard_data["animation_steps"],wizard_assets["sound"],SCREEN_HEIGHT, is_bot=False)
def start_battle():
    run_battle(SCREEN_WIDTH,SCREEN_HEIGHT,screen, draw_bg, font_small, font_med, font_large,draw_health_bar, draw_text,fighter_1,fighter_2,victory_img)

if __name__ == "__main__":
    pass

# def start_battle():
#     clock = pygame.time.Clock()
#     FPS = 60
#
#     intro_count = 3
#     last_count_update = pygame.time.get_ticks()
#     score = [0, 0]
#     round_over = False
#     ROUND_OVER_COOLDOWN = 2000
#     round_over_time = 0
#
#     paused = False
#     pause_button_rect = pygame.Rect(SCREEN_WIDTH // 2 - 40, 10, 80, 40)
#     pause_text_render = font_med.render("||", True, BLACK)
#
#     # <<< PERUBAHAN DIMULAI DI SINI >>>
#     # Render teks terlebih dahulu
#     resume_text_render = font_large.render("Resume", True, WHITE)
#     main_menu_text_render = font_large.render("Main Menu", True, WHITE)
#
#     # Dapatkan Rect dari teks dan atur posisinya (misal: tengah layar)
#     # Sesuaikan nilai Y (misal: 280 dan 360) untuk mengatur jarak vertikal
#     resume_button_rect = resume_text_render.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - 40))
#     main_menu_button_rect = main_menu_text_render.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 40))
#     # <<< PERUBAHAN SELESAI DI SINI >>>
#
#
#
#     try:
#         pygame.mixer.music.load("assets/audio/music.mp3")
#         pygame.mixer.music.set_volume(0.5)
#         pygame.mixer.music.play(-1, 0.0, 5000)
#     except pygame.error as e:
#         print(f"Error loading battle music: {e}")
#
#     run = True
#     while run:
#         clock.tick(FPS)
#         mouse_pos = pygame.mouse.get_pos()
#
#         for event in pygame.event.get():
#             if event.type == pygame.QUIT:
#                 pygame.mixer.music.stop()
#                 run = False
#
#             if event.type == pygame.MOUSEBUTTONDOWN:
#                 if event.button == 1:
#                     if paused:
#                         # Gunakan Rect yang sudah diatur untuk deteksi klik
#                         if resume_button_rect.collidepoint(mouse_pos):
#                             paused = False
#                             pygame.mixer.music.unpause()
#                         elif main_menu_button_rect.collidepoint(mouse_pos):
#                             pygame.mixer.music.stop()
#                             run = False
#                     else:
#                         if not round_over and intro_count <= 0 and pause_button_rect.collidepoint(mouse_pos):
#                             paused = True
#                             pygame.mixer.music.pause()
#
#         draw_bg()
#         draw_health_bar(fighter_1.health, 20, 20)
#         draw_health_bar(fighter_2.health, 580, 20)
#         draw_text(f"P1: {score[0]}", font_small, RED, 20, 60)
#         draw_text(f"P2: {score[1]}", font_small, RED, 580, 60)
#         pygame.draw.rect(screen, GREY, pause_button_rect)
#         screen.blit(pause_text_render, (pause_button_rect.centerx - pause_text_render.get_width() // 2,
#                                          pause_button_rect.centery - pause_text_render.get_height() // 2))
#
#         if not paused:
#             if intro_count <= 0:
#                 fighter_1.move(SCREEN_WIDTH, SCREEN_HEIGHT, screen, fighter_2, round_over)
#                 fighter_2.move(SCREEN_WIDTH, SCREEN_HEIGHT, screen, fighter_1, round_over)
#             else:
#                 draw_text(str(intro_count), font_large, RED, SCREEN_WIDTH/2 - 20, SCREEN_HEIGHT/3)
#                 if (pygame.time.get_ticks() - last_count_update) >= 1000:
#                     intro_count -= 1
#                     last_count_update = pygame.time.get_ticks()
#
#             fighter_1.update()
#             fighter_2.update()
#
#             if not round_over:
#                 if not fighter_1.alive:
#                     score[1] += 1
#                     round_over = True
#                     round_over_time = pygame.time.get_ticks()
#                 elif not fighter_2.alive:
#                     score[0] += 1
#                     round_over = True
#                     round_over_time = pygame.time.get_ticks()
#             else:
#                 screen.blit(victory_img, (360, 150))
#                 if pygame.time.get_ticks() - round_over_time > ROUND_OVER_COOLDOWN:
#                     round_over = False
#                     intro_count = 3
#                     # fighter_1 = Warrior(1, 200, SCREEN_HEIGHT, False, [*warrior_data["size"], warrior_data["scale"], warrior_data["offset"]], warrior_assets["image"], warrior_data["animation_steps"], warrior_assets["sound"], SCREEN_HEIGHT,is_bot=False)    
#                     # fighter_2 = Wizard(2, 700, SCREEN_HEIGHT, True, [*wizard_data["size"],wizard_data["scale"], wizard_data["offset"]],wizard_assets["image"],wizard_data["animation_steps"],wizard_assets["sound"],SCREEN_HEIGHT, is_bot=False)
#                     #
#         fighter_1.draw(screen)
#         fighter_2.draw(screen)
#
#         if paused:
#             overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA)
#             overlay.fill((0, 0, 0, 150))
#             screen.blit(overlay, (0, 0))
#
#             # <<< PERUBAHAN GAMBAR TOMBOL >>>
#             # Gambar latar belakang menggunakan Rect teks
#             pygame.draw.rect(screen, GREEN, resume_button_rect)
#             # Gambar teks di atas latar belakang (gunakan topleft dari Rect)
#             screen.blit(resume_text_render, resume_button_rect.topleft)
#
#             # Gambar latar belakang menggunakan Rect teks
#             pygame.draw.rect(screen, DARK_RED, main_menu_button_rect)
#             # Gambar teks di atas latar belakang
#             screen.blit(main_menu_text_render, main_menu_button_rect.topleft)
#             # <<< AKHIR PERUBAHAN GAMBAR TOMBOL >>>
#
#         pygame.display.update()
