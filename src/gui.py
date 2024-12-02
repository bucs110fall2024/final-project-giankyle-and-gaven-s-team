import pygame
import sys

pygame.init()

# Screen dimensions and setup
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Stock Predictor")

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
BLUE = (52, 152, 219)  # Default color (Blue)
LIGHT_BLUE = (41, 128, 185)
BRIGHT_RED = (255, 0, 0)
SHADOW_COLOR = (200, 200, 200)
GREEN = (39, 174, 96)  # Turned green when clicked

# Fonts
font = pygame.font.Font(None, 36)
title_font = pygame.font.Font(None, 48)

# Global state
current_screen = "home"  # Tracks the current screen
home_button_clicked = False  # Tracks if the home button was clicked

# Button definitions
def create_button(x, y, width, height):
    return pygame.Rect(x, y, width, height)

home_button = create_button(SCREEN_WIDTH - 170, SCREEN_HEIGHT - 70, 150, 50)
end_button = create_button(20, SCREEN_HEIGHT - 70, 150, 50)

# Home screen buttons
game_button = create_button(20, 20, 150, 50)  # Top-left corner
watchlist_button = create_button(SCREEN_WIDTH - 170, 20, 150, 50)  # Top-right corner
your_stocks_button = create_button(20, SCREEN_HEIGHT - 70, 150, 50)  # Bottom-left corner


def draw_button_with_shadow(surface, color, rect, shadow_color, corner_radius, shadow_offset=5):
    shadow_rect = rect.copy()
    shadow_rect.x += shadow_offset
    shadow_rect.y += shadow_offset
    pygame.draw.rect(surface, shadow_color, shadow_rect, border_radius=corner_radius)
    pygame.draw.rect(surface, color, rect, border_radius=corner_radius)


def draw_button(name, rect, color, mouse_pos):
    button_color = LIGHT_BLUE if rect.collidepoint(mouse_pos) else color
    draw_button_with_shadow(screen, button_color, rect, SHADOW_COLOR, 10)
    text = font.render(name, True, WHITE)
    text_rect = text.get_rect(center=rect.center)
    screen.blit(text, text_rect)


def draw_centered_text(text, font, color, surface, y_offset=0):
    """Helper function to draw text centered on the screen."""
    text_surface = font.render(text, True, color)
    text_rect = text_surface.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + y_offset))
    surface.blit(text_surface, text_rect)


def draw_home_screen(mouse_pos):
    draw_centered_text("Welcome to the Stock Predictor Game", title_font, BLACK, screen)

    draw_button("Game", game_button, BLUE, mouse_pos)
    draw_button("Watchlist", watchlist_button, BLUE, mouse_pos)
    draw_button("Your Stocks", your_stocks_button, BLUE, mouse_pos)


def draw_secondary_screen(title, mouse_pos):
    draw_centered_text(title, title_font, BLACK, screen)

    home_color = GREEN if home_button_clicked else BLUE
    draw_button("Home", home_button, home_color, mouse_pos)

    draw_button("End", end_button, BRIGHT_RED, mouse_pos)

running = True
while running:
    screen.fill(WHITE)
    mouse_pos = pygame.mouse.get_pos()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if current_screen == "home":
                if game_button.collidepoint(event.pos):
                    current_screen = "game"
                elif watchlist_button.collidepoint(event.pos):
                    current_screen = "watchlist"
                elif your_stocks_button.collidepoint(event.pos):
                    current_screen = "your_stocks"
            else:
                if home_button.collidepoint(event.pos):
                    current_screen = "home"
                    home_button_clicked = True  
                elif end_button.collidepoint(event.pos):
                    running = False

    if current_screen == "home":
        draw_home_screen(mouse_pos)
    elif current_screen == "game":
        draw_secondary_screen("Game Screen", mouse_pos)
    elif current_screen == "watchlist":
        draw_secondary_screen("Watchlist Screen", mouse_pos)
    elif current_screen == "your_stocks":
        draw_secondary_screen("Your Stocks Screen", mouse_pos)

    pygame.display.flip()

pygame.quit()
sys.exit()
