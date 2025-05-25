import pygame
from pygame import mixer
mixer.init()
pygame.init()
RED = (255, 0, 0)
YELLOW = (255, 255, 0)
WHITE = (255, 255, 255)
GREY = (200, 200, 200)
BLACK = (0, 0, 0)
GREEN = (0, 180, 0)
DARK_RED = (180, 0, 0)
DARK_BlUE = (74,84,98)

def start_battle(SCREEN_WIDTH,SCREEN_HEIGHT,screen, draw_bg, font_small, font_med, font_large,draw_health_bar, draw_text,fighter_1,fighter_2,victory_img,is_story=False):
    clock = pygame.time.Clock()
    FPS = 60

    intro_count = 3
    last_count_update = pygame.time.get_ticks()
    score = [0, 0] # Tidak digunakan di story mode, tapi tetap ada untuk free battle
    round_over = False
    ROUND_OVER_COOLDOWN = 2000 # Waktu sebelum battle berakhir setelah KO
    round_over_time = 0

    paused = False
    pause_button_rect = pygame.Rect(SCREEN_WIDTH // 2 - 40, 10, 80, 40)
    pause_text_render = font_med.render("||", True, BLACK)

    resume_text_render = font_large.render("Resume", True, WHITE)
    main_menu_text_render = font_large.render("Main Menu", True, WHITE)

    resume_button_rect = resume_text_render.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - 40))
    main_menu_button_rect = main_menu_text_render.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 40))
    
    return_to_main_menu = False
    
    try:
        pygame.mixer.music.load("assets/audio/music.mp3")
        pygame.mixer.music.set_volume(0.5)
        pygame.mixer.music.play(-1, 0.0, 5000)
    except pygame.error as e:
        print(f"Error loading battle music: {e}")

    run = True
    while run:
        clock.tick(FPS)
        mouse_pos = pygame.mouse.get_pos()
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.mixer.music.stop() # Hentikan musik jika menutup window
                # return True # Langsung keluar bisa jadi opsi, atau biarkan loop selesai
                run = False # Agar bisa return return_to_main_menu
                return_to_main_menu = True # Asumsikan keluar via X = kembali ke menu

            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    if paused:
                        if resume_button_rect.collidepoint(mouse_pos):
                            paused = False
                            pygame.mixer.music.unpause()
                        elif main_menu_button_rect.collidepoint(mouse_pos):
                            pygame.mixer.music.stop()
                            run = False
                            return_to_main_menu = True
                    else:
                        if not round_over and intro_count <= 0 and pause_button_rect.collidepoint(mouse_pos):
                            paused = True
                            pygame.mixer.music.pause()
            if event.type == pygame.KEYDOWN: # Tambahkan event keydown untuk escape dari pause
                if event.key == pygame.K_ESCAPE:
                    if paused:
                        paused = False
                        pygame.mixer.music.unpause()
                    # else: # Jika tidak dipause, escape tidak melakukan apa-apa di battle screen, kecuali dihandle di main menu
                    #     run = False # Contoh jika mau keluar dari battle dengan ESC
                    #     return_to_main_menu = True


        draw_bg()
        draw_health_bar(fighter_1.health, 20, 20)
        draw_health_bar(fighter_2.health, 580, 20)
        
        # Skor hanya relevan untuk non-story mode, tapi tidak masalah tergambar
        draw_text(f"P1: {score[0]}", font_small, RED, 20, 60)
        draw_text(f"P2: {score[1]}", font_small, RED, 580, 60)
        
        pygame.draw.rect(screen, GREY, pause_button_rect)
        screen.blit(pause_text_render, (pause_button_rect.centerx - pause_text_render.get_width() // 2,
                                         pause_button_rect.centery - pause_text_render.get_height() // 2))

        if not paused:
            if intro_count <= 0:
                fighter_1.move(SCREEN_WIDTH, SCREEN_HEIGHT, screen, fighter_2, round_over)
                fighter_2.move(SCREEN_WIDTH, SCREEN_HEIGHT, screen, fighter_1, round_over)
            else:
                draw_text(str(intro_count), font_large, RED, SCREEN_WIDTH/2 - 20, SCREEN_HEIGHT/3)
                if (pygame.time.get_ticks() - last_count_update) >= 1000:
                    intro_count -= 1
                    last_count_update = pygame.time.get_ticks()

            fighter_1.update()
            fighter_2.update()

            if not round_over:
                if not fighter_1.alive:
                    score[1] += 1 # P2 scores
                    round_over = True
                    round_over_time = pygame.time.get_ticks()
                elif not fighter_2.alive:
                    score[0] += 1 # P1 scores
                    round_over = True
                    round_over_time = pygame.time.get_ticks()
            else: # round_over is True
                # Modifikasi: Jangan tampilkan victory_img jika is_story True
                if not is_story:
                    screen.blit(victory_img, (SCREEN_WIDTH // 2 - victory_img.get_width() // 2, SCREEN_HEIGHT // 3 - victory_img.get_height() // 2)) # Center image
                
                if pygame.time.get_ticks() - round_over_time > ROUND_OVER_COOLDOWN:
                    if is_story: # Jika mode cerita, akhiri pertarungan setelah cooldown
                        run = False
                    else: # Jika mode bebas, reset untuk ronde berikutnya
                        round_over = False
                        intro_count = 3 # Reset intro count untuk ronde baru
                        # Reset fighter positions and health for a new round
                        fighter_1.reset()
                        fighter_2.reset()
        
        fighter_1.draw(screen)
        fighter_2.draw(screen)

        if paused:
            overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA)
            overlay.fill((0, 0, 0, 150)) # Transparan overlay
            screen.blit(overlay, (0, 0))

            pygame.draw.rect(screen, GREEN, resume_button_rect)
            screen.blit(resume_text_render, resume_button_rect.topleft)

            pygame.draw.rect(screen, DARK_RED, main_menu_button_rect)
            screen.blit(main_menu_text_render, main_menu_button_rect.topleft)
        
        pygame.display.update()
        
    # pygame.mixer.music.stop() # Hentikan musik setelah loop battle selesai, kecuali jika kembali ke menu utama dan musik menu berbeda
    return return_to_main_menu

if __name__ == "__main__":
    pass
