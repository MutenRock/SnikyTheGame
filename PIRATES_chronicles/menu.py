import pygame
import sys
from run_game import start_game  # Import the game loop from run_game

# Initialize Pygame
pygame.init()

# Constants
FPS = 60
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY = (100, 100, 100)
RED = (255, 0, 0)

# Fonts and Sizes
pygame.font.init()
TITLE_FONT = pygame.font.SysFont("Arial", 80)
MENU_FONT = pygame.font.SysFont("Arial", 40)

# Get screen resolution and set fullscreen
info = pygame.display.Info()
SCREEN_WIDTH, SCREEN_HEIGHT = info.current_w, info.current_h
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.FULLSCREEN)

# Set window caption
pygame.display.set_caption("PIRATE Chronicles")

# Clock
clock = pygame.time.Clock()

# Starter Selection
selected_starter = None
fullscreen = True  # Track fullscreen status

# Helper function to create buttons
def create_button(text, center_pos, font, bg_color, text_color):
    button_surface = font.render(text, True, text_color)
    button_rect = button_surface.get_rect(center=center_pos)
    return button_surface, button_rect

# Display the title screen
def title_screen():
    global selected_starter
    running = True
    while running:
        screen.fill(BLACK)

        # Draw Title
        title_surface = TITLE_FONT.render("PIRATE Chronicles", True, WHITE)
        title_rect = title_surface.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 4))
        screen.blit(title_surface, title_rect)

        # Create buttons
        start_button, start_rect = create_button("Start", (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2), MENU_FONT, GRAY, WHITE)
        options_button, options_rect = create_button("Options", (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 60), MENU_FONT, GRAY, WHITE)
        quit_button, quit_rect = create_button("Quit", (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 120), MENU_FONT, GRAY, WHITE)

        # Draw buttons
        screen.blit(start_button, start_rect)
        screen.blit(options_button, options_rect)
        screen.blit(quit_button, quit_rect)

        # Event Handling
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if start_rect.collidepoint(event.pos):
                    starter_screen()
                elif options_rect.collidepoint(event.pos):
                    options_menu()
                elif quit_rect.collidepoint(event.pos):
                    pygame.quit()
                    sys.exit()

        pygame.display.update()
        clock.tick(FPS)

# Starter selection screen
def starter_screen():
    global selected_starter
    running = True
    while running:
        screen.fill(BLACK)

        # Draw Title
        title_surface = TITLE_FONT.render("Choose Your Starter", True, WHITE)
        title_rect = title_surface.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 4))
        screen.blit(title_surface, title_rect)

        # Starter buttons
        sniky_button, sniky_rect = create_button("Sniky", (SCREEN_WIDTH // 2 - 150, SCREEN_HEIGHT // 2), MENU_FONT, GRAY, WHITE)
        muten_button, muten_rect = create_button("Muten", (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2), MENU_FONT, GRAY, WHITE)
        aligax_button, aligax_rect = create_button("Aligax", (SCREEN_WIDTH // 2 + 150, SCREEN_HEIGHT // 2), MENU_FONT, GRAY, WHITE)
        go_sail_button, go_sail_rect = create_button("GO SAIL", (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 100), MENU_FONT, RED, WHITE)

        # Draw starter buttons
        screen.blit(sniky_button, sniky_rect)
        screen.blit(muten_button, muten_rect)
        screen.blit(aligax_button, aligax_rect)

        # Highlight selected starter
        if selected_starter == "Sniky":
            pygame.draw.rect(screen, RED, sniky_rect, 3)
        elif selected_starter == "Muten":
            pygame.draw.rect(screen, RED, muten_rect, 3)
        elif selected_starter == "Aligax":
            pygame.draw.rect(screen, RED, aligax_rect, 3)

        # Draw "GO SAIL" button (only if starter is selected)
        if selected_starter:
            screen.blit(go_sail_button, go_sail_rect)

        # Event Handling
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if sniky_rect.collidepoint(event.pos):
                    selected_starter = "Sniky"
                elif muten_rect.collidepoint(event.pos):
                    selected_starter = "Muten"
                elif aligax_rect.collidepoint(event.pos):
                    selected_starter = "Aligax"
                elif go_sail_rect.collidepoint(event.pos) and selected_starter:
                    print(f"Starting game with {selected_starter}!")
                    start_game(selected_starter)

        pygame.display.update()
        clock.tick(FPS)

# Options menu
def options_menu():
    global fullscreen
    running = True
    while running:
        screen.fill(BLACK)

        # Draw Options Title
        options_title_surface = TITLE_FONT.render("Options", True, WHITE)
        options_title_rect = options_title_surface.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 4))
        screen.blit(options_title_surface, options_title_rect)

        # Create buttons for fullscreen toggle and return
        toggle_button_text = "Windowed Mode" if fullscreen else "Fullscreen Mode"
        toggle_button, toggle_rect = create_button(toggle_button_text, (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2), MENU_FONT, GRAY, WHITE)
        back_button, back_rect = create_button("Back to Menu", (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 60), MENU_FONT, GRAY, WHITE)

        # Draw buttons
        screen.blit(toggle_button, toggle_rect)
        screen.blit(back_button, back_rect)

        # Event Handling
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if toggle_rect.collidepoint(event.pos):
                    fullscreen = not fullscreen
                    if fullscreen:
                        screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.FULLSCREEN)
                    else:
                        screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
                elif back_rect.collidepoint(event.pos):
                    running = False  # Go back to the main menu

        pygame.display.update()
        clock.tick(FPS)

# Run the game (starting with the title screen)
if __name__ == "__main__":
    title_screen()
