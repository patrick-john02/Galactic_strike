import pygame

#colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY = (200, 200, 200)
GREEN = (0, 255, 0) 

def draw_circle_button(screen, text, x, y, radius, color, hover_color, font):
    mouse = pygame.mouse.get_pos()
    click = pygame.mouse.get_pressed()
    
    distance = ((mouse[0] - x) ** 2 + (mouse[1] - y) ** 2) ** 0.5
    if distance < radius:
        pygame.draw.circle(screen, hover_color, (x, y), radius)
        if click[0]:  
            return True
    else:
        pygame.draw.circle(screen, color, (x, y), radius)

    text_surface = font.render(text, True, BLACK)
    text_rect = text_surface.get_rect(center=(x, y))
    screen.blit(text_surface, text_rect)
    return False

def lobby_screen(screen, width, height):
    pygame.init()
    
    # Load assets
    bg = pygame.image.load("assets/images/11.png")  
    hero1 = pygame.image.load("assets/blaster/char/sprites/ship.png")
    hero2 = pygame.image.load("assets/blaster/char/sprites/enemy_kamikaze.png")
    villain = pygame.image.load("assets/blaster/char/sprites/enemy_clever.png")
    
    hero1 = pygame.transform.scale(hero1, (150, 200))
    hero2 = pygame.transform.scale(hero2, (150, 200))
    villain = pygame.transform.scale(villain, (200, 250))

    # Character Positions
    hero1_rect = hero1.get_rect(topleft=(50, height//2 - 100))
    hero2_rect = hero2.get_rect(topleft=(250, height//2 - 100))
    villain_rect = villain.get_rect(topleft=(width - 250, height//2 - 125))

    font = pygame.font.Font(None, 40)
    title_font = pygame.font.Font(None, 50)
    selected_character = None  
    running = True
    while running:
        screen.blit(bg, (0, 0))  

        #Title
        title_surface = title_font.render("Click what character do you want", True, WHITE)
        title_rect = title_surface.get_rect(center=(width // 2, 50))
        screen.blit(title_surface, title_rect)

        if selected_character == "hero1":
            pygame.draw.rect(screen, GREEN, hero1_rect.inflate(10, 10), 5)
        if selected_character == "hero2":
            pygame.draw.rect(screen, GREEN, hero2_rect.inflate(10, 10), 5)

        screen.blit(hero1, hero1_rect.topleft)
        screen.blit(hero2, hero2_rect.topleft)
        screen.blit(villain, villain_rect.topleft)

        #Character Names
        hero1_text = font.render("Spaceship", True, WHITE)
        hero1_text_rect = hero1_text.get_rect(center=(hero1_rect.centerx, hero1_rect.bottom + 20))
        screen.blit(hero1_text, hero1_text_rect)

        hero2_text = font.render("Rocket", True, WHITE)
        hero2_text_rect = hero2_text.get_rect(center=(hero2_rect.centerx, hero2_rect.bottom + 20))
        screen.blit(hero2_text, hero2_text_rect)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if hero1_rect.collidepoint(event.pos):
                    selected_character = "hero1"
                elif hero2_rect.collidepoint(event.pos):
                    selected_character = "hero2"

        if draw_circle_button(screen, "Start", width // 2 - 150, height - 100, 50, GRAY, WHITE, font):
            if selected_character:
                return selected_character  
        if draw_circle_button(screen, "Options", width // 2, height - 100, 50, GRAY, WHITE, font):
            print("Options Menu!")  
        if draw_circle_button(screen, "Exit", width // 2 + 150, height - 100, 50, GRAY, WHITE, font):
            pygame.quit()
            exit()

        pygame.display.flip()