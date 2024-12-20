import pygame
import sys
import random

# Initialize pygame
pygame.init()

# Screen dimensions
SCREEN_WIDTH = 400
SCREEN_HEIGHT = 600
SCREEN = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Flappy Bird Clone")

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)


# Clock
clock = pygame.time.Clock()

# Game variables
GRAVITY = 0.5
BIRD_JUMP = -10
PIPE_SPEED = 3
PIPE_GAP = 150
FPS = 60

# Load assets
bird_img = pygame.image.load("bird.png")  # Replace with your bird image
bird_img = pygame.transform.scale(bird_img, (40, 30))

bg_img = pygame.image.load("background.png")  # Replace with your background image
bg_img = pygame.transform.scale(bg_img, (SCREEN_WIDTH, SCREEN_HEIGHT))

pipe_img = pygame.image.load("pipe.png")  # Replace with your pipe image
pipe_img = pygame.transform.scale(pipe_img, (60, 400))

# Bird class
class Bird:
    def __init__(self):
        self.image = bird_img
        self.x = 50
        self.y = SCREEN_HEIGHT // 2
        self.velocity = 0

    def draw(self):
        SCREEN.blit(self.image, (self.x, self.y))

    def move(self):
        self.velocity += GRAVITY
        self.y += self.velocity

    def jump(self):
        self.velocity = BIRD_JUMP

# Pipe class
class Pipe:
    def __init__(self, x):
        self.x = x
        self.height = random.randint(150, SCREEN_HEIGHT - PIPE_GAP - 100)
        self.top = self.height
        self.bottom = self.height + PIPE_GAP

    def draw(self):
        # Draw top pipe
        top_pipe = pygame.transform.flip(pipe_img, False, True)
        SCREEN.blit(top_pipe, (self.x, self.top - 400))
        # Draw bottom pipe
        SCREEN.blit(pipe_img, (self.x, self.bottom))

    def move(self):
        self.x -= PIPE_SPEED

    def collide(self, bird):
        if bird.y < self.top or bird.y + bird_img.get_height() > self.bottom:
            if self.x < bird.x + bird_img.get_width() < self.x + pipe_img.get_width():
                return True
        return False

# Main game loop
def main():
    def draw_text(text, size, color, x, y):
        font = pygame.font.Font(None, size)
        text_surface = font.render(text, True, color)
        text_rect = text_surface.get_rect(center=(x, y))
        SCREEN.blit(text_surface, text_rect)

    def reset_game():
        return Bird(), [Pipe(SCREEN_WIDTH)], 0

    bird, pipes, score = reset_game()
    running = True

    while running:
        SCREEN.blit(bg_img, (0, 0))

        # Event handling
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    bird.jump()

        # Bird movement
        bird.move()
        bird.draw()

        # Pipes
        for pipe in pipes:
            pipe.move()
            pipe.draw()
            if pipe.x + pipe_img.get_width() < 0:
                pipes.remove(pipe)
                pipes.append(Pipe(SCREEN_WIDTH))
                score += 1
            if pipe.collide(bird):
                running = False

        # Check for ground collision
        if bird.y + bird_img.get_height() > SCREEN_HEIGHT or bird.y < 0:
            running = False

        # Display score
        font = pygame.font.Font(None, 36)
        score_text = font.render(f"Score: {score}", True, WHITE)
        SCREEN.blit(score_text, (10, 10))

        # Update screen
        pygame.display.flip()
        clock.tick(FPS)

    # Game Over screen  
    SCREEN.fill(BLACK)
    draw_text("Game Over", 50, WHITE, SCREEN_WIDTH // 2, SCREEN_HEIGHT // 3)
    draw_text(f"Your Score: {score}", 36, WHITE, SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)
    draw_text("Press R to Replay or Q to Quit", 30, WHITE, SCREEN_WIDTH // 2, SCREEN_HEIGHT // 1.5)
    pygame.display.flip()

    waiting = True
    while waiting:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r:  # Replay
                    bird, pipes, score = reset_game()
                    main()
                if event.key == pygame.K_q:  # Quit
                    pygame.quit()
                    sys.exit()

if __name__ == "__main__":
    main()
