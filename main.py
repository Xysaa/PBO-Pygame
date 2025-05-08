import pygame
import subprocess


pygame.init()


screen_width = 800
screen_height = 600
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Menu Utama")


try:
    background_image = pygame.image.load("assets/images/background/background_main_menu.jpeg").convert()
    background_image = pygame.transform.scale(background_image, (screen_width, screen_height))
   
except pygame.error as e:
    print(f"Error loading background image: {e}")
    background_color = (50, 50, 50)
    background_image = pygame.Surface((screen_width, screen_height))
    background_image.fill(background_color)


button_data = [
    {"text": "LORE OF THE CHOSEN", "x": 207, "y": 305, "width": 315, "height": 40, "action": "story"},
    {"text": "FREE BATTLE", "x": 207, "y": 375, "width": 315, "height": 40, "action": "free_battle"},
    {"text": "CREDITS", "x": 207, "y": 445, "width": 315, "height": 40, "action": "credits"},
    {"text": "EXIT", "x": 207, "y": 515, "width": 315, "height": 40, "action": "exit"}
]

buttons = []
for data in button_data:
    rect = pygame.Rect(data["x"], data["y"], data["width"], data["height"])
    buttons.append({"rect": rect, "action": data["action"]})

# Loop utama
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.MOUSEBUTTONDOWN:
            mouse_pos = event.pos
            for button in buttons:
                if button["rect"].collidepoint(mouse_pos):
                    print(f"Tombol dengan aksi '{button['action']}' diklik!")
                    if button["action"] == "story":
                        try:
                            subprocess.Popen(["python", "story.py"])
                            
                        except FileNotFoundError:
                            print("Error: File 'story.py' tidak ditemukan!")
                        except Exception as e:
                            print(f"Error menjalankan 'story.py': {e}")
                    elif button["action"] == "free_battle":
                        try:
                            subprocess.Popen(["python", "freebattle.py"])
                            # JANGAN SET running = False DI SINI
                        except FileNotFoundError:
                            print("Error: File 'freebattle.py' tidak ditemukan!")
                        except Exception as e:
                            print(f"Error menjalankan 'freebattle.py': {e}")
                    elif button["action"] == "credits":
                        try:
                            subprocess.Popen(["python", "credit.py"])
                            
                        except FileNotFoundError:
                            print("Error: File 'credit.py' tidak ditemukan!")
                        except Exception as e:
                            print(f"Error menjalankan 'credit.py': {e}")
                    elif button["action"] == "exit":
                        running = False


    screen.blit(background_image, (0, 0))

    
    pygame.display.flip()

# Keluar dari Pygame

