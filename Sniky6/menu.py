import pygame
from config import GameConfig
from utils import show_text
from game import main_game

def main_menu(screen, config):
    try:
        config.load_resources(screen.get_width(), screen.get_height())
        print("Resources loaded successfully.")
    except Exception as e:
        print(f"Error loading resources: {e}")
        return

    running = True
    print("Entering main menu loop.")

    while running:
        screen.fill((0, 0, 0))
        show_text('Sniky, The Game', config.font, config.WHITE, screen, screen.get_width() // 2, screen.get_height() // 2)

        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                print("Exiting game.")
                quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    print("Enter key pressed, going to level selection menu.")
                    level_selection_menu(screen, config)
                if event.key == pygame.K_ESCAPE:
                    print("Escape key pressed, exiting main menu.")
                    running = False

    print("Exiting main menu loop.")

def level_selection_menu(screen, config):
    menu = True
    selected_level = 0
    levels = [f"Level {i+1}" for i in range(10)]
    print("Entering level selection menu loop.")

    while menu:
        screen.fill((0, 0, 0))
        show_text('Level Selection', config.font, config.WHITE, screen, screen.get_width() // 2, screen.get_height() // 4)

        for i, level in enumerate(levels):
            color = config.WHITE
            if i == selected_level:
                color = config.RED
            show_text(level, config.font, color, screen, screen.get_width() // 2, screen.get_height() // 2 + i * 50)

        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                print("Exiting game from level selection menu.")
                quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_DOWN:
                    selected_level = (selected_level + 1) % len(levels)
                    print(f"Down key pressed, selected level: {selected_level}")
                elif event.key == pygame.K_UP:
                    selected_level = (selected_level - 1) % len(levels)
                    print(f"Up key pressed, selected level: {selected_level}")
                elif event.key == pygame.K_RETURN:
                    print(f"Enter key pressed, starting level {selected_level + 1}.")
                    main_game(screen, selected_level + 1, config)
                    menu = False

    print("Exiting level selection menu loop.")

if __name__ == "__main__":
    try:
        config = GameConfig()
        config.load_fonts()
        print("Fonts loaded successfully.")
    except Exception as e:
        print(f"Error loading fonts: {e}")
        quit()

    try:
        pygame.init()
        screen = pygame.display.set_mode((pygame.display.Info().current_w, pygame.display.Info().current_h), pygame.NOFRAME | pygame.SCALED)
        print("Pygame initialized and screen set.")
    except Exception as e:
        print(f"Error initializing Pygame or setting screen: {e}")
        quit()

    main_menu(screen, config)
