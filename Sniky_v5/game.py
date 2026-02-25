import pygame
import os
import random
import time
from utils import show_text
from player import Player
from enemy import Enemy
from bonus import Bonus
from bullet import Bullet
from enemy_behavior import EnemyBehavior1, EnemyBehavior2, EnemyBehavior3, EnemyBehavior4, EnemyBehavior5
from enemies_config import load_enemy_images, enemy_behaviors
from bonus_behavior import BonusBehavior
from bonus_config import load_bonus_images, bonus_behaviors

# Global variables (ensure these are updated as needed)
show_hitboxes = False
music_enabled = True
music_volume = 0.5
unlocked_levels = 1
selected_skin = "normal"

def main_game(screen, current_level, config):
    global show_hitboxes, music_enabled, music_volume, unlocked_levels, selected_skin

    # Determine background based on level
    if current_level <= 5:
        background_file = 'background_level_1.png'
    else:
        background_file = 'background_level_2.png'

    # Load the background image for the current level
    background_game = pygame.image.load(os.path.join(config.base_dir, 'backgrounds', background_file)).convert()
    
    # Define line positions based on screen height and number of lines
    num_lines = len(config.line_positions)
    line_spacing = config.screen_height // num_lines

    # Adjust sprite heights based on line spacing
    player_height = line_spacing
    player = Player(config.player_images, selected_skin, player_height)
    all_sprites = pygame.sprite.Group()
    all_sprites.add(player)
    enemies = pygame.sprite.Group()
    bullets = pygame.sprite.Group()
    bonuses = pygame.sprite.Group()

    clock = pygame.time.Clock()
    running = True
    start_time = time.time()
    enemy_spawn_time = time.time()  # Initial time for enemy spawn
    if current_level >= 7:
        level_duration = 60  # 60 seconds from level 7
    else:
        level_duration = 30  # 30 seconds for lower levels

    if music_enabled:
        pygame.mixer.music.load(os.path.join(config.base_dir, 'music', f'level{current_level}.mp3'))
        pygame.mixer.music.set_volume(music_volume)
        pygame.mixer.music.play(-1)  # Play music indefinitely

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT] and player.rect.left > 0:
            player.rect.x -= player.speed
        if keys[pygame.K_RIGHT] and player.rect.right < config.screen_width:
            player.rect.x += player.speed
        if keys[pygame.K_SPACE]:
            bullet = Bullet(player.rect.centerx, player.rect.top)
            all_sprites.add(bullet)
            bullets.add(bullet)
            if config.shoot_sound:
                config.shoot_sound.play()

        if time.time() - enemy_spawn_time > 2:  # Spawn an enemy every 2 seconds
            enemy_type = random.choice(['enemy1', 'enemy2', 'enemy3', 'enemy4', 'enemy5'])
            enemy = spawn_enemy(enemy_type, config.screen_width, config.screen_height, player_height, config)
            all_sprites.add(enemy)
            enemies.add(enemy)
            enemy_spawn_time = time.time()

        all_sprites.update()

        hits = pygame.sprite.groupcollide(bullets, enemies, True, True)
        for hit in hits:
            score += 10

        if pygame.sprite.spritecollideany(player, enemies):
            running = False
            game_over(screen, score, config)

        screen.blit(background_game, (0, 0))
        all_sprites.draw(screen)
        pygame.display.flip()
        clock.tick(60)

    pygame.quit()

def spawn_enemy(enemy_type, screen_width, screen_height, player_height, config):
    enemy_image = config.enemy_images[enemy_type]
    behavior_class = config.enemy_behaviors[enemy_type]
    enemy = Enemy(enemy_image, random.randint(2, 4), behavior_class, screen_width, screen_height, player_height, config.line_positions)
    return enemy

def level_complete(screen, score, level, config):
    continue_screen = True
    while continue_screen:
        screen.fill(config.BLACK)
        show_text(f'Level {level} Completed!', config.font, config.WHITE, screen, config.screen_width // 2, config.screen_height // 4)
        show_text('Press Enter to continue', config.small_font, config.WHITE, screen, config.screen_width // 2, config.screen_height // 2)
        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            if event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN:
                continue_screen = False
                if level < 20:
                    unlocked_levels = max(unlocked_levels, level + 1)
                    main_game(screen, level + 1, config)
                else:
                    show_leaderboard(screen, score, config)
                if level == 10:
                    global skins_unlocked
                    skins_unlocked = True

def game_over(screen, score, config):
    pygame.mixer.music.stop()
    gameover = True
    while gameover:
        screen.blit(config.background_game_over, (0, 0))
        show_text('Game Over', config.font, config.WHITE, screen, config.screen_width // 2, config.screen_height // 4)
        show_text(f'Score: {score}', config.font, config.WHITE, screen, config.screen_width // 2, config.screen_height // 2)
        show_text('Press any key to return to menu', config.small_font, config.WHITE, screen, config.screen_width // 2, config.screen_height // 2 + 100)
        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            if event.type == pygame.KEYDOWN:
                gameover = False
                from menu import main_menu
                main_menu(screen, config)

def show_leaderboard(screen, score, config):
    # Implement the leaderboard display logic here
    pass
