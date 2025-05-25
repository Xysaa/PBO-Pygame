# story.py
import pygame
from pygame import mixer
from fighter import Warrior, Mobs # Wizard tidak digunakan di story ini secara eksplisit
# import start_battle # Tidak perlu jika hanya menggunakan run_battle
from character_data import CHARACTER_DATA #
from character_assets import load_character_assets #
from start_battle import start_battle as run_battle #
from save_data import load_game_state, save_game_state, reset_story_progress, DEFAULT_GAME_STATE
import os

# Import dialog dari file dialog.py
try:
    from dialog import monk_dialog as external_monk_dialogs
    from dialog import wind_hash_dialog as external_assassin_dialogs
    # from dialog import mob_dialog # Bisa digunakan jika perlu
except ImportError:
    print("WARNING: dialog.py not found or lists are missing. Using placeholder dialogs.")
    external_monk_dialogs = ["Placeholder Monk Line"] * 5
    external_assassin_dialogs = ["Placeholder Assassin Line"] * 5

mixer.init()
pygame.init()

# Create game window
SCREEN_WIDTH = 1000
SCREEN_HEIGHT = 600
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("The Chosen - Story Mode")

# Colors
RED = (255, 0, 0); YELLOW = (255, 255, 0); WHITE = (255, 255, 255)
GREY = (200, 200, 200); BLACK = (0, 0, 0); GREEN = (0, 180, 0)
DARK_RED = (180, 0, 0)
DARK_BlUE = (74,84,98)
DIALOG_BOX_COLOR = (20, 20, 60, 220)
DIALOG_TEXT_COLOR = WHITE
DIALOG_SPEAKER_NAME_COLOR = YELLOW
DIALOG_BORDER_COLOR = (150, 150, 200)

# Load Assets
assets = load_character_assets()
# --- MODIFIED: Load default background and prepare active_bg_surface ---
try:
    bg_image_default = pygame.image.load("assets/images/background/background.jpeg").convert_alpha()
except pygame.error as e:
    print(f"FATAL ERROR: Default background 'assets/images/background/background.jpeg' not found: {e}")
    # Create a fallback black surface if default background is missing
    bg_image_default = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT))
    bg_image_default.fill(BLACK)

bg_image_default_scaled = pygame.transform.scale(bg_image_default, (SCREEN_WIDTH, SCREEN_HEIGHT))
active_bg_surface = bg_image_default_scaled # Initialize with the default scaled background
# --- END MODIFICATION ---

victory_img = pygame.image.load("assets/images/icons/victory.png").convert_alpha()
clock = pygame.time.Clock()

# Fonts
font_large = pygame.font.Font("assets/fonts/turok.ttf", 80)
font_med = pygame.font.Font("assets/fonts/turok.ttf", 40)
font_small = pygame.font.Font("assets/fonts/turok.ttf", 30)
font_dialog_text = pygame.font.Font("assets/fonts/turok.ttf", 24)
font_speaker_name = pygame.font.Font("assets/fonts/turok.ttf", 26)

# --- Story Specific Fighter Instances ---
player_fighter_story = Warrior(1, 200, SCREEN_HEIGHT, False,
                         [*CHARACTER_DATA["warrior"]["size"], CHARACTER_DATA["warrior"]["scale"], CHARACTER_DATA["warrior"]["offset"]],
                         assets["warrior"]["image"], CHARACTER_DATA["warrior"]["animation_steps"],
                         assets["warrior"]["sound"], SCREEN_HEIGHT, is_bot=False)

story_opponents = {
    "goblin": Mobs(2, 700, SCREEN_HEIGHT, True,
                   [*CHARACTER_DATA["goblin"]["size"], CHARACTER_DATA["goblin"]["scale"], CHARACTER_DATA["goblin"]["offset"]],
                   assets["goblin"]["image"], CHARACTER_DATA["goblin"]["animation_steps"],
                   assets["goblin"]["sound"], SCREEN_HEIGHT, is_bot=True),
    "golem": Mobs(2, 700, SCREEN_HEIGHT, True,
                  [*CHARACTER_DATA["golem"]["size"], CHARACTER_DATA["golem"]["scale"], CHARACTER_DATA["golem"]["offset"]],
                  assets["golem"]["image"], CHARACTER_DATA["golem"]["animation_steps"],
                  assets["golem"]["sound"], SCREEN_HEIGHT, is_bot=True),
    "assasin": Warrior(2, 700, SCREEN_HEIGHT, True,
                       [*CHARACTER_DATA["assasin"]["size"], CHARACTER_DATA["assasin"]["scale"], CHARACTER_DATA["assasin"]["offset"]],
                       assets["assasin"]["image"], CHARACTER_DATA["assasin"]["animation_steps"],
                       assets["assasin"]["sound"], SCREEN_HEIGHT, is_bot=True),
    "monk": Warrior(2, 700, SCREEN_HEIGHT, True,
                       [*CHARACTER_DATA["monk"]["size"], CHARACTER_DATA["monk"]["scale"], CHARACTER_DATA["monk"]["offset"]],
                       assets["monk"]["image"], CHARACTER_DATA["monk"]["animation_steps"],
                       assets["monk"]["sound"], SCREEN_HEIGHT, is_bot=True)
}

# --- Lore and Chapter Data ---
# --- MODIFIED: Added "background_image_path" to each chapter ---
lore_chapters_data = {
    1: {
        "name": "Chapter 1: Goblin Ambush",
        "opponent_id": "goblin",
        "background_image_path": "assets/images/background/BG1.png", # Ganti dengan path gambar yang sesuai
        "dialogue_sequence": [
            {"speaker": "narrator", "lines": "Your journey as The Chosen begins now. The path ahead is uncertain, fraught with peril from the fractured Celestial Seal."},
            {"speaker": "narrator", "lines": "Suddenly, the rustling in the bushes reveals a band of Goblins, their eyes gleaming with malice!"}
        ],
        "outro_win": [{"speaker": "narrator", "lines": "The Goblins scatter in defeat. A small victory, but your quest has just begun."}],
        "outro_lose": [{"speaker": "narrator", "lines": "Overwhelmed by the Goblins... You must gather your strength and try again."}]
    },
    2: {
        "name": "Chapter 2: The Stone Sentinel",
        "opponent_id": "golem",
        "background_image_path": "assets/images/background/BG2.png", # Ganti dengan path gambar yang sesuai
        "dialogue_sequence": [
            {"speaker": "narrator", "lines": "To proceed, you must pass the ancient proving grounds, now guarded by reanimated constructs."},
            {"speaker": "narrator", "lines": "A colossal Stone Golem, its form crackling with arcane energy, blocks your path. It seems an impassable guardian."}
        ],
        "outro_win": [{"speaker": "narrator", "lines": "The mighty Golem crumbles to inert stone! The way forward is clear."}],
        "outro_lose": [{"speaker": "narrator", "lines": "The Golem's sheer power is too much to overcome this time."}]
    },
    3: {
        "name": "Chapter 3: Dance of Shadows",
        "opponent_id": "assasin",
        "background_image_path": "assets/images/background/background.jpeg", # Ganti dengan path gambar yang sesuai
        "dialogue_sequence": [
            {"speaker": "narrator", "lines": "As you venture deeper, a chilling presence is felt. A figure emerges from the shadows - an Assassin."},
            {"speaker": "warrior", "lines": "Who are you that lurks in darkness? State your purpose!"},
            {"speaker": "assasin", "lines": external_assassin_dialogs[0]},
            {"speaker": "assasin", "lines": external_assassin_dialogs[1]},
            {"speaker": "warrior", "lines": "If silence is your answer, then our blades will do the talking!"}
        ],
        "outro_win": [
            {"speaker": "assasin", "lines": external_assassin_dialogs[2]},
            {"speaker": "assasin", "lines": external_assassin_dialogs[3]},
            {"speaker": "narrator", "lines": "The Assassin speaks in riddles and vanishes as quickly as they appeared, leaving you to ponder their words."}],
        "outro_lose": [
            {"speaker": "assasin", "lines": external_assassin_dialogs[4]},
            {"speaker": "narrator", "lines": "Too swift, too silent... The Assassin was a phantom you could not grasp."}]
    },
    4: {
        "name": "Chapter 4: The Fallen Monk, Stevanus",
        "opponent_id": "monk",
        "background_image_path": "assets/images/background/BG4.png", # Ganti dengan path gambar yang sesuai
        "dialogue_sequence": [
            {"speaker": "narrator", "lines": "You have finally reached the Skyhold. Stevanus, the once revered Monk, guardian of the Celestial Seal, awaits. His aura is immense, tinged with sorrow and immense power."},
            {"speaker": "monk", "lines": external_monk_dialogs[0]},
            {"speaker": "monk", "lines": external_monk_dialogs[1]},
            {"speaker": "warrior", "lines": "Stevanus! I have come to face my destiny and restore balance to Aetherion!"},
            {"speaker": "monk", "lines": external_monk_dialogs[2]},
            {"speaker": "monk", "lines": external_monk_dialogs[3]},
            {"speaker": "monk", "lines": external_monk_dialogs[4]},
        ],
        "outro_win": [
            {"speaker": "narrator", "lines": "Stevanus is defeated! His corrupted form dissipates, and his tormented spirit finally finds peace."},
            {"speaker": "narrator", "lines": "You have mastered the Monk's techniques! The Monk is now UNLOCKED for Free Battle!"}],
        "outro_lose": [{"speaker": "narrator", "lines": "Stevanus's power, even corrupted, is overwhelming. You are not yet ready to bear this burden."}]
    }
}
# --- END MODIFICATION ---
MAX_CHAPTERS = len(lore_chapters_data)

# --- Dialogue Box Constants and Function ---
DIALOG_BOX_RECT = pygame.Rect(50, SCREEN_HEIGHT - 210, SCREEN_WIDTH - 100, 180)
TEXT_AREA_MARGIN_X = 140
TEXT_AREA_MARGIN_Y = 25
TEXT_AREA_RECT = pygame.Rect(
    DIALOG_BOX_RECT.x + TEXT_AREA_MARGIN_X,
    DIALOG_BOX_RECT.y + TEXT_AREA_MARGIN_Y,
    DIALOG_BOX_RECT.width - TEXT_AREA_MARGIN_X - 20,
    DIALOG_BOX_RECT.height - (TEXT_AREA_MARGIN_Y * 2)
)
FACE_POS = (DIALOG_BOX_RECT.x + 15, DIALOG_BOX_RECT.y + (DIALOG_BOX_RECT.height - 110) // 2)
FACE_SIZE = (110, 110)

def show_dialogue_box_enhanced(current_screen_content_func, text_segment, speaker_id_str, speaker_face_surf):
    try:
        if not pygame.mixer.music.get_busy() or pygame.mixer.music.get_pos() == -1:
            pygame.mixer.music.load("assets/audio/story_dialogue.wav")
            pygame.mixer.music.set_volume(0.4)
            pygame.mixer.music.play(-1, 0.0, 1000)
    except pygame.error as e:
        print(f"Error handling dialogue music: {e}")

    words = text_segment.split(' ')
    wrapped_lines = []
    current_line = ""
    for word in words:
        test_line = current_line + word + " "
        if font_dialog_text.size(test_line)[0] < TEXT_AREA_RECT.width:
            current_line = test_line
        else:
            wrapped_lines.append(current_line.strip())
            current_line = word + " "
    wrapped_lines.append(current_line.strip())
    if wrapped_lines and not wrapped_lines[0]: wrapped_lines.pop(0)

    lines_per_page = max(1, TEXT_AREA_RECT.height // font_dialog_text.get_height())
    num_pages = (len(wrapped_lines) + lines_per_page - 1) // lines_per_page
    current_page_index = 0

    waiting_for_page_input = True
    while waiting_for_page_input:
        for event in pygame.event.get():
            if event.type == pygame.QUIT: pygame.quit(); exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    if pygame.mixer.music.get_busy(): pygame.mixer.music.fadeout(500)
                    return False
                current_page_index += 1
                if current_page_index >= num_pages:
                    waiting_for_page_input = False

        current_screen_content_func()

        dialog_box_surf = pygame.Surface(DIALOG_BOX_RECT.size, pygame.SRCALPHA)
        dialog_box_surf.fill(DIALOG_BOX_COLOR)
        screen.blit(dialog_box_surf, DIALOG_BOX_RECT.topleft)
        pygame.draw.rect(screen, DIALOG_BORDER_COLOR, DIALOG_BOX_RECT, 3)

        if speaker_face_surf:
            try:
                scaled_face = pygame.transform.scale(speaker_face_surf, FACE_SIZE)
                screen.blit(scaled_face, FACE_POS)
            except Exception as e: print(f"Error blitting face: {e}")

        speaker_name_capitalized = speaker_id_str.capitalize()
        if speaker_id_str == "narrator": speaker_name_capitalized = ""
        
        name_surf = font_speaker_name.render(speaker_name_capitalized, True, DIALOG_SPEAKER_NAME_COLOR)
        screen.blit(name_surf, (TEXT_AREA_RECT.x, DIALOG_BOX_RECT.y + 5))

        start_idx = current_page_index * lines_per_page
        end_idx = min(start_idx + lines_per_page, len(wrapped_lines))
        for i, line_txt in enumerate(wrapped_lines[start_idx:end_idx]):
            line_surf = font_dialog_text.render(line_txt, True, DIALOG_TEXT_COLOR)
            screen.blit(line_surf, (TEXT_AREA_RECT.x, TEXT_AREA_RECT.y + i * font_dialog_text.get_height()))

        if waiting_for_page_input:
            prompt_indicator = ">>" if current_page_index < num_pages - 1 else "Next >>"
            prompt_surf = font_dialog_text.render(prompt_indicator, True, YELLOW)
            screen.blit(prompt_surf, (DIALOG_BOX_RECT.right - prompt_surf.get_width() - 15,
                                      DIALOG_BOX_RECT.bottom - prompt_surf.get_height() - 10))
        pygame.display.flip()
        clock.tick(30)
    return True

def _play_dialogue_sequence_enhanced(current_screen_func, dialog_list):
    current_screen_func()
    pygame.display.flip()

    for segment_info in dialog_list:
        speaker_key = segment_info["speaker"]
        text_for_segment = segment_info["lines"]
        
        char_face_surface = None
        if speaker_key != "narrator" and speaker_key in assets:
            char_face_surface = assets[speaker_key].get("face")

        if not show_dialogue_box_enhanced(current_screen_func, text_for_segment, speaker_key, char_face_surface):
            return False
    return True

# --- Helper functions for battle module callback ---
# --- MODIFIED: draw_bg_story_cb now uses active_bg_surface ---
def draw_bg_story_cb():
    global active_bg_surface
    if active_bg_surface:
        screen.blit(active_bg_surface, (0, 0))
    else:
        # Fallback jika active_bg_surface tidak terdefinisi (seharusnya tidak terjadi)
        screen.fill(BLACK) 
        print("Error: active_bg_surface is None in draw_bg_story_cb. Using BLACK fill.")
# --- END MODIFICATION ---

def draw_health_bar_story_cb(health, x, y):
    ratio = health / 100
    pygame.draw.rect(screen, WHITE, (x - 2, y - 2, 404, 34)); pygame.draw.rect(screen, RED, (x, y, 400, 30))
    pygame.draw.rect(screen, DARK_BlUE, (x, y, 400 * ratio, 30))
def draw_text_for_battle_cb(text, font, color, x, y): screen.blit(font.render(text, True, color), (x, y))

def start_story_battle_flow(player, opponent_instance):
    player.reset()
    opponent_instance.reset()
    if pygame.mixer.music.get_busy(): pygame.mixer.music.fadeout(1000)

    return_signal = run_battle(
        SCREEN_WIDTH, SCREEN_HEIGHT, screen,
        draw_bg_story_cb, font_small, font_med, font_large,
        draw_health_bar_story_cb, draw_text_for_battle_cb,
        player, opponent_instance,
        victory_img, is_story=True
    )
    return return_signal

# --- Main Story Function ---
def main_story(start_new_game_flag=False):
    global player_fighter_story, active_bg_surface, bg_image_default_scaled # Tambahkan global

    game_state = load_game_state()

    if start_new_game_flag: game_state = reset_story_progress()
    
    current_chapter_num = game_state.get("current_chapter", 1)

    # --- MODIFICATION: Set default background before any story elements if needed ---
    active_bg_surface = bg_image_default_scaled 
    # --- END MODIFICATION ---

    if game_state.get("story_completed", False) and not start_new_game_flag:
        draw_bg_story_cb() 
        if not _play_dialogue_sequence_enhanced(draw_bg_story_cb, [{"speaker": "narrator", "lines": "You have already completed the story. Select 'New Story' to play again, or ESC to return to menu."}]):
            return True
        return True

    running_story_mode = True
    while running_story_mode and current_chapter_num <= MAX_CHAPTERS:
        chapter_data = lore_chapters_data.get(current_chapter_num)
        if not chapter_data: 
            print(f"Error: Chapter {current_chapter_num} data missing.")
            active_bg_surface = bg_image_default_scaled # Reset ke default jika chapter data error
            break
        
        # --- MODIFICATION: Load chapter-specific background ---
        chapter_bg_path = chapter_data.get("background_image_path")
        if chapter_bg_path:
            try:
                new_bg_surf = pygame.image.load(chapter_bg_path).convert_alpha()
                active_bg_surface = pygame.transform.scale(new_bg_surf, (SCREEN_WIDTH, SCREEN_HEIGHT))
            except pygame.error as e:
                print(f"Warning: Failed to load background for chapter {current_chapter_num} ('{chapter_bg_path}'): {e}. Using default background.")
                active_bg_surface = bg_image_default_scaled # Fallback ke default
        else:
            print(f"Warning: No background_image_path specified for chapter {current_chapter_num}. Using default background.")
            active_bg_surface = bg_image_default_scaled # Gunakan default jika path tidak ada
        # --- END MODIFICATION ---

        opponent = story_opponents.get(chapter_data["opponent_id"])
        if not opponent: 
            print(f"Error: Opponent for Chapter {current_chapter_num} missing.")
            break

        draw_bg_story_cb() 
        if not _play_dialogue_sequence_enhanced(draw_bg_story_cb, chapter_data["dialogue_sequence"]): return True

        exit_to_main_menu = start_story_battle_flow(player_fighter_story, opponent)
        if exit_to_main_menu: return True

        outro_dialogue_key = "outro_win" if player_fighter_story.alive else "outro_lose"
        draw_bg_story_cb() 
        if not _play_dialogue_sequence_enhanced(draw_bg_story_cb, chapter_data[outro_dialogue_key]): return True

        if player_fighter_story.alive: 
            if current_chapter_num == 4: 
                if not game_state.get("monk_unlocked", False): game_state["monk_unlocked"] = True
                game_state["story_completed"] = True
                game_state["current_chapter"] = MAX_CHAPTERS + 1
                save_game_state(game_state)
                running_story_mode = False 
                break 
            
            current_chapter_num += 1
            game_state["current_chapter"] = current_chapter_num
            save_game_state(game_state)
        else: 
            pass


    # --- After Story Loop ---
    # --- MODIFICATION: Optionally reset to default background for final messages ---
    # active_bg_surface = bg_image_default_scaled # Uncomment jika ingin latar default untuk pesan akhir
    # --- END MODIFICATION ---
    final_message = []
    if game_state.get("story_completed", False):
        final_message = [{"speaker": "narrator", "lines": "Congratulations! You have triumphed and completed the story of The Chosen! Press any key to return to the main menu."}]
    elif not running_story_mode and current_chapter_num <=MAX_CHAPTERS : 
        final_message = [{"speaker": "narrator", "lines": "An unexpected error occurred in your journey. Press any key to return to main menu."}]
    
    if final_message:
        draw_bg_story_cb()
        _play_dialogue_sequence_enhanced(draw_bg_story_cb, final_message)

    if pygame.mixer.music.get_busy(): pygame.mixer.music.stop()
    return True

if __name__ == "__main__":
    # Definisikan SAVE_FILE_NAME jika belum ada (biasanya dari main.py)
    # Contoh:
    SAVE_FILE_NAME = "savegame.json"
    
    # Buat file save default jika tidak ada untuk pengujian mandiri story.py
    if not os.path.exists(SAVE_FILE_NAME):
       print(f"'{SAVE_FILE_NAME}' not found. Creating default save state for testing story.py.")
       save_game_state(DEFAULT_GAME_STATE.copy())

    # Pastikan direktori assets dan gambar-gambar ada atau skrip akan error saat load
    # Contoh: Buat direktori jika belum ada untuk pengujian
    if not os.path.exists("assets/images/background"):
        os.makedirs("assets/images/background")
        print("Created directory 'assets/images/background'. Make sure to add background images there.")
    if not os.path.exists("assets/images/icons"):
        os.makedirs("assets/images/icons")
    if not os.path.exists("assets/fonts"):
        os.makedirs("assets/fonts")
        print("Created directory 'assets/fonts'. Make sure to add font files like 'turok.ttf'.")
    if not os.path.exists("assets/audio"):
        os.makedirs("assets/audio")

    # Buat file placeholder jika tidak ada untuk menghindari error pygame.image.load atau font load
    # Anda perlu mengganti ini dengan aset game Anda yang sebenarnya
    placeholder_font_path = "assets/fonts/turok.ttf"
    if not os.path.exists(placeholder_font_path):
        # pygame.font.Font(None, size) bisa jadi alternatif jika turok.ttf tidak ada, tapi kita coba print warning
        print(f"WARNING: Font '{placeholder_font_path}' not found. Text rendering might fail or use default system font if available to Pygame.")

    placeholder_icon_path = "assets/images/icons/victory.png"
    if not os.path.exists(placeholder_icon_path):
        try:
            surf = pygame.Surface((100,100), pygame.SRCALPHA)
            pygame.draw.circle(surf, GREEN, (50,50), 40)
            pygame.image.save(surf, placeholder_icon_path)
            print(f"Created placeholder '{placeholder_icon_path}'.")
        except Exception as e:
            print(f"Could not create placeholder icon: {e}")

    placeholder_dialog_audio = "assets/audio/story_dialogue.wav"
    if not os.path.exists(placeholder_dialog_audio):
        # Membuat file wav placeholder sangat kompleks, jadi kita hanya print warning
        print(f"WARNING: Dialog audio '{placeholder_dialog_audio}' not found. Dialogs will be silent.")


    main_story(start_new_game_flag=True)
    pygame.quit()
    exit()