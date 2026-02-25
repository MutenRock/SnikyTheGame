import pygame
import random

class EnemyBehavior1:
    def __init__(self, enemy, screen_width, screen_height, line_positions):
        self.enemy = enemy
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.line_positions = line_positions

    def update(self):
        # Simple downward movement
        self.enemy.rect.y += self.enemy.speed
        if self.enemy.rect.top > self.screen_height:
            self.enemy.kill()

class EnemyBehavior2:
    def __init__(self, enemy, screen_width, screen_height, line_positions):
        self.enemy = enemy
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.line_positions = line_positions

    def update(self):
        # Simple downward movement with a slight horizontal shift
        self.enemy.rect.y += self.enemy.speed
        self.enemy.rect.x += random.choice([-1, 1]) * self.enemy.speed // 2
        if self.enemy.rect.top > self.screen_height:
            self.enemy.kill()

class EnemyBehavior3:
    def __init__(self, enemy, screen_width, screen_height, line_positions):
        self.enemy = enemy
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.line_positions = line_positions

    def update(self):
        if self.enemy.rect.x < self.screen_width // 2:
            self.enemy.rect.y = random.choice(self.line_positions)

class EnemyBehavior4:
    def __init__(self, enemy, screen_width, screen_height, line_positions):
        self.enemy = enemy
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.line_positions = line_positions

    def update(self):
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
        self.fidget_time = 0

    def update(self):
        self.enemy.rect.y += self.direction * self.enemy.speed
        if self.enemy.rect.y <= 0 or self.enemy.rect.y >= self.screen_height - self.enemy.rect.height:
            self.direction *= -1
        if pygame.time.get_ticks() - self.fidget_time > 500:
            self.enemy.rect.x += random.randint(-1, 1)
            self.fidget_time = pygame.time.get_ticks()

class Enemy(pygame.sprite.Sprite):
    def __init__(self, image, speed, behavior_class, screen_width, screen_height, player_height, line_positions):
        super().__init__()
        self.image = image
        self.rect = self.image.get_rect()
        self.speed = speed
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.line_positions = line_positions
        self.behavior = behavior_class(self, screen_width, screen_height, line_positions)

    def update(self):
        self.behavior.update()

def load_enemy_images(base_dir):
    enemy_images = {}
    for i in range(1, 6):  # Assuming you have 5 types of enemies
        image_path = os.path.join(base_dir, f'sprites/enemy/enemy{i}.png')
        image = pygame.image.load(image_path)
        image = pygame.transform.scale(image, (image.get_width() // 5, image.get_height() // 5))  # Adjust the scaling as needed
        enemy_images[f'enemy{i}'] = image
    return enemy_images

enemy_behaviors = {
    'enemy1': EnemyBehavior1,
    'enemy2': EnemyBehavior2,
    'enemy3': EnemyBehavior3,
    'enemy4': EnemyBehavior4,
    'enemy5': EnemyBehavior5
}

def spawn_enemy(enemy_type, screen_width, screen_height, player_height, config):
    enemy_image = config.enemy_images[enemy_type]
    behavior_class = enemy_behaviors[enemy_type]
    enemy = Enemy(enemy_image, random.randint(2, 4), behavior_class, screen_width, screen_height, player_height, config.line_positions)
    enemy.rect.x = random.randint(0, screen_width - enemy.rect.width)
    enemy.rect.y = 0
    return enemy
