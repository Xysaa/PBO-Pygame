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
    score = [0, 0] # Skor untuk P1 dan P2
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
    
    # Variabel untuk akhir game di Free Battle
    game_over_fb = False  # fb singkatan dari Free Battle
    fb_winner_message = ""
    FB_GAME_OVER_MESSAGE_DURATION = 3000  # Durasi pesan game over ditampilkan (ms)
    fb_game_over_message_start_time = 0

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
                pygame.mixer.music.stop() 
                run = False 
                return_to_main_menu = True 

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
                    else: # Hanya bisa pause jika tidak game over dan intro selesai
                        if not game_over_fb and not round_over and intro_count <= 0 and pause_button_rect.collidepoint(mouse_pos):
                            paused = True
                            pygame.mixer.music.pause()
            if event.type == pygame.KEYDOWN: 
                if event.key == pygame.K_ESCAPE:
                    if paused:
                        paused = False
                        pygame.mixer.music.unpause()
                    


        draw_bg()
        draw_health_bar(fighter_1.health, 20, 20)
        draw_health_bar(fighter_2.health, 580, 20)
        
        if not is_story: # Hanya tampilkan skor di mode Free Battle
            draw_text(f"P1: {score[0]}", font_small, RED, 20, 60)
            draw_text(f"P2: {score[1]}", font_small, RED, 580, 60)
        
        # Tombol Pause selalu bisa digambar, tapi fungsionalitasnya dibatasi
        pygame.draw.rect(screen, GREY, pause_button_rect)
        screen.blit(pause_text_render, (pause_button_rect.centerx - pause_text_render.get_width() // 2,
                                         pause_button_rect.centery - pause_text_render.get_height() // 2))

        if paused:
            overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA)
            overlay.fill((0, 0, 0, 150)) 
            screen.blit(overlay, (0, 0))
            pygame.draw.rect(screen, GREEN, resume_button_rect)
            screen.blit(resume_text_render, resume_button_rect.topleft)
            pygame.draw.rect(screen, DARK_RED, main_menu_button_rect)
            screen.blit(main_menu_text_render, main_menu_button_rect.topleft)
        
        elif game_over_fb and not is_story: # Kondisi Game Over untuk Free Battle
            # Tampilkan pesan pemenang
            winner_text_surf = font_large.render(fb_winner_message, True, YELLOW)
            winner_text_rect = winner_text_surf.get_rect(center=(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 3))
            screen.blit(winner_text_surf, winner_text_rect)
            
            if pygame.time.get_ticks() - fb_game_over_message_start_time > FB_GAME_OVER_MESSAGE_DURATION:
                run = False # Akhiri loop pertarungan
        
        else: # Game belum berakhir (intro, pertarungan aktif, atau cooldown ronde)
            if intro_count <= 0:
                # Hanya gerakkan fighter jika ronde belum berakhir (KO)
                if not round_over:
                     fighter_1.move(SCREEN_WIDTH, SCREEN_HEIGHT, screen, fighter_2, round_over)
                     fighter_2.move(SCREEN_WIDTH, SCREEN_HEIGHT, screen, fighter_1, round_over)
            else: # Hitung mundur intro
                draw_text(str(intro_count), font_large, RED, SCREEN_WIDTH/2 - font_large.size(str(intro_count))[0]/2, SCREEN_HEIGHT/3)
                if (pygame.time.get_ticks() - last_count_update) >= 1000:
                    intro_count -= 1
                    last_count_update = pygame.time.get_ticks()

            # Update fighter (animasi, dll.) selalu dilakukan kecuali game sudah benar-benar berakhir dan pesan ditampilkan
            fighter_1.update()
            fighter_2.update()

            if not round_over: # Jika ronde masih berjalan, cek KO
                if not fighter_1.alive:
                    if not is_story: score[1] += 1 # Skor P2 bertambah
                    round_over = True
                    round_over_time = pygame.time.get_ticks()
                elif not fighter_2.alive:
                    if not is_story: score[0] += 1 # Skor P1 bertambah
                    round_over = True
                    round_over_time = pygame.time.get_ticks()
            else: # round_over == True (seseorang KO di ronde ini)
                if pygame.time.get_ticks() - round_over_time > ROUND_OVER_COOLDOWN:
                    if is_story:
                        run = False # Mode cerita berakhir setelah 1 KO dan cooldown
                    else: # Mode Free Battle
                        # Cek apakah ada pemenang game
                        if score[0] >= 2:
                            game_over_fb = True
                            fb_winner_message = "PLAYER 1 WINS!"
                            fb_game_over_message_start_time = pygame.time.get_ticks()
                            pygame.mixer.music.fadeout(1000) # Matikan musik pelan-pelan
                        elif score[1] >= 2:
                            game_over_fb = True
                            fb_winner_message = "PLAYER 2 WINS!"
                            fb_game_over_message_start_time = pygame.time.get_ticks()
                            pygame.mixer.music.fadeout(1000) # Matikan musik pelan-pelan
                        
                        if not game_over_fb: # Jika game belum selesai, reset untuk ronde berikutnya
                            round_over = False
                            intro_count = 3 
                            fighter_1.reset()
                            fighter_2.reset()
                else: # Masih dalam ROUND_OVER_COOLDOWN
                    # Tampilkan gambar kemenangan ronde hanya jika bukan mode cerita dan game belum berakhir
                    if not is_story and not game_over_fb: 
                        screen.blit(victory_img, (SCREEN_WIDTH // 2 - victory_img.get_width() // 2, SCREEN_HEIGHT // 3 - victory_img.get_height() // 2))
        
        # Gambar fighter di semua kondisi (kecuali mungkin saat pause menu menutupi penuh)
        fighter_1.draw(screen)
        fighter_2.draw(screen)
        
        pygame.display.update()
        
    return return_to_main_menu

if __name__ == "__main__":
    pass
