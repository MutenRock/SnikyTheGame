
import pygame
import os

class GameConfig:
    def __init__(self):
        self.base_dir = os.path.dirname(os.path.abspath(__file__))
        self.font = None
        self.small_font = None
        self.screen_width = 0
        self.screen_height = 0
        self.background_menu = None
        self.player_images = {}
        self.bonus_images = {}
        self.enemy_images = {}
        self.musique_niveaux = []
        self.shoot_sound = None
        self.victory_sound = None
        self.background_game_over = None
        self.line_positions = [100, 200, 300, 400, 500, 600]
        self.WHITE = (255, 255, 255)
        self.BLACK = (0, 0, 0)
        self.RED = (255, 0, 0)
        self.BLUE = (0, 0, 255)
        self.LINE_COLOR = (100, 100, 100)
        self.skins_unlocked = False

    def load_fonts(self):
        self.font = pygame.font.Font(None, 74)
        self.small_font = pygame.font.Font(None, 36)

    def load_resources(self, screen_width, screen_height):
        self.screen_width = screen_width
        self.screen_height = screen_height

        self.background_menu = pygame.image.load(os.path.join(self.base_dir, 'backgrounds', 'background_menu.png')).convert()
        self.background_game_over = pygame.image.load(os.path.join(self.base_dir, 'backgrounds', 'background_game_over.png')).convert()

        self.player_images = {
            'normal': pygame.image.load(os.path.join(self.base_dir, 'sprites', 'player', 'normal.png')),
            'normal_armed': pygame.image.load(os.path.join(self.base_dir, 'sprites', 'player', 'normal_armed.png')),
            'aligax': pygame.image.load(os.path.join(self.base_dir, 'sprites', 'player', 'aligax.png')),
            'aligax_armed': pygame.image.load(os.path.join(self.base_dir, 'sprites', 'player', 'aligax_armed.png')),
            'mutenrock': pygame.image.load(os.path.join(self.base_dir, 'sprites', 'player', 'mutenrock.png')),
            'mutenrock_armed': pygame.image.load(os.path.join(self.base_dir, 'sprites', 'player', 'mutenrock_armed.png')),
            'sniky': pygame.image.load(os.path.join(self.base_dir, 'sprites', 'player', 'sniky.png')),
            'sniky_armed': pygame.image.load(os.path.join(self.base_dir, 'sprites', 'player', 'sniky_armed.png')),
            'sniky2': pygame.image.load(os.path.join(self.base_dir, 'sprites', 'player', 'sniky2.png')),
            'sniky2_armed': pygame.image.load(os.path.join(self.base_dir, 'sprites', 'player', 'sniky2_armed.png')),
        }

        self.shoot_sound = pygame.mixer.Sound(os.path.join(self.base_dir, 'sounds', 'shoot.wav'))


