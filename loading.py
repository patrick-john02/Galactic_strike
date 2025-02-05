import pygame
import time

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

WIDTH, HEIGHT = 800, 490

pygame.init()
font = pygame.font.Font(None, 40)

def loading_screen(screen):
    screen.fill(BLACK)
    screen.blit(pygame.image.load("assets/images/bb.gif"), (0, 0)) #background image ng loading screen

    text = font.render("Loading...", True, WHITE)
    screen.blit(text, (WIDTH // 2 - 50, HEIGHT // 2))  
    pygame.display.flip()

    time.sleep(2)  # Simulate loading time
