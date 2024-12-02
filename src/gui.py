import pygame
import sys
import yfinance as yf

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

# Fonts
font = pygame.font.Font(None, 36)
user_font = pygame.font.Font(None, 50)
title_font = pygame.font.Font(None, 48)

# Load background image
background_image_path = "../assets/stockBackground.png"
background_image = pygame.image.load(background_image_path)
background_image = pygame.transform.scale(background_image, (SCREEN_WIDTH, SCREEN_HEIGHT))

# Global state
current_screen = "home"
home_button_clicked = False
user_input = ""
response_message = ""

# Button definitions
def create_button(x, y, width, height):
    return pygame.Rect(x, y, width, height)

home_button = create_button(SCREEN_WIDTH - 170, SCREEN_HEIGHT - 70, 150, 50)
end_button = create_button(20, SCREEN_HEIGHT - 70, 150, 50)

game_button = create_button(20, 20, 150, 50)
watchlist_button = create_button(SCREEN_WIDTH - 170, 20, 150, 50)
your_stocks_button = create_button(20, SCREEN_HEIGHT - 70, 150, 50)

# Functions for rendering elements
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
    text_surface = font.render(text, True, color)
    text_rect = text_surface.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + y_offset))
    surface.blit(text_surface, text_rect)

# Screen rendering functions
def draw_home_screen(mouse_pos):
    draw_centered_text("Welcome to the Stock Predictor Game", title_font, WHITE, screen)
    draw_button("Game", game_button, BLUE, mouse_pos)
    draw_button("Watchlist", watchlist_button, BLUE, mouse_pos)
    draw_button("Your Stocks", your_stocks_button, BLUE, mouse_pos)

def draw_secondary_screen(title, mouse_pos):
    draw_centered_text(title, title_font, BLACK, screen)
    home_color = BLUE if home_button_clicked else GREEN
    draw_button("Home", home_button, home_color, mouse_pos)
    draw_button("End", end_button, BRIGHT_RED, mouse_pos)

def validate_stock_ticker(ticker):
    try:
        data = yf.download(ticker, period="1d")
        return not data.empty
    except Exception:
        return False

def draw_your_stocks_screen(mouse_pos):
    # draw_centered_text("Your Stocks Screen", title_font, BLACK, screen)
    
    # Define the input box rectangle
    input_box = pygame.Rect(200, 250, 400, 50)
    
    # Draw the input box (white background with a black border)
    pygame.draw.rect(screen, WHITE, input_box)  # White background
    pygame.draw.rect(screen, BLACK, input_box, 2)  # Black border (2 pixels wide)

    # Draw the text inside the input box
    text_surface = user_font.render(user_input, True, BLACK)
    screen.blit(text_surface, (input_box.x + 5, input_box.y + 5))
    
    # Draw the buttons
    home_color = BLUE if home_button_clicked else GREEN
    draw_button("Home", home_button, home_color, mouse_pos)
    draw_button("End", end_button, BRIGHT_RED, mouse_pos)
    
    # Draw the response message
    if response_message:
        draw_centered_text(response_message, font, BLACK, screen, 50)

# Main loop
running = True
while running:
    screen.blit(background_image, (0, 0))  # Draw the background image
    mouse_pos = pygame.mouse.get_pos()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if current_screen == "home":
                if game_button.collidepoint(event.pos):
                    current_screen = "game"
                    home_button_clicked = False  # Reset the home button click state
                elif watchlist_button.collidepoint(event.pos):
                    current_screen = "watchlist"
                    home_button_clicked = False
                elif your_stocks_button.collidepoint(event.pos):
                    current_screen = "your_stocks"
                    home_button_clicked = False
            elif current_screen == "your_stocks":
                if home_button.collidepoint(event.pos):
                    current_screen = "home"
                    home_button_clicked = True  # Set to True when "Home" is clicked
                elif end_button.collidepoint(event.pos):
                    running = False
            else:
                if home_button.collidepoint(event.pos):
                    current_screen = "home"
                    home_button_clicked = True  # Set to True when "Home" is clicked
                elif end_button.collidepoint(event.pos):
                    running = False
        elif event.type == pygame.KEYDOWN:
            if current_screen == "your_stocks":
                if event.key == pygame.K_RETURN:
                    response_message = "Valid Stock!" if validate_stock_ticker(user_input) else "Invalid Stock!"
                    user_input = ""  # Clear the input field after pressing Enter
                elif event.key == pygame.K_BACKSPACE:
                    user_input = user_input[:-1]
                else:
                    user_input += event.unicode

    if current_screen == "home":
        draw_home_screen(mouse_pos)
    elif current_screen == "game":
        draw_secondary_screen("Game Screen", mouse_pos)
    elif current_screen == "watchlist":
        draw_secondary_screen("Watchlist Screen", mouse_pos)
    elif current_screen == "your_stocks":
        draw_your_stocks_screen(mouse_pos)

    pygame.display.flip()

pygame.quit()
sys.exit()
