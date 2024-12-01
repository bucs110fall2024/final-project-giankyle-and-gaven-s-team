import pygame
import sys

pygame.init()

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Stock Predictor Game")

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY = (230, 230, 230)
BLUE = (52, 152, 219)
LIGHT_BLUE = (41, 128, 185)
SHADOW_COLOR = (200, 200, 200)

font = pygame.font.Font(None, 36)
title_font = pygame.font.Font(None, 48)

def draw_button_with_shadow(surface, color, rect, shadow_color, corner_radius, shadow_offset=5):
    shadow_rect = rect.copy()
    shadow_rect.x += shadow_offset
    shadow_rect.y += shadow_offset
    pygame.draw.rect(surface, shadow_color, shadow_rect, border_radius=corner_radius)
    pygame.draw.rect(surface, color, rect, border_radius=corner_radius)

buttons = {
    "Home": pygame.Rect(20, 20, 150, 50),  # Top-left corner
    "Game": pygame.Rect(SCREEN_WIDTH - 170, 20, 150, 50),  # Top-right corner
    "Watchlist": pygame.Rect(20, SCREEN_HEIGHT - 70, 150, 50),  # Bottom-left corner
    "Your Stocks": pygame.Rect(SCREEN_WIDTH - 170, SCREEN_HEIGHT - 70, 150, 50),  # Bottom-right corner
}

def draw_buttons():
    mouse_pos = pygame.mouse.get_pos()
    for name, rect in buttons.items():
        if rect.collidepoint(mouse_pos):
            color = LIGHT_BLUE
        else:
            color = BLUE

        draw_button_with_shadow(screen, color, rect, SHADOW_COLOR, 10)

        text = font.render(name, True, WHITE)
        text_rect = text.get_rect(center=rect.center)
        screen.blit(text, text_rect)

def draw_welcome_message():
    text = title_font.render("Welcome to the Stock Predictor Game", True, BLACK)
    text_rect = text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2))
    screen.blit(text, text_rect)

def draw_home_screen():
    text = title_font.render("Home Screen", True, BLACK)
    text_rect = text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2))
    screen.blit(text, text_rect)

def draw_game_screen():
    text = title_font.render("Game Screen", True, BLACK)
    text_rect = text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2))
    screen.blit(text, text_rect)

def draw_watchlist_screen():
    text = title_font.render("Watchlist Screen", True, BLACK)
    text_rect = text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2))
    screen.blit(text, text_rect)

def draw_your_stocks_screen():
    text = title_font.render("Your Stocks Screen", True, BLACK)
    text_rect = text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2))
    screen.blit(text, text_rect)

current_screen = "main"  
running = True
while running:
    screen.fill(WHITE)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if current_screen == "main":  
                for name, rect in buttons.items():
                    if rect.collidepoint(event.pos):
                        current_screen = name.lower()  
                        print(f"{name} button clicked")

    if current_screen == "main":
        draw_buttons()
        draw_welcome_message()
    elif current_screen == "home":
        draw_home_screen()
    elif current_screen == "game":
        draw_game_screen()
    elif current_screen == "watchlist":
        draw_watchlist_screen()
    elif current_screen == "your stocks":
        draw_your_stocks_screen()

    pygame.display.flip()

pygame.quit()
sys.exit()
