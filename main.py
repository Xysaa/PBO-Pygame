# main.py
import pygame
import story # story.py
import freebattle
import credit
from pygame import mixer
from save_data import load_game_state, DEFAULT_GAME_STATE # For story submenu logic

# Initialize save file if it doesn't exist at the very start of the game
import os
from save_data import save_game_state as init_save_main # Alias for clarity
SAVE_FILE_NAME = "game_save_data.json" # Match this with save_data.py
if not os.path.exists(SAVE_FILE_NAME):
    init_save_main(DEFAULT_GAME_STATE.copy())
    print(f"Initialized {SAVE_FILE_NAME} from main.py")

mixer.init()
pygame.init()

# --- Story Submenu Function (Halaman baru dengan tombol baru) ---
def show_story_submenu(screen, main_bg_image, clock):
    screen_width = screen.get_width()
    screen_height = screen.get_height()

    # Gunakan font yang sama atau berbeda untuk submenu jika diinginkan
    submenu_font = pygame.font.Font("assets/fonts/turok.ttf", 28) # Font untuk tombol submenu

    button_text_color = (255, 255, 255)
    button_bg_color = (70, 70, 70)
    button_hover_color = (100, 100, 100)
    button_disabled_color = (40, 40, 40)
    button_disabled_text_color = (100, 100, 100)

    submenu_button_properties = [
        {"text": "NEW STORY", "action": "new_story", "y_pos": screen_height // 2 - 70},
        {"text": "CONTINUE STORY", "action": "continue_story", "y_pos": screen_height // 2 - 10},
        {"text": "BACK", "action": "back", "y_pos": screen_height // 2 + 50},
    ]

    submenu_buttons = []
    button_width = 380 # Lebar tombol submenu
    button_height = 50  # Tinggi tombol submenu
    for prop in submenu_button_properties:
        rect = pygame.Rect(screen_width // 2 - button_width // 2, prop["y_pos"], button_width, button_height)
        submenu_buttons.append({
            "rect": rect, "text": prop["text"], "action": prop["action"],
            "surface": submenu_font.render(prop["text"], True, button_text_color),
            "disabled_surface": submenu_font.render(prop["text"], True, button_disabled_text_color)
        })

    submenu_running = True
    while submenu_running:
        mouse_pos = pygame.mouse.get_pos()
        game_state_current = load_game_state()

        can_continue_story = not game_state_current["story_completed"]

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                for button in submenu_buttons:
                    if button["rect"].collidepoint(mouse_pos):
                        action = button["action"]

                        if action == "continue_story" and not can_continue_story:
                            print("'Continue Story' disabled: Story is completed.")
                            continue

                        if action == "new_story":
                            pygame.mixer.music.stop()
                            story.main_story(start_new_game_flag=True)
                            return # Kembali ke loop main_menu
                        elif action == "continue_story":
                            pygame.mixer.music.stop()
                            story.main_story(start_new_game_flag=False)
                            return # Kembali ke loop main_menu
                        elif action == "back":
                            submenu_running = False
        
        screen.blit(pygame.transform.scale(main_bg_image, screen.get_size()), (0, 0))
        overlay = pygame.Surface((screen_width, screen_height), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 150)) # Overlay gelap transparan
        screen.blit(overlay, (0,0))

        submenu_title_text = submenu_font.render("Story Options", True, (255,255,150))
        screen.blit(submenu_title_text, (screen_width // 2 - submenu_title_text.get_width() // 2, screen_height // 2 - 160))

        for button in submenu_buttons:
            current_bg_color = button_bg_color
            current_text_surface = button["surface"]
            is_disabled = button["action"] == "continue_story" and not can_continue_story

            if is_disabled:
                current_bg_color = button_disabled_color
                current_text_surface = button["disabled_surface"]
            elif button["rect"].collidepoint(mouse_pos):
                current_bg_color = button_hover_color
            
            pygame.draw.rect(screen, current_bg_color, button["rect"])
            screen.blit(current_text_surface, (
                button["rect"].centerx - current_text_surface.get_width() // 2,
                button["rect"].centery - current_text_surface.get_height() // 2
            ))
        pygame.display.flip()
        clock.tick(60)
    # Keluar dari loop submenu_running, kembali ke main_menu

# --- Main Menu Function (Menggunakan struktur tombol asli Anda) ---
def main_menu():
    screen_width = 1000
    screen_height = 600
    screen = pygame.display.set_mode((screen_width, screen_height)) # Hapus RESIZABLE jika tidak diimplementasikan penuh
    pygame.display.set_caption("The Chosen - Main Menu")
    clock = pygame.time.Clock()

    try:
        pygame.mixer.music.load("assets/audio/music_main.wav")
        pygame.mixer.music.set_volume(0.7)
        pygame.mixer.music.play(-1, 0.0, 5000)
    except pygame.error as e: print(f"Error loading main menu music: {e}")

    try:
        background_image = pygame.image.load("assets/images/background/background_main_menu.jpeg").convert()
    except pygame.error as e:
        print(f"Error loading background image: {e}")
        background_image = pygame.Surface((screen_width, screen_height)); background_image.fill((50,50,50))
    
    # Font untuk tombol menu utama (sesuaikan dengan font asli Anda jika berbeda)
    # Dari file asli Anda, sepertinya tidak ada font yang didefinisikan secara eksplisit untuk tombol
    # jadi kita akan gunakan font default atau font yang sama dengan submenu untuk konsistensi visual
    # Jika Anda punya font spesifik dari "assets/fonts/turok.ttf" untuk ini, gunakan itu.
        # Menggunakan definisi tombol dari file main.py asli Anda
    button_data_original = [
        {"text": "LORE OF THE CHOSEN", "x": 258.75, "y": 305, "width": 393.75, "height": 40, "action": "story_submenu"}, # Action diubah ke submenu
        {"text": "FREE BATTLE", "x": 258.75, "y": 375, "width": 393.75, "height": 40, "action": "free_battle"},
        {"text": "CREDITS", "x": 258.75, "y": 445, "width": 393.75, "height": 40, "action": "credits"},
        {"text": "EXIT", "x": 258.75, "y": 515, "width": 393.75, "height": 40, "action": "exit"}
    ]
    
    main_buttons = []
    for data in button_data_original:
        rect = pygame.Rect(data["x"], data["y"], data["width"], data["height"])
        main_buttons.append({
            "rect": rect,
            "text": data["text"], # Simpan teks untuk dirender
            "action": data["action"],
           # Pre-render surface
        })

    running = True
    while running:
        mouse_pos = pygame.mouse.get_pos()
        # Resizable window logic (jika Anda ingin mempertahankannya dari file asli)
        # current_screen_width, current_screen_height = screen.get_size()
        # scale_x = current_screen_width / screen_width # screen_width adalah lebar awal
        # scale_y = current_screen_height / screen_height

        for event in pygame.event.get():
            if event.type == pygame.QUIT: running = False
            # if event.type == pygame.VIDEORESIZE: # Jika menggunakan mode resizable
            #     # Update screen dan skala ulang tombol jika diperlukan (logika ini kompleks)
            #     # Untuk saat ini, kita asumsikan ukuran tetap atau logika resize sudah ada
            #     pass

            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                # Skala mouse_pos jika layar resizable dan tombol tidak diskala ulang setiap frame
                # scaled_mouse_pos = (mouse_pos[0] / scale_x, mouse_pos[1] / scale_y) # Contoh
                for button in main_buttons:
                    # Gunakan button.rect yang mungkin sudah disesuaikan jika resizable
                    # atau mouse_pos yang diskalakan
                    if button["rect"].collidepoint(mouse_pos): # Gunakan mouse_pos langsung jika tombol tidak diskala
                        action = button["action"]
                        should_restart_music_after_action = True

                        if action == "story_submenu":
                            show_story_submenu(screen, background_image, clock)
                            # Setelah submenu kembali, pastikan musik menu utama berlanjut jika perlu
                            if not pygame.mixer.music.get_busy():
                                pygame.mixer.music.load("assets/audio/music_main.wav")
                                pygame.mixer.music.play(-1, 0.0, 5000)
                            should_restart_music_after_action = False

                        elif action == "free_battle":
                            pygame.mixer.music.stop()
                            freebattle.start_battle()
                        elif action == "credits":
                            pygame.mixer.music.stop()
                            credit.run_credit()
                        elif action == "exit":
                            running = False; should_restart_music_after_action = False
                        
                        if should_restart_music_after_action and running:
                            try:
                                pygame.mixer.music.load("assets/audio/music_main.wav")
                                pygame.mixer.music.play(-1, 0.0, 5000)
                            except pygame.error as e: print(f"Error restarting menu music: {e}")
        
        # Menggambar background
        # Jika resizable, scaled_background harus menggunakan ukuran layar saat ini
        current_screen_size = screen.get_size()
        screen.blit(pygame.transform.scale(background_image, current_screen_size), (0, 0))

        # Menggambar tombol menu utama
        # Asumsi fixed size atau rect sudah diupdate

        pygame.display.flip()
        clock.tick(60)
        
    pygame.quit()
    exit()

if __name__ == "__main__":
    main_menu()
