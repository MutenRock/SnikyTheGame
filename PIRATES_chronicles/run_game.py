import pygame
import random

# Initialize Pygame
pygame.init()

# Get screen resolution from menu.py dimensions (fullscreen)
info = pygame.display.Info()
SCREEN_WIDTH, SCREEN_HEIGHT = info.current_w, info.current_h
FPS = 60
LIVES = 5
LANE_COUNT = 5  # Number of vertical "lanes" or corridors
LANE_HEIGHT = SCREEN_HEIGHT // LANE_COUNT  # Height of each lane

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

# Scaling constants
BOAT_SCALE_FACTOR = 1 / 20  # Boat should be 1/20th of screen width
GOLD_COIN_SCORE = 10  # Gold collected per coin

# Setup screen
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("PIRATE Chronicles")

# Load boat sprite and scale it
boat_image_raw = pygame.image.load('assets/images/boat.png')
boat_width = int(SCREEN_WIDTH * BOAT_SCALE_FACTOR)  # Boat width is 1/20 of screen width
boat_image = pygame.transform.scale(boat_image_raw, (boat_width, boat_width))  # Square image

# Base size for obstacles (1 boat unit in width)
obstacle_size = boat_width

# Gold coin image (placeholder)
gold_image_raw = pygame.image.load('assets/images/gold_coin.png')
gold_image = pygame.transform.scale(gold_image_raw, (boat_width, boat_width))  # Scale to 1 BOAT width

# Boat (Player) Class
class Boat:
    def __init__(self, starter):
        self.image = boat_image
        self.rect = self.image.get_rect()
        self.rect.x = 50  # Starting position on the left
        self.current_lane = LANE_COUNT // 2  # Start in the middle lane
        self.speed = boat_width  # Move by the height of 1 boat
        self.starter = starter
        self.update_position()

    def update_position(self):
        """ Update the boat's position based on its current lane. """
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

# Obstacle Class
class Obstacle:
    def __init__(self, image, lane, speed):
        self.image = pygame.transform.scale(pygame.image.load(image), (obstacle_size, obstacle_size))
        self.rect = self.image.get_rect()
        self.rect.x = SCREEN_WIDTH
        self.lane = lane
        self.speed = speed
        self.rect.y = self.lane * LANE_HEIGHT + (LANE_HEIGHT - self.rect.height) // 2

    def update(self):
        self.rect.x -= self.speed
        if self.rect.x < -self.rect.width:  # Remove if out of screen
            return False
        return True

    def draw(self, surface):
        surface.blit(self.image, self.rect)

# Gold Coin Class
class GoldCoin:
    def __init__(self, lane):
        self.image = gold_image
        self.rect = self.image.get_rect()
        self.rect.x = SCREEN_WIDTH
        self.lane = lane
        self.rect.y = self.lane * LANE_HEIGHT + (LANE_HEIGHT - self.rect.height) // 2

    def update(self):
        self.rect.x -= ENEMY_SPEED
        if self.rect.x < -self.rect.width:  # Remove if out of screen
            return False
        return True

    def draw(self, surface):
        surface.blit(self.image, self.rect)

# Main game loop
def start_game(starter):
    print(f"Starting game with {starter}")
    clock = pygame.time.Clock()
    boat = Boat(starter)

    # Load obstacle images (placeholders)
    obstacle_images = [
        'assets/images/rock.png',
        'assets/images/barrel.png',
        'assets/images/bomb.png'
    ]
    obstacles = []
    gold_coins = []
    lives = LIVES
    score = 0  # Track player's score (gold count)

    running = True

    while running:
        screen.fill(BLACK)
        boat.draw(screen)

        # Handle events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        # Player input (Up/Down)
        keys = pygame.key.get_pressed()
        if keys[pygame.K_UP]:
            boat.move_up()
        if keys[pygame.K_DOWN]:
            boat.move_down()

        # Spawn random obstacles in random lanes
        if random.randint(0, 100) < 3:  # 3% chance to spawn each frame
            lane = random.randint(0, LANE_COUNT - 1)
            new_obstacle = Obstacle(random.choice(obstacle_images), lane, ENEMY_SPEED)
            obstacles.append(new_obstacle)

        # Spawn gold coin randomly
        if random.randint(0, 500) < 2:  # Rare chance to spawn a gold coin
            lane = random.randint(0, LANE_COUNT - 1)
            new_gold_coin = GoldCoin(lane)
            gold_coins.append(new_gold_coin)

        # Update obstacles
        for obstacle in obstacles[:]:
            if not obstacle.update():
                obstacles.remove(obstacle)
            obstacle.draw(screen)

        # Update gold coins
        for coin in gold_coins[:]:
            if not coin.update():
                gold_coins.remove(coin)
            coin.draw(screen)

        # Collision detection (obstacles)
        for obstacle in obstacles:
            if boat.rect.colliderect(obstacle.rect):
                lives -= 1
                obstacles.remove(obstacle)
                print(f"Hit! Lives left: {lives}")
                if lives == 0:
                    print("Game Over!")
                    running = False  # Game Over

        # Collision detection (gold coins)
        for coin in gold_coins[:]:
            if boat.rect.colliderect(coin.rect):
                score += GOLD_COIN_SCORE
                gold_coins.remove(coin)
                print(f"Collected gold! Total gold: {score}")

        # Update screen
        pygame.display.flip()
        clock.tick(FPS)

    pygame.quit()
