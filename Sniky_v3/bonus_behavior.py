# bonus_behavior.py
import pygame

class BonusBehavior:
    def __init__(self, bonus, player):
        self.bonus = bonus
        self.player = player

    def update(self):
        self.bonus.rect.x -= self.bonus.speed_x
        if pygame.sprite.collide_rect(self.bonus, self.player):
            self.bonus.kill()
            self.player.ammo += 1
            if self.player.ammo > 3:
                self.player.ammo = 3
            self.player.flicker_timer = 12  # Flicker effect for 0.2 seconds (12 frames at 60 fps)
