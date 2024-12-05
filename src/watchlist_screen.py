from src.gui_base import screen, title_font, draw_button, BLUE
import pygame

watchlist = [("AAPL", 10), ("GOOGL", 5)]  # Example watchlist items

home_button = pygame.Rect(650, 500, 100, 50)

def draw_watchlist_screen(mouse_pos, event):
    global watchlist
    y_offset = 0
    for stock, days in watchlist:
        stock_button = pygame.Rect(300, 150 + y_offset, 200, 50)
        draw_button(f"{stock} ({days} days)", stock_button, BLUE, mouse_pos, screen)
        y_offset += 60

    draw_button("Home", home_button, BLUE, mouse_pos, screen)

    if event.type == pygame.MOUSEBUTTONDOWN:
        if home_button.collidepoint(event.pos):
            return "home"

    return "watchlist"
