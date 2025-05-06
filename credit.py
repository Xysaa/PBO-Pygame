
import pygame

pygame.init()


screen_width = 800
screen_height = 600
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Story")


white = (255, 255, 255)
black = (0, 0, 0)
button_color = (80, 80, 80)
text_color = (200, 200, 200)


font = pygame.font.Font(None, 36)

coming_soon_text = font.render("COMING SOON", True, black)
text_rect = coming_soon_text.get_rect(center=(screen_width // 2, screen_height // 2 - 50))


back_button_width = 200
back_button_height = 50
back_button_x = screen_width // 2 - back_button_width // 2
back_button_y = screen_height - 100
back_button_rect = pygame.Rect(back_button_x, back_button_y, back_button_width, back_button_height)
back_button_text = font.render("Kembali ke Menu", True, text_color)
back_button_text_rect = back_button_text.get_rect(center=back_button_rect.center)

def jalankan_story():
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                if back_button_rect.collidepoint(event.pos):
                    print("Tombol 'Kembali ke Menu' diklik!")
                    running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False

        screen.fill(white)

        
        screen.blit(coming_soon_text, text_rect)

        pygame.draw.rect(screen, button_color, back_button_rect)
        screen.blit(back_button_text, back_button_text_rect)

        
        pygame.display.flip()

    pygame.quit() 

if __name__ == '__main__':
    jalankan_story()