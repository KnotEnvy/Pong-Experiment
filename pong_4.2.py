import pygame
import sys
import random
import math

# Initialize Pygame
pygame.init()
# clock = pygame.Clock()
FPS = 60


# Set the dimensions of the window
screen_width = 800
screen_height = 600
screen = pygame.display.set_mode((screen_width, screen_height))

# Set the title of the window
pygame.display.set_caption('Pong Game')

# Set the font for the start screen
font = pygame.font.Font(None, 36)

clock = pygame.time.Clock()
start_time = pygame.time.get_ticks()


# Function to display the start screen
def display_start_screen():
    font = pygame.font.Font(None, 80)
    pong_text = font.render("KNOTZ_PONG!!", True, (25, 255, 55))
    font = pygame.font.Font(None, 36)
    start_text = font.render("Press 'S' to Start the Game", True, (255, 255, 255))
    quit_text = font.render("Press 'Q' to Quit the Game", True, (255, 255, 255))

    screen.blit(pong_text, ((screen_width-70) / 2 - start_text.get_width() / 2, (screen_height -175) / 2 - start_text.get_height() / 2))
    screen.blit(start_text, (screen_width / 2 - start_text.get_width() / 2, screen_height / 2 - start_text.get_height() / 2))
    screen.blit(quit_text, (screen_width / 2 - quit_text.get_width() / 2, screen_height / 2 + quit_text.get_height()))
def display_game_over_screen():
    font = pygame.font.Font(None, 60)

    game_over_text = font.render("Game Over", True, (150, 20, 35))
    font = pygame.font.Font(None, 36)
    restart_text = font.render("Press 'R' to Restart the Game", True, (255, 255, 255))
    quit_text = font.render("Press 'Q' to Quit the Game", True, (255, 255, 255))

    screen.blit(game_over_text, (screen_width / 2 - game_over_text.get_width() / 2, (screen_height -50)  / 2 - game_over_text.get_height() / 2))
    screen.blit(restart_text, (screen_width / 2 - restart_text.get_width() / 2, screen_height / 2))
    screen.blit(quit_text, (screen_width / 2 - quit_text.get_width() / 2, screen_height / 2 + quit_text.get_height()))


def display_scores():
    player_score_text = font.render(str(player_score), True, (255, 255, 255))
    ai_score_text = font.render(str(ai_score), True, (255, 255, 255))

    screen.blit(player_score_text, (screen_width / 2 - 50, 10))
    screen.blit(ai_score_text, (screen_width / 2 + 20, 10))

def display_time():
    elapsed_time = (pygame.time.get_ticks() - start_time) / 1000  # Convert milliseconds to seconds
    time_text = font.render("Time: " + str(int(elapsed_time)), True, (255, 255, 255))

    screen.blit(time_text, (10, 10))

class Particle:
    def __init__(self, x, y):
        self.rect = pygame.Rect(x, y, 5, 5)
        self.speed = random.randint(2, 5)
        self.angle = random.uniform(0, 2 * math.pi)
        self.lifetime = random.randint(5, 80)  # Lifetime in frames

    def move(self):
        self.rect.move_ip(self.speed * math.cos(self.angle), self.speed * math.sin(self.angle))
        self.lifetime -= 1

    def draw(self, screen):
        pygame.draw.rect(screen, (255, 255, 255), self.rect)

class ParticleEmitter:
    def __init__(self, x, y, num_particles):
        self.particles = [Particle(x, y) for _ in range(num_particles)]

    def emit(self):
        for particle in self.particles:
            particle.move()
            if particle.lifetime > 0:
                particle.draw(screen)
class FireParticle:
    def __init__(self, x, y, ball_direction):
        self.speed = random.uniform(2, 5)  # Vary the speed
        self.size = random.uniform(3, 10)  # Vary the size
        self.rect = pygame.Rect(x, y, self.size, self.size)  # Use size for both width and height
        self.angle = ball_direction + math.pi  # Make particles move in the opposite direction of the ball
        self.lifetime = random.randint(5, 15)  # Decrease lifetime to make the trail disappear more quickly
        self.color = random.choice([(255, 69, 0), (255, 165, 0), (255, 223, 0)])  # Shades of red, orange, and yellow


    def move(self):
        self.rect.move_ip(self.speed * math.cos(self.angle), self.speed * math.sin(self.angle))
        self.lifetime -= 1

    def draw(self, screen):
        if self.lifetime > 0:
            pygame.draw.rect(screen, self.color, self.rect)



class FireParticleEmitter:
    def __init__(self, x, y, num_particles, ball_direction):
        self.particles = [FireParticle(x, y, ball_direction) for _ in range(num_particles)]

    def emit(self):
        for particle in self.particles:
            particle.move()
            particle.draw(screen)


class Star:
    def __init__(self):
        self.reset()

    def reset(self):
        self.y = random.uniform(0, screen_height)
        self.x = random.uniform(0, screen_width)
        self.speed = random.uniform(0.1, 1)
        self.size = random.uniform(1, 3)

    def move(self):
        self.y += self.speed
        if self.y > screen_height:
            self.reset()

    def draw(self, screen):
        pygame.draw.circle(screen, (255, 255, 255), (int(self.x), int(self.y)), int(self.size))

class Paddle:
    def __init__(self, x, y):
        self.rect = pygame.Rect(x, y, 15, 80)

    def draw(self, screen):
        pygame.draw.rect(screen, (255, 255, 255), self.rect)

    def move(self, speed):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_UP]:
            self.rect.move_ip(0, -speed)
        if keys[pygame.K_DOWN]:
            self.rect.move_ip(0, speed)

        if self.rect.top < 0:
            self.rect.top = 0
        if self.rect.bottom > screen_height:
            self.rect.bottom = screen_height

class AI_Paddle(Paddle):
    def move(self, speed, ball):
        if random.random() < .87:  # 70% of the time, move towards the ball
            if self.rect.centery < ball.rect.centery:
                self.rect.move_ip(0, speed)
            else:
                self.rect.move_ip(0, -speed)
        else:  # 30% of the time, continue moving in the current direction
            self.rect.move_ip(0, speed if self.rect.centery < screen_height / 2 else -speed)

        if self.rect.top < 0:
            self.rect.top = 0
        if self.rect.bottom > screen_height:
            self.rect.bottom = screen_height

class Ball:
    def __init__(self, x, y, speed):
        self.rect = pygame.Rect(x, y, 15, 15)
        self.speed = speed
        self.dx = 1  # Direction of movement in x axis (1 is right, -1 is left)
        self.dy = 1  # Direction of movement in y axis (1 is down, -1 is up)
        self.bounce_timer = 30
    def draw(self, screen):
        pygame.draw.ellipse(screen, (255, 255, 255), self.rect)

    

    def move(self):
        self.rect.move_ip(self.speed * self.dx, self.speed * self.dy)

        # Bounce off the top and bottom edges of the screen
        if self.rect.top < 0 or self.rect.bottom > screen_height:
            self.dy *= -1 

    def direction(self):
        return math.atan2(self.dy, self.dx)

    def bounce(self):
        self.dx *= -1
        emitters.append(ParticleEmitter(ball.rect.centerx, ball.rect.centery, 20))
        self.bounce_timer = 15


    def reset(self):
        self.rect.center = (screen_width / 2, screen_height / 2)
        self.dx *= -1  # Change the direction of the ball


player = Paddle(50, screen_height / 2)
ai = AI_Paddle(screen_width - 65, screen_height / 2)
ball = Ball(screen_width / 2, screen_height / 2, 5)
player_score = 0
ai_score = 0
emitters = []
stars = [Star() for _ in range(200)]
game_started = False
game_over = False

# Game loop
running = True
while running:
    clock.tick(60)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_s:
                game_started = True
            elif event.key == pygame.K_q:
                running = False
            elif event.key == pygame.K_z:
                game_over = True
            elif event.key == pygame.K_r:
                game_started = False
                game_over = False
                player_score = 0
                ai_score = 0

    # Fill the screen with black
    screen.fill((0, 0, 0))

    if game_over:
        display_game_over_screen()
    elif game_started:
        # Game logic here...

        ball.move()

        if ball.bounce_timer > 0:
            emitters.append(FireParticleEmitter(ball.rect.centerx, ball.rect.centery, 20, ball.direction()))
            ball.bounce_timer -= 1

        # If the ball hits a paddle, bounce and create a particle effect
        if ball.rect.colliderect(player.rect) or ball.rect.colliderect(ai.rect):
            ball.bounce()
            emitters.append(ParticleEmitter(ball.rect.centerx, ball.rect.centery, 20))
            emitters.append(FireParticleEmitter(ball.rect.centerx, ball.rect.centery, 20, ball.direction()))


        # If the ball hits the left or right edge of the screen, score a point, reset the ball, and create a particle effect
        if ball.rect.left < 0:
            ai_score += 1
            emitters.append(ParticleEmitter(ball.rect.centerx, ball.rect.centery, 50))
            ball.reset()
        elif ball.rect.right > screen_width:
            player_score += 1
            emitters.append(ParticleEmitter(ball.rect.centerx, ball.rect.centery, 50))
            ball.reset()
        
        # Check if either player has reached 10 points
        if player_score >= 10 or ai_score >= 10:
            game_over = True
        
        
        # Emit particles
        for emitter in emitters:
            emitter.emit()

        # Move and draw stars
        for star in stars:
            star.move()
            star.draw(screen)

        player.draw(screen)
        player.move(5)
        ai.draw(screen)
        ai.move(5, ball)
        ball.draw(screen)
        display_scores()
        display_time()

    else:
        # Display the start screen
        display_start_screen()

    # Update the display
    pygame.display.flip()

# Quit Pygame
pygame.quit()
sys.exit()


