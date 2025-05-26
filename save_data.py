# save_data.py
import json
import os

SAVE_FILE = "game_save_data.json" 

DEFAULT_GAME_STATE = {
    "monk_unlocked": False,
    "current_chapter": 1,       
    "story_completed": False    
}

def load_game_state():
    if os.path.exists(SAVE_FILE):
        try:
            with open(SAVE_FILE, 'r') as f:
                saved_state = json.load(f)
                updated_state = DEFAULT_GAME_STATE.copy()
                updated_state.update(saved_state) 
                return updated_state
        except json.JSONDecodeError:
            print(f"Error decoding {SAVE_FILE}. Using default game state.")
            return DEFAULT_GAME_STATE.copy()
    return DEFAULT_GAME_STATE.copy()

def save_game_state(game_state):
    try:
        with open(SAVE_FILE, 'w') as f:
            json.dump(game_state, f, indent=4)
        print(f"Game state saved: {game_state}")
    except IOError:
        print(f"Error saving game state to {SAVE_FILE}.")

def reset_story_progress():
    print("Resetting story progress...")
    new_game_state = DEFAULT_GAME_STATE.copy()
    save_game_state(new_game_state) 
    return new_game_state


if __name__ == '__main__':
   
    if not os.path.exists(SAVE_FILE):
        print(f"{SAVE_FILE} does not exist. Initializing with default state.")
        save_game_state(DEFAULT_GAME_STATE.copy())

    state = load_game_state()
    print(f"Initial game state: {state}")

   
