
# character_assets.py
import pygame
from character_data import CHARACTER_DATA

def load_character_assets():
    assets = {}
    for name, data in CHARACTER_DATA.items():
        try:
            image = pygame.image.load(data["image_path"]).convert_alpha()
        except pygame.error as e:
            print(f"Error loading image for {name} at {data['image_path']}: {e}")
            # Anda mungkin ingin menggunakan placeholder image jika gagal load
            image = pygame.Surface((50,50)); image.fill((255,0,255)) # Magenta placeholder

        try:
            sound = pygame.mixer.Sound(data["sound_path"])
            if "sword" in data["sound_path"]: #
                sound.set_volume(0.5) #
            else:
                sound.set_volume(0.75) #
        except pygame.error as e:
            print(f"Error loading sound for {name} at {data['sound_path']}: {e}")
            # Anda mungkin ingin menggunakan placeholder sound
            sound = None # Atau objek sound dummy

        face_surface = None
        if "face_path" in data and data["face_path"]:
            try:
                face_surface = pygame.image.load(data["face_path"]).convert_alpha()
            except pygame.error as e:
                print(f"Warning: Could not load face for {name} from {data['face_path']}: {e}")
                face_surface = None # Fallback jika gagal load
        
        assets[name] = {
            "image": image,
            "sound": sound,
            "face": face_surface # Menambahkan surface wajah ke assets
        }
    return assets
