import pygame
import sys


# Initialize Pygame
pygame.init()

# Set up the window and game clock
WINDOW_WIDTH = 800
WINDOW_HEIGHT = 600
WINDOW_TITLE = "Pong"

window = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
pygame.display.set_caption(WINDOW_TITLE)

clock = pygame.time.Clock()

# Define game objects
BALL_RADIUS = 10
BALL_VELOCITY = [5, 5]
ball_pos = [WINDOW_WIDTH//2, WINDOW_HEIGHT//2]

PADDLE_WIDTH = 10
PADDLE_HEIGHT = 100
PADDLE_VELOCITY = 5
player_paddle_pos = [0, WINDOW_HEIGHT//2 - PADDLE_HEIGHT//2]
ai_paddle_pos = [WINDOW_WIDTH - PADDLE_WIDTH, WINDOW_HEIGHT//2 - PADDLE_HEIGHT//2]

player_score = 0
ai_score = 0
game_over = False

# Define background
BACKGROUND_COLOR = pygame.Color("grey12")
LINE_COLOR = pygame.Color("white")
center_line = pygame.Rect(WINDOW_WIDTH//2 - 2, 0, 4, WINDOW_HEIGHT)

# Define movement and collision detection
def move_ball(ball_pos, ball_velocity):
    ball_pos[0] += ball_velocity[0]
    ball_pos[1] += ball_velocity[1]
    return ball_pos

def move_player_paddle(player_paddle_pos, direction):
    player_paddle_pos[1] += direction * PADDLE_VELOCITY
    if player_paddle_pos[1] < 0:
        player_paddle_pos[1] = 0
    elif player_paddle_pos[1] > WINDOW_HEIGHT - PADDLE_HEIGHT:
        player_paddle_pos[1] = WINDOW_HEIGHT - PADDLE_HEIGHT
    return player_paddle_pos

def move_ai_paddle(ai_paddle_pos, ball_pos):
    if ball_pos[1] < ai_paddle_pos[1] + PADDLE_HEIGHT//2:
        ai_paddle_pos[1] -= PADDLE_VELOCITY
    elif ball_pos[1] > ai_paddle_pos[1] + PADDLE_HEIGHT//2:
        ai_paddle_pos[1] += PADDLE_VELOCITY
    if ai_paddle_pos[1] < 0:
        ai_paddle_pos[1] = 0
    elif ai_paddle_pos[1] > WINDOW_HEIGHT - PADDLE_HEIGHT:
        ai_paddle_pos[1] = WINDOW_HEIGHT - PADDLE_HEIGHT
    return ai_paddle_pos

def check_wall_collision(ball_pos, ball_velocity):
    if ball_pos[1] <= BALL_RADIUS or ball_pos[1] >= WINDOW_HEIGHT - BALL_RADIUS:
        ball_velocity[1] = -ball_velocity[1]
    return ball_velocity

def check_paddle_collision(ball_pos, ball_velocity, player_paddle_pos, ai_paddle_pos):
    if ball_pos[0] <= PADDLE_WIDTH + BALL_RADIUS and player_paddle_pos[1] <= ball_pos[1] <= player_paddle_pos[1] + PADDLE_HEIGHT:
        ball_velocity[0] = -ball_velocity[0]
    elif ball_pos[0] >= WINDOW_WIDTH - PADDLE_WIDTH - BALL_RADIUS and ai_paddle_pos[1] <= ball_pos[1] <= ai_paddle_pos[1] + PADDLE_HEIGHT:
        ball_velocity[0] = -ball_velocity[0]
    return ball_velocity

def draw_objects(ball_pos, player_paddle_pos, ai_paddle_pos):
    window.fill(BACKGROUND_COLOR)
    pygame.draw.rect(window, LINE_COLOR, center_line)
    pygame.draw.circle(window, pygame.Color("white"), ball_pos, BALL_RADIUS)
    pygame.draw.rect(window, pygame.Color("white"), pygame.Rect(player_paddle_pos[0], player_paddle_pos[1], PADDLE_WIDTH, PADDLE_HEIGHT))
    pygame.draw.rect(window, pygame.Color("white"), pygame.Rect(ai_paddle_pos[0], ai_paddle_pos[1], PADDLE_WIDTH, PADDLE_HEIGHT))
    player_score_text = pygame.font.SysFont(None, 50).render(str(player_score), True, pygame.Color("white"))
    ai_score_text = pygame.font.SysFont(None, 50).render(str(ai_score), True, pygame.Color("white"))
    window.blit(player_score_text, (WINDOW_WIDTH//2 - 70, 10))
    window.blit(ai_score_text, (WINDOW_WIDTH//2 + 50, 10))
    pygame.display.flip()

def start_screen():
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                return
        window.fill(BACKGROUND_COLOR)
        title_font = pygame.font.SysFont(None, 100)
        title_text = title_font.render("Pong", True, pygame.Color("white"))
        title_rect = title_text.get_rect(center=(WINDOW_WIDTH//2, WINDOW_HEIGHT//3))

        instructions_font = pygame.font.SysFont(None, 40)
        instructions_text1 = instructions_font.render("Use the up and down arrow keys to control the paddle.", True, pygame.Color("white"))
        instructions_text2 = instructions_font.render("First player to score 10 points wins.", True, pygame.Color("white"))
        instructions_rect1 = instructions_text1.get_rect(center=(WINDOW_WIDTH//2, WINDOW_HEIGHT//2))
        instructions_rect2 = instructions_text2.get_rect(center=(WINDOW_WIDTH//2, WINDOW_HEIGHT//2 + 50))

        start_font = pygame.font.SysFont(None, 60)
        start_text = start_font.render("Press Space to Start", True, pygame.Color("white"))
        start_rect = start_text.get_rect(center=(WINDOW_WIDTH//2, WINDOW_HEIGHT//2 + 150))

        window.blit(title_text, title_rect)
        window.blit(instructions_text1, instructions_rect1)
        window.blit(instructions_text2, instructions_rect2)
        window.blit(start_text, start_rect)
        pygame.display.flip()

        clock.tick(60)

def game_over_screen(player_score, ai_score):
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                return

        window.fill(BACKGROUND_COLOR)
        gameover_font = pygame.font.SysFont(None, 80)
        gameover_text = gameover_font.render("Game Over", True, pygame.Color("white"))
        gameover_rect = gameover_text.get_rect(center=(WINDOW_WIDTH//2, WINDOW_HEIGHT//3))

        score_font = pygame.font.SysFont(None, 40)
        score_text = score_font.render(f"Player: {player_score}  AI: {ai_score}", True, pygame.Color("white"))
        score_rect = score_text.get_rect(center=(WINDOW_WIDTH//2, WINDOW_HEIGHT//2))

        restart_font = pygame.font.SysFont(None, 60)
        restart_text = restart_font.render("Press Space to Restart", True, pygame.Color("white"))
        restart_rect = restart_text.get_rect(center=(WINDOW_WIDTH//2, WINDOW_HEIGHT//2 + 150))

        window.blit(gameover_text, gameover_rect)
        window.blit(score_text, score_rect)
        window.blit(restart_text, restart_rect)
        pygame.display.flip()

        clock.tick(60)



    # Set up initial game state


start_screen()

# Game loop
while not game_over:
    
    # Handle events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            game_over = True
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                player_paddle_pos = move_player_paddle(player_paddle_pos, -1)
            elif event.key == pygame.K_DOWN:
                player_paddle_pos = move_player_paddle(player_paddle_pos, 1)

    # Move ball and AI paddle
    ball_pos = move_ball(ball_pos, BALL_VELOCITY)
    ai_paddle_pos = move_ai_paddle(ai_paddle_pos, ball_pos)

    # Check for collisions and update game state
    BALL_VELOCITY = check_wall_collision(ball_pos, BALL_VELOCITY)
    BALL_VELOCITY = check_paddle_collision(ball_pos, BALL_VELOCITY, player_paddle_pos, ai_paddle_pos)

    # Update score and check for winner
    if ball_pos[0] <= 0:
        ai_score += 1
        ball_pos = [WINDOW_WIDTH//2, WINDOW_HEIGHT//2]
        BALL_VELOCITY[0] = -BALL_VELOCITY[0]
    elif ball_pos[0] >= WINDOW_WIDTH:
        player_score += 1
        ball_pos = [WINDOW_WIDTH//2, WINDOW_HEIGHT//2]
        BALL_VELOCITY[0] = -BALL_VELOCITY[0]
    if player_score >= 10 or ai_score >= 10:
        game_over = True
        game_over_screen(player_score, ai_score)

    # Draw game objects and update display
    draw_objects(ball_pos, player_paddle_pos, ai_paddle_pos)
    pygame.display.update()

    # Limit frame rate
    clock.tick(60)