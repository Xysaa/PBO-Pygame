import pygame
import random
from fighter import Warrior
from character_data import CHARACTER_DATA as ALL_CHARACTER_DATA #
from save_data import load_game_state #

# Gamepad Button Constants (defined in main.py or globally)
JUMP_BUTTON = 0      # X / Cross (used as Confirm here)
ATTACK1_BUTTON = 2
ATTACK2_BUTTON = 1   # Circle / B (used as Back here)
ATTACK3_BUTTON = 3
# For menus
MENU_CONFIRM_BUTTON = JUMP_BUTTON 
MENU_BACK_BUTTON = ATTACK2_BUTTON 


# Colors
WHITE = (255, 255, 255); BLACK = (0, 0, 0); RED = (255, 0, 0); BLUE = (0, 0, 255)
GREEN = (0, 255, 0); GREY = (128, 128, 128); YELLOW = (255, 255, 0)
LIGHT_GREY = (200, 200, 200); P1_COLOR = BLUE; P2_COLOR = RED
LOCKED_COLOR = GREY; HOVER_COLOR = YELLOW

# Grid constants
BOX_SIZE = 100; PADDING = 20; TOP_OFFSET = 150 
SIDE_OFFSET_SELECTED = 50; CHAR_FACE_SIZE = (80, 80); SELECTED_FACE_SIZE = (120, 120)

def get_available_characters(assets): #
    game_state = load_game_state() #
    available_chars = []
    player_selectable_ids = ["warrior", "assasin", "monk", "wizard"] 
    for char_id in player_selectable_ids:
        if char_id not in ALL_CHARACTER_DATA: continue #
        if char_id not in assets: continue
        char_info = {"id": char_id, "name": char_id.capitalize()}
        char_info["face_asset"] = assets[char_id].get("face") #
        char_info["unlocked"] = (char_id != "monk" or game_state.get("monk_unlocked", False)) #
        if char_info["face_asset"] is None:
            placeholder_face = pygame.Surface(CHAR_FACE_SIZE) # This is correct
            placeholder_face.fill(RED)
            pygame.draw.rect(placeholder_face, BLACK, placeholder_face.get_rect(),1)
            char_info["face_asset"] = placeholder_face
        available_chars.append(char_info)
    return available_chars

def select_characters_new(screen, mode, assets, screen_width, screen_height, font_small, font_med, clock, joysticks): # Added joysticks
    available_chars_list = get_available_characters(assets)
    if not available_chars_list: return None, None

    num_chars = len(available_chars_list)
    cols = min(num_chars, 4 if num_chars > 3 else num_chars) 
    rows = (num_chars + cols - 1) // cols 
    grid_width = cols * (BOX_SIZE + PADDING) - PADDING
    grid_start_x = (screen_width - grid_width) // 2

    char_boxes = []
    for i, char_info in enumerate(available_chars_list):
        row, col = divmod(i, cols)
        x = grid_start_x + col * (BOX_SIZE + PADDING)
        y = TOP_OFFSET + row * (BOX_SIZE + PADDING)
        rect = pygame.Rect(x, y, BOX_SIZE, BOX_SIZE)
        char_boxes.append({"rect": rect, "info": char_info, "id": i}) # Add id for cursor

    player1_selected_id_str = None 
    player2_selected_id_str = None 
    current_player_turn = 1  
    
    cursor_idx = 0 

    button_font = font_small
    p1_random_text = button_font.render("P1 Random", True, WHITE)
    p2_random_text = button_font.render("P2 Random", True, WHITE)
    bot_random_text = button_font.render("Bot Random", True, WHITE)
    
    RANDOM_P1_BTN_ID = num_chars 
    RANDOM_P2_BOT_BTN_ID = num_chars + 1
    
    p1_random_rect = pygame.Rect(SIDE_OFFSET_SELECTED, screen_height - PADDING - 50, p1_random_text.get_width() + 20, 40)
    p2_random_rect = pygame.Rect(screen_width - SIDE_OFFSET_SELECTED - p2_random_text.get_width() - 20, screen_height - PADDING - 50, p2_random_text.get_width() + 20, 40)
    
    running_selection = True
    while running_selection:
        mouse_pos = pygame.mouse.get_pos()
        
        temp_hover_idx = -1
        for i, box_data in enumerate(char_boxes):
            if box_data["rect"].collidepoint(mouse_pos):
                temp_hover_idx = i; break
        if p1_random_rect.collidepoint(mouse_pos): temp_hover_idx = RANDOM_P1_BTN_ID
        if p2_random_rect.collidepoint(mouse_pos): temp_hover_idx = RANDOM_P2_BOT_BTN_ID
        if temp_hover_idx != -1 : cursor_idx = temp_hover_idx

        action_confirmed = False
        for event in pygame.event.get():
            if event.type == pygame.QUIT: return None, None
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE: return None, None
                if event.key == pygame.K_RIGHT:
                    if cursor_idx < num_chars -1 : cursor_idx = (cursor_idx + 1) 
                    elif cursor_idx == RANDOM_P1_BTN_ID : cursor_idx = RANDOM_P2_BOT_BTN_ID 
                elif event.key == pygame.K_LEFT:
                    if cursor_idx > 0 and cursor_idx < num_chars: cursor_idx = (cursor_idx - 1)
                    elif cursor_idx == RANDOM_P2_BOT_BTN_ID : cursor_idx = RANDOM_P1_BTN_ID 
                elif event.key == pygame.K_DOWN:
                    if cursor_idx < num_chars: 
                        new_idx = cursor_idx + cols
                        if new_idx < num_chars: cursor_idx = new_idx
                        else: cursor_idx = RANDOM_P1_BTN_ID 
                elif event.key == pygame.K_UP:
                    if cursor_idx >= cols and cursor_idx < num_chars: cursor_idx -= cols 
                    elif cursor_idx == RANDOM_P1_BTN_ID or cursor_idx == RANDOM_P2_BOT_BTN_ID: 
                        cursor_idx = num_chars - 1 
                if event.key == pygame.K_RETURN or event.key == pygame.K_SPACE: action_confirmed = True
            
            if event.type == pygame.JOYHATMOTION:
                hat_x, hat_y = event.value
                if hat_x == 1: 
                    if cursor_idx < num_chars -1 : cursor_idx = (cursor_idx + 1)
                    elif cursor_idx == RANDOM_P1_BTN_ID : cursor_idx = RANDOM_P2_BOT_BTN_ID
                elif hat_x == -1: 
                    if cursor_idx > 0 and cursor_idx < num_chars: cursor_idx = (cursor_idx - 1)
                    elif cursor_idx == RANDOM_P2_BOT_BTN_ID : cursor_idx = RANDOM_P1_BTN_ID
                elif hat_y == -1: 
                    if cursor_idx < num_chars:
                        new_idx = cursor_idx + cols
                        if new_idx < num_chars: cursor_idx = new_idx
                        else: cursor_idx = RANDOM_P1_BTN_ID
                elif hat_y == 1: 
                    if cursor_idx >= cols and cursor_idx < num_chars: cursor_idx -= cols
                    elif cursor_idx == RANDOM_P1_BTN_ID or cursor_idx == RANDOM_P2_BOT_BTN_ID:
                        cursor_idx = num_chars - 1 
            
            if event.type == pygame.JOYBUTTONDOWN:
                if event.button == MENU_CONFIRM_BUTTON: action_confirmed = True
                if event.button == MENU_BACK_BUTTON: return None, None 

            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1: action_confirmed = True

            if action_confirmed:
                selected_char_id_str_action = None; is_random_selection_action = False
                if cursor_idx < num_chars: 
                    if char_boxes[cursor_idx]["info"]["unlocked"]: selected_char_id_str_action = char_boxes[cursor_idx]["info"]["id"]
                    else: print(f"{char_boxes[cursor_idx]['info']['name']} is locked!"); continue
                elif cursor_idx == RANDOM_P1_BTN_ID or cursor_idx == RANDOM_P2_BOT_BTN_ID: is_random_selection_action = True
                
                unlocked_char_ids = [c["id"] for c in available_chars_list if c["unlocked"]]
                if not unlocked_char_ids: continue

                if current_player_turn == 1:
                    if is_random_selection_action and cursor_idx == RANDOM_P1_BTN_ID: player1_selected_id_str = random.choice(unlocked_char_ids)
                    elif selected_char_id_str_action: player1_selected_id_str = selected_char_id_str_action
                    if player1_selected_id_str: current_player_turn = 2 if mode == "pvp" else 3; cursor_idx = 0 # Reset cursor for next player
                
                elif current_player_turn == 2: 
                    if is_random_selection_action and cursor_idx == RANDOM_P2_BOT_BTN_ID:
                        available_for_p2 = [cid for cid in unlocked_char_ids if cid != player1_selected_id_str]
                        player2_selected_id_str = random.choice(available_for_p2 if available_for_p2 else unlocked_char_ids)
                    elif selected_char_id_str_action: player2_selected_id_str = selected_char_id_str_action
                    if player2_selected_id_str: running_selection = False

                elif current_player_turn == 3: 
                    if is_random_selection_action and cursor_idx == RANDOM_P2_BOT_BTN_ID: 
                        player2_selected_id_str = random.choice(unlocked_char_ids)
                    elif selected_char_id_str_action: player2_selected_id_str = selected_char_id_str_action
                    if player2_selected_id_str: running_selection = False
        
        screen.fill(BLACK) 
        prompt_y = 30
        if current_player_turn == 1: prompt_text = "Player 1: Choose Your Fighter"
        elif mode == "pvp" and current_player_turn == 2: prompt_text = "Player 2: Choose Your Fighter"
        elif mode == "pvbot" and current_player_turn == 3: prompt_text = "Player 1: Choose Bot's Fighter"
        else: prompt_text = "Confirming selections..."
        prompt_surface = font_med.render(prompt_text, True, YELLOW)
        screen.blit(prompt_surface, (screen_width // 2 - prompt_surface.get_width() // 2, prompt_y))

        for i, box_data in enumerate(char_boxes):
            rect, info = box_data["rect"], box_data["info"]
            box_color, outline_color, outline_thickness = LIGHT_GREY, WHITE, 2
            is_current_cursor_on_box = (cursor_idx == i)

            if not info["unlocked"]: pygame.draw.rect(screen, GREY, rect) 
            else: pygame.draw.rect(screen, box_color, rect, 1) 

            if info["face_asset"]:
                face_to_blit = info["face_asset"]
                if not info["unlocked"]:
                    locked_face = info["face_asset"].copy()
                    locked_face.fill((80,80,80), special_flags=pygame.BLEND_RGB_MULT) 
                    if is_current_cursor_on_box : locked_face.fill((120,120,120), special_flags=pygame.BLEND_RGB_MULT)
                    face_to_blit = locked_face
                scaled_face = pygame.transform.scale(face_to_blit, CHAR_FACE_SIZE)
                screen.blit(scaled_face, (rect.centerx-CHAR_FACE_SIZE[0]//2, rect.centery-CHAR_FACE_SIZE[1]//2))

            if not info["unlocked"]: 
                font_locked = pygame.font.Font(None, 24) 
                locked_surf = font_locked.render("LOCKED", True, BLACK)
                screen.blit(locked_surf, (rect.centerx-locked_surf.get_width()//2, rect.centery+CHAR_FACE_SIZE[1]//2-locked_surf.get_height()-2))

            current_char_id_str_loop = info["id"] 
            if current_char_id_str_loop == player1_selected_id_str:
                outline_color, outline_thickness = P1_COLOR, 4
                # CORRECTED LINE: Use (width, height) tuple for Surface
                s = pygame.Surface((BOX_SIZE, BOX_SIZE), pygame.SRCALPHA); s.fill((*P1_COLOR, 100)); screen.blit(s, rect.topleft)
            elif current_char_id_str_loop == player2_selected_id_str:
                outline_color, outline_thickness = P2_COLOR, 4
                # CORRECTED LINE: Use (width, height) tuple for Surface
                s = pygame.Surface((BOX_SIZE, BOX_SIZE), pygame.SRCALPHA); s.fill((*P2_COLOR, 100)); screen.blit(s, rect.topleft)
            elif is_current_cursor_on_box and info["unlocked"]: 
                if current_player_turn == 1 or (mode == "pvbot" and current_player_turn == 3): outline_color = P1_COLOR
                elif mode == "pvp" and current_player_turn == 2: outline_color = P2_COLOR
                else: outline_color = HOVER_COLOR
                outline_thickness = 3
            pygame.draw.rect(screen, outline_color, rect, outline_thickness)
            name_surf = font_small.render(info["name"], True, WHITE if info["unlocked"] else GREY)
            screen.blit(name_surf, (rect.centerx - name_surf.get_width()//2, rect.bottom + 5))

        if player1_selected_id_str:
            p1_face = assets[player1_selected_id_str].get("face") #
            if p1_face: screen.blit(pygame.transform.scale(p1_face, SELECTED_FACE_SIZE), (SIDE_OFFSET_SELECTED, TOP_OFFSET))
            p1_name_surf = font_med.render(player1_selected_id_str.capitalize(), True, P1_COLOR)
            screen.blit(p1_name_surf, (SIDE_OFFSET_SELECTED, TOP_OFFSET + SELECTED_FACE_SIZE[1] + 10))

        if player2_selected_id_str: 
            p2_face = assets[player2_selected_id_str].get("face") #
            if p2_face: screen.blit(pygame.transform.scale(p2_face, SELECTED_FACE_SIZE), (screen_width - SIDE_OFFSET_SELECTED - SELECTED_FACE_SIZE[0], TOP_OFFSET))
            p2_name_text = player2_selected_id_str.capitalize()
            if mode == "pvbot": p2_name_text += " (Bot)"
            p2_name_surf = font_med.render(p2_name_text, True, P2_COLOR)
            screen.blit(p2_name_surf, (screen_width - SIDE_OFFSET_SELECTED - p2_name_surf.get_width(), TOP_OFFSET + SELECTED_FACE_SIZE[1] + 10))
            
        btn1_bg, btn2_bg = LIGHT_GREY, LIGHT_GREY
        if cursor_idx == RANDOM_P1_BTN_ID: btn1_bg = GREEN
        if cursor_idx == RANDOM_P2_BOT_BTN_ID: btn2_bg = GREEN
        pygame.draw.rect(screen, btn1_bg, p1_random_rect)
        screen.blit(p1_random_text, (p1_random_rect.centerx - p1_random_text.get_width()//2, p1_random_rect.centery - p1_random_text.get_height()//2))
        current_p2_random_text = bot_random_text if mode == "pvbot" else p2_random_text
        pygame.draw.rect(screen, btn2_bg, p2_random_rect) 
        screen.blit(current_p2_random_text, (p2_random_rect.centerx - current_p2_random_text.get_width()//2, p2_random_rect.centery - current_p2_random_text.get_height()//2))

        pygame.display.flip()
        clock.tick(30)

    if player1_selected_id_str and player2_selected_id_str:
        p1_joystick = joysticks[0] if joysticks else None
        p2_joystick = joysticks[1] if len(joysticks) > 1 and mode == "pvp" else None
        if mode == "pvbot": p2_joystick = None 

        p1_char_cdata = ALL_CHARACTER_DATA[player1_selected_id_str] #
        p1_char_assets = assets[player1_selected_id_str]
        fighter1 = Warrior(player=1, x=200, y=screen_height, flip=False, #
            data=[*p1_char_cdata["size"], p1_char_cdata["scale"], p1_char_cdata["offset"]], #
            sprite_sheet=p1_char_assets["image"], animation_steps=p1_char_cdata["animation_steps"], #
            sound=p1_char_assets["sound"], screen_height=screen_height, is_bot=False, joystick=p1_joystick) #

        p2_char_cdata = ALL_CHARACTER_DATA[player2_selected_id_str] #
        p2_char_assets = assets[player2_selected_id_str]
        fighter2 = Warrior(player=2, x=700, y=screen_height, flip=True, #
            data=[*p2_char_cdata["size"], p2_char_cdata["scale"], p2_char_cdata["offset"]], #
            sprite_sheet=p2_char_assets["image"], animation_steps=p2_char_cdata["animation_steps"], #
            sound=p2_char_assets["sound"], screen_height=screen_height, is_bot=(mode == "pvbot"), joystick=p2_joystick) #
        return fighter1, fighter2
    return None, None
