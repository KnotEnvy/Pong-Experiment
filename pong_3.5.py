import pygame

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
    pygame.draw.circle(window, LINE_COLOR, ball_pos, BALL_RADIUS)
    pygame.draw.rect(window, LINE_COLOR, (player_paddle_pos[0], player_paddle_pos[1], PADDLE_WIDTH, PADDLE_HEIGHT))
    pygame.draw.rect(window, LINE_COLOR, (ai_paddle_pos[0], ai_paddle_pos[1], PADDLE_WIDTH, PADDLE_HEIGHT))

    # Set up initial game state
player_score = 0
ai_score = 0
game_over = False

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

    # Draw game objects and update display
    draw_objects(ball_pos, player_paddle_pos, ai_paddle_pos)
    pygame.display.update()

    # Limit frame rate
    clock.tick(60)