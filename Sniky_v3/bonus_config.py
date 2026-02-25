# bonus_config.py
import pygame
import os

def load_bonus_images(base_dir):
    bonus_images = {}
    for i in range(1, 2):  # Assuming you have 1 type of bonus for now
        image_path = os.path.join(base_dir, f'sprites/items/bonus{i}.png')
        image = pygame.image.load(image_path)
        image = pygame.transform.scale(image, (image.get_width() // 6, image.get_height() // 6))  # Adjust the scaling as needed
        bonus_images[f'bonus{i}'] = image
    return bonus_images

# Mapping of bonus types to their behaviors
bonus_behaviors = {
    'bonus1': 'BonusBehavior'
}
