import pygame
import time
import os

# Define colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)

def loading_screen(screen, width, height):
    pygame.init()

    frames = []
    for i in range(1, 7):
        frame_path = f"assets/images/frames/{i}.jpg"
        if os.path.exists(frame_path):
            frames.append(pygame.image.load(frame_path))
        else:
            print(f"Error: {frame_path} not found!")

    if not frames:
        print("Error: No frames were loaded!")
        return

    frames = [pygame.transform.scale(frame, (width, height - 100)) for frame in frames]

    font = pygame.font.Font(None, 50)
    text = font.render("Loading...", True, WHITE)

    clock = pygame.time.Clock()
    frame_index = 0
    running = True
    start_time = time.time()

    while running:
        screen.fill(BLACK)

        # Display current frame
        screen.blit(frames[frame_index], (0, 0))

        # Display loading text
        text_rect = text.get_rect(center=(width // 2, height - 50))
        screen.blit(text, text_rect)

        pygame.display.flip()
        clock.tick(10) 

        frame_index = (frame_index + 1) % len(frames)  

        # Stop after 3 seconds
        if time.time() - start_time > 3:
            running = False
