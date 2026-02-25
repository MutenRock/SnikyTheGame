# player.py

class Player:
    def __init__(self, character):
        self.chosen_character = character  # Stores selected character: Sniky, Muten, or Aligax
        self.lives_count = 5  # Initial lives
        self.win_score = 1  # Initial win score
        self.gold_coin = 0  # Initial gold count

    def lose_life(self):
        self.lives_count -= 1

    def add_gold(self, amount):
        self.gold_coin += amount

    def win_level(self):
        self.win_score += 1
        self.gold_coin += 8

    def get_stats(self):
        return {
            "character": self.chosen_character,
            "lives": self.lives_count,
            "win_score": self.win_score,
            "gold": self.gold_coin
        }
