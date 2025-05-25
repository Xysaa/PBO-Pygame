import pygame
import story
import freebattle
import credit
pygame.init()

# Ukuran awal jendela
def main_menu():
    screen_width= 1000
    screen_height = 600
    screen = pygame.display.set_mode((screen_width, screen_height), pygame.RESIZABLE)
    pygame.display.set_caption("Menu Utama")

    try:
        background_image = pygame.image.load("assets/images/background/background_main_menu.jpeg").convert()
    except pygame.error as e:
        print(f"Error loading background image: {e}")
        background_color = (50, 50, 50)
        background_image = pygame.Surface((screen_width, screen_height))
        background_image.fill(background_color)

    fullscreen = False

    button_data = [
        {"text": "LORE OF THE CHOSEN", "x": 258.75, "y": 305, "width": 393.75, "height": 40, "action": "story"},
        {"text": "FREE BATTLE", "x": 258.75, "y": 375, "width": 393.75, "height": 40, "action": "free_battle"},
        {"text": "CREDITS", "x": 258.75, "y": 445, "width": 393.75, "height": 40, "action": "credits"},
        {"text": "EXIT", "x": 258.75, "y": 515, "width": 393.75, "height": 40, "action": "exit"}
    ]

    buttons = []
    for data in button_data:
        rect = pygame.Rect(data["x"], data["y"], data["width"], data["height"])
        buttons.append({"rect": rect, "action": data["action"]})

# Loop utama
    running = True
    while running:
        
        for event in pygame.event.get():
            pygame.mixer_music.stop()
            if event.type == pygame.QUIT:
                
                running = False
            
            if event.type == pygame.VIDEORESIZE:
                lebar_layar, tinggi_layar = event.size
                screen = pygame.display.set_mode((lebar_layar, tinggi_layar), pygame.RESIZABLE)
                skala_x = lebar_layar / screen_width
                skala_y = tinggi_layar / screen_height
                buttons = []
                
                for data in button_data:
                    rect = pygame.Rect(int(data["x"] * skala_x), int(data["y"] * skala_y),
                                    int(data["width"] * skala_x), int(data["height"] * skala_y))
                    buttons.append({"rect": rect, "action": data["action"]})

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_F11:
                    fullscreen = not fullscreen
                    if fullscreen:
                        screen = pygame.display.set_mode((pygame.display.Info().current_w, pygame.display.Info().current_h), pygame.FULLSCREEN)
                    else:
                        screen = pygame.display.set_mode((screen_width, screen_height), pygame.RESIZABLE)

                
            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = event.pos
                for button in buttons:
                    if button["rect"].collidepoint(mouse_pos):
                        if button["action"] == "story":
                            # pygame.mixer_music.play(-1)
                            story.main_story()  # Memanggil fungsi main_story dari modul story
                        if button["action"] == "free_battle":
                            pygame.mixer_music.play(-1)
                            freebattle.start_battle() # Memanggil fungsi main dari modul freebattle
                        elif button["action"] == "credits":
                            credit.run_credit()      # Memanggil fungsi main dari modul credit
                        elif button["action"] == "exit":
                            running = False
        scaled_background = pygame.transform.scale(background_image, (screen.get_width(), screen.get_height()))
        screen.blit(scaled_background, (0, 0))

        pygame.display.flip()
if __name__ == "__main__":
    main_menu()
# Keluar dari Pygame
pygame.quit()
