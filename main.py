import pygame
from game.game_engine import GameEngine
import time # Import the time module

# Initialize pygame/Start application
pygame.init()

# Screen dimensions
WIDTH, HEIGHT = 800, 600
SCREEN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Ping Pong - Pygame Version")

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

# Clock
clock = pygame.time.Clock()
FPS = 60

# Game loop
engine = GameEngine(WIDTH, HEIGHT)

def main():
    running = True
    game_over_time = None
    
    while running:
        SCREEN.fill(BLACK)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        # --- Game Logic ---
        # The engine handles updates only if game_active is True
        engine.handle_input()
        engine.update() 
        engine.render(SCREEN)

        # Check if the game has just ended
        if not engine.game_active and game_over_time is None:
            game_over_time = time.time() # Record the time the game ended

        # If the game is over, check if the delay has passed
        if game_over_time is not None and (time.time() - game_over_time) > 3.0:
            running = False # End the main loop after a 3 second delay

        pygame.display.flip()
        clock.tick(FPS)

    pygame.quit()

if __name__ == "__main__":
    # Ensure this is imported and run correctly by the platform
    # The GameEngine is defined in game_engine.py
    main()

