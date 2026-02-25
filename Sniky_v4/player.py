import pygame
from settings import line_positions, small_font, WHITE

class Player(pygame.sprite.Sprite):
    def __init__(self, player_images, selected_skin):
        super().__init__()
        self.images = player_images
        self.selected_skin = selected_skin
        self.image = self.images[self.selected_skin]
        self.rect = self.image.get_rect()
        self.rect.x = 50
        self.rect.y = line_positions[0]  # Commencer sur la première ligne
        self.line_index = 0  # Index de la ligne actuelle
        self.ammo = 0  # Ajout d'une capacité de tir
        self.flicker_timer = 0  # Timer pour l'effet de frémissement

    def update(self):
        if self.ammo > 0:
            self.image = self.images[f'{self.selected_skin}_armed']
        else:
            self.image = self.images[self.selected_skin]
        self.rect.y = line_positions[self.line_index]
        if self.flicker_timer > 0:
            self.flicker_timer -= 1
            if self.flicker_timer % 2 == 0:
                self.rect.x += 2
            else:
                self.rect.x -= 2

    def draw_ammo(self, screen):
        if self.ammo > 0:
            ammo_text = small_font.render(str(self.ammo), True, WHITE)
            screen.blit(ammo_text, (self.rect.x, self.rect.y - 20))

    def check_collision(self, enemy):
        if enemy.rect.x <= self.rect.width // 2 and enemy.rect.y == self.rect.y:
            return True
        return False
