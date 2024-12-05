import pygame

pygame.init()

# Screen dimensions and setup
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Stock Predictor")

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
BLUE = (52, 152, 219)
LIGHT_BLUE = (41, 128, 185)
BRIGHT_RED = (255, 0, 0)
SHADOW_COLOR = (200, 200, 200)
GREEN = (39, 174, 96)
GREY = (169, 169, 169)

# Fonts
font = pygame.font.Font(None, 36)
user_font = pygame.font.Font(None, 50)
title_font = pygame.font.Font(None, 48)

# Load background image
background_image_path = "assets/stockBackground.png"  # Update this path if necessary
background_image = pygame.image.load(background_image_path)
background_image = pygame.transform.scale(background_image, (SCREEN_WIDTH, SCREEN_HEIGHT))

def draw_button(name, rect, color, mouse_pos, screen):
    button_color = LIGHT_BLUE if rect.collidepoint(mouse_pos) else color
    pygame.draw.rect(screen, button_color, rect, border_radius=10)
    text = font.render(name, True, WHITE)
    text_rect = text.get_rect(center=rect.center)
    screen.blit(text, text_rect)

def draw_centered_text(screen, text, font, color, rect):
    text_surface = font.render(text, True, color)
    text_rect = text_surface.get_rect(center=rect.center)
    screen.blit(text_surface, text_rect)