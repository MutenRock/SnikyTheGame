import pygame
import random  # Ajout de l'importation du module random
from settings import line_positions

class Enemy(pygame.sprite.Sprite):
    def __init__(self, image, speed, behavior_class, screen_width, sprite_height, line_positions):
        super().__init__()
        self.image = pygame.transform.scale(image, (image.get_width(), sprite_height))
        self.rect = self.image.get_rect()
        self.rect.x = screen_width
        self.rect.y = random.choice(line_positions)
        self.speed = speed
        self.behavior = behavior_class(self, screen_width, screen_height, line_positions)

    def update(self):
        self.behavior.update()
        self.rect.x -= self.speed

    def check_collision(self, sprite):
        return self.rect.colliderect(sprite.rect)

class EnemyBehavior1:
    def __init__(self, enemy, screen_width, screen_height, line_positions):
        self.enemy = enemy
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.line_positions = line_positions

    def update(self):
        pass  # Comportement spécifique de EnemyBehavior1

class EnemyBehavior2:
    def __init__(self, enemy, screen_width, screen_height, line_positions):
        self.enemy = enemy
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.line_positions = line_positions

    def update(self):
        pass  # Comportement spécifique de EnemyBehavior2

class EnemyBehavior3:
    def __init__(self, enemy, screen_width, screen_height, line_positions):
        self.enemy = enemy
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.line_positions = line_positions

    def update(self):
        # Comportement spécifique de EnemyBehavior3
        # Change de ligne à mi-chemin
        if self.enemy.rect.x < self.screen_width // 2:
            self.enemy.rect.y = random.choice(self.line_positions)

class EnemyBehavior4:
    def __init__(self, enemy, screen_width, screen_height, line_positions):
        self.enemy = enemy
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.line_positions = line_positions

    def update(self):
        # Comportement spécifique de EnemyBehavior4
        # Plus rapide que Enemy1 et change de ligne à mi-chemin
        if self.enemy.rect.x < self.screen_width // 2:
            self.enemy.rect.y = random.choice(self.line_positions)
        self.enemy.speed += 0.05

class EnemyBehavior5:
    def __init__(self, enemy, screen_width, screen_height, line_positions):
        self.enemy = enemy
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.line_positions = line_positions
        self.direction = 1

    def update(self):
        # Comportement spécifique de EnemyBehavior5
        # Se déplace en zigzag
        self.enemy.rect.y += self.direction * self.enemy.speed
        if self.enemy.rect.y <= 0 or self.enemy.rect.y >= self.screen_height - self.enemy.rect.height:
            self.direction *= -1
