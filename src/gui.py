import pygame
import sys
import yfinance as yf
import matplotlib.pyplot as plt

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
background_image_path = "../assets/stockBackground.png"  # Update this path if necessary
background_image = pygame.image.load(background_image_path)
background_image = pygame.transform.scale(background_image, (SCREEN_WIDTH, SCREEN_HEIGHT))

# Global state
current_screen = "home"
user_input = ""
response_message = ""
current_question = "stock_ticker"  # 'stock_ticker' or 'forecast_days'
watchlist = []  # List to store watchlist items
ticker = None
forecast_days = None
selected_stock = None
selected_days = None
graph_shown = {}  # Dictionary to track graph shown for each stock

# Button definitions
def create_button(x, y, width, height):
    return pygame.Rect(x, y, width, height)

home_button = create_button(SCREEN_WIDTH - 170, SCREEN_HEIGHT - 70, 150, 50)
end_button = create_button(20, SCREEN_HEIGHT - 70, 150, 50)
clear_button = create_button(610, 250, 100, 50)  # Clear button next to the input box

game_button = create_button(0, 0, 200, 50)
watchlist_button = create_button(0, 0, 200, 50)
your_stocks_button = create_button(0, 0, 200, 50)

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
    welcome_text = "Welcome to the Stock Predictor Game"
    text_surface = title_font.render(welcome_text, True, WHITE)
    text_rect = text_surface.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 4))
    screen.blit(text_surface, text_rect)

    button_width = 200
    button_height = 50
    vertical_spacing = 20
    center_x = SCREEN_WIDTH // 2 - button_width // 2

    game_button.topleft = (center_x, SCREEN_HEIGHT // 2 - button_height - vertical_spacing)
    watchlist_button.topleft = (center_x, SCREEN_HEIGHT // 2)
    your_stocks_button.topleft = (center_x, SCREEN_HEIGHT // 2 + button_height + vertical_spacing)

    draw_button("Game", game_button, BLUE, mouse_pos)
    draw_button("Watchlist", watchlist_button, BLUE, mouse_pos)
    draw_button("Your Stocks", your_stocks_button, BLUE, mouse_pos)

def draw_watchlist_screen(mouse_pos):
    draw_centered_text("Watchlist", title_font, WHITE, screen, -200)
    
    y_offset = 0
    
    # Iterate through the watchlist and display each stock as a button
    for i, (stock, days) in enumerate(watchlist, start=1):
        stock_button_rect = pygame.Rect(SCREEN_WIDTH // 2 - 150, 250 + y_offset, 300, 50)
        draw_button(f"{stock} ({days} days)", stock_button_rect, BLUE, mouse_pos)
        
        # Handle button click to select stock for viewing graph
        if stock_button_rect.collidepoint(mouse_pos) and pygame.mouse.get_pressed()[0]:
            global selected_stock, selected_days
            # Only change selection if the stock is different from the current selection
            if selected_stock != stock or selected_days != days:
                selected_stock = stock
                selected_days = days
                graph_shown[selected_stock] = False  # Reset the flag for the selected stock
        
        y_offset += 60  # Adjust the offset for the next stock button

    # If a stock was selected and the graph has not been shown, show the graph for that stock
    if selected_stock and selected_days and not graph_shown.get(selected_stock, False):
        show_graph_for_stock(selected_stock, selected_days)
        graph_shown[selected_stock] = True  # Mark that the graph has been shown
    
    # Draw the Home and End buttons for the Watchlist screen
    draw_button("Home", home_button, BLUE, mouse_pos)
    draw_button("End", end_button, BRIGHT_RED, mouse_pos)

def draw_game_screen(mouse_pos):
    draw_centered_text("Game Screen - Play the Game!", title_font, WHITE, screen, -150)
    
    # Draw the Home and End buttons for the Game screen
    draw_button("Home", home_button, BLUE, mouse_pos)
    draw_button("End", end_button, BRIGHT_RED, mouse_pos)

def draw_your_stocks_screen(mouse_pos):
    if current_question == "stock_ticker":
        draw_centered_text("Enter Stock Ticker:", font, WHITE, screen, -150)
    elif current_question == "forecast_days":
        draw_centered_text("Enter Number of Forecast Days:", font, WHITE, screen, -150)

    input_box = pygame.Rect(200, 250, 400, 50)
    pygame.draw.rect(screen, WHITE, input_box)
    pygame.draw.rect(screen, BLACK, input_box, 2)
    text_surface = user_font.render(user_input, True, BLACK)
    screen.blit(text_surface, (input_box.x + 5, input_box.y + 5))

    # Draw the "Clear" button next to the input box
    draw_button("Clear", clear_button, BLUE, mouse_pos)
    
    if response_message:
        draw_centered_text(response_message, font, WHITE, screen, 100)

    draw_button("Home", home_button, BLUE, mouse_pos)
    draw_button("End", end_button, BRIGHT_RED, mouse_pos)

def validate_stock_ticker(ticker):
    try:
        data = yf.download(ticker, period="1d")
        return not data.empty
    except Exception:
        return False

def validate_forecast_days(days):
    try:
        return int(days) > 0
    except ValueError:
        return False

def show_graph_in_window(data):
    plt.figure()
    plt.plot(data.index, data['Close'], label="Close Price")
    plt.title(f"Stock Forecast for {ticker} ({forecast_days} days)")
    plt.xlabel("Date")
    plt.ylabel("Price")
    plt.legend()
    plt.show()  # Opens a new window with the graph

def show_graph_for_stock(stock, forecast_days):
    """ Fetch data and show the graph for the selected stock and forecast days """
    data = yf.download(stock, period="1y")
    show_graph_in_window(data)

# Reset the stock selection when navigating away from the watchlist screen
def reset_selected_stock():
    global selected_stock, selected_days
    selected_stock = None
    selected_days = None
    graph_shown.clear()  # Clear all graph shown flags

# Main loop
running = True
while running:
    screen.blit(background_image, (0, 0))
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
            elif current_screen == "watchlist":
                if home_button.collidepoint(event.pos):
                    reset_selected_stock()
                    current_screen = "home"
                elif end_button.collidepoint(event.pos):
                    reset_selected_stock()
                    running = False
            elif current_screen == "your_stocks":
                if home_button.collidepoint(event.pos):
                    current_screen = "home"
                elif end_button.collidepoint(event.pos):
                    running = False
                elif clear_button.collidepoint(event.pos):
                    user_input = ""

        elif event.type == pygame.KEYDOWN:
            if current_screen == "your_stocks":
                if event.key == pygame.K_RETURN:
                    if current_question == "stock_ticker":
                        if validate_stock_ticker(user_input):
                            ticker = user_input
                            current_question = "forecast_days"
                            user_input = ""
                        else:
                            response_message = "Invalid stock ticker."
                    elif current_question == "forecast_days":
                        if validate_forecast_days(user_input):
                            forecast_days = int(user_input)
                            watchlist.append((ticker, forecast_days))
                            user_input = ""
                            current_question = "stock_ticker"
                            response_message = f"Added {ticker} to watchlist."
                        else:
                            response_message = "Please enter a valid number of days."
                elif event.key == pygame.K_BACKSPACE:
                    user_input = user_input[:-1]
                else:
                    user_input += event.unicode

    if current_screen == "home":
        draw_home_screen(mouse_pos)
    elif current_screen == "watchlist":
        draw_watchlist_screen(mouse_pos)
    elif current_screen == "game":
        draw_game_screen(mouse_pos)
    elif current_screen == "your_stocks":
        draw_your_stocks_screen(mouse_pos)

    pygame.display.flip()
    pygame.time.Clock().tick(60)

pygame.quit()
sys.exit()
