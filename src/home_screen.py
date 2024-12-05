from src.gui_base import screen, title_font, draw_button, BLUE
import pygame

# Button definitions
tutorial_button = pygame.Rect(300, 200, 200, 50)
watchlist_button = pygame.Rect(300, 300, 200, 50)
your_stocks_button = pygame.Rect(300, 400, 200, 50)

def draw_home_screen(mouse_pos, event):
    # Example buttons
    watchlist_button = pygame.Rect(100, 100, 200, 50)
    stocks_button = pygame.Rect(100, 200, 200, 50)

    # Draw buttons
    pygame.draw.rect(screen, (0, 128, 255), watchlist_button)  # Blue button
    pygame.draw.rect(screen, (0, 255, 128), stocks_button)     # Green button


    # Handle button clicks
    if watchlist_button.collidepoint(mouse_pos):
        if event.type == pygame.MOUSEBUTTONDOWN:
            return "watchlist"  # Navigate to watchlist screen

    if stocks_button.collidepoint(mouse_pos):
        if event.type == pygame.MOUSEBUTTONDOWN:
            return "your_stocks"  # Navigate to your stocks screen

    return "home"  # Stay on home screen if no button clicked
    