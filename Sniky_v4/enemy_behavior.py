import random

class EnemyBehavior1:
    def __init__(self, enemy, screen_width, screen_height, line_positions):
        self.enemy = enemy
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.line_positions = line_positions

    def update(self):
        pass  # Comportement spécifique de EnemyBehavior1

class EnemyBehavior2:
    def __init__(self, enemy, screen_width, screen_height, line_positions):
        self.enemy = enemy
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.line_positions = line_positions

    def update(self):
        pass  # Comportement spécifique de EnemyBehavior2

class EnemyBehavior3:
    def __init__(self, enemy, screen_width, screen_height, line_positions):
        self.enemy = enemy
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.line_positions = line_positions

    def update(self):
        # Comportement spécifique de EnemyBehavior3
        # Change de ligne à mi-chemin
        if self.enemy.rect.x < self.screen_width // 2:
            self.enemy.rect.y = random.choice(self.line_positions)

class EnemyBehavior4:
    def __init__(self, enemy, screen_width, screen_height, line_positions):
        self.enemy = enemy
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.line_positions = line_positions

    def update(self):
        # Comportement spécifique de EnemyBehavior4
        # Plus rapide que Enemy1 et change de ligne à mi-chemin
        if self.enemy.rect.x < self.screen_width // 2:
            self.enemy.rect.y = random.choice(self.line_positions)
        self.enemy.speed += 0.05  # Utilisation de l'attribut 'speed'

class EnemyBehavior5:
    def __init__(self, enemy, screen_width, screen_height, line_positions):
        self.enemy = enemy
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.line_positions = line_positions
        self.direction = 1
        self.fidget_time = 0

    def update(self):
        # Comportement spécifique de EnemyBehavior5
        # Se déplace en zigzag
        self.enemy.rect.y += self.direction * self.enemy.speed
        if self.enemy.rect.y <= 0 or self.enemy.rect.y >= self.screen_height - self.enemy.rect.height:
            self.direction *= -1

        # Ajouter un léger mouvement de frétiment à intervalle régulier
        if pygame.time.get_ticks() - self.fidget_time > 500:  # Intervalle de 500 ms
            self.enemy.rect.x += random.randint(-1, 1)
            self.fidget_time = pygame.time.get_ticks()
