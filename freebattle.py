import pygame
from pygame import mixer
import os # For listing arena files
import random

# Assuming char_sel.py now contains select_characters_new
from char_sel import select_characters_new
from character_assets import load_character_assets #
from start_battle import start_battle as run_battle #

mixer.init()
# Pygame.init() typically called in main.py

# Colors (already defined in freebattle.py, ensure consistency or import from a central place)
RED = (255, 0, 0)
YELLOW = (255, 255, 0)
WHITE = (255, 255, 255)
GREY = (128,128,128) # Used for button color
LIGHT_GREY = (200, 200, 200)
BLACK = (0, 0, 0)
GREEN = (0, 180, 0)
BLUE = (0, 0, 255)
# VICTORY_IMG and some other globals from original freebattle.py might be needed by run_battle if not passed

# Fonts (ensure these are loaded or passed if needed by new functions)
# font_large = pygame.font.Font("assets/fonts/turok.ttf", 80)
# font_med = pygame.font.Font("assets/fonts/turok.ttf", 40)
# font_small = pygame.font.Font("assets/fonts/turok.ttf", 30)


# --- Helper: Load Victory Image (needed by run_battle) ---
try:
    victory_img_path = "assets/images/icons/victory.png"
    victory_img = pygame.image.load(victory_img_path).convert_alpha() #
except pygame.error as e:
    print(f"Warning: Victory image not found at {victory_img_path}: {e}")
    victory_img = pygame.Surface((100, 50)); victory_img.fill(GREEN)


def draw_text_simple(screen, text, font, color, center_x, y):
    img = font.render(text, True, color)
    rect = img.get_rect(center=(center_x, y))
    screen.blit(img, rect)

def select_battle_mode(screen, screen_width, screen_height, font_med, font_large, clock):
    """Displays mode selection: PvP or PvBot."""
    button_width = 300
    button_height = 60
    btn_pvp_rect = pygame.Rect(screen_width // 2 - button_width // 2, screen_height // 2 - 80, button_width, button_height)
    btn_pvbot_rect = pygame.Rect(screen_width // 2 - button_width // 2, screen_height // 2, button_width, button_height)
    btn_back_rect = pygame.Rect(screen_width // 2 - button_width // 2, screen_height // 2 + 80, button_width, button_height)

    running = True
    while running:
        mouse_pos = pygame.mouse.get_pos()
        screen.fill(BLACK)

        draw_text_simple(screen, "Select Battle Mode", font_large, YELLOW, screen_width // 2, 100)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return None # Signal to exit or go back to main
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    return None 
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                if btn_pvp_rect.collidepoint(mouse_pos):
                    return "pvp"
                if btn_pvbot_rect.collidepoint(mouse_pos):
                    return "pvbot"
                if btn_back_rect.collidepoint(mouse_pos):
                    return None

        # Draw buttons
        pygame.draw.rect(screen, GREEN if btn_pvp_rect.collidepoint(mouse_pos) else GREY, btn_pvp_rect)
        draw_text_simple(screen, "Player vs Player", font_med, WHITE, btn_pvp_rect.centerx, btn_pvp_rect.centery)
        
        pygame.draw.rect(screen, GREEN if btn_pvbot_rect.collidepoint(mouse_pos) else GREY, btn_pvbot_rect)
        draw_text_simple(screen, "Player vs Bot", font_med, WHITE, btn_pvbot_rect.centerx, btn_pvbot_rect.centery)

        pygame.draw.rect(screen, RED if btn_back_rect.collidepoint(mouse_pos) else GREY, btn_back_rect)
        draw_text_simple(screen, "Back to Menu", font_med, WHITE, btn_back_rect.centerx, btn_back_rect.centery)

        pygame.display.flip()
        clock.tick(30)
    return None


def get_arena_paths():
    arena_dir = "assets/images/background/"
    arenas = []
    try:
        for f_name in os.listdir(arena_dir):
            if (f_name.lower().endswith(".png") or f_name.lower().endswith(".jpeg")) and \
               f_name not in ["background_main_menu.jpeg", "backgroundCreditScene.png", "background.jpeg"]: # Exclude specific non-arena BGs
                arenas.append(os.path.join(arena_dir, f_name))
    except FileNotFoundError:
        print(f"Warning: Arena directory not found: {arena_dir}")
    if not arenas: # Fallback if no arenas found or dir missing
        print("Warning: No arenas found, using default background.jpeg as fallback arena.")
        arenas.append("assets/images/background/background.jpeg") # Default fallback
    return arenas

def select_arena(screen, mode, screen_width, screen_height, font_med, font_large, clock):
    arena_paths = get_arena_paths()
    num_arenas = len(arena_paths)
    if num_arenas == 0:
        print("No arenas available!")
        return "assets/images/background/background.jpeg" # Default if truly none

    cols = min(num_arenas, 3) # Max 3 arena thumbnails per row
    rows = (num_arenas + cols - 1) // cols
    
    thumb_width = 200
    thumb_height = 120
    padding = 20
    grid_width = cols * (thumb_width + padding) - padding
    start_x = (screen_width - grid_width) // 2
    start_y = 150

    arena_rects = []
    loaded_arena_thumbs = []
    for i, path in enumerate(arena_paths):
        try:
            img = pygame.image.load(path).convert()
            thumb = pygame.transform.scale(img, (thumb_width, thumb_height))
            loaded_arena_thumbs.append(thumb)
        except pygame.error as e:
            print(f"Error loading arena thumbnail {path}: {e}")
            placeholder_thumb = pygame.Surface((thumb_width, thumb_height))
            placeholder_thumb.fill(RED)
            loaded_arena_thumbs.append(placeholder_thumb)

        row = i // cols
        col = i % cols
        x = start_x + col * (thumb_width + padding)
        y = start_y + row * (thumb_height + padding)
        rect = pygame.Rect(x, y, thumb_width, thumb_height)
        arena_rects.append({"rect": rect, "path": path, "thumb": loaded_arena_thumbs[-1]})

    p1_arena_choice_path = None
    p2_arena_choice_path = None # Only for PvP
    current_turn = 1 # 1 for P1, 2 for P2 (PvP)

    running = True
    while running:
        mouse_pos = pygame.mouse.get_pos()
        screen.fill(BLACK)
        
        prompt = "Player 1: Select Arena"
        if mode == "pvp" and current_turn == 2:
            prompt = "Player 2: Select Arena"
        elif mode == "pvp" and p1_arena_choice_path and not p2_arena_choice_path: # P1 has chosen, waiting for P2
             prompt = "Player 2: Select Arena"


        draw_text_simple(screen, prompt, font_large, YELLOW, screen_width // 2, 70)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return None # Signal to go back
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    return None
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                for arena_data in arena_rects:
                    if arena_data["rect"].collidepoint(mouse_pos):
                        if current_turn == 1:
                            p1_arena_choice_path = arena_data["path"]
                            if mode == "pvbot":
                                running = False # P1 chooses for PvBot
                            else: # PvP
                                current_turn = 2 
                        elif mode == "pvp" and current_turn == 2:
                            p2_arena_choice_path = arena_data["path"]
                            running = False # Both chosen in PvP
                        break
        
        for arena_data in arena_rects:
            screen.blit(arena_data["thumb"], arena_data["rect"].topleft)
            outline_color = BLACK
            outline_width = 2
            if arena_data["rect"].collidepoint(mouse_pos):
                outline_color = YELLOW
                outline_width = 3
            if arena_data["path"] == p1_arena_choice_path:
                outline_color = BLUE
                outline_width = 4
            if mode == "pvp" and arena_data["path"] == p2_arena_choice_path: # If P2 also chose this
                if p1_arena_choice_path == p2_arena_choice_path: # Both chose same
                     # Could draw combined outline or special indicator
                     pygame.draw.line(screen, BLUE, arena_data["rect"].topleft, arena_data["rect"].bottomright, 4)
                     pygame.draw.line(screen, RED, arena_data["rect"].bottomleft, arena_data["rect"].topright, 4)
                else: # P2 chose this, P1 chose different
                    outline_color = RED
                    outline_width = 4
            
            pygame.draw.rect(screen, outline_color, arena_data["rect"], outline_width)

        pygame.display.flip()
        clock.tick(30)

    if mode == "pvbot":
        return p1_arena_choice_path
    elif mode == "pvp":
        if p1_arena_choice_path and p2_arena_choice_path:
            if p1_arena_choice_path == p2_arena_choice_path:
                return p1_arena_choice_path
            else:
                return random.choice([p1_arena_choice_path, p2_arena_choice_path])
        elif p1_arena_choice_path: # Should not happen if logic is correct (P2 must choose)
             return p1_arena_choice_path 
    return arena_paths[0] # Fallback, should be handled by returning None earlier to go back

def initiate_free_battle_sequence(screen, screen_width, screen_height, clock):
   
    # Consistent fonts for the sequence
    font_large = pygame.font.Font("assets/fonts/turok.ttf", 60) # Smaller large for sequence
    font_med = pygame.font.Font("assets/fonts/turok.ttf", 30)
    font_small = pygame.font.Font("assets/fonts/turok.ttf", 24)

    assets = load_character_assets() # Load all assets once

    battle_mode = select_battle_mode(screen, screen_width, screen_height, font_med, font_large, clock)
    if not battle_mode:
        return # Returned to main menu

    fighter1, fighter2 = select_characters_new(screen, battle_mode, assets, screen_width, screen_height, font_small, font_med, clock)
    if not fighter1 or not fighter2:
        return # Returned to main menu or mode select

    selected_arena_path = select_arena(screen, battle_mode, screen_width, screen_height, font_med, font_large, clock)
    if not selected_arena_path:
        return # Returned to main menu
    pygame.mixer.music.stop()
    # Prepare the dynamic draw_bg function for run_battle
    try:
        loaded_arena_bg = pygame.image.load(selected_arena_path).convert_alpha()
        scaled_arena_bg = pygame.transform.scale(loaded_arena_bg, (screen_width, screen_height))
    except pygame.error as e:
        print(f"Critical Error: Could not load selected arena '{selected_arena_path}': {e}. Using fallback.")
        # Fallback to a very basic background if final load fails
        scaled_arena_bg = pygame.Surface((screen_width, screen_height))
        scaled_arena_bg.fill(BLACK)
        # Draw error text on this fallback bg
        err_text = font_small.render(f"Arena Load Error: {os.path.basename(selected_arena_path)}", True, RED)
        scaled_arena_bg.blit(err_text, (20, screen_height - 40))


    def dynamic_draw_bg_for_battle():
        screen.blit(scaled_arena_bg, (0, 0))

    # Health bar drawing function (already in original freebattle.py)
    def draw_health_bar(health, x, y): #
        ratio = health / 100
        pygame.draw.rect(screen, WHITE, (x - 2, y - 2, 404, 34))
        pygame.draw.rect(screen, RED, (x, y, 400, 30))
        pygame.draw.rect(screen, (74,84,98), (x, y, 400 * ratio, 30)) # DARK_BLUE from original

    # Text drawing function (already in original freebattle.py)
    def draw_text_for_battle(text, font, color, x, y): #
        img = font.render(text, True, color)
        screen.blit(img, (x, y))

    # Now call run_battle with the dynamically created background drawing function
    # and other necessary components from the original freebattle.py or loaded here.
    run_battle(
        screen_width, screen_height, screen,
        dynamic_draw_bg_for_battle, # Pass the function that knows which BG to draw
        font_small, font_med, font_large, # Pass the fonts needed by run_battle
        draw_health_bar, draw_text_for_battle, # Pass utility functions
        fighter1, fighter2,
        victory_img, # Loaded at the top of this file
        is_story=False
    )
    # After battle, music for main menu should be restarted by main.py's loop

# Original start_battle function is replaced by initiate_free_battle_sequence
# The old start_battle() in freebattle.py is no longer directly called by main.py

if __name__ == "__main__":
    # Minimal test setup for freebattle sequence (requires full Pygame init from main)
    # pygame.init()
    # s_width = 1000
    # s_height = 600
    # scr = pygame.display.set_mode((s_width, s_height))
    # pygame.display.set_caption("Free Battle Test")
    # clk = pygame.time.Clock()
    # # A dummy background for testing the sequence screens
    # dummy_bg = pygame.Surface((s_width, s_height)); dummy_bg.fill((30,30,30))
    #
    # initiate_free_battle_sequence(scr, s_width, s_height, clk, dummy_bg)
    # pygame.quit()
    pygame.init()
    s_width = 1000
    s_height = 600
    scr = pygame.display.set_mode((s_width, s_height))
    pygame.display.set_caption("Free Battle Sequence Test")
    clk = pygame.time.Clock()
    
    # Start main menu music for testing
    try:
        pygame.mixer.music.load("assets/audio/music_main.wav")
        pygame.mixer.music.set_volume(0.7)
        pygame.mixer.music.play(-1, 0.0, 5000)
    except pygame.error as e: print(f"Test music error: {e}")

    initiate_free_battle_sequence(scr, s_width, s_height, clk)
    
    # After sequence, if music should restart (e.g. user backed out to main menu)
    # This logic would normally be in main.py's main loop
    if not pygame.mixer.music.get_busy():
         try:
            print("Restarting main menu music after test sequence.")
            pygame.mixer.music.load("assets/audio/music_main.wav")
            pygame.mixer.music.play(-1, 0.0, 5000)
         except pygame.error as e: print(f"Test music restart error: {e}")
    else:
        print("Music is still playing (likely battle music if battle started).")

    # Keep window open for a bit if battle didn't run to see final screen
    # if not fighter1 or not fighter2 or not selected_arena_path: # pseudo check
    #    pygame.time.wait(2000)

    pygame.quit()
