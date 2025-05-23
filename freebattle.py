import pygame
from pygame import mixer
from fighter import Warrior, Wizard

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
WARRIOR_SIZE = [288, 128]
WARRIOR_SCALE = 3
WARRIOR_OFFSET = [125, 50]
WARRIOR_DATA = [*WARRIOR_SIZE, WARRIOR_SCALE, WARRIOR_OFFSET]
WIZARD_SIZE = [288, 128]
WIZARD_SCALE = 3
WIZARD_OFFSET = [125, 50]
WIZARD_DATA = [*WIZARD_SIZE, WIZARD_SCALE, WIZARD_OFFSET]

# Assets
sword_fx = pygame.mixer.Sound("assets/audio/sword.wav")
sword_fx.set_volume(0.5)
magic_fx = pygame.mixer.Sound("assets/audio/magic.wav")
magic_fx.set_volume(0.75)

bg_image = pygame.image.load("assets/images/background/background.jpg").convert_alpha()
victory_img = pygame.image.load("assets/images/icons/victory.png").convert_alpha()
warrior_sheet = pygame.image.load("assets/images/fire_warrior/fireWar_spritesheets1.png").convert_alpha()
wizard_sheet = pygame.image.load("assets/images/fire_warrior/fireWar_spritesheets1.png").convert_alpha()

WARRIOR_ANIM = [8, 8, 26, 11, 19, 18, 6, 13]
WIZARD_ANIM = [8, 8, 26, 11, 19, 18, 6, 13]

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

def start_battle():
    clock = pygame.time.Clock()
    FPS = 60

    intro_count = 3
    last_count_update = pygame.time.get_ticks()
    score = [0, 0]
    round_over = False
    ROUND_OVER_COOLDOWN = 2000
    round_over_time = 0
    game_over_time = None  # Untuk jeda sebelum kembali ke menu

    paused = False
    pause_button_rect = pygame.Rect(SCREEN_WIDTH // 2 - 40, 10, 80, 40)
    pause_text_render = font_med.render("||", True, BLACK)

    # <<< PERUBAHAN DIMULAI DI SINI >>>
    # Render teks terlebih dahulu
    resume_text_render = font_large.render("Resume", True, WHITE)
    main_menu_text_render = font_large.render("Main Menu", True, WHITE)

    # Dapatkan Rect dari teks dan atur posisinya (misal: tengah layar)
    # Sesuaikan nilai Y (misal: 280 dan 360) untuk mengatur jarak vertikal
    resume_button_rect = resume_text_render.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - 40))
    main_menu_button_rect = main_menu_text_render.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 40))
    # <<< PERUBAHAN SELESAI DI SINI >>>

    fighter_1 = Warrior(1, 200, SCREEN_HEIGHT, False, WARRIOR_DATA, warrior_sheet, WARRIOR_ANIM, sword_fx, SCREEN_HEIGHT, is_bot=False)
    fighter_2 = Wizard(2, 700, SCREEN_HEIGHT, True, WIZARD_DATA, wizard_sheet, WIZARD_ANIM, magic_fx, SCREEN_HEIGHT, is_bot=False)

    try:
        pygame.mixer.music.load("assets/audio/music.mp3")
        pygame.mixer.music.set_volume(0.5)
        pygame.mixer.music.play(-1, 0.0, 5000)
    except pygame.error as e:
        print(f"Error loading battle music: {e}")

    run = True
    while run:
        clock.tick(FPS)
        mouse_pos = pygame.mouse.get_pos()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.mixer.music.stop()
                run = False

            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    if paused:
                        # Gunakan Rect yang sudah diatur untuk deteksi klik
                        if resume_button_rect.collidepoint(mouse_pos):
                            paused = False
                            pygame.mixer.music.unpause()
                        elif main_menu_button_rect.collidepoint(mouse_pos):
                            pygame.mixer.music.stop()
                            run = False
                    else:
                        if not round_over and intro_count <= 0 and pause_button_rect.collidepoint(mouse_pos):
                            paused = True
                            pygame.mixer.music.pause()

        draw_bg()
        draw_health_bar(fighter_1.health, 20, 20)
        draw_health_bar(fighter_2.health, 580, 20)
        draw_text(f"P1: {score[0]}", font_small, RED, 20, 60)
        draw_text(f"P2: {score[1]}", font_small, RED, 580, 60)
        pygame.draw.rect(screen, GREY, pause_button_rect)
        screen.blit(pause_text_render, (pause_button_rect.centerx - pause_text_render.get_width() // 2,
                                         pause_button_rect.centery - pause_text_render.get_height() // 2))

        if not paused:
            if intro_count <= 0:
                fighter_1.move(SCREEN_WIDTH, SCREEN_HEIGHT, screen, fighter_2, round_over)
                fighter_2.move(SCREEN_WIDTH, SCREEN_HEIGHT, screen, fighter_1, round_over)
            else:
                draw_text(str(intro_count), font_large, RED, SCREEN_WIDTH/2 - 20, SCREEN_HEIGHT/3)
                if (pygame.time.get_ticks() - last_count_update) >= 1000:
                    intro_count -= 1
                    last_count_update = pygame.time.get_ticks()

            fighter_1.update()
            fighter_2.update()

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
                    round_over = False
                    intro_count = 3
                    fighter_1 = Warrior(1, 200, SCREEN_HEIGHT, False, WARRIOR_DATA, warrior_sheet, WARRIOR_ANIM, sword_fx, SCREEN_HEIGHT, is_bot=False)
                    fighter_2 = Wizard(2, 700, SCREEN_HEIGHT, True, WIZARD_DATA, wizard_sheet, WIZARD_ANIM, magic_fx, SCREEN_HEIGHT, is_bot=False)

        fighter_1.draw(screen)
        fighter_2.draw(screen)

        if paused:
            overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA)
            overlay.fill((0, 0, 0, 150))
            screen.blit(overlay, (0, 0))

            # <<< PERUBAHAN GAMBAR TOMBOL >>>
            # Gambar latar belakang menggunakan Rect teks
            pygame.draw.rect(screen, GREEN, resume_button_rect)
            # Gambar teks di atas latar belakang (gunakan topleft dari Rect)
            screen.blit(resume_text_render, resume_button_rect.topleft)

            # Gambar latar belakang menggunakan Rect teks
            pygame.draw.rect(screen, DARK_RED, main_menu_button_rect)
            # Gambar teks di atas latar belakang
            screen.blit(main_menu_text_render, main_menu_button_rect.topleft)
            # <<< AKHIR PERUBAHAN GAMBAR TOMBOL >>>

        # Cek jika salah satu pemain mencapai 3 poin, beri jeda 3 detik sebelum kembali ke main menu
        if score[0] >= 3 or score[1] >= 3:
            if game_over_time is None:
                pygame.mixer.music.stop()
                game_over_time = pygame.time.get_ticks()
            elif pygame.time.get_ticks() - game_over_time > 3000:
                round_over = False
                intro_count = 3
                run = False
            

        # Update display
        pygame.display.update()