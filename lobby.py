import pygame

# Screen dimensions
WIDTH, HEIGHT = 850, 600

background = pygame.image.load("assets/images/11.png")  # Background for the lobby
character_1 = pygame.image.load("assets/images/character.gif")  # First character
character_2 = pygame.image.load("assets/images/alien.gif")  # Second character

# size ng characters
CHARACTER_SIZE = (200, 200)
character_1 = pygame.transform.scale(character_1, CHARACTER_SIZE)
character_2 = pygame.transform.scale(character_2, CHARACTER_SIZE)

# Character attributes speed at power ng character
characters = {
    "character_1": {"name": "Space Hero", "speed": 5, "power": 7},
    "character_2": {"name": "Alien Warrior", "speed": 7, "power": 5}
}

def draw_button(screen, text, x, y, width, height, color, hover_color, font):
    """Draws a button and detects hover effect."""
    mouse_x, mouse_y = pygame.mouse.get_pos()
    button_rect = pygame.Rect(x, y, width, height)

    if button_rect.collidepoint(mouse_x, mouse_y):
        pygame.draw.rect(screen, hover_color, button_rect)
    else:
        pygame.draw.rect(screen, color, button_rect)

    text_surf = font.render(text, True, (255, 255, 255))
    screen.blit(text_surf, (x + (width - text_surf.get_width()) // 2, y + (height - text_surf.get_height()) // 2))

    return button_rect

def character_lobby(screen):
    """Displays the character selection lobby."""
    font = pygame.font.Font(None, 40)  
    stat_font = pygame.font.Font(None, 25) 
    WHITE = (255, 255, 255)
    BLUE = (0, 0, 255)
    LIGHT_BLUE = (100, 100, 255)

    running = True
    selected_character = None

    while running:
        screen.blit(background, (0, 0))

        # Adjusted positions for characters
        char1_x, char1_y = 200, HEIGHT // 3 - 100
        char2_x, char2_y = WIDTH - 400, HEIGHT // 3 - 100

        screen.blit(character_1, (char1_x, char1_y))
        screen.blit(character_2, (char2_x, char2_y))

        # Adjusted positioning for character descriptions
        char1_text = stat_font.render(f"{characters['character_1']['name']}", True, WHITE)
        char1_stats = stat_font.render(f"Speed: {characters['character_1']['speed']}  Power: {characters['character_1']['power']}", True, WHITE)

        char2_text = stat_font.render(f"{characters['character_2']['name']}", True, WHITE)
        char2_stats = stat_font.render(f"Speed: {characters['character_2']['speed']}  Power: {characters['character_2']['power']}", True, WHITE)

        screen.blit(char1_text, (char1_x + (CHARACTER_SIZE[0] // 2 - char1_text.get_width() // 2), char1_y + CHARACTER_SIZE[1] + 10))
        screen.blit(char1_stats, (char1_x + (CHARACTER_SIZE[0] // 2 - char1_stats.get_width() // 2), char1_y + CHARACTER_SIZE[1] + 35))

        screen.blit(char2_text, (char2_x + (CHARACTER_SIZE[0] // 2 - char2_text.get_width() // 2), char2_y + CHARACTER_SIZE[1] + 10))
        screen.blit(char2_stats, (char2_x + (CHARACTER_SIZE[0] // 2 - char2_stats.get_width() // 2), char2_y + CHARACTER_SIZE[1] + 35))

        # Buttons for selecting characters
        char1_button = draw_button(screen, "Select", char1_x + 25, char1_y + CHARACTER_SIZE[1] + 60, 150, 50, BLUE, LIGHT_BLUE, font)
        char2_button = draw_button(screen, "Select", char2_x + 25, char2_y + CHARACTER_SIZE[1] + 60, 150, 50, BLUE, LIGHT_BLUE, font)

        pygame.display.flip()

        # Event handling
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                mouse_x, mouse_y = pygame.mouse.get_pos()
                if char1_button.collidepoint(mouse_x, mouse_y):
                    selected_character = characters["character_1"]
                    running = False  # Exit lobby
                elif char2_button.collidepoint(mouse_x, mouse_y):
                    selected_character = characters["character_2"]
                    running = False  # Exit lobby

    return selected_character
