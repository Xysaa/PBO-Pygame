# main.py
import pygame
import story
import freebattle
import credit
from pygame import mixer
from save_data import load_game_state, DEFAULT_GAME_STATE #
import os

# Gamepad Button Constants (adjust if your gamepad has different mappings)
JUMP_BUTTON = 0      # Typically X on PS-style, A on Xbox-style
ATTACK1_BUTTON = 2   # Typically Square on PS-style, X on Xbox-style
ATTACK2_BUTTON = 1   # Typically Circle on PS-style, B on Xbox-style
ATTACK3_BUTTON = 3   # Typically Triangle on PS-style, Y on Xbox-style
PAUSE_RESUME_BUTTON = 7 # Typically Start button
# For menus, JUMP_BUTTON can often double as a "confirm" button
MENU_CONFIRM_BUTTON = JUMP_BUTTON
MENU_BACK_BUTTON = ATTACK2_BUTTON # e.g., Circle or B for "back"

SAVE_FILE_NAME = "game_save_data.json"
if not os.path.exists(SAVE_FILE_NAME):
    from save_data import save_game_state as init_save_main #
    init_save_main(DEFAULT_GAME_STATE.copy()) #
    print(f"Initialized {SAVE_FILE_NAME} from main.py")

mixer.init()
pygame.init()
pygame.joystick.init() # Initialize the joystick module

joysticks = []
for i in range(pygame.joystick.get_count()):
    joystick = pygame.joystick.Joystick(i)
    joystick.init()
    joysticks.append(joystick)
    print(f"Initialized Joystick {i}: {joystick.get_name()}")

if not joysticks:
    print("No joysticks detected.")

# Define colors that might be used for fill
BLACK = (0, 0, 0)

# --- Story Submenu Function ---
def show_story_submenu(screen, clock): # Removed main_bg_image
    screen_width = screen.get_width()
    screen_height = screen.get_height()
    submenu_font = pygame.font.Font("assets/fonts/turok.ttf", 28)
    # ... (button properties remain the same) ...
    button_text_color = (255, 255, 255)
    button_bg_color = (70, 70, 70)
    button_hover_color = (100, 100, 100)
    button_disabled_color = (40, 40, 40)
    button_disabled_text_color = (100, 100, 100)

    submenu_button_properties = [
        {"text": "NEW STORY", "action": "new_story", "y_pos": screen_height // 2 - 70, "id": 0},
        {"text": "CONTINUE STORY", "action": "continue_story", "y_pos": screen_height // 2 - 10, "id": 1},
        {"text": "BACK", "action": "back", "y_pos": screen_height // 2 + 50, "id": 2},
    ]
    submenu_buttons = []
    button_width = 380 
    button_height = 50  
    for prop in submenu_button_properties:
        rect = pygame.Rect(screen_width // 2 - button_width // 2, prop["y_pos"], button_width, button_height)
        submenu_buttons.append({
            "rect": rect, "text": prop["text"], "action": prop["action"], "id": prop["id"],
            "surface": submenu_font.render(prop["text"], True, button_text_color),
            "disabled_surface": submenu_font.render(prop["text"], True, button_disabled_text_color)
        })
    
    selected_button_idx = 0 # For D-pad navigation

    submenu_running = True
    while submenu_running:
        mouse_pos = pygame.mouse.get_pos()
        game_state_current = load_game_state() #
        can_continue_story = not game_state_current["story_completed"] #

        # Update selected_button_idx based on mouse hover for visual consistency
        for i, button in enumerate(submenu_buttons):
            if button["rect"].collidepoint(mouse_pos):
                selected_button_idx = i
                break

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            
            action_to_perform = None

            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                for i, button in enumerate(submenu_buttons):
                    if button["rect"].collidepoint(mouse_pos):
                        selected_button_idx = i # Ensure correct button is selected on click
                        action_to_perform = button["action"]
                        break
            
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    submenu_running = False
                if event.key == pygame.K_UP:
                    selected_button_idx = (selected_button_idx - 1 + len(submenu_buttons)) % len(submenu_buttons)
                if event.key == pygame.K_DOWN:
                    selected_button_idx = (selected_button_idx + 1) % len(submenu_buttons)
                if event.key == pygame.K_RETURN or event.key == pygame.K_SPACE:
                    action_to_perform = submenu_buttons[selected_button_idx]["action"]

            if event.type == pygame.JOYHATMOTION:
                if event.value[1] == -1: # D-pad Down
                    selected_button_idx = (selected_button_idx + 1) % len(submenu_buttons)
                elif event.value[1] == 1: # D-pad Up
                    selected_button_idx = (selected_button_idx - 1 + len(submenu_buttons)) % len(submenu_buttons)
            
            if event.type == pygame.JOYBUTTONDOWN:
                if event.button == MENU_CONFIRM_BUTTON: # X or A
                     action_to_perform = submenu_buttons[selected_button_idx]["action"]
                elif event.button == MENU_BACK_BUTTON: # Circle or B
                    submenu_running = False


            if action_to_perform:
                button_data = submenu_buttons[selected_button_idx]
                if action_to_perform == "continue_story" and not can_continue_story:
                    print("'Continue Story' disabled: Story is completed.")
                    continue
                if action_to_perform == "new_story":
                    story.main_story(start_new_game_flag=True) #
                    return 
                elif action_to_perform == "continue_story":
                    story.main_story(start_new_game_flag=False) #
                    return 
                elif action_to_perform == "back":
                    submenu_running = False
        
        screen.fill(BLACK) 
        submenu_title_text = submenu_font.render("Story Options", True, (255,255,150))
        screen.blit(submenu_title_text, (screen_width // 2 - submenu_title_text.get_width() // 2, screen_height // 2 - 160))

        for i, button in enumerate(submenu_buttons):
            current_bg_color = button_bg_color
            current_text_surface = button["surface"]
            is_disabled = button["action"] == "continue_story" and not can_continue_story

            if is_disabled:
                current_bg_color = button_disabled_color
                current_text_surface = button["disabled_surface"]
            # Highlight if selected by D-pad/arrow OR hovered by mouse
            elif i == selected_button_idx: 
                current_bg_color = button_hover_color
            
            pygame.draw.rect(screen, current_bg_color, button["rect"])
            screen.blit(current_text_surface, (
                button["rect"].centerx - current_text_surface.get_width() // 2,
                button["rect"].centery - current_text_surface.get_height() // 2
            ))
        pygame.display.flip()
        clock.tick(60)

# --- Main Menu Function ---
def main_menu():
    screen_width = 1000
    screen_height = 600
    screen = pygame.display.set_mode((screen_width, screen_height))
    pygame.display.set_caption("The Chosen - Main Menu")
    clock = pygame.time.Clock()

    try:
        pygame.mixer.music.load("assets/audio/music_main.wav") #
        pygame.mixer.music.set_volume(0.7) #
        pygame.mixer.music.play(-1, 0.0, 5000) #
    except pygame.error as e: print(f"Error loading main menu music: {e}")

    try:
        background_image = pygame.image.load("assets/images/background/background_main_menu.jpeg").convert() #
    except pygame.error as e:
        print(f"Error loading background image: {e}")
        background_image = pygame.Surface((screen_width, screen_height)); background_image.fill((50,50,50))
    
    button_data_original = [
        {"text": "LORE OF THE CHOSEN", "x": 258.75, "y": 305, "width": 393.75, "height": 40, "action": "story_submenu", "id": 0}, #
        {"text": "FREE BATTLE", "x": 258.75, "y": 375, "width": 393.75, "height": 40, "action": "free_battle", "id": 1}, #
        {"text": "CREDITS", "x": 258.75, "y": 445, "width": 393.75, "height": 40, "action": "credits", "id": 2}, #
        {"text": "EXIT", "x": 258.75, "y": 515, "width": 393.75, "height": 40, "action": "exit", "id": 3} #
    ]
    
    main_buttons = []
    for data in button_data_original:
        rect = pygame.Rect(data["x"], data["y"], data["width"], data["height"])
        main_buttons.append({
            "rect": rect, "text": data["text"], "action": data["action"], "id": data["id"]
        })
    
    selected_button_idx = 0 # For D-pad/keyboard navigation

    running = True
    while running:
        mouse_pos = pygame.mouse.get_pos()

        # Update selected_button_idx based on mouse hover
        for i, button in enumerate(main_buttons):
            if button["rect"].collidepoint(mouse_pos):
                selected_button_idx = i
                break
        
        action_to_perform = None

        for event in pygame.event.get():
            if event.type == pygame.QUIT: running = False
            
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                for i, button in enumerate(main_buttons):
                    if button["rect"].collidepoint(mouse_pos):
                        selected_button_idx = i
                        action_to_perform = button["action"]
                        break
            
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE: running = False # Exit game on ESC from main menu
                if event.key == pygame.K_UP:
                    selected_button_idx = (selected_button_idx - 1 + len(main_buttons)) % len(main_buttons)
                if event.key == pygame.K_DOWN:
                    selected_button_idx = (selected_button_idx + 1) % len(main_buttons)
                if event.key == pygame.K_RETURN or event.key == pygame.K_SPACE:
                    action_to_perform = main_buttons[selected_button_idx]["action"]

            if event.type == pygame.JOYHATMOTION: # D-pad navigation
                 if event.value[1] == -1: # Down
                    selected_button_idx = (selected_button_idx + 1) % len(main_buttons)
                 elif event.value[1] == 1: # Up
                    selected_button_idx = (selected_button_idx - 1 + len(main_buttons)) % len(main_buttons)

            if event.type == pygame.JOYBUTTONDOWN:
                if event.button == MENU_CONFIRM_BUTTON: # X or A button
                    action_to_perform = main_buttons[selected_button_idx]["action"]
                # No specific MENU_BACK_BUTTON on main menu, ESC or gamepad Start usually quits/opens system menu

            if action_to_perform:
                if action_to_perform == "story_submenu":
                    show_story_submenu(screen, clock)
                    if not pygame.mixer.music.get_busy(): # If music stopped
                        try:
                            pygame.mixer.music.load("assets/audio/music_main.wav") #
                            pygame.mixer.music.play(-1, 0.0, 5000) #
                        except pygame.error as e: print(f"Error restarting menu music: {e}")
                
                elif action_to_perform == "free_battle":
                    # Main menu music continues, freebattle.py handles stopping it later
                    freebattle.initiate_free_battle_sequence(screen, screen_width, screen_height, clock, joysticks) # Pass joysticks
                
                elif action_to_perform == "credits":
                    pygame.mixer.music.stop()
                    credit.run_credit() #
                    try: # Restart music after credits
                        pygame.mixer.music.load("assets/audio/music_main.wav") #
                        pygame.mixer.music.play(-1, 0.0, 5000) #
                    except pygame.error as e: print(f"Error restarting menu music: {e}")

                elif action_to_perform == "exit":
                    running = False
                
                action_to_perform = None # Reset action

        current_screen_size = screen.get_size()
        screen.blit(pygame.transform.scale(background_image, current_screen_size), (0, 0))

        # font_button = pygame.font.Font("assets/fonts/turok.ttf", 24) 
        # for i, button in enumerate(main_buttons):
        #     btn_color = (70, 70, 70)
        #     text_color = (255,255,255)
        #     if i == selected_button_idx: # Highlight if selected by D-pad/keyboard OR hovered by mouse
        #         btn_color = (100,100,100) 
        #
        #     pygame.draw.rect(screen, btn_color, button["rect"])
        #     text_surf = font_button.render(button["text"], True, text_color)
        #     text_rect = text_surf.get_rect(center=button["rect"].center)
        #     screen.blit(text_surf, text_rect)

        pygame.display.flip()
        clock.tick(60)
        
    pygame.quit()
    exit()

if __name__ == "__main__":
    main_menu()
