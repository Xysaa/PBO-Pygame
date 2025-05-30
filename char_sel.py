import pygame
import random
from fighter import Warrior
from character_data import CHARACTER_DATA as ALL_CHARACTER_DATA #
from save_data import load_game_state #

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
GREEN = (0, 255, 0)
GREY = (128, 128, 128)
YELLOW = (255, 255, 0)
LIGHT_GREY = (200, 200, 200)
P1_COLOR = BLUE
P2_COLOR = RED
LOCKED_COLOR = GREY
HOVER_COLOR = YELLOW

# Constants for character grid
BOX_SIZE = 100
PADDING = 20
TOP_OFFSET = 150 # Space for prompts
SIDE_OFFSET_SELECTED = 50 # Space on sides to show selected char faces
CHAR_FACE_SIZE = (80, 80) # Size of face inside the box
SELECTED_FACE_SIZE = (120, 120) # Size of selected character face display

def get_available_characters(assets):
    game_state = load_game_state() #
    available_chars = []
    
    # Define the order or filter characters you want to appear in selection
    # For example, excluding 'goblin', 'golem', 'skeleton' as they are mobs
    player_selectable_ids = ["warrior", "assasin", "monk"] # Add 'wizard' if it becomes fully playable

    for char_id in player_selectable_ids:
        if char_id not in ALL_CHARACTER_DATA:
            print(f"Warning: Character ID '{char_id}' not in ALL_CHARACTER_DATA.")
            continue
        if char_id not in assets:
            print(f"Warning: Assets for '{char_id}' not loaded.")
            continue

        char_info = {"id": char_id, "name": char_id.capitalize()}
        char_info["face_asset"] = assets[char_id].get("face")

        if char_id == "monk":
            char_info["unlocked"] = game_state.get("monk_unlocked", False) #
        else:
            # Other characters are unlocked by default for free battle, or add specific unlock conditions
            char_info["unlocked"] = True 
        
        if char_info["face_asset"] is None:
            print(f"Warning: Face asset for {char_id} is missing. Creating placeholder.")
            placeholder_face = pygame.Surface(CHAR_FACE_SIZE)
            placeholder_face.fill(RED) # Placeholder color
            pygame.draw.rect(placeholder_face, BLACK, placeholder_face.get_rect(),1)
            char_info["face_asset"] = placeholder_face
            
        available_chars.append(char_info)
    return available_chars

def select_characters_new(screen, mode, assets, screen_width, screen_height, font_small, font_med, clock):
    available_chars_list = get_available_characters(assets)
    if not available_chars_list:
        print("No characters available for selection!")
        return None, None

    num_chars = len(available_chars_list)
    # Dynamic columns based on available characters, aiming for ~4-5 per row
    cols = min(num_chars, 4 if num_chars > 3 else num_chars) # Max 4 columns, or fewer if not enough chars
    rows = (num_chars + cols - 1) // cols 
    
    grid_width = cols * (BOX_SIZE + PADDING) - PADDING
    grid_start_x = (screen_width - grid_width) // 2

    char_boxes = []
    for i, char_info in enumerate(available_chars_list):
        row = i // cols
        col = i % cols
        x = grid_start_x + col * (BOX_SIZE + PADDING)
        y = TOP_OFFSET + row * (BOX_SIZE + PADDING)
        rect = pygame.Rect(x, y, BOX_SIZE, BOX_SIZE)
        char_boxes.append({"rect": rect, "info": char_info})

    player1_selected_id = None
    player2_selected_id = None
    current_player_turn = 1  # 1 for P1, 2 for P2 (PvP), 3 for P1 choosing for Bot (PvBot)
    
    p1_cursor_idx = 0
    p2_cursor_idx = 0 # Only relevant if allowing simultaneous keyboard, usually sequential

    # Random buttons
    button_font = font_small
    p1_random_text = button_font.render("P1 Random", True, WHITE)
    p2_random_text = button_font.render("P2 Random", True, WHITE)
    bot_random_text = button_font.render("Bot Random", True, WHITE)
    
    p1_random_rect = pygame.Rect(SIDE_OFFSET_SELECTED, screen_height - PADDING - 50, p1_random_text.get_width() + 20, 40)
    p2_random_rect = pygame.Rect(screen_width - SIDE_OFFSET_SELECTED - p2_random_text.get_width() - 20, screen_height - PADDING - 50, p2_random_text.get_width() + 20, 40)
    # bot_random_rect will reuse p2_random_rect's position

    running_selection = True
    while running_selection:
        mouse_pos = pygame.mouse.get_pos()
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return None, None
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    return None, None

                current_cursor_idx = p1_cursor_idx if current_player_turn == 1 or (mode == "pvbot" and current_player_turn == 3) else p2_cursor_idx
                
                if event.key == pygame.K_RIGHT:
                    current_cursor_idx = (current_cursor_idx + 1) % num_chars
                elif event.key == pygame.K_LEFT:
                    current_cursor_idx = (current_cursor_idx - 1 + num_chars) % num_chars
                elif event.key == pygame.K_DOWN:
                    current_cursor_idx = (current_cursor_idx + cols) % num_chars # approximate
                    if current_cursor_idx >= num_chars : current_cursor_idx = current_cursor_idx % cols # wrap to first row if overshoot
                    # This basic down/up can be improved for more accurate grid movement
                elif event.key == pygame.K_UP:
                    current_cursor_idx = (current_cursor_idx - cols + num_chars) % num_chars # approximate
                    if current_cursor_idx < 0 : current_cursor_idx = num_chars - 1 - (abs(current_cursor_idx) %cols)

                if current_player_turn == 1 or (mode == "pvbot" and current_player_turn == 3):
                    p1_cursor_idx = current_cursor_idx
                else: # P2's turn in PvP
                    p2_cursor_idx = current_cursor_idx

                if event.key == pygame.K_RETURN or event.key == pygame.K_SPACE:
                    selected_box_idx = p1_cursor_idx if (current_player_turn == 1 or (mode == "pvbot" and current_player_turn == 3)) else p2_cursor_idx
                    if char_boxes[selected_box_idx]["info"]["unlocked"]:
                        char_id = char_boxes[selected_box_idx]["info"]["id"]
                        if current_player_turn == 1:
                            player1_selected_id = char_id
                            current_player_turn = 2 if mode == "pvp" else 3 # Move to P2 or Bot selection
                        elif current_player_turn == 2: # PvP P2
                            if char_id != player1_selected_id : # Basic check: P2 can't be same as P1 (optional)
                                player2_selected_id = char_id
                                running_selection = False # Both selected
                        elif current_player_turn == 3: # PvBot Bot
                            player2_selected_id = char_id # Bot is P2
                            running_selection = False # Both selected
                    else:
                        print(f"{char_boxes[selected_box_idx]['info']['name']} is locked!")


            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                # Character box clicks
                for i, box_data in enumerate(char_boxes):
                    if box_data["rect"].collidepoint(mouse_pos):
                        if box_data["info"]["unlocked"]:
                            char_id = box_data["info"]["id"]
                            if current_player_turn == 1:
                                player1_selected_id = char_id
                                current_player_turn = 2 if mode == "pvp" else 3
                                p1_cursor_idx = i # Move cursor to clicked
                            elif current_player_turn == 2: # PvP P2
                                if char_id != player1_selected_id: # Optional: prevent same char
                                    player2_selected_id = char_id
                                    running_selection = False
                                    p2_cursor_idx = i
                            elif current_player_turn == 3: # PvBot Bot
                                player2_selected_id = char_id
                                running_selection = False
                                p1_cursor_idx = i # P1's cursor used for bot selection too
                        else:
                            print(f"{box_data['info']['name']} is locked!")
                        break
                
                # Random button clicks
                unlocked_char_ids = [c["id"] for c in available_chars_list if c["unlocked"]]
                if not unlocked_char_ids: continue # Should not happen if list is not empty

                if p1_random_rect.collidepoint(mouse_pos) and current_player_turn == 1:
                    player1_selected_id = random.choice(unlocked_char_ids)
                    current_player_turn = 2 if mode == "pvp" else 3
                
                if mode == "pvp" and p2_random_rect.collidepoint(mouse_pos) and current_player_turn == 2:
                    available_for_p2 = [cid for cid in unlocked_char_ids if cid != player1_selected_id]
                    if available_for_p2: player2_selected_id = random.choice(available_for_p2)
                    else: player2_selected_id = random.choice(unlocked_char_ids) # allow same if only one unlocked
                    running_selection = False

                if mode == "pvbot" and p2_random_rect.collidepoint(mouse_pos) and current_player_turn == 3: # Re-using p2_random_rect for bot
                    player2_selected_id = random.choice(unlocked_char_ids)
                    running_selection = False


        # --- Drawing ---
        screen.fill(BLACK)
        prompt_y = 30
        if current_player_turn == 1:
            prompt_text = "Player 1: Choose Your Fighter"
        elif mode == "pvp" and current_player_turn == 2:
            prompt_text = "Player 2: Choose Your Fighter"
        elif mode == "pvbot" and current_player_turn == 3:
            prompt_text = "Player 1: Choose Bot's Fighter"
        else: # Should be resolved
            prompt_text = "Confirming selections..."

        prompt_surface = font_med.render(prompt_text, True, YELLOW)
        screen.blit(prompt_surface, (screen_width // 2 - prompt_surface.get_width() // 2, prompt_y))

        # Draw character grid
        for i, box_data in enumerate(char_boxes):
            rect = box_data["rect"]
            info = box_data["info"]
            
            box_color = LIGHT_GREY
            outline_color = BLACK
            outline_thickness = 2

            is_p1_hover = (current_player_turn == 1 or (mode == "pvbot" and current_player_turn == 3)) and i == p1_cursor_idx
            is_p2_hover = (mode == "pvp" and current_player_turn == 2) and i == p2_cursor_idx

            if not info["unlocked"]:
                box_color = GREY
                if info["face_asset"]:
                    # Create a desaturated/greyed-out version for locked characters
                    locked_face = info["face_asset"].copy()
                    locked_face.fill((50, 50, 50), special_flags=pygame.BLEND_RGB_MULT) # Darken
                    screen.blit(pygame.transform.scale(locked_face, CHAR_FACE_SIZE), 
                                (rect.centerx - CHAR_FACE_SIZE[0]//2, rect.centery - CHAR_FACE_SIZE[1]//2))
                font_locked = pygame.font.Font(None, 24) # Using default font for simplicity
                locked_surf = font_locked.render("LOCKED", True, BLACK)
                screen.blit(locked_surf, (rect.centerx - locked_surf.get_width()//2, rect.centery + CHAR_FACE_SIZE[1]//2 - locked_surf.get_height()))

            elif info["face_asset"]:
                 screen.blit(pygame.transform.scale(info["face_asset"], CHAR_FACE_SIZE), 
                            (rect.centerx - CHAR_FACE_SIZE[0]//2, rect.centery - CHAR_FACE_SIZE[1]//2))


            if info["id"] == player1_selected_id:
                outline_color = P1_COLOR
                outline_thickness = 4
                # Transparent fill for P1
                s = pygame.Surface((BOX_SIZE,BOX_SIZE), pygame.SRCALPHA)
                s.fill((P1_COLOR[0], P1_COLOR[1], P1_COLOR[2], 100)) # P1 color with alpha
                screen.blit(s, (rect.x, rect.y))
            elif mode == "pvp" and info["id"] == player2_selected_id:
                outline_color = P2_COLOR
                outline_thickness = 4
                s = pygame.Surface((BOX_SIZE,BOX_SIZE), pygame.SRCALPHA)
                s.fill((P2_COLOR[0], P2_COLOR[1], P2_COLOR[2], 100)) # P2 color with alpha
                screen.blit(s, (rect.x, rect.y))
            elif mode == "pvbot" and info["id"] == player2_selected_id : # Bot selected
                outline_color = P2_COLOR # Bot uses P2 color for now
                outline_thickness = 4
                s = pygame.Surface((BOX_SIZE,BOX_SIZE), pygame.SRCALPHA)
                s.fill((P2_COLOR[0], P2_COLOR[1], P2_COLOR[2], 100)) 
                screen.blit(s, (rect.x, rect.y))


            if is_p1_hover and info["unlocked"]: outline_color = P1_COLOR; outline_thickness = 3
            if is_p2_hover and info["unlocked"]: outline_color = P2_COLOR; outline_thickness = 3
            
            pygame.draw.rect(screen, box_color, rect, 0 if not info["unlocked"] else 1) # fill if locked, else border for unlocked
            pygame.draw.rect(screen, outline_color, rect, outline_thickness)
            
            name_surf = font_small.render(info["name"], True, WHITE if info["unlocked"] else GREY)
            screen.blit(name_surf, (rect.centerx - name_surf.get_width()//2, rect.bottom + 5))

        # Draw selected character faces on sides
        if player1_selected_id:
            p1_face = assets[player1_selected_id].get("face")
            if p1_face:
                screen.blit(pygame.transform.scale(p1_face, SELECTED_FACE_SIZE), 
                            (SIDE_OFFSET_SELECTED, TOP_OFFSET))
            p1_name_surf = font_med.render(player1_selected_id.capitalize(), True, P1_COLOR)
            screen.blit(p1_name_surf, (SIDE_OFFSET_SELECTED, TOP_OFFSET + SELECTED_FACE_SIZE[1] + 10))

        if player2_selected_id: # Works for P2 in PvP and Bot in PvBot
            p2_face = assets[player2_selected_id].get("face")
            if p2_face:
                 screen.blit(pygame.transform.scale(p2_face, SELECTED_FACE_SIZE), 
                            (screen_width - SIDE_OFFSET_SELECTED - SELECTED_FACE_SIZE[0], TOP_OFFSET))
            p2_name_text = player2_selected_id.capitalize()
            if mode == "pvbot": p2_name_text += " (Bot)"
            p2_name_surf = font_med.render(p2_name_text, True, P2_COLOR)
            screen.blit(p2_name_surf, (screen_width - SIDE_OFFSET_SELECTED - SELECTED_FACE_SIZE[0], TOP_OFFSET + SELECTED_FACE_SIZE[1] + 10))
            
        # Draw Random Buttons
        pygame.draw.rect(screen, GREEN if p1_random_rect.collidepoint(mouse_pos) else LIGHT_GREY, p1_random_rect)
        screen.blit(p1_random_text, (p1_random_rect.centerx - p1_random_text.get_width()//2, p1_random_rect.centery - p1_random_text.get_height()//2))

        current_p2_random_text = bot_random_text if mode == "pvbot" else p2_random_text
        pygame.draw.rect(screen, GREEN if p2_random_rect.collidepoint(mouse_pos) else LIGHT_GREY, p2_random_rect) # p2_random_rect used for bot too
        screen.blit(current_p2_random_text, (p2_random_rect.centerx - current_p2_random_text.get_width()//2, p2_random_rect.centery - current_p2_random_text.get_height()//2))


        pygame.display.flip()
        clock.tick(30)

    if player1_selected_id and player2_selected_id:
        p1_char_cdata = ALL_CHARACTER_DATA[player1_selected_id]
        p1_char_assets = assets[player1_selected_id]
        fighter1 = Warrior( #
            player=1, x=200, y=screen_height, # y is bottom of screen for fighter init
            flip=False,
            data=[*p1_char_cdata["size"], p1_char_cdata["scale"], p1_char_cdata["offset"]], #
            sprite_sheet=p1_char_assets["image"],
            animation_steps=p1_char_cdata["animation_steps"], #
            sound=p1_char_assets["sound"],
            screen_height=screen_height, # Pass actual screen_height
            is_bot=False
        )

        p2_char_cdata = ALL_CHARACTER_DATA[player2_selected_id]
        p2_char_assets = assets[player2_selected_id]
        fighter2 = Warrior( #
            player=2, x=700, y=screen_height, # y is bottom of screen for fighter init
            flip=True,
            data=[*p2_char_cdata["size"], p2_char_cdata["scale"], p2_char_cdata["offset"]], #
            sprite_sheet=p2_char_assets["image"],
            animation_steps=p2_char_cdata["animation_steps"], #
            sound=p2_char_assets["sound"],
            screen_height=screen_height, # Pass actual screen_height
            is_bot=(mode == "pvbot")
        )
        return fighter1, fighter2
    else:
        return None, None
