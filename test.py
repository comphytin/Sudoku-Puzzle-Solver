import pygame
import sys

pygame.init()
screen = pygame.display.set_mode((800, 600))
pygame.display.set_caption("Drag and Drop Example")
clock = pygame.time.Clock()

# Define a rectangle (x, y, width, height)
rect = pygame.Rect(300, 200, 150, 100)
rect_color = (0, 128, 255)

dragging = False
offset_x = 0
offset_y = 0

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        # Mouse button down
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if rect.collidepoint(event.pos):  # Check if click inside rect
                dragging = True
                # Calculate offset between rect corner and mouse click position
                mouse_x, mouse_y = event.pos
                offset_x = rect.x - mouse_x
                offset_y = rect.y - mouse_y

        # Mouse button up
        elif event.type == pygame.MOUSEBUTTONUP:
            dragging = False

        # Mouse movement
        elif event.type == pygame.MOUSEMOTION:
            if dragging:
                mouse_x, mouse_y = event.pos
                rect.x = mouse_x + offset_x
                rect.y = mouse_y + offset_y

    screen.fill((30, 30, 30))  # Background color
    pygame.draw.rect(screen, rect_color, rect)  # Draw the draggable rect
    pygame.display.flip()
    clock.tick(60)
