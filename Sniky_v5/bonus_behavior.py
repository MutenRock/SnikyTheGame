# bonus_behavior.py
import pygame

class BonusBehavior:
    def __init__(self, bonus, player, screen_width):
        self.bonus = bonus
        self.player = player
        self.screen_width = screen_width

    def update(self):
        # Faire avancer le bonus vers le joueur
        self.bonus.rect.x -= self.bonus.speed

        # Vérifier la collision avec le joueur
        if self.bonus.check_collision(self.player):
            self.player.ammo = min(self.player.ammo + 1, 3)  # Limite de munitions à 3
            self.bonus.kill()
