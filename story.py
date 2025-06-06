# story.py
import pygame
from pygame import mixer
from fighter import Warrior, Mobs 
from character_data import CHARACTER_DATA #
from character_assets import load_character_assets #
from start_battle import start_battle as run_battle #
from save_data import load_game_state, save_game_state, reset_story_progress, DEFAULT_GAME_STATE #
import os

# Gamepad Button Constants (defined in main.py or globally)
DIALOG_NEXT_BUTTON = 0   # JUMP_BUTTON (X/Cross or A) for dialogue next
DIALOG_EXIT_BUTTON = 7   # PAUSE_RESUME_BUTTON (Start) for exiting dialogue to menu (consistent with battle pause)


try:
    from dialog import monk_dialog as external_monk_dialogs #
    from dialog import wind_hash_dialog as external_assassin_dialogs #
except ImportError:
    print("WARNING: dialog.py not found or lists are missing. Using placeholder dialogs.")
    external_monk_dialogs = ["Placeholder Monk Line"] * 5
    external_assassin_dialogs = ["Placeholder Assassin Line"] * 5

mixer.init()
pygame.init() # Pygame already init in main

SCREEN_WIDTH = 1000
SCREEN_HEIGHT = 600
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("The Chosen - Story Mode")

# Colors
RED = (255, 0, 0); YELLOW = (255, 255, 0); WHITE = (255, 255, 255)
GREY = (200, 200, 200); BLACK = (0, 0, 0); GREEN = (0, 180, 0)
DARK_RED = (180, 0, 0); DARK_BLUE = (74,84,98) # Corrected from DARK_BlUE
DIALOG_BOX_COLOR = (20, 20, 60, 220); DIALOG_TEXT_COLOR = WHITE
DIALOG_SPEAKER_NAME_COLOR = YELLOW; DIALOG_BORDER_COLOR = (150, 150, 200)

assets = load_character_assets() #
try:
    bg_image_default = pygame.image.load("assets/images/background/background.jpeg").convert_alpha() #
except pygame.error as e:
    print(f"FATAL ERROR: Default background 'assets/images/background/background.jpeg' not found: {e}")
    bg_image_default = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT)); bg_image_default.fill(BLACK)

bg_image_default_scaled = pygame.transform.scale(bg_image_default, (SCREEN_WIDTH, SCREEN_HEIGHT)) #
active_bg_surface = bg_image_default_scaled #

try:
    victory_img_placeholder = pygame.image.load("assets/images/icons/victory.png").convert_alpha() #
except pygame.error as e:
    print(f"Warning: Victory icon not found: {e}. Creating placeholder.")
    victory_img_placeholder = pygame.Surface((100,50)); victory_img_placeholder.fill(GREEN)

clock = pygame.time.Clock()

# Fonts
font_large = pygame.font.Font("assets/fonts/turok.ttf", 80)
font_med = pygame.font.Font("assets/fonts/turok.ttf", 40)
font_small = pygame.font.Font("assets/fonts/turok.ttf", 30)
font_dialog_text = pygame.font.Font("assets/fonts/turok.ttf", 24)
font_speaker_name = pygame.font.Font("assets/fonts/turok.ttf", 26)
font_outcome = pygame.font.Font("assets/fonts/turok.ttf", 100)

# Player and Opponent Setup
# For story mode, player always uses default joystick (0) if available
player1_joystick = pygame.joystick.Joystick(0) if pygame.joystick.get_count() > 0 else None

player_fighter_story = Warrior(1, 200, SCREEN_HEIGHT, False, #
                         [*CHARACTER_DATA["warrior"]["size"], CHARACTER_DATA["warrior"]["scale"], CHARACTER_DATA["warrior"]["offset"]], #
                         assets["warrior"]["image"], CHARACTER_DATA["warrior"]["animation_steps"], #
                         assets["warrior"]["sound"], SCREEN_HEIGHT, is_bot=False, joystick=player1_joystick) #

story_opponents = {
    "goblin": Mobs(2, 700, SCREEN_HEIGHT, True, #
                   [*CHARACTER_DATA["goblin"]["size"], CHARACTER_DATA["goblin"]["scale"], CHARACTER_DATA["goblin"]["offset"]], #
                   assets["goblin"]["image"], CHARACTER_DATA["goblin"]["animation_steps"], #
                   assets["goblin"]["sound"], SCREEN_HEIGHT, is_bot=True), #
    "golem": Mobs(2, 700, SCREEN_HEIGHT, True, #
                  [*CHARACTER_DATA["golem"]["size"], CHARACTER_DATA["golem"]["scale"], CHARACTER_DATA["golem"]["offset"]], #
                  assets["golem"]["image"], CHARACTER_DATA["golem"]["animation_steps"], #
                  assets["golem"]["sound"], SCREEN_HEIGHT, is_bot=True), #
    "assasin": Warrior(2, 700, SCREEN_HEIGHT, True, #
                       [*CHARACTER_DATA["assasin"]["size"], CHARACTER_DATA["assasin"]["scale"], CHARACTER_DATA["assasin"]["offset"]], #
                       assets["assasin"]["image"], CHARACTER_DATA["assasin"]["animation_steps"], #
                       assets["assasin"]["sound"], SCREEN_HEIGHT, is_bot=True), #
    "monk": Warrior(2, 700, SCREEN_HEIGHT, True, #
                       [*CHARACTER_DATA["monk"]["size"], CHARACTER_DATA["monk"]["scale"], CHARACTER_DATA["monk"]["offset"]], #
                       assets["monk"]["image"], CHARACTER_DATA["monk"]["animation_steps"], #
                       assets["monk"]["sound"], SCREEN_HEIGHT, is_bot=True) #
}

lore_chapters_data = { #
    # ... (chapter data remains the same) ...
    1: {
        "name": "Chapter 1: Goblin Ambush", "opponent_id": "goblin",
        "background_image_path": "assets/images/background/BG1.png",
        "dialogue_sequence": [
            {"speaker": "narrator", "lines": "Perjalananmu sebagai Sang Terpilih dimulai sekarang. Jalan di depan tidak pasti, penuh dengan bahaya dari Segel Surgawi yang retak."},
            {"speaker": "narrator", "lines": "Tiba-tiba, gemerisik di semak-semak mengungkapkan sekelompok Goblin, mata mereka berkilat dengan niat jahat!"}
        ],
        "outro_win": [{"speaker": "narrator", "lines": "Para Goblin lari kocar-kacir dalam kekalahan. Kemenangan kecil, tapi pencarianmu baru saja dimulai."}],
        "outro_lose": [{"speaker": "narrator", "lines": "Kewalahan oleh para Goblin... Kau harus mengumpulkan kekuatanmu dan mencoba lagi."}]
    },
    2: {
        "name": "Chapter 2: The Stone Sentinel", "opponent_id": "golem",
        "background_image_path": "assets/images/background/BG2.png",
        "dialogue_sequence": [
            {"speaker": "narrator", "lines": "Untuk melanjutkan, kau harus melewati tempat pembuktian kuno, yang sekarang dijaga oleh konstruksi yang dihidupkan kembali."},
            {"speaker": "narrator", "lines": "Golem Batu raksasa, wujudnya berderak dengan energi misterius, menghalangi jalanmu. Tampaknya ia adalah penjaga yang tak dapat dilewati."}
        ],
        "outro_win": [{"speaker": "narrator", "lines": "Golem perkasa itu hancur menjadi batu tak bernyawa! Jalan ke depan telah terbuka."}],
        "outro_lose": [{"speaker": "narrator", "lines": "Kekuatan Golem yang luar biasa terlalu berat untuk diatasi kali ini."}]
    },
    3: {
        "name": "Chapter 3: Dance of Shadows", "opponent_id": "assasin",
        "background_image_path": "assets/images/background/background.jpeg",
        "dialogue_sequence": [
            {"speaker": "narrator", "lines": "Saat kau menjelajah lebih dalam, kehadiran yang mengerikan terasa. Sesosok muncul dari bayang-bayang - seorang Assassin (Pembunuh Bayaran)."},
            {"speaker": "warrior", "lines": "Siapa kau yang bersembunyi dalam kegelapan? Sebutkan tujuanmu!"},
            {"speaker": "assasin", "lines": external_assassin_dialogs[0]}, {"speaker": "assasin", "lines": external_assassin_dialogs[1]},
            {"speaker": "warrior", "lines": "Jika diam adalah jawabanmu, maka pedang kita yang akan berbicara!"}
        ],
        "outro_win": [
            {"speaker": "assasin", "lines": external_assassin_dialogs[2]}, {"speaker": "assasin", "lines": external_assassin_dialogs[3]},
            {"speaker": "narrator", "lines": "Assassin itu berbicara dalam teka-teki dan menghilang secepat kemunculannya, meninggalkanmu untuk merenungkan kata-katanya."}],
        "outro_lose": [
            {"speaker": "assasin", "lines": external_assassin_dialogs[4]},
            {"speaker": "narrator", "lines": "Terlalu cepat, terlalu senyap... Assassin itu adalah hantu yang tak bisa kau tangkap."}]
    },
    4: {
        "name": "Chapter 4: The Fallen Monk, Stevanus", "opponent_id": "monk",
        "background_image_path": "assets/images/background/BG4.png",
        "dialogue_sequence": [
            {"speaker": "narrator", "lines": "Kau akhirnya mencapai Skyhold. Stevanus, Biksu yang dulu dihormati, penjaga Segel Surgawi, menanti. Auranya sangat besar, diwarnai kesedihan dan kekuatan dahsyat."},
            {"speaker": "monk", "lines": external_monk_dialogs[0]}, {"speaker": "monk", "lines": external_monk_dialogs[1]},
            {"speaker": "warrior", "lines": "Stevanus! Aku datang untuk menghadapi takdirku dan mengembalikan keseimbangan di Aetherion!"},
            {"speaker": "monk", "lines": external_monk_dialogs[2]}, {"speaker": "monk", "lines": external_monk_dialogs[3]},
            {"speaker": "monk", "lines": external_monk_dialogs[4]},
        ],
        "outro_win": [
            {"speaker": "narrator", "lines": "Stevanus telah dikalahkan! Wujudnya yang rusak menghilang, dan jiwanya yang tersiksa akhirnya menemukan kedamaian."},
            {"speaker": "narrator", "lines": "Kau telah menguasai teknik Biksu! Karakter Biksu sekarang TERBUKA untuk Pertarungan Bebas!"}],
        "outro_lose": [{"speaker": "narrator", "lines": "Kekuatan Stevanus, bahkan yang rusak sekalipun, sungguh luar biasa. Kau belum siap menanggung beban ini."}]
    }
}
MAX_CHAPTERS = len(lore_chapters_data) #

# Dialog Box Geometry
DIALOG_BOX_RECT = pygame.Rect(50, SCREEN_HEIGHT - 210, SCREEN_WIDTH - 100, 180)
TEXT_AREA_MARGIN_X = 140; TEXT_AREA_MARGIN_Y = 25
TEXT_AREA_RECT = pygame.Rect( DIALOG_BOX_RECT.x + TEXT_AREA_MARGIN_X, DIALOG_BOX_RECT.y + TEXT_AREA_MARGIN_Y,
    DIALOG_BOX_RECT.width - TEXT_AREA_MARGIN_X - 20, DIALOG_BOX_RECT.height - (TEXT_AREA_MARGIN_Y * 2))
FACE_POS = (DIALOG_BOX_RECT.x + 15, DIALOG_BOX_RECT.y + (DIALOG_BOX_RECT.height - 110) // 2)
FACE_SIZE = (110, 110)

def show_dialogue_box_enhanced(current_screen_content_func, text_segment, speaker_id_str, speaker_face_surf): #
    try:
        if not pygame.mixer.music.get_busy() or pygame.mixer.music.get_pos() == -1: 
            pygame.mixer.music.load("assets/audio/story_dialogue.wav") #
            pygame.mixer.music.set_volume(0.4) #
            pygame.mixer.music.play(-1, 0.0, 1000) #
    except pygame.error as e: print(f"Error handling dialogue music: {e}")

    words = text_segment.split(' '); wrapped_lines = []; current_line = ""
    for word in words:
        test_line = current_line + word + " "
        if font_dialog_text.size(test_line)[0] < TEXT_AREA_RECT.width: current_line = test_line
        else: wrapped_lines.append(current_line.strip()); current_line = word + " "
    wrapped_lines.append(current_line.strip())
    if wrapped_lines and not wrapped_lines[0]: wrapped_lines.pop(0)

    lines_per_page = max(1, TEXT_AREA_RECT.height // font_dialog_text.get_height())
    num_pages = (len(wrapped_lines) + lines_per_page - 1) // lines_per_page
    current_page_index = 0; waiting_for_page_input = True
    
    while waiting_for_page_input:
        for event in pygame.event.get():
            if event.type == pygame.QUIT: pygame.quit(); exit()
            
            advance_dialogue = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    if pygame.mixer.music.get_busy(): pygame.mixer.music.fadeout(500) #
                    return False # Signal to return to menu
                advance_dialogue = True # Any other key press
            
            if event.type == pygame.JOYBUTTONDOWN:
                if event.button == DIALOG_EXIT_BUTTON: # e.g., Start button
                    if pygame.mixer.music.get_busy(): pygame.mixer.music.fadeout(500)
                    return False # Signal to return to menu
                if event.button == DIALOG_NEXT_BUTTON: # e.g., X or A button
                    advance_dialogue = True
            
            if advance_dialogue:
                current_page_index += 1
                if current_page_index >= num_pages: waiting_for_page_input = False
        
        current_screen_content_func() 
        dialog_box_surf = pygame.Surface(DIALOG_BOX_RECT.size, pygame.SRCALPHA); dialog_box_surf.fill(DIALOG_BOX_COLOR) #
        screen.blit(dialog_box_surf, DIALOG_BOX_RECT.topleft)
        pygame.draw.rect(screen, DIALOG_BORDER_COLOR, DIALOG_BOX_RECT, 3) #

        if speaker_face_surf:
            try: screen.blit(pygame.transform.scale(speaker_face_surf, FACE_SIZE), FACE_POS) #
            except Exception as e: print(f"Error blitting face: {e}")
        
        speaker_name_capitalized = speaker_id_str.capitalize() if speaker_id_str != "narrator" else "" #
        name_surf = font_speaker_name.render(speaker_name_capitalized, True, DIALOG_SPEAKER_NAME_COLOR) #
        screen.blit(name_surf, (TEXT_AREA_RECT.x, DIALOG_BOX_RECT.y + 5))

        start_idx = current_page_index * lines_per_page; end_idx = min(start_idx + lines_per_page, len(wrapped_lines))
        for i, line_txt in enumerate(wrapped_lines[start_idx:end_idx]):
            line_surf = font_dialog_text.render(line_txt, True, DIALOG_TEXT_COLOR) #
            screen.blit(line_surf, (TEXT_AREA_RECT.x, TEXT_AREA_RECT.y + i * font_dialog_text.get_height()))

        if waiting_for_page_input:
            prompt_indicator = "Next (Press Any Key / Button)" # Updated prompt
            prompt_surf = font_dialog_text.render(prompt_indicator, True, YELLOW) #
            screen.blit(prompt_surf, (DIALOG_BOX_RECT.right - prompt_surf.get_width() - 15, DIALOG_BOX_RECT.bottom - prompt_surf.get_height() - 10))
        pygame.display.flip(); clock.tick(30)
    return True

def _play_dialogue_sequence_enhanced(current_screen_func, dialog_list): #
    current_screen_func(); pygame.display.flip() 
    for segment_info in dialog_list:
        speaker_key = segment_info["speaker"]; text_for_segment = segment_info["lines"]
        char_face_surface = assets[speaker_key].get("face") if speaker_key != "narrator" and speaker_key in assets else None #
        if not show_dialogue_box_enhanced(current_screen_func, text_for_segment, speaker_key, char_face_surface): return False
    return True

# Drawing Callbacks
def draw_bg_story_cb(): #
    global active_bg_surface
    if active_bg_surface: screen.blit(active_bg_surface, (0, 0))
    else: screen.fill(BLACK); print("Error: active_bg_surface is None. Using BLACK fill.")

def draw_health_bar_story_cb(health, x, y): #
    ratio = health / 100
    pygame.draw.rect(screen, WHITE, (x - 2, y - 2, 404, 34)); pygame.draw.rect(screen, RED, (x, y, 400, 30))
    pygame.draw.rect(screen, DARK_BLUE, (x, y, 400 * ratio, 30)) # Use DARK_BLUE
def draw_text_for_battle_cb(text, font, color, x, y): screen.blit(font.render(text, True, color), (x, y)) #

def show_battle_outcome_message(message_text, duration_ms): #
    global screen, font_outcome, clock, active_bg_surface, SCREEN_WIDTH, SCREEN_HEIGHT, YELLOW, RED, BLACK
    start_time = pygame.time.get_ticks()
    text_color = YELLOW if message_text == "VICTORY!" else RED
    message_surf = font_outcome.render(message_text, True, text_color)
    message_rect = message_surf.get_rect(center=(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2)) 

    while pygame.time.get_ticks() - start_time < duration_ms:
        for event in pygame.event.get():
            if event.type == pygame.QUIT: pygame.quit(); exit()
            if event.type == pygame.KEYDOWN or event.type == pygame.JOYBUTTONDOWN : # Allow skip with key or joy button
                if pygame.time.get_ticks() - start_time > 300: return
        draw_bg_story_cb() 
        screen.blit(message_surf, message_rect) 
        pygame.display.flip(); clock.tick(30)

def start_story_battle_flow(player, opponent_instance): #
    player.reset(); opponent_instance.reset() #
    if pygame.mixer.music.get_busy(): pygame.mixer.music.fadeout(1000) 

    return_signal = run_battle( #
        SCREEN_WIDTH, SCREEN_HEIGHT, screen,
        draw_bg_story_cb, font_small, font_med, font_large,
        draw_health_bar_story_cb, draw_text_for_battle_cb,
        player, opponent_instance,
        victory_img_placeholder, is_story=True 
    )
    return return_signal 

def main_story(start_new_game_flag=False): #
    global player_fighter_story, active_bg_surface, bg_image_default_scaled

    game_state = load_game_state() #
    if start_new_game_flag: game_state = reset_story_progress() #
    
    current_chapter_num = game_state.get("current_chapter", 1) #
    active_bg_surface = bg_image_default_scaled 

    if game_state.get("story_completed", False) and not start_new_game_flag: #
        draw_bg_story_cb() 
        if not _play_dialogue_sequence_enhanced(draw_bg_story_cb, [{"speaker": "narrator", "lines": "You have already completed the story. Select 'New Story' to play again, or ESC/START to return to menu."}]):
            return True 
        return True 

    running_story_mode = True
    while running_story_mode and current_chapter_num <= MAX_CHAPTERS: #
        chapter_data = lore_chapters_data.get(current_chapter_num) #
        if not chapter_data: 
            print(f"Error: Chapter {current_chapter_num} data missing.")
            active_bg_surface = bg_image_default_scaled; break
        
        chapter_bg_path = chapter_data.get("background_image_path") #
        if chapter_bg_path:
            try:
                new_bg_surf = pygame.image.load(chapter_bg_path).convert_alpha()
                active_bg_surface = pygame.transform.scale(new_bg_surf, (SCREEN_WIDTH, SCREEN_HEIGHT))
            except pygame.error as e:
                print(f"Warning: Failed to load background for chapter {current_chapter_num} ('{chapter_bg_path}'): {e}. Using default.")
                active_bg_surface = bg_image_default_scaled
        else:
            print(f"Warning: No background_image_path specified for chapter {current_chapter_num}. Using default."); active_bg_surface = bg_image_default_scaled

        opponent = story_opponents.get(chapter_data["opponent_id"]) #
        if not opponent: print(f"Error: Opponent for Chapter {current_chapter_num} missing."); break

        draw_bg_story_cb() 
        if not _play_dialogue_sequence_enhanced(draw_bg_story_cb, chapter_data["dialogue_sequence"]): return True #

        exit_to_main_menu_from_battle = start_story_battle_flow(player_fighter_story, opponent)
        if exit_to_main_menu_from_battle: return True 

        if player_fighter_story.alive: show_battle_outcome_message("VICTORY!", 2500) #
        else: show_battle_outcome_message("DEFEAT!", 2500) #

        outro_dialogue_key = "outro_win" if player_fighter_story.alive else "outro_lose" #
        draw_bg_story_cb() 
        if not _play_dialogue_sequence_enhanced(draw_bg_story_cb, chapter_data[outro_dialogue_key]): return True #

        if player_fighter_story.alive: 
            if current_chapter_num == 4: 
                if not game_state.get("monk_unlocked", False): game_state["monk_unlocked"] = True #
                game_state["story_completed"] = True #
                game_state["current_chapter"] = MAX_CHAPTERS + 1 #
                save_game_state(game_state) #
                running_story_mode = False; break 
            
            current_chapter_num += 1 
            game_state["current_chapter"] = current_chapter_num #
            save_game_state(game_state) #
        # else: Player lost, loop continues with same chapter_num or exits if they choose from menu

    final_message = [] #
    if game_state.get("story_completed", False): #
        final_message = [{"speaker": "narrator", "lines": "Congratulations! You have triumphed and completed the story of The Chosen! Press Any Key / Button to return to the main menu."}]
    elif not running_story_mode and not game_state.get("story_completed", False):  #
        if not player_fighter_story.alive and current_chapter_num == MAX_CHAPTERS :
             final_message = [{"speaker": "narrator", "lines": "The final battle was too much... Your journey ends here for now. Return to try again!"}]
        elif not game_state.get("story_completed", False) : #
             final_message = [{"speaker": "narrator", "lines": "Your journey pauses here. Press Any Key / Button to return to the main menu."}]

    if final_message:
        draw_bg_story_cb() 
        _play_dialogue_sequence_enhanced(draw_bg_story_cb, final_message)

    if pygame.mixer.music.get_busy(): 
        pygame.mixer.music.stop()
    # running_story_mode should already be False or loop exited
    return True # Signal to return to main menu

if __name__ == "__main__":
    # Initialize joysticks for standalone testing
    pygame.joystick.init()
    if pygame.joystick.get_count() > 0:
        joy = pygame.joystick.Joystick(0)
        joy.init()
        print(f"Joystick for story test: {joy.get_name()}")
        player_fighter_story._joystick = joy # Assign to the global instance for testing

    SAVE_FILE_NAME = "game_save_data.json" #
    if not os.path.exists(SAVE_FILE_NAME):
       print(f"'{SAVE_FILE_NAME}' not found. Creating default save state for testing story.py.")
       save_game_state(DEFAULT_GAME_STATE.copy()) #

    main_story(start_new_game_flag=True) 
    pygame.quit()
    exit()
