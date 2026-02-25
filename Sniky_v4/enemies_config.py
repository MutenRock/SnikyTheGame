# enemies_config.py
import pygame
import os

def load_enemy_images(base_dir):
    enemy_images = {}
    for i in range(1, 6):  # Assuming you have 5 types of enemies
        image_path = os.path.join(base_dir, f'sprites/enemies/enemy{i}.png')
        image = pygame.image.load(image_path)
        image = pygame.transform.scale(image, (image.get_width() // 5, image.get_height() // 5))  # Adjust the scaling as needed
        enemy_images[f'enemy{i}'] = image
    return enemy_images

# Mapping of enemy types to their behaviors
enemy_behaviors = {
    'enemy1': 'EnemyBehavior1',
    'enemy2': 'EnemyBehavior2',
    'enemy3': 'EnemyBehavior3',
    'enemy4': 'EnemyBehavior4',
    'enemy5': 'EnemyBehavior5'
}
