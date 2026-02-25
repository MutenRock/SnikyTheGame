import random

class EnemyBehavior:
    def __init__(self, enemy, screen_width, screen_height, line_positions):
        self.enemy = enemy
        self.screen_width = screen_width
        self.screen_height = screen_height
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
    def __init__(self, enemy, screen_width, screen_height, line_positions):
        super().__init__(enemy, screen_width, screen_height, line_positions)
        self.enemy.changed_line = False

    def update(self):
        if self.enemy.rect.x < self.screen_width // 2 and not self.enemy.changed_line:
            self.enemy.rect.y = random.choice(self.line_positions)
            self.enemy.changed_line = True
        super().update()

class EnemyBehavior4(EnemyBehavior):
    def __init__(self, enemy, screen_width, screen_height, line_positions):
        super().__init__(enemy, screen_width, screen_height, line_positions)
        self.enemy.changed_line = False

    def update(self):
        if self.enemy.rect.x < self.screen_width // 2 and not self.enemy.changed_line:
            self.enemy.rect.y = random.choice(self.line_positions)
            self.enemy.changed_line = True
        self.enemy.speed_x += 0.01  # Accélération progressive
        super().update()

class EnemyBehavior5(EnemyBehavior):
    def __init__(self, enemy, screen_width, screen_height, line_positions):
        super().__init__(enemy, screen_width, screen_height, line_positions)
        self.direction = 1  # 1 for down, -1 for up

    def update(self):
        self.enemy.rect.x -= self.enemy.speed_x
        self.enemy.rect.y += self.direction * self.enemy.speed_x
        if self.enemy.rect.y <= 0 or self.enemy.rect.y >= self.screen_height - self.enemy.rect.height:
            self.direction *= -1  # Change direction
        if self.enemy.rect.x < 0:
            self.enemy.kill()
