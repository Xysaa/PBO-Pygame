import pygame
import os
from pygame import mixer

mixer.init()
pygame.init()

hitam = (0, 0, 0)
putih = (255, 255, 255)


font_judul = pygame.font.Font("assets/fonts/turok.ttf", 72)
font_teks_besar = pygame.font.Font("assets/fonts/turok.ttf", 60)
font_teks_kecil = pygame.font.Font("assets/fonts/turok.ttf", 30)

daftar_kredit = [
    "TERIMA KASIH TELAH BERMAIN!",
    " ",
    "Pengembang utama",
    "Daniel Calvin Simanjuntak",
    "Danang Ridho Laksono",
    "Garis Rayya Rabbani",
    "Arrauf Setiawan Muhammad Jabar",
    "Stevanus Cahya anggara",
    " ",
    "Programmer",
    "Daniel Calvin Simanjuntak",
    "Danang Ridho Laksono",
    "Garis Rayya Rabbani",
    "Arrauf Setiawan Muhammad Jabar",
    "Stevanus Cahya anggara",
    " ",
    "Designer",
    "Daniel Calvin Simanjuntak",
    "Danang Ridho Laksono",
    "Garis Rayya Rabbani",
    " ",
    "Sfx",
    "Stevanus Cahya Anggara",
    "Garis Rayya Rabbani",
    " ",
    "Copyright (c) 2025 Kebelet Production",
]


#jalankan credit 
def run_credit():
    screen_width, screen_height = 1000, 600
    screen = pygame.display.set_mode((screen_width, screen_height), pygame.RESIZABLE)
    pygame.display.set_caption("Credits with Scaled Background")

    y_kredit = screen_height

    kecepatan_gulir = 1


    try:
        background_img_original = pygame.image.load("assets/images/background/backgroundCreditScene.png").convert()
    except Exception as e:
        print(f"Error loading background image: {e}")
        background_img_original = None
    try:
        pygame.mixer.music.load("assets/audio/music_main.wav")
        pygame.mixer.music.set_volume(0.7)
        pygame.mixer.music.play(-1, 0.0, 5000)
    except pygame.error as e: print(f"Error loading main menu music: {e}")
    clock = pygame.time.Clock()

    running = True
    pause_menu = False
    while running:
        dt = clock.tick(60)  # Limit FPS to 60

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            elif event.type == pygame.VIDEORESIZE:
                screen_width, screen_height = event.w, event.h
                screen = pygame.display.set_mode((screen_width, screen_height), pygame.RESIZABLE)

           
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False

       
        if background_img_original:
            scaled_bg = pygame.transform.smoothscale(background_img_original, (screen_width, screen_height))
            screen.blit(scaled_bg, (0, 0))
        else:
            screen.fill(hitam)

    
        y_pos = y_kredit
        for teks in daftar_kredit:
            if teks:
                if daftar_kredit.index(teks) == 0:  # Judul
                    teks_render = font_judul.render(teks, True, putih)
                elif ("Pengembang" in teks or "Programmer" in teks or "Designer" in teks or "Sfx" in teks
                    or "Special Thanks To" in teks):
                    teks_render = font_teks_besar.render(teks, True, putih)
                else:
                    teks_render = font_teks_kecil.render(teks, True, putih)

                teks_rect = teks_render.get_rect(center=(screen_width // 2, int(y_pos)))
                screen.blit(teks_render, teks_rect)
                y_pos += teks_rect.height + 10

        
        y_kredit -= kecepatan_gulir

        if y_pos < 0:
            y_kredit = screen_height

        pygame.display.flip()
    
          

if __name__ == "__main__":
    run_credit()
