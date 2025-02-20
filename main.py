
import pygame
import loading
import game

pygame.init() 

WIDTH, HEIGHT = 800, 490
screen = pygame.display.set_mode((WIDTH, HEIGHT))  

if __name__ == "__main__":
    loading.loading_screen(screen)  
    game.run_game(screen)  
