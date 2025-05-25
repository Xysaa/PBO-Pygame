# save_data.py
import json
import os

SAVE_FILE = "game_save_data.json" # Stores all game progress

DEFAULT_GAME_STATE = {
    "monk_unlocked": False,
    "current_chapter": 1,       # Start at chapter 1
    "story_completed": False    # To track if the full story has been beaten
}

def load_game_state():
    """Loads game state from a JSON file."""
    if os.path.exists(SAVE_FILE):
        try:
            with open(SAVE_FILE, 'r') as f:
                saved_state = json.load(f)
                # Ensure all default keys are present in the loaded state
                # This helps with backward compatibility if new keys are added later
                updated_state = DEFAULT_GAME_STATE.copy()
                updated_state.update(saved_state) # Overwrite defaults with saved values
                return updated_state
        except json.JSONDecodeError:
            print(f"Error decoding {SAVE_FILE}. Using default game state.")
            return DEFAULT_GAME_STATE.copy()
    return DEFAULT_GAME_STATE.copy()

def save_game_state(game_state):
    """Saves game state to a JSON file."""
    try:
        with open(SAVE_FILE, 'w') as f:
            json.dump(game_state, f, indent=4)
        print(f"Game state saved: {game_state}")
    except IOError:
        print(f"Error saving game state to {SAVE_FILE}.")

def reset_story_progress():
    """Resets story-related progress to default for a new game and saves it."""
    print("Resetting story progress...")
    new_game_state = DEFAULT_GAME_STATE.copy() # Get a fresh default state
    # If you have other game settings not related to story, load existing and only reset story parts:
    # current_overall_state = load_game_state()
    # current_overall_state["monk_unlocked"] = False
    # current_overall_state["current_chapter"] = 1
    # current_overall_state["story_completed"] = False
    # save_game_state(current_overall_state)
    save_game_state(new_game_state) # For this scope, resetting all to default is fine
    return new_game_state


if __name__ == '__main__':
    # Example usage:
    if not os.path.exists(SAVE_FILE):
        print(f"{SAVE_FILE} does not exist. Initializing with default state.")
        save_game_state(DEFAULT_GAME_STATE.copy())

    state = load_game_state()
    print(f"Initial game state: {state}")

    # Simulate completing a chapter
    # state['current_chapter'] = 2
    # save_game_state(state)
    # print(f"Updated game state: {load_game_state()}")

    # Simulate resetting for a new game
    # reset_story_progress()
    # print(f"State after reset: {load_game_state()}")
