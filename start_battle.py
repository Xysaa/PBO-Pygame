import pygame
from pygame import mixer

# Colors
RED = (255, 0, 0)
YELLOW = (255, 255, 0)
WHITE = (255, 255, 255)
GREY = (200, 200, 200)
BLACK = (0, 0, 0)
GREEN = (0, 180, 0)
DARK_RED = (180, 0, 0)
DARK_BLUE = (74,84,98) 

# Gamepad Button Constant (from main.py or defined globally)
PAUSE_RESUME_BUTTON = 7 # Typically Start button

def start_battle(SCREEN_WIDTH,SCREEN_HEIGHT,screen, draw_bg, font_small, font_med, font_large,draw_health_bar, draw_text,fighter_1,fighter_2,victory_img,is_story=False): #
    clock = pygame.time.Clock()
    FPS = 60

    intro_count = 3
    last_count_update = pygame.time.get_ticks()
    score = [0, 0] 
    round_over = False
    ROUND_OVER_COOLDOWN = 2000 
    round_over_time = 0

    paused = False
    pause_button_rect = pygame.Rect(SCREEN_WIDTH // 2 - 40, 10, 80, 40)
    pause_text_render = font_med.render("||", True, BLACK) #

    resume_text_render = font_large.render("Resume", True, WHITE) #
    main_menu_text_render = font_large.render("Main Menu", True, WHITE) #
    resume_button_rect = resume_text_render.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - 40)) #
    main_menu_button_rect = main_menu_text_render.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 40)) #
    
    return_to_main_menu = False #
    
    game_over_fb = False  
    fb_winner_message = ""
    FB_GAME_OVER_MESSAGE_DURATION = 3000  
    fb_game_over_message_start_time = 0

    if not pygame.mixer.music.get_busy(): # Start battle music if nothing else is playing
        try:
            pygame.mixer.music.load("assets/audio/music.mp3") #
            pygame.mixer.music.set_volume(0.5) #
            pygame.mixer.music.play(-1, 0.0, 5000) #
        except pygame.error as e:
            print(f"Error loading battle music in start_battle: {e}")

    run = True
    while run:
        clock.tick(FPS)
        mouse_pos = pygame.mouse.get_pos()
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                if pygame.mixer.get_init() : pygame.mixer.music.stop() 
                run = False 
                return_to_main_menu = True 

            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1: 
                    if paused:
                        if resume_button_rect.collidepoint(mouse_pos):
                            paused = False
                            if pygame.mixer.get_init(): pygame.mixer.music.unpause() #
                        elif main_menu_button_rect.collidepoint(mouse_pos):
                            if pygame.mixer.get_init(): pygame.mixer.music.stop() #
                            run = False
                            return_to_main_menu = True
                    else: 
                        if not game_over_fb and not round_over and intro_count <= 0 and pause_button_rect.collidepoint(mouse_pos):
                            paused = True
                            if pygame.mixer.get_init(): pygame.mixer.music.pause() #
            
            if event.type == pygame.KEYDOWN: 
                if event.key == pygame.K_ESCAPE: # ESC also pauses/resumes
                    if not game_over_fb and intro_count <= 0 : # Can only pause if game is running
                        paused = not paused # Toggle pause
                        if paused:
                            if pygame.mixer.get_init(): pygame.mixer.music.pause()
                        else:
                            if pygame.mixer.get_init(): pygame.mixer.music.unpause()
            
            if event.type == pygame.JOYBUTTONDOWN:
                if event.button == PAUSE_RESUME_BUTTON: # Joystick Start button
                    if not game_over_fb and intro_count <= 0: # Can only pause if game is running
                        paused = not paused # Toggle pause
                        if paused:
                            if pygame.mixer.get_init(): pygame.mixer.music.pause()
                        else:
                            if pygame.mixer.get_init(): pygame.mixer.music.unpause()


        # --- Game Logic and Updates (only if not paused) ---
        if not paused:
            if intro_count <= 0:
                if not round_over:
                     fighter_1.move(SCREEN_WIDTH, SCREEN_HEIGHT, screen, fighter_2, round_over) #
                     fighter_2.move(SCREEN_WIDTH, SCREEN_HEIGHT, screen, fighter_1, round_over) #
            else: 
                if (pygame.time.get_ticks() - last_count_update) >= 1000:
                    intro_count -= 1
                    last_count_update = pygame.time.get_ticks()

            # fighter_1.update() #
            # fighter_2.update() #
            fighter_1.update(fighter_2) # Pass fighter_2 as target
            fighter_2.update(fighter_1) # Pass fighter_1 as target

            if not round_over: 
                if not fighter_1.alive:
                    if not is_story: score[1] += 1 
                    round_over = True; round_over_time = pygame.time.get_ticks()
                elif not fighter_2.alive:
                    if not is_story: score[0] += 1 
                    round_over = True; round_over_time = pygame.time.get_ticks()
            else: 
                if pygame.time.get_ticks() - round_over_time > ROUND_OVER_COOLDOWN: #
                    if is_story: run = False 
                    else: 
                        if score[0] >= 2: 
                            game_over_fb = True; fb_winner_message = "PLAYER 1 WINS!"
                            fb_game_over_message_start_time = pygame.time.get_ticks()
                            if pygame.mixer.get_init(): pygame.mixer.music.fadeout(1000)
                        elif score[1] >= 2: 
                            game_over_fb = True; fb_winner_message = "PLAYER 2 WINS!"
                            fb_game_over_message_start_time = pygame.time.get_ticks()
                            if pygame.mixer.get_init(): pygame.mixer.music.fadeout(1000)
                        if not game_over_fb: 
                            round_over = False; intro_count = 3 
                            fighter_1.reset() #
                            fighter_2.reset() #

        # --- Drawing ---
        draw_bg() 
        draw_health_bar(fighter_1.health, 20, 20) #
        draw_health_bar(fighter_2.health, 580, 20) #
        if not is_story:
            draw_text(f"P1: {score[0]}", font_small, RED, 20, 60) #
            draw_text(f"P2: {score[1]}", font_small, RED, 580, 60) #

        fighter_1.draw(screen) #
        fighter_2.draw(screen) #
        
        if intro_count > 0 and not paused: 
            draw_text(str(intro_count), font_large, RED, SCREEN_WIDTH/2 - font_large.size(str(intro_count))[0]/2, SCREEN_HEIGHT/3) #

        if round_over and (pygame.time.get_ticks() - round_over_time <= ROUND_OVER_COOLDOWN):
            if not is_story and not game_over_fb: 
                screen.blit(victory_img, (SCREEN_WIDTH // 2 - victory_img.get_width() // 2, SCREEN_HEIGHT // 3 - victory_img.get_height() // 2)) #

        if paused:
            overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA)
            overlay.fill((0, 0, 0, 150)) 
            screen.blit(overlay, (0, 0))
            pygame.draw.rect(screen, GREEN, resume_button_rect) #
            screen.blit(resume_text_render, resume_button_rect.topleft) #
            pygame.draw.rect(screen, DARK_RED, main_menu_button_rect) #
            screen.blit(main_menu_text_render, main_menu_button_rect.topleft) #
        
        elif game_over_fb and not is_story: 
            winner_text_surf = font_large.render(fb_winner_message, True, YELLOW) #
            winner_text_rect = winner_text_surf.get_rect(center=(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 3)) #
            screen.blit(winner_text_surf, winner_text_rect) #
            if pygame.time.get_ticks() - fb_game_over_message_start_time > FB_GAME_OVER_MESSAGE_DURATION: #
                run = False 

        pygame.draw.rect(screen, GREY, pause_button_rect) #
        screen.blit(pause_text_render, (pause_button_rect.centerx - pause_text_render.get_width() // 2,
                                         pause_button_rect.centery - pause_text_render.get_height() // 2)) #
        
        pygame.display.update()
        
    return return_to_main_menu

if __name__ == "__main__":
    pass
