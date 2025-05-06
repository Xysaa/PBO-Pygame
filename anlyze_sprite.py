import pygame
import sys

pygame.init()

# Set up display
screen = pygame.display.set_mode((800, 600))
pygame.display.set_caption("Sprite Sheet Analyzer")

# Load the sprite sheet
try:
    sprite_sheet = pygame.image.load("assets/images/warrior/Sprites/warrior.png").convert_alpha()
    print(f"Successfully loaded sprite sheet")
    print(f"Sprite sheet dimensions: {sprite_sheet.get_width()}x{sprite_sheet.get_height()}")
except Exception as e:
    print(f"Error loading sprite sheet: {e}")
    pygame.quit()
    sys.exit()

# Let's try different sizes to see which one works
test_sizes = [32, 48, 50, 60, 64, 80, 100, 120, 150, 162, 180, 200]
animation_steps = [10, 8, 1, 7, 7, 3, 7]

def test_sprite_extraction(size):
    print(f"\nTesting with frame size: {size}x{size}")
    success_count = 0
    fail_count = 0
    
    for y, steps in enumerate(animation_steps):
        for x in range(steps):
            try:
                # Calculate coordinates
                x_pos = x * size
                y_pos = y * size
                
                # Check if these coordinates are within the sprite sheet
                if (x_pos + size <= sprite_sheet.get_width() and 
                    y_pos + size <= sprite_sheet.get_height()):
                    # Try to extract subsurface
                    temp_img = sprite_sheet.subsurface(x_pos, y_pos, size, size)
                    success_count += 1
                else:
                    print(f"  Position out of bounds: ({x_pos}, {y_pos}) with size {size}")
                    fail_count += 1
            except Exception as e:
                print(f"  Error extracting frame at ({x}, {y}): {e}")
                fail_count += 1
    
    print(f"Results for size {size}: {success_count} successes, {fail_count} failures")
    return success_count, fail_count

# Test all sizes
best_size = None
max_success = -1

for size in test_sizes:
    success, fail = test_sprite_extraction(size)
    if success > max_success and fail == 0:
        max_success = success
        best_size = size

if best_size:
    print(f"\nRecommended size: {best_size}")
    print(f"Suggested configuration:")
    print(f"WARRIOR_SIZE = {best_size}")
    print(f"WARRIOR_SCALE = 3  # Adjust as needed")
    print(f"WARRIOR_OFFSET = [22, 16]  # May need adjustment")
    print(f"WARRIOR_DATA = [WARRIOR_SIZE, WARRIOR_SCALE, WARRIOR_OFFSET]")
    print(f"WARRIOR_ANIMATION_STEPS = {animation_steps}")
else:
    print("\nCould not determine optimal size, try manual inspection")

# Main loop to keep window open
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    
    # Display the sprite sheet
    screen.fill((0, 0, 0))
    screen.blit(sprite_sheet, (50, 50))
    pygame.display.flip()

pygame.quit()
