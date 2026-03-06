# -*- coding: utf-8 -*-
import pygame
import random
import time
import os

# Initialisation de Pygame
pygame.init()

# Définir le répertoire de base
base_dir = os.path.dirname(os.path.abspath(__file__))

# Dimensions de l'écran
screen_width = 2690
screen_height = 1024
screen = pygame.display.set_mode((screen_width, screen_height))
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
line_positions = [screen_height // 5 - 20, (screen_height // 5) * 2 - 20, (screen_height // 5) * 3 - 20, (screen_height // 5) * 4 - 20]

# Chargement des images de fond
background_menu = pygame.image.load(os.path.join(base_dir, 'backgrounds', 'background_menu.png'))
background_game_over = pygame.image.load(os.path.join(base_dir, 'backgrounds', 'background_destroyed_city.png'))
background_leaderboard = pygame.image.load(os.path.join(base_dir, 'backgrounds', 'background_leaderboard.png'))
background_game = pygame.image.load(os.path.join(base_dir, 'backgrounds', 'background_game.png'))
background_game = pygame.transform.scale(background_game, (int(screen_width * 1.2), screen_height))  # Adapter l'image de fond


# Chargement des sprites (les images doivent être générées et placées dans le dossier du projet)
sniky_image = pygame.image.load(os.path.join(base_dir, 'sprites', 'player', 'sniky.png'))
enemy1_image = pygame.image.load(os.path.join(base_dir, 'sprites', 'enemies', 'enemy1.png'))
enemy1_image = pygame.transform.scale(enemy1_image, (enemy1_image.get_width() // 5, enemy1_image.get_height() // 5))  # Redimensionner l'image de l'ennemi
enemy2_image = pygame.image.load(os.path.join(base_dir, 'sprites', 'enemies', 'enemy2.png'))
enemy2_image = pygame.transform.scale(enemy2_image, (enemy2_image.get_width() // 5, enemy2_image.get_height() // 5))  # Redimensionner l'image de l'ennemi
enemy3_image = pygame.image.load(os.path.join(base_dir, 'sprites', 'enemies', 'enemy3.png'))
enemy3_image = pygame.transform.scale(enemy3_image, (enemy3_image.get_width() // 5, enemy3_image.get_height() // 5))  # Redimensionner l'image de l'ennemi
enemy4_image = pygame.image.load(os.path.join(base_dir, 'sprites', 'enemies', 'enemy4.png'))
enemy4_image = pygame.transform.scale(enemy4_image, (enemy4_image.get_width() // 5, enemy4_image.get_height() // 5))  # Redimensionner l'image de l'ennemi
bonus_image = pygame.image.load(os.path.join(base_dir, 'sprites', 'items', 'weapon.png'))
bonus_image = pygame.transform.scale(bonus_image, (bonus_image.get_width() // 6, bonus_image.get_height() // 6))  # Redimensionner l'image du bonus

# Chargement des musiques
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

# Variables globales
show_hitboxes = False  # Variable de contrôle pour les hitboxes
unlocked_levels = 1

# Classes pour les entités
class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = sniky_image
        self.rect = self.image.get_rect()
        self.rect.x = 50
        self.rect.y = line_positions[0]  # Commencer sur la première ligne
        self.line_index = 0  # Index de la ligne actuelle
        self.ammo = 0  # Ajout d'une capacité de tir
        self.flicker_timer = 0  # Timer pour l'effet de frémissement

    def update(self):
        self.rect.y = line_positions[self.line_index]
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

class Enemy(pygame.sprite.Sprite):
    def __init__(self, image, speed):
        super().__init__()
        self.image = image
        self.rect = self.image.get_rect()
        self.rect.x = screen_width
        self.rect.y = random.choice(line_positions)
        self.speed_x = speed

    def update(self):
        self.rect.x -= self.speed_x
        if self.rect.x < 0:
            self.kill()

class Bonus(pygame.sprite.Sprite):
    def __init__(self, player):
        super().__init__()
        self.image = bonus_image
        self.rect = self.image.get_rect()
        self.rect.x = screen_width
        self.rect.y = random.choice(line_positions)
        self.speed_x = 2
        self.player = player  # Stocker la référence au joueur

    def update(self):
        self.rect.x -= self.speed_x
        if pygame.sprite.collide_rect(self, self.player):
            self.kill()
            self.player.ammo += 3
            if self.player.ammo > 10:
                self.player.ammo = 10
            self.player.flicker_timer = 12  # Frémissement pendant 0.2 seconde (12 frames à 60 fps)

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

        for i in range(10):
            color = WHITE if i < unlocked_levels else RED
            show_text(f'Level {i + 1}', font, color, screen, screen_width // 2, screen_height // 2 + i * 50)

        # Ajouter un sélecteur visuel pour le niveau sélectionné
        pygame.draw.rect(screen, GREEN, (screen_width // 2 - 100, screen_height // 2 + selected_option * 50 - 25, 200, 50), 2)

        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_DOWN:
                    selected_option = (selected_option + 1) % 10
                elif event.key == pygame.K_UP:
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

# Dimensions de l'écran
screen_width = 1024
screen_height = 1345
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption('Sniky, the Game')

# Centrer les images de fond
background_game = pygame.image.load(os.path.join(base_dir, 'backgrounds', 'background_game.png'))
background_game = pygame.transform.scale(background_game, (int(screen_width * 1.2), screen_height))  # Adapter l'image de fond

# Fonction de jeu principale
def main_game(current_level):
    global show_hitboxes
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

    while running:
        screen.fill(BLACK)
        # Centrer l'image de fond
        screen.blit(background_game, ((screen_width - background_game.get_width()) // 2, 0))
        elapsed_time = time.time() - start_time

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

        all_sprites.update()

        # Faire apparaître des ennemis progressivement
        if time.time() - enemy_spawn_time > enemy_spawn_interval:  # Intervalle pour le spawn des ennemis
            if current_level == 1:
                enemy = Enemy(enemy1_image, random.randint(2, 3))
            elif current_level == 2:
                enemy = random.choice([Enemy(enemy1_image, random.randint(2, 3)), Enemy(enemy2_image, random.randint(3, 4))])
            elif current_level == 3:
                enemy = random.choice([Enemy(enemy1_image, random.randint(2, 3)), Enemy(enemy3_image, random.randint(2, 3))])
            elif current_level == 4:
                enemy = random.choice([Enemy(enemy2_image, random.randint(3, 4)), Enemy(enemy3_image, random.randint(2, 3))])
            elif current_level == 5:
                enemy = Enemy(enemy4_image, random.randint(3, 4))
            else:
                enemy = random.choice([Enemy(enemy1_image, random.randint(2, 3)), Enemy(enemy2_image, random.randint(3, 4)), Enemy(enemy3_image, random.randint(2, 3)), Enemy(enemy4_image, random.randint(3, 4))])
            all_sprites.add(enemy)
            enemies.add(enemy)
            enemy_spawn_time = time.time()

        # Faire apparaître des bonus
        for bonus_spawn_time in bonus_spawn_times:
            if elapsed_time > bonus_spawn_time:
                bonus = Bonus(player)
                all_sprites.add(bonus)
                bonuses.add(bonus)
                bonus_spawn_times.remove(bonus_spawn_time)

        # Vérifier si un ennemi atteint le bord gauche de l'écran sur la même ligne que le joueur
        for enemy in enemies:
            if enemy.rect.x <= 0 and enemy.rect.y == player.rect.y:
                running = False
                game_over(score)

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
                pygame.draw.line(screen, LINE_COLOR, (0, line_y + 60), (screen_width, line_y + 60), 2)  # Ajouter une fine ligne en bas de chaque ligne

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
    global show_hitboxes
    options = True
    selected_option = 0
    options_list = ["Show Hitboxes: OFF", "Back"]

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
                        options = False

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
