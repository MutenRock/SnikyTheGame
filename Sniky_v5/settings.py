import pygame
import os

# Dimensions de l'écran
screen_width = 1024
screen_height = 768

# Couleurs
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
LINE_COLOR = (200, 200, 200)

# Répertoire de base
base_dir = os.path.dirname(os.path.abspath(__file__))

# Lignes de jeu
line_positions = [100, 200, 300, 400]

# Initialisation des polices
pygame.font.init()  # Assurez-vous que Pygame est initialisé
font = pygame.font.Font(None, 74)
small_font = pygame.font.Font(None, 36)
