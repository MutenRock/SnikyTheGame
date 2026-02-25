import pygame
import random  # Ajout de l'importation du module random
from settings import line_positions

class Bonus(pygame.sprite.Sprite):
    def __init__(self, image, speed, behavior_class, player, screen_width):
        super().__init__()
        self.image = image
        self.rect = self.image.get_rect()
        self.rect.x = screen_width
        self.rect.y = random.choice(line_positions)
        self.speed = speed
        self.behavior = behavior_class(self, player, screen_width)

    def update(self):
        self.behavior.update()
        self.rect.x -= self.speed

    def check_collision(self, sprite):
        return self.rect.colliderect(sprite.rect)
