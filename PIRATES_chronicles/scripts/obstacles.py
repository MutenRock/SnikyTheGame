# obstacles.py
import pygame
import random

class Obstacle:
    def __init__(self, image, lane, speed, boat_width, screen_width, screen_height):
        self.image = pygame.transform.scale(pygame.image.load(image), (boat_width, boat_width))
        self.rect = self.image.get_rect()
        self.rect.x = screen_width
        self.lane = lane
        self.speed = speed
        lane_height = screen_height // 5  # 5 lanes
        self.rect.y = self.lane * lane_height + (lane_height - self.rect.height) // 2

    def update(self):
        self.rect.x -= self.speed
        return self.rect.x > -self.rect.width  # Returns False if the obstacle is off the screen

    def draw(self, surface):
        surface.blit(self.image, self.rect)

def spawn_obstacle(obstacle_images, boat_width, screen_width, screen_height, speed):
    lane = random.randint(0, 4)  # Random lane (0 to 4)
    image = random.choice(obstacle_images)
    return Obstacle(image, lane, speed, boat_width, screen_width, screen_height)
