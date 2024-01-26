#!/usr/bin/env python
# coding: utf-8

# In[ ]:


import pygame
import random
import sys

# Initialize Pygame
pygame.init()

# Set up the screen dimensions and clock
screen_width = 700
screen_height = 500
screen = pygame.display.set_mode((screen_width, screen_height))
clock = pygame.time.Clock()

# Colors
background_color = (36, 36, 36)  # Dark gray for background
paddle_color = (236, 240, 241)  # Light gray for paddles
ball_color = (46, 204, 113)  # Bright green for ball
text_color = (255, 255, 0)  # Bright yellow for the title
menu_bg_color = (173, 216, 230)  # Light blue for menu background
green = (0, 255, 0)  # Define green color for the start button
red = (255, 0, 0)  
blue = (0, 0, 139)    # Dark Blue
pink = (255, 192, 203)     # Pink
dgreen = (0, 100, 0)  

# Initialize game variables
game_started = False
running = True

# Initialize animation balls with new colors
animation_balls = [
    (screen_width // 4, screen_height // 2, 2, 2, red),          # Red ball
    (3 * screen_width // 4, screen_height // 2, -2, 2, blue), # Dark Blue ball
    (screen_width // 2, screen_height // 4, 2, -2, pink),         # Pink ball
    (screen_width // 2, 3 * screen_height // 4, -2, -2, dgreen) # Dark Green ball
]


# Paddle and ball variables
paddle_width = 10
paddle_height = 100
ball_radius = 10
ball_x, ball_y = screen_width // 2, screen_height // 2
ball_dx, ball_dy = random.choice([-4, 4]), random.choice([-4, 4])
paddle1_x, paddle2_x = 20, screen_width - 20 - paddle_width
paddle1_y, paddle2_y = (screen_height - paddle_height) // 2, (screen_height - paddle_height) // 2
player_score, ai_score = 0, 0

# Font and Text
try:
    font_large = pygame.font.SysFont('comicsansms', 50, bold=True)
    font_medium = pygame.font.SysFont('comicsansms', 30)
except:
    font_large = pygame.font.Font(None, 50)
    font_medium = pygame.font.Font(None, 30)

# Define the start window
button_width = 120
button_height = 50
button_x = (screen_width - 2 * button_width - 30) // 2
start_button_x = button_x
exit_button_x = button_x + button_width + 30
button_y = (screen_height // 2) - (button_height // 2)
start_button_y = button_y
exit_button_y = button_y
    
def draw_start_window(animation_balls):
    screen.fill(menu_bg_color)  # Set the menu background color

    # Welcome Text
    welcome_text = font_large.render("Welcome to Paddle Pro!", True, text_color)
    welcome_text_rect = welcome_text.get_rect(center=(screen_width // 2, screen_height // 4))
    screen.blit(welcome_text, welcome_text_rect)

    # Animated Balls with different colors
    for ball in animation_balls:
        pygame.draw.circle(screen, ball[4], (int(ball[0]), int(ball[1])), ball_radius)

    # Start Button
    pygame.draw.rect(screen, green, (start_button_x, button_y, button_width, button_height))
    start_text = font_medium.render("Start", True, background_color)
    start_text_rect = start_text.get_rect(center=(start_button_x + button_width // 2, button_y + button_height // 2))
    screen.blit(start_text, start_text_rect)

    # Exit Button
    pygame.draw.rect(screen, red, (exit_button_x, button_y, button_width, button_height))
    exit_text = font_medium.render("Exit", True, background_color)
    exit_text_rect = exit_text.get_rect(center=(exit_button_x + button_width // 2, button_y + button_height // 2))
    screen.blit(exit_text, exit_text_rect)

    # Control Instructions Text
    instructions_text = font_medium.render("Use 'W' to go up, 'S' to go down", True, text_color)
    instructions_text_rect = instructions_text.get_rect(center=(screen_width // 2, button_y + button_height + 40))
    screen.blit(instructions_text, instructions_text_rect)

    pygame.display.flip()

def update_animation_balls(animation_balls):
    for i, ball in enumerate(animation_balls):
        x, y, dx, dy, color = ball
        x += dx
        y += dy
        if x < ball_radius or x > screen_width - ball_radius:
            dx *= -1
        if y < ball_radius or y > screen_height - ball_radius:
            dy *= -1
        animation_balls[i] = (x, y, dx, dy, color)
    return animation_balls

def draw_game_objects():
    # Draw paddles
    pygame.draw.rect(screen, paddle_color, (paddle1_x, paddle1_y, paddle_width, paddle_height))
    pygame.draw.rect(screen, paddle_color, (paddle2_x, paddle2_y, paddle_width, paddle_height))
    
    # Draw ball
    pygame.draw.circle(screen, ball_color, (int(ball_x), int(ball_y)), ball_radius)
    
    # Draw scores
    player_score_text = font_medium.render(f"Player: {player_score}", True, text_color)
    ai_score_text = font_medium.render(f"AI: {ai_score}", True, text_color)
    screen.blit(player_score_text, (50, 20))
    screen.blit(ai_score_text, (screen_width - 150, 20))


# Game loop
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            mouse_pos = pygame.mouse.get_pos()
            if not game_started:
                if button_x <= mouse_pos[0] <= button_x + button_width and \
                        start_button_y <= mouse_pos[1] <= start_button_y + button_height:
                    game_started = True
                elif button_x <= mouse_pos[0] <= button_x + button_width and \
                        exit_button_y <= mouse_pos[1] <= exit_button_y + button_height:
                    running = False
            elif game_started and button_x <= mouse_pos[0] <= button_x + button_width and \
                    restart_button_y <= mouse_pos[1] <= restart_button_y + button_height:
                game_started = True
                player_score, ai_score = 0, 0

    if game_started:
        # Clear the screen
        screen.fill(background_color)

        # User controls paddle1
        keys = pygame.key.get_pressed()
        if keys[pygame.K_w] and paddle1_y > 0:
            paddle1_y -= 5
        if keys[pygame.K_s] and paddle1_y < screen_height - paddle_height:
            paddle1_y += 5

        # AI-controlled paddle2
        if ball_y < paddle2_y + paddle_height // 2:
            paddle2_y -= 5
        elif ball_y > paddle2_y + paddle_height // 2:
            paddle2_y += 5

        # Ball movement and collision
        ball_x += ball_dx
        ball_y += ball_dy

        if ball_y < 0 or ball_y > screen_height:
            ball_dy *= -1

        if ball_x < paddle1_x + paddle_width and paddle1_y < ball_y < paddle1_y + paddle_height:
            ball_dx *= -1
            player_score += 1

        if ball_x > paddle2_x - ball_radius and paddle2_y < ball_y < paddle2_y + paddle_height:
            ball_dx *= -1
            ai_score += 1

        # Check if the ball is missed and display exit screen
        if ball_x < 0 or ball_x > screen_width:
            game_started = False
            pygame.display.flip()
            ball_x, ball_y = screen_width // 2, screen_height // 2
            ball_dx, ball_dy = random.choice([-4, 4]), random.choice([-4, 4])

        # Draw game objects
        draw_game_objects()
        # Update the display
        pygame.display.flip()
    else:
        # Update and draw the bouncing balls on the start window
        animation_balls = update_animation_balls(animation_balls)
        draw_start_window(animation_balls)

    # Cap the frame rate
    clock.tick(60)

pygame.quit()
sys.exit()

