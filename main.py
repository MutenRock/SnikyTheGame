# -*- coding: utf-8 -*-
import pygame
import random
import time
import os
from enemy_behavior import EnemyBehavior1, EnemyBehavior2, EnemyBehavior3, EnemyBehavior4, EnemyBehavior5
from enemies_config import load_enemy_images, enemy_behaviors
from bonus_behavior import BonusBehavior
from bonus_config import load_bonus_images, bonus_behaviors

# Initialisation de Pygame
pygame.init()

# Définir le répertoire de base
base_dir = os.path.dirname(os.path.abspath(__file__))

# Dimensions de l'écran - Plein écran
screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
screen_width, screen_height = screen.get_size()
pygame.display.set_caption('Sniky, the Game')

# Couleurs
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
LINE_COLOR = (255, 255, 255, 50)  # Couleur des lignes définies, légèrement transparente

# Police
font = pygame.font.Font(None, 74)
small_font = pygame.font.Font(None, 36)

# Définir les positions de ligne pour le joueur et les ennemis
line_positions = [screen_height // 5, (screen_height // 5) * 2, (screen_height // 5) * 3, (screen_height // 5) * 4]

# Chargement des images de fond
background_menu = pygame.image.load(os.path.join(base_dir, 'backgrounds', 'background_menu.png'))
background_game_over = pygame.image.load(os.path.join(base_dir, 'backgrounds', 'background_destroyed_city.png'))
background_leaderboard = pygame.image.load(os.path.join(base_dir, 'backgrounds', 'background_leaderboard.png'))
background_game = pygame.image.load(os.path.join(base_dir, 'backgrounds', 'background_game.png'))
background_game = pygame.transform.scale(background_game, (int(screen_width * 1.2), screen_height))  # Adapter l'image de fond

# Chargement des sprites du joueur et des bonus
player_images = {
    'normal': pygame.image.load(os.path.join(base_dir, 'sprites', 'player', 'sniky.png')),
    'armed': pygame.image.load(os.path.join(base_dir, 'sprites', 'player', 'sniky_armed.png'))
}
bonus_images = load_bonus_images(base_dir)

# Chargement des images des ennemis
enemy_images = load_enemy_images(base_dir)

# Chargement des musiques et effets sonores
musique_menu = os.path.join(base_dir, 'musique_menu.mp3')
musique_niveaux = [
    os.path.join(base_dir, 'musique_niveau1.mp3'),
    os.path.join(base_dir, 'musique_niveau2.mp3'),
    os.path.join(base_dir, 'musique_niveau3.mp3'),
    os.path.join(base_dir, 'musique_niveau4.mp3'),
    os.path.join(base_dir, 'musique_niveau5.mp3'),
    os.path.join(base_dir, 'musique_niveau6.mp3'),
    os.path.join(base_dir, 'musique_niveau7.mp3'),
    os.path.join(base_dir, 'musique_niveau8.mp3'),
    os.path.join(base_dir, 'musique_niveau9.mp3'),
    os.path.join(base_dir, 'musique_niveau10.mp3')
]
shoot_sound = pygame.mixer.Sound(os.path.join(base_dir, 'sounds', 'shoot.wav'))

# Variables globales
show_hitboxes = False  # Variable de contrôle pour les hitboxes
music_enabled = True  # Musique activée par défaut
music_volume = 0.5  # Volume de la musique à 50% par défaut
unlocked_levels = 1

# Classes pour les entités
class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.images = player_images
        self.image = self.images['normal']
        self.rect = self.image.get_rect()
        self.rect.x = 50
        self.rect.y = line_positions[0]  # Commencer sur la première ligne
        self.line_index = 0  # Index de la ligne actuelle
        self.ammo = 0  # Ajout d'une capacité de tir
        self.flicker_timer = 0  # Timer pour l'effet de frémissement

    def update(self):
        self.rect.y = line_positions[self.line_index]
        if self.ammo > 0:
            self.image = self.images['armed']
        else:
            self.image = self.images['normal']
        if self.flicker_timer > 0:
            self.flicker_timer -= 1
            if self.flicker_timer % 2 == 0:
                self.rect.x += 2
            else:
                self.rect.x -= 2

    def draw_ammo(self):
        if self.ammo > 0:
            ammo_text = small_font.render(str(self.ammo), True, WHITE)
            screen.blit(ammo_text, (self.rect.x, self.rect.y - 20))

    def check_collision(self, enemy):
        if enemy.rect.x <= self.rect.width // 2 and enemy.rect.y == self.rect.y:
            return True
        return False

class Enemy(pygame.sprite.Sprite):
    def __init__(self, image, speed, behavior_class):
        super().__init__()
        self.image = image
        self.rect = self.image.get_rect()
        self.rect.x = screen_width
        self.rect.y = random.choice(line_positions)
        self.speed_x = speed
        self.behavior = behavior_class(self, screen_width, screen_height, line_positions)

    def update(self):
        self.behavior.update()

class Bonus(pygame.sprite.Sprite):
    def __init__(self, image, speed, behavior_class, player):
        super().__init__()
        self.image = image
        self.rect = self.image.get_rect()
        self.rect.x = screen_width
        self.rect.y = random.choice(line_positions)
        self.speed_x = speed
        self.behavior = behavior_class(self, player)

    def update(self):
        self.behavior.update()

class Bullet(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.Surface([20, 8])
        self.image.fill(RED)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

    def update(self):
        self.rect.x += 10
        if self.rect.x > screen_width:
            self.kill()

# Fonctions pour les écrans
def show_text(text, font, color, surface, x, y):
    textobj = font.render(text, True, color)
    textrect = textobj.get_rect()
    textrect.center = (x, y)
    surface.blit(textobj, textrect)

def level_selection_menu():
    global unlocked_levels
    menu = True
    selected_option = 0

    while menu:
        screen.blit(background_menu, (0, 0))
        show_text('Select Level', font, WHITE, screen, screen_width // 2, screen_height // 4)

        levels_per_row = 5
        rows = 2
        level_width = 200
        level_height = 50
        margin_x = (screen_width - level_width * levels_per_row) // 2
        margin_y = screen_height // 2 - level_height * rows // 2

        for i in range(10):
            row = i // levels_per_row
            col = i % levels_per_row
            color = WHITE if i < unlocked_levels else RED
            x = margin_x + col * level_width
            y = margin_y + row * level_height
            show_text(f'Level {i + 1}', font, color, screen, x + level_width // 2, y + level_height // 2)

        # Ajouter un sélecteur visuel pour le niveau sélectionné
        row = selected_option // levels_per_row
        col = selected_option % levels_per_row
        x = margin_x + col * level_width
        y = margin_y + row * level_height
        pygame.draw.rect(screen, GREEN, (x, y, level_width, level_height), 2)

        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_DOWN:
                    selected_option = (selected_option + levels_per_row) % 10
                elif event.key == pygame.K_UP:
                    selected_option = (selected_option - levels_per_row) % 10
                elif event.key == pygame.K_RIGHT:
                    selected_option = (selected_option + 1) % 10
                elif event.key == pygame.K_LEFT:
                    selected_option = (selected_option - 1) % 10
                elif event.key == pygame.K_RETURN:
                    if selected_option < unlocked_levels:
                        main_game(selected_option + 1)
                        menu = False

def main_menu():
    # Jouer la musique du menu
    pygame.mixer.music.load(musique_menu)
    pygame.mixer.music.play(-1)

    menu = True
    selected_option = 0
    options = ["Start", "Options", "Quit"]

    while menu:
        screen.blit(background_menu, (0, 0))
        show_text('Sniky, the Game', font, WHITE, screen, screen_width // 2, screen_height // 4)

        for i, option in enumerate(options):
            color = WHITE
            if i == selected_option:
                color = RED
            show_text(option, font, color, screen, screen_width // 2, screen_height // 2 + i * 100)

        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_DOWN:
                    selected_option = (selected_option + 1) % len(options)
                elif event.key == pygame.K_UP:
                    selected_option = (selected_option - 1) % len(options)
                elif event.key == pygame.K_RETURN:
                    if selected_option == 0:
                        level_selection_menu()
                    elif selected_option == 1:
                        options_menu()
                    elif selected_option == 2:
                        pygame.quit()
                        quit()

def main_game(current_level):
    global show_hitboxes, music_enabled, music_volume
    player = Player()
    all_sprites = pygame.sprite.Group()
    all_sprites.add(player)
    enemies = pygame.sprite.Group()
    bullets = pygame.sprite.Group()
    bonuses = pygame.sprite.Group()

    clock = pygame.time.Clock()
    running = True
    start_time = time.time()
    enemy_spawn_time = time.time()  # Temps initial pour le spawn des ennemis
    if current_level >= 7:
        level_duration = 60  # 60 seconds à partir du niveau 7
    else:
        level_duration = 30  # 30 seconds pour les niveaux inférieurs
    score = 0
    enemy_spawn_interval = level_duration / (current_level * 10)  # Réduire le nombre d'ennemis par niveau
    bonus_spawn_times = [random.uniform(0, 20) for _ in range(current_level)]  # Moments aléatoires pour les bonus

    # Démarrer la musique pour le niveau actuel
    pygame.mixer.music.load(musique_niveaux[current_level - 1])
    pygame.mixer.music.play(-1)  # -1 signifie jouer en boucle
    pygame.mixer.music.set_volume(music_volume)

    def spawn_enemy(enemy_type):
        behavior_class_name = enemy_behaviors[enemy_type]
        behavior_class = globals()[behavior_class_name]
        enemy_image = enemy_images[enemy_type]
        enemy = Enemy(enemy_image, random.randint(2, 4), behavior_class)
        all_sprites.add(enemy)
        enemies.add(enemy)

    def spawn_bonus(bonus_type):
        behavior_class_name = bonus_behaviors[bonus_type]
        behavior_class = globals()[behavior_class_name]
        bonus_image = bonus_images[bonus_type]
        bonus = Bonus(bonus_image, 2, behavior_class, player)
        all_sprites.add(bonus)
        bonuses.add(bonus)

    while running:
        screen.fill(BLACK)
        # Centrer l'image de fond
        screen.blit(background_game, ((screen_width - background_game.get_width()) // 2, 0))
        elapsed_time = time.time() - start_time

        # Accélérer la musique dans les 10 dernières secondes
        if level_duration - elapsed_time <= 10:
            pygame.mixer.music.set_endevent(pygame.USEREVENT + 1)
            if pygame.mixer.music.get_busy() == 0:
                pygame.mixer.music.load(musique_niveaux[current_level - 1])
                pygame.mixer.music.play(-1)
                pygame.mixer.music.set_volume(1.2)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    player.line_index = (player.line_index - 1) % len(line_positions)
                elif event.key == pygame.K_DOWN:
                    player.line_index = (player.line_index + 1) % len(line_positions)
                elif event.key == pygame.K_SPACE and player.ammo > 0:
                    bullet = Bullet(player.rect.x + player.rect.width, player.rect.y + player.rect.height // 2)
                    all_sprites.add(bullet)
                    bullets.add(bullet)
                    player.ammo -= 1
                    shoot_sound.play()

        all_sprites.update()

        # Faire apparaître des ennemis progressivement
        if time.time() - enemy_spawn_time > enemy_spawn_interval:  # Intervalle pour le spawn des ennemis
            if current_level == 1:
                spawn_enemy('enemy1')
            elif current_level == 2:
                spawn_enemy(random.choice(['enemy1', 'enemy2']))
            elif current_level == 3:
                spawn_enemy(random.choice(['enemy1', 'enemy3']))
            elif current_level == 4:
                spawn_enemy(random.choice(['enemy2', 'enemy3']))
            elif current_level == 5:
                spawn_enemy('enemy4')
            elif current_level == 6:
                spawn_enemy('enemy5')
            else:
                spawn_enemy(random.choice(['enemy1', 'enemy2', 'enemy3', 'enemy4', 'enemy5']))
            enemy_spawn_time = time.time()

        # Faire apparaître des bonus
        for bonus_spawn_time in bonus_spawn_times:
            if elapsed_time > bonus_spawn_time:
                spawn_bonus('bonus1')
                bonus_spawn_times.remove(bonus_spawn_time)

        # Vérifier si un ennemi atteint le bord gauche de l'écran sur la même ligne que le joueur
        for enemy in enemies:
            if player.check_collision(enemy):
                running = False
                game_over(score)
            elif enemy.rect.x <= 0:
                enemy.kill()

        for bullet in bullets:
            enemy_hit_list = pygame.sprite.spritecollide(bullet, enemies, True)
            for enemy in enemy_hit_list:
                bullet.kill()
                score += 100

        all_sprites.draw(screen)
        player.draw_ammo()

        # Afficher les hitboxes si l'option est activée
        if show_hitboxes:
            for enemy in enemies:
                pygame.draw.rect(screen, RED, enemy.rect, 1)

        # Afficher le timer
        remaining_time = max(0, level_duration - elapsed_time)
        timer_width = int((remaining_time / level_duration) * screen_width)
        pygame.draw.rect(screen, BLUE, (0, 0, timer_width, 20))  # Augmenter la largeur de la barre bleue

        show_text(f'Score: {score}', small_font, WHITE, screen, screen_width // 2, 30)

        # Ajouter des lignes définies pour les cinq premiers niveaux
        if current_level <= 5:
            for line_y in line_positions:
                pygame.draw.line(screen, LINE_COLOR, (0, line_y + player.rect.height), (screen_width, line_y + player.rect.height), 2)  # Ajouter une fine ligne en bas de chaque ligne

        pygame.display.flip()
        clock.tick(60)

        if elapsed_time > level_duration:
            running = False
            level_completed(score, current_level, player.ammo)

def level_completed(score, level, ammo):
    global unlocked_levels
    pygame.mixer.music.stop()
    continue_screen = True
    while continue_screen:
        screen.fill(BLACK)
        show_text(f'Level {level} Completed!', font, WHITE, screen, screen_width // 2, screen_height // 4)
        show_text('Press Enter to continue', small_font, WHITE, screen, screen_width // 2, screen_height // 2)
        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            if event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN:
                continue_screen = False
                if level < 10:
                    unlocked_levels = max(unlocked_levels, level + 1)
                    main_game(level + 1)
                else:
                    show_leaderboard(score)

def options_menu():
    global show_hitboxes, music_enabled, music_volume
    options = True
    selected_option = 0
    options_list = [
        "Show Hitboxes: OFF",
        "Music: ON",
        "Music Volume: 50%",
        "Back"
    ]

    while options:
        screen.fill(BLACK)
        show_text('Options', font, WHITE, screen, screen_width // 2, screen_height // 4)

        for i, option in enumerate(options_list):
            color = WHITE
            if i == selected_option:
                color = RED
            show_text(option, font, color, screen, screen_width // 2, screen_height // 2 + i * 50)

        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_DOWN:
                    selected_option = (selected_option + 1) % len(options_list)
                elif event.key == pygame.K_UP:
                    selected_option = (selected_option - 1) % len(options_list)
                elif event.key == pygame.K_RETURN:
                    if selected_option == 0:
                        show_hitboxes = not show_hitboxes
                        options_list[0] = f"Show Hitboxes: {'ON' if show_hitboxes else 'OFF'}"
                    elif selected_option == 1:
                        music_enabled = not music_enabled
                        options_list[1] = f"Music: {'ON' if music_enabled else 'OFF'}"
                        if music_enabled:
                            pygame.mixer.music.unpause()
                        else:
                            pygame.mixer.music.pause()
                    elif selected_option == 2:
                        pass  # Handled by left/right keys
                    elif selected_option == 3:
                        options = False
                elif event.key == pygame.K_RIGHT:
                    if selected_option == 2:
                        music_volume = min(100, music_volume + 10)
                        options_list[2] = f"Music Volume: {music_volume}%"
                        pygame.mixer.music.set_volume(music_volume / 100.0)
                elif event.key == pygame.K_LEFT:
                    if selected_option == 2:
                        music_volume = max(0, music_volume - 10)
                        options_list[2] = f"Music Volume: {music_volume}%"
                        pygame.mixer.music.set_volume(music_volume / 100.0)

def game_over(score):
    pygame.mixer.music.stop()
    gameover = True
    while gameover:
        screen.blit(background_game_over, (0, 0))
        show_text('Game Over', font, WHITE, screen, screen_width // 2, screen_height // 4)
        show_text(f'Score: {score}', font, WHITE, screen, screen_width // 2, screen_height // 2)
        show_text('Press any key to return to menu', small_font, WHITE, screen, screen_width // 2, screen_height // 2 + 100)
        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            if event.type == pygame.KEYDOWN:
                gameover = False
                main_menu()

def show_leaderboard(score):
    leaderboard = True
    initials = ""
    while leaderboard:
        screen.blit(background_leaderboard, (0, 0))
        show_text('Game Over', font, WHITE, screen, screen_width // 2, screen_height // 4)
        show_text(f'Score: {score}', font, WHITE, screen, screen_width // 2, screen_height // 2)
        show_text(f'Enter Initials: {initials}', small_font, WHITE, screen, screen_width // 2, screen_height // 2 + 100)
        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            if event.type == pygame.KEYDOWN:
                if event.unicode.isalpha() and len(initials) < 5:
                    initials += event.unicode.upper()
                if event.key == pygame.K_RETURN and len(initials) > 0:
                    with open(os.path.join(base_dir, "leaderboard.txt"), "a") as file:
                        file.write(f'{initials} {score}\n')
                    leaderboard = False
                    main_menu()

main_menu()
pygame.quit()
