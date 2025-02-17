from loading import loading_screen
from lobby import lobby_screen
import pygame
import random

# Initialize pygame
pygame.init()

# Screen dimensions
WIDTH, HEIGHT = 850, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Galactic Strike")

loading_screen(screen, WIDTH, HEIGHT) 
selected_character_name = lobby_screen(screen, WIDTH, HEIGHT) 

# Define colors
WHITE = (255, 255, 255)
RED = (255, 0, 0)

# Load assets
background = pygame.image.load("assets/images/11.png")
spaceship_img = pygame.image.load("assets/blaster/char/sprites/ship.png")
rocket_img = pygame.image.load("assets/blaster/char/sprites/enemy_kamikaze.png")
alien_img = pygame.image.load("assets/blaster/char/sprites/enemy_clever.png")
asteroid_img = pygame.image.load("assets/images/asteroid.png")

# Resize images
PLAYER_SIZE = (80, 80)
spaceship_img = pygame.transform.scale(spaceship_img, PLAYER_SIZE)
rocket_img = pygame.transform.scale(rocket_img, PLAYER_SIZE)
alien_img = pygame.transform.scale(alien_img, (100, 100))
asteroid_img = pygame.transform.scale(asteroid_img, (50, 50))

# Character selection attributes
characters = {
    "hero1": {"name": "Space Fighter", "image": spaceship_img, "speed": 7, "attack_power": 2, "fire_rate": 300},
    "hero2": {"name": "Rocket Warrior", "image": rocket_img, "speed": 6, "attack_power": 3, "fire_rate": 400}
}
selected_character = characters.get(selected_character_name, characters["hero1"])

# Initialize font
font = pygame.font.Font(None, 36)

class Player(pygame.sprite.Sprite):
    def __init__(self, character):
        super().__init__()
        self.image = character["image"]
        self.rect = self.image.get_rect(center=(WIDTH // 2, HEIGHT - 80))
        self.speed = character["speed"]
        self.attack_power = character["attack_power"]
        self.fire_rate = character["fire_rate"]
        self.lives = 3
        self.score = 0
        self.last_shot_time = 0

    def move(self, keys):
        if keys[pygame.K_LEFT] and self.rect.x > 0:
            self.rect.x -= self.speed
        if keys[pygame.K_RIGHT] and self.rect.x < WIDTH - self.rect.width:
            self.rect.x += self.speed

    def shoot(self):
        current_time = pygame.time.get_ticks()
        if current_time - self.last_shot_time >= self.fire_rate:
            bullet = Bullet(self.rect.centerx, self.rect.top, self.attack_power)
            bullets.add(bullet)
            self.last_shot_time = current_time

class Bullet(pygame.sprite.Sprite):
    def __init__(self, x, y, attack_power):
        super().__init__()
        self.image = pygame.Surface((5, 10))
        self.image.fill(WHITE)
        self.rect = self.image.get_rect(center=(x, y))
        self.speed = -10
        self.attack_power = attack_power

    def update(self):
        self.rect.y += self.speed
        if self.rect.bottom < 0:
            self.kill()

class Asteroid(pygame.sprite.Sprite):
    def __init__(self, x):
        super().__init__()
        self.image = asteroid_img
        self.rect = self.image.get_rect(midtop=(x, 0))
        self.speed = random.randint(3, 6)

    def update(self):
        self.rect.y += self.speed
        if self.rect.top > HEIGHT:
            player.lives -= 1  
            self.kill()

class Alien(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = alien_img
        self.rect = self.image.get_rect(midtop=(WIDTH // 2, 10))
        self.speed = 3
        self.direction = 1
        self.last_throw_time = 0
        self.throw_interval = 1500

    def move(self):
        self.rect.x += self.speed * self.direction
        if self.rect.right >= WIDTH or self.rect.left <= 0:
            self.direction *= -1

    def throw_asteroid(self):
        current_time = pygame.time.get_ticks()
        if current_time - self.last_throw_time >= self.throw_interval:
            asteroid = Asteroid(self.rect.centerx)
            asteroids.add(asteroid)
            self.last_throw_time = current_time

# Initialize Player and Alien
player = Player(selected_character)
player_group = pygame.sprite.Group(player)
bullets = pygame.sprite.Group()
asteroids = pygame.sprite.Group()
alien = Alien()
alien_group = pygame.sprite.Group(alien)

# Game loop
running = True
clock = pygame.time.Clock()

while running:
    screen.blit(background, (0, 0))

    bullets.update()
    asteroids.update()
    alien.move()
    alien.throw_asteroid()

    bullets.draw(screen)
    asteroids.draw(screen)
    alien_group.draw(screen)
    player_group.draw(screen)

    # Check bullet collisions with asteroids
    for bullet in bullets:
        asteroid_hit = pygame.sprite.spritecollide(bullet, asteroids, True)
        if asteroid_hit:
            player.score += 10
            bullet.kill()

    # Check if player is hit by an asteroid
    if pygame.sprite.spritecollide(player, asteroids, True):
        player.lives -= 1
    if player.lives <= 0:
        loading_screen(screen, WIDTH, HEIGHT) 
        selected_character_name = lobby_screen(screen, WIDTH, HEIGHT)  
        selected_character = characters.get(selected_character_name, characters["hero1"]) 
        player = Player(selected_character)  
        asteroids.empty()  
        bullets.empty()  
        running = True 

    # Display score and lives
    score_text = font.render(f"Score: {player.score}", True, WHITE)
    lives_text = font.render(f"Lives: {player.lives}", True, WHITE)
    screen.blit(score_text, (10, 10))  
    screen.blit(lives_text, (WIDTH - 100, 10))  

    keys = pygame.key.get_pressed()
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                player.shoot()

    player.move(keys)
    pygame.display.flip()
    clock.tick(60)

pygame.quit()