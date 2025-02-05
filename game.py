import pygame
import random
import time
import lobby

# Screen dimensions
WIDTH, HEIGHT = 850, 600

# Define colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

# loading screens
background_frames = [
    pygame.image.load("assets/images/frames/1.jpg"),
    pygame.image.load("assets/images/frames/2.jpg"),
    pygame.image.load("assets/images/frames/3.jpg"),
    pygame.image.load("assets/images/frames/4.jpg"),
    pygame.image.load("assets/images/frames/5.jpg")
]

# main menu background
main_menu_bg = pygame.image.load("assets/images/11.png")

# pictures ng mga characters bida and yung alien
space_character = pygame.image.load("assets/images/character.gif")
alien_villain = pygame.image.load("assets/images/alien.gif")

# size ng mga images (di pa final)
SPACE_CHARACTER_SIZE = (200, 200)
ALIEN_VILLAIN_SIZE = (200, 200)
space_character = pygame.transform.scale(space_character, SPACE_CHARACTER_SIZE)
alien_villain = pygame.transform.scale(alien_villain, ALIEN_VILLAIN_SIZE)

# Player and Bullet setup (medyo di pa refined pero gumagana naman na)
class Bullet(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.Surface((10, 20))
        self.image.fill(WHITE)
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)

    def update(self):
        self.rect.y -= 10 
        if self.rect.bottom < 0: 
            self.kill()

class Player(pygame.sprite.Sprite):
    def __init__(self, character_image):
        super().__init__()
        self.image = character_image
        self.rect = self.image.get_rect()
        self.rect.center = (WIDTH // 2, HEIGHT - 190)  


    def update(self, keys):
        speed = 5
        if keys[pygame.K_LEFT] and self.rect.left > 0:
            self.rect.x -= speed
        if keys[pygame.K_RIGHT] and self.rect.right < WIDTH:
            self.rect.x += speed

def show_loading_screen(screen):
    WHITE = (255, 255, 255)
    font = pygame.font.Font(None, 50)
    clock = pygame.time.Clock()

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        for bg_frame in background_frames:
            screen.blit(bg_frame, (0, 0))
            title_text = font.render("Loading...", True, WHITE)
            screen.blit(title_text, (WIDTH // 2 - title_text.get_width() // 2, HEIGHT // 6))
            pygame.display.flip()
            clock.tick(5)

    show_main_menu(screen)

def show_main_menu(screen):
    font = pygame.font.Font(None, 50)
    button_font = pygame.font.Font(None, 40)
    WHITE = (255, 255, 255)
    BLUE = (0, 0, 255)
    LIGHT_BLUE = (100, 100, 255)

    screen.blit(main_menu_bg, (0, 0))
    title_text = font.render("Galactic Strike", True, WHITE)
    screen.blit(title_text, (WIDTH // 2 - title_text.get_width() // 2, HEIGHT // 6))
    screen.blit(space_character, (50, HEIGHT // 3 - space_character.get_height() // 2))
    screen.blit(alien_villain, (WIDTH - alien_villain.get_width() - 50, HEIGHT // 3 - alien_villain.get_height() // 2))

    play_button = draw_button(screen, "Play", 100, HEIGHT // 2 + 100, 200, 50, BLUE, LIGHT_BLUE, button_font)
    task_button = draw_button(screen, "Task", 325, HEIGHT // 2 + 100, 200, 50, BLUE, LIGHT_BLUE, button_font)
    options_button = draw_button(screen, "Options", 550, HEIGHT // 2 + 100, 200, 50, BLUE, LIGHT_BLUE, button_font)

    pygame.display.flip()
    return play_button, task_button, options_button

def draw_button(screen, text, x, y, width, height, color, hover_color, font):
    mouse_x, mouse_y = pygame.mouse.get_pos()
    button_rect = pygame.Rect(x, y, width, height)

    if button_rect.collidepoint(mouse_x, mouse_y):
        pygame.draw.rect(screen, hover_color, button_rect)
    else:
        pygame.draw.rect(screen, color, button_rect)

    text_surf = font.render(text, True, (255, 255, 255))
    screen.blit(text_surf, (x + (width - text_surf.get_width()) // 2, y + (height - text_surf.get_height()) // 2))

    return button_rect

def start_game(screen, selected_character):
    player = Player(selected_character)
    player_group = pygame.sprite.Group()
    player_group.add(player)
    bullets = pygame.sprite.Group()

    # mga red na enemies
    alien_group = pygame.sprite.Group()
    for _ in range(5):  # Add 5 enemies
        alien = pygame.sprite.Sprite()
        alien.image = pygame.Surface((50, 50))
        alien.image.fill((255, 0, 0))  # Red alien
        alien.rect = alien.image.get_rect()
        alien.rect.x = random.randint(0, WIDTH - 50)
        alien.rect.y = random.randint(-100, -50)
        alien_group.add(alien)

    clock = pygame.time.Clock()
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        keys = pygame.key.get_pressed()
        player_group.update(keys)

        # Shoot trigger
        if keys[pygame.K_SPACE]:
            bullet = Bullet(player.rect.centerx, player.rect.top)
            bullets.add(bullet)
        bullets.update()

        # colission logics ng mga bullets at aliens
        for alien in alien_group:
            alien.rect.y += 2  # Move alien downward
            if alien.rect.top > HEIGHT:
                alien.rect.y = random.randint(-100, -50)
                alien.rect.x = random.randint(0, WIDTH - 50)

        # also here
        for bullet in bullets:
            hit_aliens = pygame.sprite.spritecollide(bullet, alien_group, True)
            if hit_aliens:
                bullet.kill()

        screen.fill(BLACK)
        player_group.draw(screen)
        bullets.draw(screen)
        alien_group.draw(screen)

        pygame.display.flip()
        clock.tick(60)

    pygame.quit()

def run_game(screen):
    selected_character = lobby.character_lobby(screen)
    print(f"Selected Character: {selected_character['name']}")
    start_game(screen, space_character)

if __name__ == "__main__":
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    show_loading_screen(screen)
    run_game(screen)
