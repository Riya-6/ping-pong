import pygame
from .paddle import Paddle
from .ball import Ball

# Game Engine

WHITE = (255, 255, 255)
MAX_SCORE = 5 # Set the winning score

class GameEngine:
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.paddle_width = 10
        self.paddle_height = 100

        self.player = Paddle(10, height // 2 - 50, self.paddle_width, self.paddle_height)
        self.ai = Paddle(width - 20, height // 2 - 50, self.paddle_width, self.paddle_height)
        self.ball = Ball(width // 2, height // 2, 7, 7, width, height)

        self.player_score = 0
        self.ai_score = 0
        self.font = pygame.font.SysFont("Arial", 30)
        self.game_active = True # New state variable

    def handle_input(self):
        # Only handle movement input if the game is active
        if self.game_active:
            keys = pygame.key.get_pressed()
            if keys[pygame.K_w]:
                self.player.move(-10, self.height)
            if keys[pygame.K_s]:
                self.player.move(10, self.height)

    def check_game_over(self):
        """Checks if a player has reached the max score and sets game_active to False."""
        if self.player_score >= MAX_SCORE:
            self.game_active = False
            return "Player"
        elif self.ai_score >= MAX_SCORE:
            self.game_active = False
            return "AI"
        return None

    def update(self):
        if self.game_active:
            self.ball.move()
            self.ball.check_collision(self.player, self.ai)

            # Scoring logic
            if self.ball.x <= 0:
                self.ai_score += 1
                self.ball.reset()
            elif self.ball.x >= self.width:
                self.player_score += 1
                self.ball.reset()

            self.ai.auto_track(self.ball, self.height)
            
            # Check for game end after scores update
            self.check_game_over()


    def display_winner(self, screen, winner):
        """Renders the game over screen with the winner's name."""
        # Use a larger font for the winner message
        winner_font = pygame.font.SysFont("Arial", 72, bold=True)
        
        if winner == "Player":
            text_surface = winner_font.render("PLAYER WINS!", True, WHITE)
        else:
            text_surface = winner_font.render("AI WINS!", True, WHITE)
            
        text_rect = text_surface.get_rect(center=(self.width // 2, self.height // 2))
        
        # Draw a semi-transparent background box to make the text pop
        s = pygame.Surface((self.width, 100)) 
        s.set_alpha(128) # Opacity 0-255
        s.fill((0, 0, 0)) # Black background
        screen.blit(s, (0, self.height // 2 - 50))
        
        # Draw the winner text
        screen.blit(text_surface, text_rect)


    def render(self, screen):
        # 1. Draw standard elements
        pygame.draw.rect(screen, WHITE, self.player.rect())
        pygame.draw.rect(screen, WHITE, self.ai.rect())
        pygame.draw.ellipse(screen, WHITE, self.ball.rect())
        pygame.draw.aaline(screen, WHITE, (self.width//2, 0), (self.width//2, self.height))

        # 2. Draw score
        player_text = self.font.render(str(self.player_score), True, WHITE)
        ai_text = self.font.render(str(self.ai_score), True, WHITE)
        screen.blit(player_text, (self.width//4, 20))
        screen.blit(ai_text, (self.width * 3//4, 20))

        # 3. Check for winner and display game over screen
        winner = self.check_game_over()
        if winner:
            self.display_winner(screen, winner)


        # Draw score
        player_text = self.font.render(str(self.player_score), True, WHITE)
        ai_text = self.font.render(str(self.ai_score), True, WHITE)
        screen.blit(player_text, (self.width//4, 20))
        screen.blit(ai_text, (self.width * 3//4, 20))

