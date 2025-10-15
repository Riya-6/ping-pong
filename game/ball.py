import pygame
import random

class Ball:
    def __init__(self, x, y, width, height, screen_width, screen_height, sound_paddle_hit, sound_wall_bounce):
        self.original_x = x
        self.original_y = y
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.velocity_x = random.choice([-5, 5])
        self.velocity_y = random.choice([-3, 3])
        
        # Store sound objects passed from GameEngine
        self.sound_paddle_hit = sound_paddle_hit
        self.sound_wall_bounce = sound_wall_bounce

    def move(self):
        self.x += self.velocity_x
        self.y += self.velocity_y

        if self.y <= 0 or self.y + self.height >= self.screen_height:
            self.velocity_y *= -1
            # Play wall bounce sound
            if self.sound_wall_bounce:
                self.sound_wall_bounce.play()

    def check_collision(self, player, ai):
        max_bounce_speed = 6 # Max vertical speed after hitting a paddle

        # Determine which paddle the ball is moving towards
        if self.velocity_x < 0: # Moving left (towards player)
            paddle = player
            is_player_hit = True
        else: # Moving right (towards AI)
            paddle = ai
            is_player_hit = False

        # Check for collision with the target paddle
        if self.rect().colliderect(paddle.rect()):
            
            # Play paddle hit sound
            if self.sound_paddle_hit:
                self.sound_paddle_hit.play()
            
            # CRITICAL FIX FOR TUNNELLING: Reposition the ball to the edge of the paddle
            if is_player_hit:
                # If moving left, set X to the right edge of the paddle
                self.x = paddle.x + paddle.width
            else:
                # If moving right, set X to the left edge of the paddle
                self.x = paddle.x - self.width

            # Reverse the X direction
            self.velocity_x *= -1

            # Calculate and apply new Y-velocity for spin/angle
            hit_center_y = self.y + (self.height / 2)
            paddle_center_y = paddle.y + (paddle.height / 2)
            
            relative_y = hit_center_y - paddle_center_y
            normalized_y = relative_y / (paddle.height / 2) 

            self.velocity_y = normalized_y * max_bounce_speed

    def reset(self):
        self.x = self.original_x
        self.y = self.original_y
        self.velocity_x *= -1
        self.velocity_y = random.choice([-3, 3])

    def rect(self):
        return pygame.Rect(self.x, self.y, self.width, self.height)

