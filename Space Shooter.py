import pygame
import random
import math
import sys

pygame.init()

# Screen
WIDTH, HEIGHT = 900, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Space Shooter with Particle Effects")

clock = pygame.time.Clock()
font = pygame.font.SysFont("arial", 30)
game_over_font = pygame.font.SysFont("arial", 70)

# Colors
WHITE = (255, 255, 255)
RED = (255, 80, 80)
YELLOW = (255, 220, 100)
BLUE = (100, 150, 255)
BLACK = (0, 0, 0)

# Player
player = pygame.Rect(WIDTH // 2 - 25, HEIGHT - 80, 50, 50)
player_speed = 6

# Bullets
bullets = []
bullet_speed = -8

# Enemies
enemies = []
enemy_spawn_timer = 0

# Score
score = 0
game_over = False

# Stars (background)
stars = [[random.randint(0, WIDTH), random.randint(0, HEIGHT)] for _ in range(80)]

# Particle class
class Particle:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.radius = random.randint(2, 4)
        self.life = random.randint(20, 40)
        angle = random.uniform(0, math.pi * 2)
        speed = random.uniform(1, 4)
        self.vx = math.cos(angle) * speed
        self.vy = math.sin(angle) * speed
        self.color = random.choice([RED, YELLOW])

    def update(self):
        self.x += self.vx
        self.y += self.vy
        self.life -= 1

    def draw(self):
        if self.life > 0:
            pygame.draw.circle(screen, self.color, (int(self.x), int(self.y)), self.radius)

particles = []

# Main Loop
running = True
while running:
    clock.tick(60)
    screen.fill(BLACK)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Star background
    for star in stars:
        star[1] += 1
        if star[1] > HEIGHT:
            star[0] = random.randint(0, WIDTH)
            star[1] = 0
        pygame.draw.circle(screen, WHITE, star, 2)

    if not game_over:
        # Input
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT] and player.left > 0:
            player.x -= player_speed
        if keys[pygame.K_RIGHT] and player.right < WIDTH:
            player.x += player_speed
        if keys[pygame.K_SPACE]:
            if len(bullets) < 5:
                bullets.append(pygame.Rect(player.centerx - 3, player.top, 6, 12))

        # Update bullets
        for bullet in bullets[:]:
            bullet.y += bullet_speed
            pygame.draw.rect(screen, BLUE, bullet)
            if bullet.bottom < 0:
                bullets.remove(bullet)

        # Spawn enemies
        enemy_spawn_timer += 1
        if enemy_spawn_timer > 40:
            enemies.append(pygame.Rect(random.randint(0, WIDTH - 40), -40, 40, 40))
            enemy_spawn_timer = 0

        # Update enemies
        for enemy in enemies[:]:
            enemy.y += 3
            pygame.draw.rect(screen, RED, enemy)

            # GAME OVER condition
            if enemy.colliderect(player):
                game_over = True

                # Explosion effect
                for _ in range(50):
                    particles.append(Particle(player.centerx, player.centery))

            # Bullet collision
            for bullet in bullets[:]:
                if enemy.colliderect(bullet):
                    score += 10
                    enemies.remove(enemy)
                    bullets.remove(bullet)

                    for _ in range(30):
                        particles.append(Particle(enemy.centerx, enemy.centery))
                    break

    # Update particles
    for particle in particles[:]:
        particle.update()
        particle.draw()
        if particle.life <= 0:
            particles.remove(particle)

    # Draw player
    if not game_over:
        pygame.draw.polygon(
            screen,
            BLUE,
            [
                (player.centerx, player.top),
                (player.left, player.bottom),
                (player.right, player.bottom)
            ]
        )

    # UI
    score_text = font.render(f"Score: {score}", True, WHITE)
    screen.blit(score_text, (20, 20))

    # GAME OVER screen
    if game_over:
        text = game_over_font.render("GAME OVER", True, RED)
        screen.blit(text, (WIDTH // 2 - 180, HEIGHT // 2 - 50))

    pygame.display.flip()

pygame.quit()
sys.exit()


