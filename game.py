import pygame
import random
import time

# Initialize pygame
pygame.init()

# Screen dimensions
WIDTH, HEIGHT = 850, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Galactic Strike")

# Define colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)

# Load assets
background = pygame.image.load("assets/images/11.png")
space_character = pygame.image.load("assets/images/spaceship.png")
alien_villain = pygame.image.load("assets/images/alien.gif")

# Resize images
SPACE_CHARACTER_SIZE = (80, 80)
ALIEN_VILLAIN_SIZE = (80, 80)
space_character = pygame.transform.scale(space_character, SPACE_CHARACTER_SIZE)
alien_villain = pygame.transform.scale(alien_villain, ALIEN_VILLAIN_SIZE)

# Define characters for selection
character_1 = space_character
character_2 = alien_villain

def loading_screen():
    screen.fill(BLACK)
    font = pygame.font.Font(None, 50)
    text = font.render("Loading...", True, WHITE)
    screen.blit(text, (WIDTH // 2 - 60, HEIGHT // 2))
    pygame.display.flip()
    time.sleep(2)  # Simulate loading time

def character_selection():
    selected = None
    font = pygame.font.Font(None, 36)
    while selected is None:
        screen.fill(BLACK)
        screen.blit(character_1, (WIDTH // 3 - 40, HEIGHT // 2 - 40))
        screen.blit(character_2, (2 * WIDTH // 3 - 40, HEIGHT // 2 - 40))
        text = font.render("Choose Your Character: Press 1 or 2", True, WHITE)
        screen.blit(text, (WIDTH // 2 - 180, HEIGHT // 4))
        pygame.display.flip()
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_1:
                    selected = character_1
                elif event.key == pygame.K_2:
                    selected = character_2
    return selected

# Classes
class Bullet(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.Surface((10, 20))
        self.image.fill(WHITE)
        self.rect = self.image.get_rect(center=(x, y))

    def update(self):
        self.rect.y -= 10
        if self.rect.bottom < 0:
            self.kill()

class AlienBullet(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.Surface((10, 20))
        self.image.fill(RED)
        self.rect = self.image.get_rect(center=(x, y))

    def update(self):
        self.rect.y += 7
        if self.rect.top > HEIGHT:
            self.kill()

class Player(pygame.sprite.Sprite):
    def __init__(self, character):
        super().__init__()
        self.image = character
        self.rect = self.image.get_rect(center=(WIDTH // 2, HEIGHT - 100))
        self.lives = 3

    def update(self, keys):
        speed = 5
        if keys[pygame.K_LEFT] and self.rect.left > 0:
            self.rect.x -= speed
        if keys[pygame.K_RIGHT] and self.rect.right < WIDTH:
            self.rect.x += speed

class Alien(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = alien_villain
        self.rect = self.image.get_rect(x=random.randint(0, WIDTH - 50), y=random.randint(50, 150))
        self.direction = random.choice([-1, 1])
        self.speed = random.randint(1, 3)
        self.shoot_timer = random.randint(30, 120)

    def update(self):
        self.rect.x += self.direction * self.speed
        if self.rect.left <= 0 or self.rect.right >= WIDTH:
            self.direction *= -1
        self.shoot_timer -= 1
        if self.shoot_timer <= 0:
            alien_bullet = AlienBullet(self.rect.centerx, self.rect.bottom)
            alien_bullets.add(alien_bullet)
            self.shoot_timer = random.randint(50, 150)

# Groups
def reset_game():
    """ Resets the game state after a game over. """
    player.lives = 3
    bullets.empty()
    alien_bullets.empty()
    alien_group.empty()
    for _ in range(5):
        alien_group.add(Alien())
    return 0  # Reset score

# Display loading screen
loading_screen()

# Character selection
selected_character = character_selection()

# Create player with selected character
player = Player(selected_character)
player_group = pygame.sprite.Group(player)
bullets = pygame.sprite.Group()
alien_bullets = pygame.sprite.Group()
alien_group = pygame.sprite.Group()

for _ in range(5):
    alien_group.add(Alien())

# Score
score = 0
font = pygame.font.Font(None, 36)

def draw_text(text, x, y, color=WHITE):
    screen.blit(font.render(text, True, color), (x, y))

def game_over():
    """ Displays the Game Over screen and waits for the player to restart. """
    screen.fill(BLACK)
    draw_text("GAME OVER", WIDTH // 2 - 80, HEIGHT // 2)
    draw_text("Press R to Restart", WIDTH // 2 - 100, HEIGHT // 2 + 40)
    pygame.display.flip()

    waiting = True
    while waiting:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            if event.type == pygame.KEYDOWN and event.key == pygame.K_r:
                return reset_game()

def update_score(score):
    """ Handles bullet-alien collision and updates the score. """
    for bullet in bullets:
        hit = pygame.sprite.spritecollide(bullet, alien_group, True)
        if hit:
            bullet.kill()
            score += 10
            alien_group.add(Alien())
    return score

# Main Loop
running = True
while running:
    screen.blit(background, (0, 0))
    keys = pygame.key.get_pressed()
    player_group.update(keys)
    bullets.update()
    alien_group.update()
    alien_bullets.update()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
            bullet = Bullet(player.rect.centerx, player.rect.top)
            bullets.add(bullet)

    # Update Score
    score = update_score(score)

    # Check collision with player
    if pygame.sprite.spritecollide(player, alien_bullets, True):
        player.lives -= 1
        if player.lives == 0:
            score = game_over()

    # Draw everything
    player_group.draw(screen)
    bullets.draw(screen)
    alien_group.draw(screen)
    alien_bullets.draw(screen)

    # Display score and lives
    draw_text(f"Score: {score}", 10, 10)
    draw_text(f"Lives: {player.lives}", WIDTH - 100, 10)

    pygame.display.flip()
    pygame.time.delay(30)

pygame.quit()
