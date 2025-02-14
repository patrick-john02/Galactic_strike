# main.py
import pygame
import loading
import game
 
# start ng pygame
pygame.init() 

# eto yung laki ng screens
WIDTH, HEIGHT = 800, 490
screen = pygame.display.set_mode((WIDTH, HEIGHT))  

if __name__ == "__main__":
    loading.loading_screen(screen)  # Display the loading screen 
    game.run_game(screen)  # Start the game and show the main menu
