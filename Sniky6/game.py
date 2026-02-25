import pygame
import random
from enemy import Enemy, load_enemy_images, spawn_enemy
from bonus import Bonus, load_bonus_images, bonus_behaviors

class Player(pygame.sprite.Sprite):
    def __init__(self, images, skin, height):
        super().__init__()
        self.images = images
        self.image = self.images[skin]
        self.rect = self.image.get_rect()
        self.rect.height = height
        self.rect.width = height  # Assuming the width is also scaled accordingly
        self.rect.centerx = 400  # Starting position (adjust as needed)
        self.rect.bottom = 580   # Starting position (adjust as needed)
        self.speed = 5

    def update(self, screen_width):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT] and self.rect.left > 0:
            self.rect.x -= self.speed
        if keys[pygame.K_RIGHT] and self.rect.right < screen_width:
            self.rect.x += self.speed
        if keys[pygame.K_UP] and self.rect.top > 0:
            self.rect.y -= self.speed
        if keys[pygame.K_DOWN] and self.rect.bottom < 600:  # Adjust based on screen height
            self.rect.y += self.speed

    def shoot(self, bullet_group):
        bullet = Bullet(self.rect.centerx, self.rect.top)
        bullet_group.add(bullet)

class Bullet(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.Surface((5, 10))
        self.image.fill((255, 0, 0))  # Red color for the bullet
        self.rect = self.image.get_rect()
        self.rect.centerx = x
        self.rect.bottom = y
        self.speed = -10

    def update(self):
        self.rect.y += self.speed
        if self.rect.bottom < 0:
            self.kill()

def main_game(screen, config):
    # Initialize player
    player = Player(config.player_images, 'normal', 50)  # Example parameters
    all_sprites = pygame.sprite.Group()
    all_sprites.add(player)
    bullets = pygame.sprite.Group()
    enemies = pygame.sprite.Group()
    bonuses = pygame.sprite.Group()

    # Load enemy images
    enemy_images = load_enemy_images(config.base_dir)
    config.enemy_images = enemy_images

    # Load bonus images
    bonus_images = load_bonus_images(config.base_dir)
    config.bonus_images = bonus_images

    # Example enemy spawn
    for _ in range(5):  # Spawn 5 enemies as an example
        enemy = spawn_enemy('enemy1', config.screen_width, config.screen_height, 50, config)
        enemies.add(enemy)
        all_sprites.add(enemy)

    clock = pygame.time.Clock()
    running = True

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                player.shoot(bullets)

        # Spawn bonus randomly
        if random.randint(1, 100) == 1:  # Example: 1% chance to spawn a bonus each frame
            bonus_type = random.choice(['bonus1', 'bonus2', 'bonus3'])
            bonus_image = config.bonus_images[bonus_type]
            bonus = Bonus(bonus_image, bonus_type, random.randint(0, config.screen_width), 0)
            bonuses.add(bonus)
            all_sprites.add(bonus)

        all_sprites.update()
        bullets.update()
        bonuses.update()

        # Collision detection, drawing, etc.
        screen.fill((0, 0, 0))
        all_sprites.draw(screen)
        bullets.draw(screen)
        bonuses.draw(screen)
        pygame.display.flip()
        clock.tick(60)

    pygame.quit()

if __name__ == '__main__':
    from config import GameConfig
    config = GameConfig()
    config.load_fonts()
    pygame.init()
    screen = pygame.display.set_mode((800, 600))
    main_game(screen, config)
