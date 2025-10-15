import pygame
from game.game_engine import GameEngine

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
# Initialize the game with the default winning score (5)
engine = GameEngine(WIDTH, HEIGHT)

def main():
    running = True
    
    while running:
        SCREEN.fill(BLACK)
        
        # --- Event Handling ---
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            
            # Handle menu input only when the game is over
            if not engine.game_active and event.type == pygame.KEYDOWN:
                # 3: Best of 3
                if event.key == pygame.K_3:
                    engine.set_max_score(3)
                    engine.reset_game_state()
                # 5: Best of 5
                elif event.key == pygame.K_5:
                    engine.set_max_score(5)
                    engine.reset_game_state()
                # 7: Best of 7
                elif event.key == pygame.K_7:
                    engine.set_max_score(7)
                    engine.reset_game_state()
                # ESC: Exit
                elif event.key == pygame.K_ESCAPE:
                    running = False


        # --- Game Logic (Updates and Rendering) ---
        
        # This handles input/movement only if engine.game_active is True
        engine.handle_input()
        
        # This handles ball movement, scoring, and AI movement
        engine.update() 
        
        # This handles drawing everything, including the winner screen if the game is over
        engine.render(SCREEN)

        pygame.display.flip()
        clock.tick(FPS)

    pygame.quit()

if __name__ == "__main__":
    main()


