import pygame
from pygame import mixer
import os 
import random

from char_sel import select_characters_new #
from character_assets import load_character_assets #
from start_battle import start_battle as run_battle #

mixer.init()

# Gamepad Button Constants (defined in main.py or globally)
JUMP_BUTTON = 0      # X / Cross (used as Confirm here)
ATTACK2_BUTTON = 1   # Circle / B (used as Back here)
MENU_CONFIRM_BUTTON = JUMP_BUTTON 
MENU_BACK_BUTTON = ATTACK2_BUTTON 

# Colors
RED = (255,0,0); YELLOW = (255,255,0); WHITE = (255,255,255); GREY = (128,128,128)
LIGHT_GREY = (200,200,200); BLACK = (0,0,0); GREEN = (0,180,0); BLUE = (0,0,255)

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

def select_battle_mode(screen, screen_width, screen_height, font_med, font_large, clock): #
    buttons_props = [
        {"text": "Player vs Player", "action": "pvp", "id": 0, "y_offset": -80},
        {"text": "Player vs Bot", "action": "pvbot", "id": 1, "y_offset": 0},
        {"text": "Back to Menu", "action": "back", "id": 2, "y_offset": 80, "color": RED}
    ]
    buttons = []
    button_width, button_height = 300, 60
    for prop in buttons_props:
        rect = pygame.Rect(screen_width // 2 - button_width // 2, screen_height // 2 + prop["y_offset"], button_width, button_height)
        buttons.append({"rect": rect, **prop})
    
    selected_button_idx = 0

    running = True
    while running:
        mouse_pos = pygame.mouse.get_pos()
        screen.fill(BLACK)
        draw_text_simple(screen, "Select Battle Mode", font_large, YELLOW, screen_width // 2, 100)

        for i, btn in enumerate(buttons): # Mouse hover updates selected_button_idx
            if btn["rect"].collidepoint(mouse_pos): selected_button_idx = i; break
        
        action_to_perform = None

        for event in pygame.event.get():
            if event.type == pygame.QUIT: return None 
            
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE: return None 
                if event.key == pygame.K_UP: selected_button_idx = (selected_button_idx - 1 + len(buttons)) % len(buttons)
                if event.key == pygame.K_DOWN: selected_button_idx = (selected_button_idx + 1) % len(buttons)
                if event.key == pygame.K_RETURN or event.key == pygame.K_SPACE: action_to_perform = buttons[selected_button_idx]["action"]
            
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                if buttons[selected_button_idx]["rect"].collidepoint(mouse_pos): # Check selected one
                    action_to_perform = buttons[selected_button_idx]["action"]

            if event.type == pygame.JOYHATMOTION:
                if event.value[1] == 1: selected_button_idx = (selected_button_idx - 1 + len(buttons)) % len(buttons) # Up
                if event.value[1] == -1: selected_button_idx = (selected_button_idx + 1) % len(buttons) # Down
            
            if event.type == pygame.JOYBUTTONDOWN:
                if event.button == MENU_CONFIRM_BUTTON: action_to_perform = buttons[selected_button_idx]["action"]
                if event.button == MENU_BACK_BUTTON: return None # Back with joy B/Circle

            if action_to_perform:
                if action_to_perform == "back": return None
                return action_to_perform # "pvp" or "pvbot"

        for i, btn in enumerate(buttons):
            color = btn.get("color", GREY) # Default GREY, or RED for "Back"
            if i == selected_button_idx: color = GREEN # Hover/selection color
            pygame.draw.rect(screen, color, btn["rect"])
            draw_text_simple(screen, btn["text"], font_med, WHITE, btn["rect"].centerx, btn["rect"].centery)
        pygame.display.flip()
        clock.tick(30)
    return None

def get_arena_paths(): #
    # ... (remains the same)
    arena_dir = "assets/images/background/"
    arenas = []
    try:
        for f_name in os.listdir(arena_dir):
            if (f_name.lower().endswith(".png") or f_name.lower().endswith(".jpeg")) and \
               not f_name.startswith("background_main_menu") and \
               not f_name.startswith("backgroundCreditScene") and \
               not f_name == "background.jpeg": 
                arenas.append(os.path.join(arena_dir, f_name))
    except FileNotFoundError: print(f"Warning: Arena directory not found: {arena_dir}")
    if not arenas: 
        print("Warning: No specific arenas found, using default background.jpeg as fallback arena.")
        arenas.append("assets/images/background/background.jpeg") 
    return arenas


def select_arena(screen, mode, screen_width, screen_height, font_med, font_large, clock): #
    arena_paths = get_arena_paths()
    num_arenas = len(arena_paths)
    if num_arenas == 0: return "assets/images/background/background.jpeg" 

    cols = min(num_arenas, 3); rows = (num_arenas + cols - 1) // cols
    thumb_width, thumb_height, padding = 200, 120, 20
    grid_width = cols * (thumb_width + padding) - padding
    start_x, start_y = (screen_width - grid_width) // 2, 150

    arena_elements = []
    for i, path in enumerate(arena_paths):
        try: img = pygame.image.load(path).convert(); thumb = pygame.transform.scale(img, (thumb_width, thumb_height))
        except pygame.error as e:
            print(f"Error loading arena thumbnail {path}: {e}"); thumb = pygame.Surface((thumb_width, thumb_height)); thumb.fill(RED)
        row, col = divmod(i, cols)
        rect = pygame.Rect(start_x + col * (thumb_width + padding), start_y + row * (thumb_height + padding), thumb_width, thumb_height)
        arena_elements.append({"rect": rect, "path": path, "thumb": thumb, "id": i})

    p1_choice, p2_choice = None, None
    current_turn = 1 # 1 for P1, 2 for P2(PvP)
    cursor_idx = 0

    running = True
    while running:
        mouse_pos = pygame.mouse.get_pos()
        screen.fill(BLACK)
        prompt = "Player 1: Select Arena"
        if mode == "pvp" and current_turn == 2: prompt = "Player 2: Select Arena"
        draw_text_simple(screen, prompt, font_large, YELLOW, screen_width // 2, 70)

        for i, el in enumerate(arena_elements): # Mouse hover updates cursor
            if el["rect"].collidepoint(mouse_pos): cursor_idx = i; break

        action_confirmed = False
        for event in pygame.event.get():
            if event.type == pygame.QUIT: return None 
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE: return None
                # Basic grid navigation with keyboard arrows
                if event.key == pygame.K_RIGHT: cursor_idx = (cursor_idx + 1) % num_arenas
                if event.key == pygame.K_LEFT: cursor_idx = (cursor_idx - 1 + num_arenas) % num_arenas
                if event.key == pygame.K_DOWN: cursor_idx = (cursor_idx + cols) % num_arenas if cursor_idx + cols < num_arenas else (num_arenas -1 if num_arenas > 0 else 0) # simplified
                if event.key == pygame.K_UP: cursor_idx = (cursor_idx - cols + num_arenas) % num_arenas if cursor_idx - cols >= 0 else 0 # simplified
                if event.key == pygame.K_RETURN or event.key == pygame.K_SPACE: action_confirmed = True
            
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                if arena_elements[cursor_idx]["rect"].collidepoint(mouse_pos): action_confirmed = True
            
            if event.type == pygame.JOYHATMOTION:
                hat_x, hat_y = event.value
                if hat_x == 1: cursor_idx = (cursor_idx + 1) % num_arenas
                if hat_x == -1: cursor_idx = (cursor_idx - 1 + num_arenas) % num_arenas
                if hat_y == -1: cursor_idx = (cursor_idx + cols) % num_arenas if cursor_idx + cols < num_arenas else (num_arenas-1 if num_arenas >0 else 0)
                if hat_y == 1: cursor_idx = (cursor_idx - cols + num_arenas) % num_arenas if cursor_idx - cols >= 0 else 0
            
            if event.type == pygame.JOYBUTTONDOWN:
                if event.button == MENU_CONFIRM_BUTTON: action_confirmed = True
                if event.button == MENU_BACK_BUTTON: return None

            if action_confirmed:
                chosen_path = arena_elements[cursor_idx]["path"]
                if current_turn == 1:
                    p1_choice = chosen_path
                    if mode == "pvbot": running = False
                    else: current_turn = 2; cursor_idx = 0 # Reset cursor for P2
                elif mode == "pvp" and current_turn == 2:
                    p2_choice = chosen_path; running = False
        
        for i, el in enumerate(arena_elements):
            screen.blit(el["thumb"], el["rect"].topleft)
            o_color, o_width = WHITE, 2
            if i == cursor_idx: o_color, o_width = YELLOW, 3
            if el["path"] == p1_choice: o_color, o_width = BLUE, 4
            if mode == "pvp" and el["path"] == p2_choice:
                if p1_choice == p2_choice: pygame.draw.line(screen, RED, el["rect"].bottomleft, el["rect"].topright, 4) # Cross line if both picked same
                else: o_color, o_width = RED, 4
            pygame.draw.rect(screen, o_color, el["rect"], o_width)
        pygame.display.flip()
        clock.tick(30)

    if mode == "pvbot": return p1_choice
    elif mode == "pvp":
        if p1_choice and p2_choice: return random.choice([p1_choice, p2_choice]) if p1_choice != p2_choice else p1_choice
        elif p1_choice: return p1_choice # Should not happen in PvP if P2 must choose
    return arena_paths[0] if arena_paths else "assets/images/background/background.jpeg"

def initiate_free_battle_sequence(screen, screen_width, screen_height, clock, joysticks): # Added joysticks
    font_large_config = pygame.font.Font("assets/fonts/turok.ttf", 60) 
    font_med_config = pygame.font.Font("assets/fonts/turok.ttf", 30)
    font_small_config = pygame.font.Font("assets/fonts/turok.ttf", 24)
    assets = load_character_assets() #

    battle_mode = select_battle_mode(screen, screen_width, screen_height, font_med_config, font_large_config, clock)
    if not battle_mode: return 

    fighter1, fighter2 = select_characters_new(screen, battle_mode, assets, screen_width, screen_height, font_small_config, font_med_config, clock, joysticks) #
    if not fighter1 or not fighter2: return 

    selected_arena_path = select_arena(screen, battle_mode, screen_width, screen_height, font_med_config, font_large_config, clock)
    if not selected_arena_path: return 

    if pygame.mixer.get_init(): pygame.mixer.music.stop() # Stop main menu music

    try:
        loaded_arena_bg = pygame.image.load(selected_arena_path).convert_alpha()
        scaled_arena_bg = pygame.transform.scale(loaded_arena_bg, (screen_width, screen_height))
    except pygame.error as e:
        print(f"Critical Error: Could not load selected arena '{selected_arena_path}': {e}. Using fallback.")
        scaled_arena_bg = pygame.Surface((screen_width, screen_height)); scaled_arena_bg.fill(BLACK)
        err_text = font_small_config.render(f"Arena Load Error: {os.path.basename(selected_arena_path)}", True, RED)
        scaled_arena_bg.blit(err_text, (20, screen_height - 40))

    def dynamic_draw_bg_for_battle(): screen.blit(scaled_arena_bg, (0, 0))
    def draw_health_bar(health, x, y): #
        ratio = health / 100
        pygame.draw.rect(screen, WHITE, (x-2,y-2,404,34)); pygame.draw.rect(screen, RED, (x,y,400,30))
        pygame.draw.rect(screen, (74,84,98), (x,y,400*ratio,30)) 
    def draw_text_for_battle(text, font, color, x, y): screen.blit(font.render(text,True,color),(x,y)) #

    run_battle(screen_width, screen_height, screen, dynamic_draw_bg_for_battle, #
        font_small_config, font_med_config, font_large_config, 
        draw_health_bar, draw_text_for_battle, 
        fighter1, fighter2, victory_img, is_story=False)

if __name__ == "__main__":
    pygame.init()
    pygame.joystick.init() # Init joysticks for test
    test_joysticks = [pygame.joystick.Joystick(i) for i in range(pygame.joystick.get_count())]
    for joy in test_joysticks: joy.init()
    if test_joysticks: print(f"Joysticks for test: {[joy.get_name() for joy in test_joysticks]}")

    s_width, s_height = 1000, 600
    scr = pygame.display.set_mode((s_width, s_height))
    pygame.display.set_caption("Free Battle Sequence Test (with Joysticks)")
    clk = pygame.time.Clock()
    try:
        pygame.mixer.music.load("assets/audio/music_main.wav"); pygame.mixer.music.set_volume(0.7)
        pygame.mixer.music.play(-1, 0.0, 5000)
    except pygame.error as e: print(f"Test music error: {e}")
    initiate_free_battle_sequence(scr, s_width, s_height, clk, test_joysticks) # Pass test_joysticks
    if not pygame.mixer.music.get_busy():
         try:
            print("Restarting main menu music after test sequence.")
            pygame.mixer.music.load("assets/audio/music_main.wav"); pygame.mixer.music.play(-1, 0.0, 5000)
         except pygame.error as e: print(f"Test music restart error: {e}")
    pygame.quit()
