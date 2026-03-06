# enemy_behavior.py
import random

class EnemyBehavior:
    def __init__(self, enemy, screen_width, line_positions):
        self.enemy = enemy
        self.screen_width = screen_width
        self.line_positions = line_positions

    def update(self):
        self.enemy.rect.x -= self.enemy.speed_x
        if self.enemy.rect.x < 0:
            self.enemy.kill()

class EnemyBehavior1(EnemyBehavior):
    def update(self):
        super().update()

class EnemyBehavior2(EnemyBehavior):
    def update(self):
        self.enemy.speed_x += 0.01  # Accélération progressive
        super().update()

class EnemyBehavior3(EnemyBehavior):
    def update(self):
        if self.enemy.rect.x < self.screen_width // 2 and not self.enemy.changed_line:
            self.enemy.rect.y = random.choice(self.line_positions)
            self.enemy.changed_line = True
        super().update()

class EnemyBehavior4(EnemyBehavior):
    def update(self):
        if self.enemy.rect.x < self.screen_width // 2 and not self.enemy.changed_line:
            self.enemy.rect.y = random.choice(self.line_positions)
            self.enemy.changed_line = True
        self.enemy.speed_x += 0.01  # Accélération progressive
        super().update()
