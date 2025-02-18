# Initialize Pygame
import pygame
pygame.init()

# Screen dimensions
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Text Opacity")

# Font and text
font = pygame.font.Font(None, 74)  # Default font with size 74
text = font.render("Hello, Pygame!", True, (255, 255, 255))  # Rendered text in white
text_rect = text.get_rect(center=(WIDTH // 2, HEIGHT // 2))  # Center the text

# Create a surface for the text
text_surface = pygame.Surface(text.get_size(), pygame.SRCALPHA)  # Support transparency
text_surface.blit(text, (0, 0))  # Draw the text onto the surface

# Initial opacity
opacity = 255

# Clock for frame rate
clock = pygame.time.Clock()

fade_speed = 2
fade_out = True

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:  # Increase opacity
                opacity = min(opacity + 10, 255)
            elif event.key == pygame.K_DOWN:  # Decrease opacity
                opacity = max(opacity - 10, 0)

    # Set the opacity of the text surface
    text_surface.set_alpha(opacity)

    # Fill the screen with a background color
    screen.fill((30, 30, 30))

    # Inside the main loop
    if fade_out:
        opacity -= fade_speed
        if opacity <= 0:
            fade_out = False
    else:
        opacity += fade_speed
        if opacity >= 255:
            fade_out = True

    # Blit the text surface onto the screen
    screen.blit(text_surface, text_rect.topleft)

    # Update the display
    pygame.display.flip()
    clock.tick(60)  # Limit to 60 FPS

pygame.quit()