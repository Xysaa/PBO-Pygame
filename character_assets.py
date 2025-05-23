
import pygame
from character_data import CHARACTER_DATA

def load_character_assets():
    assets = {}
    for name, data in CHARACTER_DATA.items():
        image = pygame.image.load(data["image_path"]).convert_alpha()
        sound = pygame.mixer.Sound(data["sound_path"])
        if "sword" in data["sound_path"]:
            sound.set_volume(0.5)
        else:
            sound.set_volume(0.75)
        assets[name] = {
            "image": image,
            "sound": sound
        }
    return assets
