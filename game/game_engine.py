import pygame
from .paddle import Paddle
from .ball import Ball

# Game Engine

WHITE = (255, 255, 255)

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
        self.game_active = True
        self.max_score = 5 # Default winning score (Best of 5)

    def set_max_score(self, score):
        """Sets the new score target for a match."""
        self.max_score = score
        
    def reset_game_state(self):
        """Resets scores, sets game active, and resets the ball position for a new match."""
        self.player_score = 0
        self.ai_score = 0
        self.game_active = True
        self.ball.reset() # Reset ball direction and position
        # Also ensure paddles are centered
        self.player.y = self.height // 2 - self.paddle_height // 2
        self.ai.y = self.height // 2 - self.paddle_height // 2


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
        if self.player_score >= self.max_score:
            self.game_active = False
            return "Player"
        elif self.ai_score >= self.max_score:
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
            
        text_rect = text_surface.get_rect(center=(self.width // 2, self.height // 2 - 50))
        
        # Draw a semi-transparent background box for the winner text
        s = pygame.Surface((self.width, 100)) 
        s.set_alpha(128) # Opacity 0-255
        s.fill((0, 0, 0)) # Black background
        screen.blit(s, (0, self.height // 2 - 100))
        
        # Draw the winner text
        screen.blit(text_surface, text_rect)
        
        self.display_replay_menu(screen)
        
    def display_replay_menu(self, screen):
        """Renders the replay options menu."""
        menu_font = pygame.font.SysFont("Arial", 24)
        
        # Menu options list
        options = [
            (f"Press [3] for Best of 3 (Target: 3)", 3),
            (f"Press [5] for Best of 5 (Target: 5)", 5),
            (f"Press [7] for Best of 7 (Target: 7)", 7),
            (f"Press [ESC] to Exit Game", 0), # 0 is a placeholder for Exit
        ]
        
        start_y = self.height // 2 + 50
        line_spacing = 30
        
        # Draw each option
        for i, (text, score) in enumerate(options):
            # Highlight current score choice
            is_active_target = (score == self.max_score) and (score != 0)
            color = (255, 255, 0) if is_active_target else WHITE 
            
            text_surface = menu_font.render(text, True, color)
            text_rect = text_surface.get_rect(center=(self.width // 2, start_y + i * line_spacing))
            screen.blit(text_surface, text_rect)


    def render(self, screen):
        # 1. Draw standard elements
        pygame.draw.rect(screen, WHITE, self.player.rect())
        pygame.draw.rect(screen, WHITE, self.ai.rect())
        
        # Only draw the ball if the game is active
        if self.game_active:
            pygame.draw.ellipse(screen, WHITE, self.ball.rect())
            
        pygame.draw.aaline(screen, WHITE, (self.width//2, 0), (self.width//2, self.height))

        # 2. Draw score (Always show score)
        player_text = self.font.render(str(self.player_score), True, WHITE)
        ai_text = self.font.render(str(self.ai_score), True, WHITE)
        screen.blit(player_text, (self.width//4, 20))
        screen.blit(ai_text, (self.width * 3//4, 20))

        # 3. Check for winner and display game over screen/menu
        winner = self.check_game_over()
        if winner:
            self.display_winner(screen, winner)


