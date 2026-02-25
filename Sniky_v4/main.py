import pygame
import random
import time
import os

# Initialiser Pygame avant d'importer les paramètres
pygame.init()
pygame.mixer.init()

from settings import font, small_font, WHITE, BLACK, RED, GREEN, BLUE, LINE_COLOR, base_dir
from utils import show_text
from player import Player
from enemy import Enemy
from bonus import Bonus
from bullet import Bullet
from enemy_behavior import EnemyBehavior1, EnemyBehavior2, EnemyBehavior3, EnemyBehavior4, EnemyBehavior5
from enemies_config import load_enemy_images, enemy_behaviors
from bonus_behavior import BonusBehavior
from bonus_config import load_bonus_images, bonus_behaviors

# Obtenez la taille de l'écran
info = pygame.display.Info()
screen_width, screen_height = info.current_w, info.current_h

# Création de l'écran en plein écran fenêtré
screen = pygame.display.set_mode((screen_width, screen_height), pygame.FULLSCREEN | pygame.SCALED)

# Chargement des sprites du joueur et des bonus
player_images = {
    'normal': pygame.image.load(os.path.join(base_dir, 'sprites', 'player', 'sniky.png')),
    'normal_armed': pygame.image.load(os.path.join(base_dir, 'sprites', 'player', 'sniky_armed.png')),
    'aligax': pygame.image.load(os.path.join(base_dir, 'sprites', 'player', 'aligax.png')),
    'aligax_armed': pygame.image.load(os.path.join(base_dir, 'sprites', 'player', 'aligax_armed.png')),
    'mutenrock': pygame.image.load(os.path.join(base_dir, 'sprites', 'player', 'mutenrock.png')),
    'mutenrock_armed': pygame.image.load(os.path.join(base_dir, 'sprites', 'player', 'mutenrock_armed.png')),
    'sniky2': pygame.image.load(os.path.join(base_dir, 'sprites', 'player', 'sniky2.png')),
    'sniky2_armed': pygame.image.load(os.path.join(base_dir, 'sprites', 'player', 'sniky2_armed.png'))
}
bonus_images = load_bonus_images(base_dir)

# Chargement des images des ennemis
enemy_images = load_enemy_images(base_dir)

# Chemin du dossier des musiques
music_folder = os.path.join(base_dir, 'musique_niveaux')

# Charger les musiques
musique_niveaux = [os.path.join(music_folder, file) for file in os.listdir(music_folder) if file.endswith('.mp3')]

# Chargement des effets sonores
shoot_sound = pygame.mixer.Sound(os.path.join(base_dir, 'sounds', 'shoot.wav'))
victory_sound = pygame.mixer.Sound(os.path.join(base_dir, 'sounds', 'victory.wav'))
explosion_sound = pygame.mixer.Sound(os.path.join(base_dir, 'sounds', 'explosion.wav'))

# Chargement des sons de sélection des skins
skin_sounds = {
    'normal': pygame.mixer.Sound(os.path.join(base_dir, 'sounds', 'sniky_intro.wav')),
    'aligax': pygame.mixer.Sound(os.path.join(base_dir, 'sounds', 'aligax_intro.wav')),
    'mutenrock': pygame.mixer.Sound(os.path.join(base_dir, 'sounds', 'mutenrock_intro.wav')),
    'sniky2': pygame.mixer.Sound(os.path.join(base_dir, 'sounds', 'sniky2_intro.wav'))
}

# Chargement des images de fond
background_menu = pygame.image.load(os.path.join(base_dir, 'backgrounds', 'background_menu.png')).convert()
background_game_over = pygame.image.load(os.path.join(base_dir, 'backgrounds', 'background_destroyed_city.png')).convert()

# Variables globales
show_hitboxes = False  # Variable de contrôle pour les hitboxes
music_enabled = True  # Musique activée par défaut
music_volume = 0.5  # Volume de la musique à 50% par défaut
unlocked_levels = 1
skins_unlocked = False  # Option "Skin" déblocable après le niveau 10
selected_skin = 'normal'

# Assurez-vous que les lignes sont définies correctement en fonction de la hauteur du sprite du personnage
player_height = player_images['normal'].get_height()
line_positions = [i for i in range(0, screen_height, player_height)]

def main_game(screen, current_level):
    global show_hitboxes, music_enabled, music_volume, unlocked_levels, skins_unlocked, selected_skin

    # Charger l'image de fond pour le niveau actuel
    background_game = pygame.image.load(os.path.join(base_dir, 'backgrounds', f'background_level_{current_level}.png')).convert()
    
    player = Player(player_images, selected_skin)
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
    total_enemies = current_level * 10

    # Démarrer la musique pour le niveau actuel
    current_music = random.choice(musique_niveaux)
    pygame.mixer.music.load(current_music)
    pygame.mixer.music.play(-1)  # -1 signifie jouer en boucle
    pygame.mixer.music.set_volume(music_volume)

    def spawn_enemy(enemy_type):
        behavior_class_name = enemy_behaviors[enemy_type]
        behavior_class = globals()[behavior_class_name]
        enemy_image = enemy_images[enemy_type]
        enemy = Enemy(enemy_image, random.randint(2, 4), behavior_class, screen_width, screen_height, line_positions)
        all_sprites.add(enemy)
        enemies.add(enemy)

    def spawn_bonus(bonus_type):
        behavior_class_name = bonus_behaviors[bonus_type]
        behavior_class = globals()[behavior_class_name]
        bonus_image = bonus_images[bonus_type]
        bonus = Bonus(bonus_image, 2, behavior_class, player, screen_width)  # Réduction du nombre d'arguments
        all_sprites.add(bonus)
        bonuses.add(bonus)

    def pause_menu(screen):
        paused = True
        pause_options = ["Resume", "Restart", "Main Menu"]
        selected_option = 0

        while paused:
            screen.fill(BLACK)
            show_text('Paused', font, WHITE, screen, screen_width // 2, screen_height // 4)

            for i, option in enumerate(pause_options):
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
                        selected_option = (selected_option + 1) % len(pause_options)
                    elif event.key == pygame.K_UP:
                        selected_option = (selected_option - 1) % len(pause_options)
                    elif event.key == pygame.K_RETURN:
                        if selected_option == 0:  # Resume
                            paused = False
                        elif selected_option == 1:  # Restart
                            main_game(screen, current_level)
                            paused = False
                        elif selected_option == 2:  # Main Menu
                            from menu import main_menu
                            main_menu(screen, skins_unlocked)
                            paused = False

    while running:
        screen.fill(BLACK)
        # Centrer l'image de fond
        screen.blit(background_game, ((screen_width - background_game.get_width()) // 2, 0))
        elapsed_time = time.time() - start_time

        # Accélérer la musique dans les 10 dernières secondes
        if level_duration - elapsed_time <= 10:
            pygame.mixer.music.set_endevent(pygame.USEREVENT + 1)
            if pygame.mixer.music.get_busy() == 0:
                pygame.mixer.music.load(current_music)
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
                elif event.key == pygame.K_ESCAPE:
                    pause_menu(screen)

        all_sprites.update()

        # Faire apparaître des ennemis progressivement
        if time.time() - enemy_spawn_time > enemy_spawn_interval and total_enemies > 0:  # Intervalle pour le spawn des ennemis
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
            total_enemies -= 1

        # Faire apparaître des bonus
        for bonus_spawn_time in bonus_spawn_times:
            if elapsed_time > bonus_spawn_time:
                spawn_bonus('bonus1')
                bonus_spawn_times.remove(bonus_spawn_time)

        # Vérifier si un ennemi atteint le bord gauche de l'écran sur la même ligne que le joueur
        for enemy in enemies:
            if player.check_collision(enemy):
                running = False
                game_over(screen, score)
            elif enemy.rect.x <= 0:
                enemy.kill()

        for bullet in bullets:
            enemy_hit_list = pygame.sprite.spritecollide(bullet, enemies, True)
            for enemy in enemy_hit_list:
                bullet.kill()
                score += 100

        all_sprites.draw(screen)
        player.draw_ammo(screen)

        # Afficher les hitboxes si l'option est activée
        if show_hitboxes:
            for enemy in enemies:
                pygame.draw.rect(screen, RED, enemy.rect, 1)

        # Afficher le timer
        remaining_time = max(0, level_duration - elapsed_time)
        timer_width = int((remaining_time / level_duration) * screen_width)
        pygame.draw.rect(screen, BLUE, (0, 0, timer_width, 20))  # Augmenter la largeur de la barre bleue

        show_text(f'Score: {score}', small_font, WHITE, screen, screen_width // 2, 30)

        # Ajouter des lignes définies pour le premier niveau
        if current_level == 1:
            for line_y in line_positions:
                pygame.draw.line(screen, LINE_COLOR, (0, line_y + player.rect.height), (screen_width, line_y + player.rect.height), 2)  # Ajouter une fine ligne en bas de chaque ligne

        pygame.display.flip()
        clock.tick(60)

        if elapsed_time > level_duration:
            running = False
            level_completed(screen, score, current_level, player.ammo)

def level_completed(screen, score, level, ammo):
    global unlocked_levels
    pygame.mixer.music.stop()
    victory_sound.play()
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
                if level < 20:
                    unlocked_levels = max(unlocked_levels, level + 1)
                    main_game(screen, level + 1)
                else:
                    show_leaderboard(screen, score)
                if level == 10:
                    global skins_unlocked
                    skins_unlocked = True

def options_menu(screen):
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

def game_over(screen, score):
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
                from menu import main_menu
                main_menu(screen, skins_unlocked)

def show_leaderboard(screen, score):
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
                    from menu import main_menu
                    main_menu(screen, skins_unlocked)

# Démarrage du jeu
if __name__ == "__main__":
    from menu import main_menu
    main_menu(screen, skins_unlocked)
    pygame.quit()
