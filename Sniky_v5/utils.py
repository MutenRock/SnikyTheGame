import pygame

def show_text(message, font, color, surface, x, y):
    text = font.render(message, True, color)
    rect = text.get_rect(center=(x, y))
    surface.blit(text, rect)
