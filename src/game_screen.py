import pygame
from src.gui_base import draw_centered_text, draw_button

# Screen dimensions and colors
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
BLUE = (52, 152, 219)
WHITE = (255, 255, 255)
BRIGHT_RED = (255, 0, 0)
SHADOW_COLOR = (200, 200, 200)

# Fonts
title_font = pygame.font.Font(None, 48)

# Buttons
def create_button(x, y, width, height):
    return pygame.Rect(x, y, width, height)

home_button = create_button(SCREEN_WIDTH - 170, SCREEN_HEIGHT - 70, 150, 50)
end_button = create_button(20, SCREEN_HEIGHT - 70, 150, 50)

def draw_game_screen(screen, mouse_pos):
    """
    Render the Game Screen components.
    """
    # Correct button positions on the game screen
    home_button.topleft = (SCREEN_WIDTH - 170, SCREEN_HEIGHT - 70)
    end_button.topleft = (20, SCREEN_HEIGHT - 70)

    # Render Game Screen title
    draw_centered_text("Game Screen", title_font, WHITE, screen, -150)

    # Render buttons
    draw_button("Home", home_button, BLUE, mouse_pos)
    draw_button("End", end_button, BRIGHT_RED, mouse_pos)
    
def draw_tutorial_screen(screen):
    screen.fill((0, 0, 0))  # Fill the screen with black
    font = pygame.font.Font(None, 36)
    text_surface = font.render("Tutorial Screen", True, (255, 255, 255))
    text_rect = text_surface.get_rect(center=(screen.get_width() // 2, screen.get_height() // 2))
    screen.blit(text_surface, text_rect)
    pygame.display.flip()
