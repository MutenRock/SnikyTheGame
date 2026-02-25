import pygame

class Player(pygame.sprite.Sprite):
    def __init__(self, images, selected_skin, sprite_height):
        super().__init__()
        self.images = images
        self.selected_skin = selected_skin
        self.image = pygame.transform.scale(self.images[self.selected_skin], (self.images[self.selected_skin].get_width(), sprite_height))
        self.rect = self.image.get_rect()
        self.line_index = 0
        self.ammo = 10

    def update(self):
        # Mettre à jour la position verticale en fonction de la ligne actuelle
        self.rect.y = self.line_index * self.rect.height

    def draw_ammo(self, screen):
        pass  # Implement the ammo drawing logic

    def check_collision(self, other):
        return self.rect.colliderect(other.rect)
