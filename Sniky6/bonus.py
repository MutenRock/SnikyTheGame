import pygame

class Bonus(pygame.sprite.Sprite):
    def __init__(self, image, bonus_type, x, y):
        super().__init__()
        self.image = image
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        self.bonus_type = bonus_type

    def update(self):
        # Bonus update logic
        self.rect.y += 2  # Example: Move down the screen
        if self.rect.top > 600:  # Assuming screen height is 600
            self.kill()

class BonusBehavior:
    def __init__(self, bonus):
        self.bonus = bonus

    def update(self):
        # Behavior update logic
        pass

def load_bonus_images(base_dir):
    bonus_images = {}
    for i in range(1, 4):  # Assuming you have 3 types of bonuses
        image_path = os.path.join(base_dir, f'sprites/bonus/bonus{i}.png')
        image = pygame.image.load(image_path)
        bonus_images[f'bonus{i}'] = image
    return bonus_images

bonus_behaviors = {
    'bonus1': BonusBehavior,
    'bonus2': BonusBehavior,
    'bonus3': BonusBehavior
}
