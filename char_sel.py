
import pygame
from fighter import Warrior 
from character_data import CHARACTER_DATA as ALL_CHARACTER_DATA
from save_data import load_game_state 
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
GREY = (128, 128, 128)
YELLOW = (255, 255, 0)
BLACK = (0,0,0)

def select_characters(screen, font_small, font_med, assets, screen_width, screen_height):
    game_state = load_game_state()
    monk_unlocked = game_state.get("monk_unlocked", False)
   
    available_chars_info = [
        {"id": "warrior", "name": "Warrior", "key_p1": pygame.K_1, "key_p2": pygame.K_q, "unlocked": True},
        {"id": "assasin", "name": "Assassin", "key_p1": pygame.K_2, "key_p2": pygame.K_w, "unlocked": True},
        {"id": "monk", "name": "Monk", "key_p1": pygame.K_3, "key_p2": pygame.K_e, "unlocked": monk_unlocked}
    ]

    player1_selected_id = None
    player2_selected_id = None
    current_player_turn = 1

    running_selection = True
    clock = pygame.time.Clock()

    while running_selection:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return None, None 
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    return None, None 
               
                for char_info in available_chars_info:
                    if current_player_turn == 1 and event.key == char_info["key_p1"]:
                        if char_info["unlocked"]:
                            player1_selected_id = char_info["id"]
                            current_player_turn = 2
                        else:
                            print(f"{char_info['name']} is locked!")
                        break
                    elif current_player_turn == 2 and event.key == char_info["key_p2"]:
                        if char_info["unlocked"]:
                            player2_selected_id = char_info["id"]
                            running_selection = False
                        else:
                            print(f"{char_info['name']} is locked!")
                        break
        
        screen.fill(BLACK)

        prompt_text = f"Player {current_player_turn}, Choose Your Fighter!"
        prompt_surface = font_med.render(prompt_text, True, YELLOW)
        screen.blit(prompt_surface, (screen_width // 2 - prompt_surface.get_width() // 2, 50))

        y_offset = 150
        line_height = 40
        
        for i, char_info in enumerate(available_chars_info):
            display_name = char_info["name"]
            text_color = WHITE

            if not char_info["unlocked"]:
                display_name += " (Locked)"
                text_color = GREY
            
            p_key_name = pygame.key.name(char_info["key_p1" if current_player_turn == 1 else "key_p2"]).upper()
            char_text = f"Press ({p_key_name}) for {display_name}"
            

            char_surface = font_small.render(char_text, True, text_color)
            screen.blit(char_surface, (100, y_offset + i * line_height))

        if player1_selected_id:
            p1_confirm = font_small.render(f"P1: {player1_selected_id.capitalize()}", True, GREEN)
            screen.blit(p1_confirm, (50, screen_height - 70))
        if player2_selected_id: # This will only show after selection is fully done
             p2_confirm = font_small.render(f"P2: {player2_selected_id.capitalize()}", True, GREEN)
             screen.blit(p2_confirm, (screen_width - p2_confirm.get_width() - 50, screen_height - 70))


        pygame.display.flip()
        clock.tick(30) 

    if player1_selected_id and player2_selected_id:
        
        p1_char_cdata = ALL_CHARACTER_DATA[player1_selected_id]
        p1_char_assets = assets[player1_selected_id]
        fighter1 = Warrior(
            player=1, x=200, y=screen_height,
            flip=False,
            data=[*p1_char_cdata["size"], p1_char_cdata["scale"], p1_char_cdata["offset"]],
            sprite_sheet=p1_char_assets["image"],
            animation_steps=p1_char_cdata["animation_steps"],
            sound=p1_char_assets["sound"],
            screen_height=screen_height,
            is_bot=False 
        )

        
        p2_char_cdata = ALL_CHARACTER_DATA[player2_selected_id]
        p2_char_assets = assets[player2_selected_id]
        fighter2 = Warrior( 
            player=2, x=700, y=screen_height,
            flip=True,
            data=[*p2_char_cdata["size"], p2_char_cdata["scale"], p2_char_cdata["offset"]],
            sprite_sheet=p2_char_assets["image"],
            animation_steps=p2_char_cdata["animation_steps"],
            sound=p2_char_assets["sound"],
            screen_height=screen_height,
            is_bot=False 
        )
        return fighter1, fighter2
    else:
        return None, None 
