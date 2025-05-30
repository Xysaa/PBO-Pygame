import pygame

# Data karakter

CHARACTER_DATA = {
    "warrior": {
        "size": [288, 128],
        "scale": 3,
        "offset": [125, 50],
        "animation_steps": [8, 8, 26, 11, 19, 18, 6, 13],
        "sound_path": "assets/audio/sword.wav",
        "image_path": "assets/images/fire_warrior/fireWar_spritesheets1.png",
        "face_path" : "assets/images/fire_warrior/face.png"
    },
    "goblin": {
        "size": [150, 150],
        "scale": 3,
        "offset": [50, 20],
        "animation_steps": [4, 8, 8, 4, 4],
        "sound_path": "assets/audio/sword.wav",
        "image_path": "assets/images/Goblin/goblin.png",
    },
    "golem": {
        "size": [90, 64],
        "scale": 4,
        "offset": [10, 7],
        "animation_steps": [8, 10, 11, 4, 12],
        "sound_path": "assets/audio/sword.wav",
        "image_path": "assets/images/golem/golem.png",
    },
    "skeleton": {
        "size": [150, 150],
        "scale": 3,
        "offset": [50, 20],
        "animation_steps": [4, 4, 8, 4, 4],
        "sound_path": "assets/audio/sword.wav",
        "image_path": "assets/images/Skeleton/skeleton.png",
    },
    "assasin": {
        "size": [288, 128],
        "scale": 3,
        "offset": [125, 50],
        "animation_steps": [8,8,6,8,18,30,6,19],
        "sound_path": "assets/audio/assasin.mpeg",
        "image_path": "assets/images/assasin/assasin_sprites.png",
        "face_path" : "assets/images/assasin/face.png"
    },

    "monk": {
        "size": [288, 128],
        "scale": 4,
        "offset": [125, 63],
        "animation_steps": [6,8,6,6,9,25,6,18],
        "sound_path": "assets/audio/monk.wav",
        "image_path": "assets/images/monk/monk_spritesheets.png",
        "face_path" : "assets/images/monk/face.png"
    },

}

