import pygame
import os  # Ajout de l'importation du module os
from settings import WHITE, RED, GREEN, font, screen_width, screen_height, base_dir
from utils import show_text
from main import main_game, options_menu, unlocked_levels, skins_unlocked, selected_skin, skin_sounds

# Charger l'image de fond du menu
background_menu = pygame.image.load(os.path.join(base_dir, 'backgrounds', 'background_menu.png')).convert()

def level_selection_menu(screen, unlocked_levels):
    menu = True
    selected_option = 0

    while menu:
        screen.fill((0, 0, 0))
        show_text('Select Level', font, WHITE, screen, screen_width // 2, screen_height // 4)

        levels_per_row = 5
        rows = 4
        level_width = 200
        level_height = 50
        margin_x = (screen_width - level_width * levels_per_row) // 2
        margin_y = screen_height // 2 - level_height * rows // 2

        for i in range(20):
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
                    selected_option = (selected_option + levels_per_row) % 20
                elif event.key == pygame.K_UP:
                    selected_option = (selected_option - levels_per_row) % 20
                elif event.key == pygame.K_RIGHT:
                    selected_option = (selected_option + 1) % 20
                elif event.key == pygame.K_LEFT:
                    selected_option = (selected_option - 1) % 20
                elif event.key == pygame.K_RETURN:
                    if selected_option < unlocked_levels:
                        main_game(screen, selected_option + 1)
                        menu = False

def skins_menu(screen):
    global selected_skin
    menu = True
    selected_option = 0
    skins = ['normal', 'aligax', 'sniky2', 'mutenrock']

    while menu:
        screen.fill((0, 0, 0))
        show_text('Select Skin', font, WHITE, screen, screen_width // 2, screen_height // 4)

        for i, skin in enumerate(skins):
            color = WHITE
            if i == selected_option:
                color = RED
            show_text(skin.capitalize(), font, color, screen, screen_width // 2, screen_height // 2 + i * 100)

        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_DOWN:
                    selected_option = (selected_option + 1) % len(skins)
                    pygame.mixer.Sound.play(select_sound)
                elif event.key == pygame.K_UP:
                    selected_option = (selected_option - 1) % len(skins)
                    pygame.mixer.Sound.play(select_sound)
                elif event.key == pygame.K_RETURN:
                    selected_skin = skins[selected_option]
                    pygame.mixer.Sound.play(skin_sounds[selected_skin])
                    menu = False

def main_menu(screen, skins_unlocked):
    pygame.mixer.music.load(os.path.join(base_dir, 'musique_menu.mp3'))
    pygame.mixer.music.play(-1)

    menu = True
    selected_option = 0
    options = ["Start", "Options", "Skins", "Quit"]

    while menu:
        screen.fill((0, 0, 0))
        screen.blit(background_menu, ((screen_width - background_menu.get_width()) // 2, 0))
        show_text('Sniky, the Game', font, WHITE, screen, screen_width // 2, screen_height // 4)

        for i, option in enumerate(options):
            color = WHITE
            if i == selected_option:
                color = RED
            if option == "Skins" and not skins_unlocked:
                color = (100, 100, 100)  # Grisé si non déblocable
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
                        level_selection_menu(screen, unlocked_levels)
                    elif selected_option == 1:
                        options_menu(screen)
                    elif selected_option == 2 and skins_unlocked:
                        skins_menu(screen)
                    elif selected_option == 3:
                        pygame.quit()
                        quit()
