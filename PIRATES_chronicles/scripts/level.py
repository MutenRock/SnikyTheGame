# level.py

import pygame
import random
from scripts.player import Player
from scripts.obstacles import spawn_obstacle
from scripts.obstacles import Obstacle

# Constants
FPS = 60
SCREEN_WIDTH, SCREEN_HEIGHT = pygame.display.Info().current_w, pygame.display.Info().current_h
LANE_COUNT = 5
LANE_HEIGHT = SCREEN_HEIGHT // LANE_COUNT
BOAT_SCALE_FACTOR = 1 / 20

# Initialize Pygame
pygame.init()

# Load images
boat_image_raw = pygame.image.load('assets/images/boat.png')
boat_width = int(SCREEN_WIDTH * BOAT_SCALE_FACTOR)
boat_image = pygame.transform.scale(boat_image_raw, (boat_width, boat_width))

obstacle_images = ['assets/images/rock.png', 'assets/images/barrel.png', 'assets/images/bomb.png']
gold_image_raw = pygame.image.load('assets/images/gold_coin.png')
gold_image = pygame.transform.scale(gold_image_raw, (boat_width, boat_width))

# Boat class
class Boat:
    def __init__(self, player):
        self.image = boat_image
        self.rect = self.image.get_rect()
        self.rect.x = 50  # Start position
        self.current_lane = LANE_COUNT // 2  # Start in the middle lane
        self.speed = boat_width  # Move by the height of 1 boat
        self.player = player
        self.update_position()

    def update_position(self):
        self.rect.y = self.current_lane * LANE_HEIGHT + (LANE_HEIGHT - self.rect.height) // 2

    def move_up(self):
        if self.current_lane > 0:
            self.current_lane -= 1
            self.update_position()

    def move_down(self):
        if self.current_lane < LANE_COUNT - 1:
            self.current_lane += 1
            self.update_position()

    def draw(self, surface):
        surface.blit(self.image, self.rect)

# Main game loop
def sailing_phase(player):
    clock = pygame.time.Clock()
    boat = Boat(player)
    obstacles = []
    gold_coins = []
    running = True
    level_time = 60  # 1-minute level

    start_ticks = pygame.time.get_ticks()  # For tracking time

    while running:
        screen.fill((0, 0, 0))  # Black background

        elapsed_seconds = (pygame.time.get_ticks() - start_ticks) / 1000
        if elapsed_seconds >= level_time:
            player.win_level()  # Player wins the level
            return "win"

        # Event handling
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        # Player movement (up/down)
        keys = pygame.key.get_pressed()
        if keys[pygame.K_UP]:
            boat.move_up()
        if keys[pygame.K_DOWN]:
            boat.move_down()

        # Spawn obstacles (scaled by player.win_score)
        if random.random() < (0.05 * (1 + player.win_score) / FPS):  # Dynamic spawn rate
            obstacles.append(spawn_obstacle(obstacle_images, boat_width, SCREEN_WIDTH, SCREEN_HEIGHT, 5 + player.win_score))

        # Update obstacles
        for obstacle in obstacles[:]:
            if not obstacle.update():
                obstacles.remove(obstacle)
            obstacle.draw(screen)

        # Display player stats (lives, gold, etc.)
        font = pygame.font.SysFont('Arial', 30)
        lives_text = font.render(f"Lives: {player.lives_count}", True, (255, 255, 255))
        screen.blit(lives_text, (10, 10))

        # Update screen
        pygame.display.flip()
        clock.tick(FPS)
