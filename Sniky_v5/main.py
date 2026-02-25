import pygame
from config import GameConfig
from menu import main_menu

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
