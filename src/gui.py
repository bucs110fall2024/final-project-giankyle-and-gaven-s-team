import pygame
import sys
import yfinance as yf
import matplotlib.pyplot as plt
from stockprediction import stockpredictor  # Import your stock prediction module
from io import BytesIO

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
home_button_clicked = False
user_input = ""
response_message = ""
forecast_days = None
current_question = "stock_ticker"  # 'stock_ticker' or 'forecast_days'

# Button definitions
def create_button(x, y, width, height):
    return pygame.Rect(x, y, width, height)

home_button = create_button(SCREEN_WIDTH - 170, SCREEN_HEIGHT - 70, 150, 50)
end_button = create_button(20, SCREEN_HEIGHT - 70, 150, 50)

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

def draw_secondary_screen(title, mouse_pos):
    draw_centered_text(title, title_font, WHITE, screen, -200)
    
    # Display "Home" and "End" buttons for the Game and Your Stocks screens
    if title == "Game" or title == "Your Stocks":
        draw_button("Home", home_button, BLUE, mouse_pos)
        draw_button("End", end_button, BRIGHT_RED, mouse_pos)

    # For the Watchlist screen, display a message or list content
    if title == "Watchlist":
        # You can display a message or actual watchlist items here
        watchlist_message = "Your Watchlist is empty"  # Modify this to display actual watchlist items
        draw_centered_text(watchlist_message, font, WHITE, screen, 50)

        # Show Home and End buttons for Watchlist screen
        draw_button("Home", home_button, BLUE, mouse_pos)
        draw_button("End", end_button, BRIGHT_RED, mouse_pos)

def draw_your_stocks_screen(mouse_pos):
    # Ask for stock ticker if it's the first question
    if current_question == "stock_ticker":
        instruction_text = "Enter Stock Ticker:"
        instruction_surface = font.render(instruction_text, True, WHITE)
        instruction_rect = instruction_surface.get_rect(center=(SCREEN_WIDTH // 2, 200))
        screen.blit(instruction_surface, instruction_rect)

        # Draw input box
        input_box = pygame.Rect(200, 250, 400, 50)
        pygame.draw.rect(screen, WHITE, input_box)
        pygame.draw.rect(screen, BLACK, input_box, 2)
        text_surface = user_font.render(user_input, True, BLACK)
        screen.blit(text_surface, (input_box.x + 5, input_box.y + 5))

        if response_message:
            response_surface = font.render(response_message, True, BLACK)
            response_rect = response_surface.get_rect(center=(SCREEN_WIDTH // 2, 330))
            screen.blit(response_surface, response_rect)

    # Ask for forecast days if it's the second question
    elif current_question == "forecast_days":
        instruction_text = "Enter Number of Forecast Days:"
        instruction_surface = font.render(instruction_text, True, WHITE)
        instruction_rect = instruction_surface.get_rect(center=(SCREEN_WIDTH // 2, 200))
        screen.blit(instruction_surface, instruction_rect)

        # Draw input box
        input_box = pygame.Rect(200, 250, 400, 50)
        pygame.draw.rect(screen, WHITE, input_box)
        pygame.draw.rect(screen, BLACK, input_box, 2)
        text_surface = user_font.render(user_input, True, BLACK)
        screen.blit(text_surface, (input_box.x + 5, input_box.y + 5))

        if response_message:
            response_surface = font.render(response_message, True, BLACK)
            response_rect = response_surface.get_rect(center=(SCREEN_WIDTH // 2, 330))
            screen.blit(response_surface, response_rect)

    # Draw buttons
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

# Function to embed matplotlib plot in pygame without resizing the screen
def plot_and_save():
    # Create a sample plot
    plt.plot([1, 2, 3, 4], [10, 20, 25, 30])
    plt.title("Stock Forecast")

    # Save the plot to a BytesIO buffer instead of displaying it
    buf = BytesIO()
    plt.savefig(buf, format='png')
    buf.seek(0)
    
    # Load the plot into a pygame surface
    plot_image = pygame.image.load(buf)

    # Scale the plot image to a fixed size (without resizing the window)
    plot_image = pygame.transform.scale(plot_image, (600, 400))  # Resize the plot image if necessary
    return plot_image

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
            elif current_screen == "your_stocks":
                if home_button.collidepoint(event.pos):
                    current_screen = "home"
                elif end_button.collidepoint(event.pos):
                    running = False
            elif current_screen == "watchlist":
                if home_button.collidepoint(event.pos):
                    current_screen = "home"
                elif end_button.collidepoint(event.pos):
                    running = False
            elif current_screen == "game":
                if home_button.collidepoint(event.pos):
                    current_screen = "home"
                elif end_button.collidepoint(event.pos):
                    running = False
        elif event.type == pygame.KEYDOWN:
            if current_screen == "your_stocks":
                if event.key == pygame.K_RETURN:
                    if current_question == "stock_ticker":
                        if validate_stock_ticker(user_input):
                            ticker = user_input.upper()
                            response_message = "Ticker Validated!"
                            current_question = "forecast_days"
                            user_input = ""
                        else:
                            response_message = "Invalid Ticker!"
                    elif current_question == "forecast_days":
                        if validate_forecast_days(user_input):
                            forecast_days = int(user_input)
                            response_message = "Fetching forecast..."
                            predictor = stockpredictor(ticker)
                            predictor.data_fetch()
                            predictor.model_training()
                            forecast_df = predictor.stock_prediction(forecast_days)
                            predictor.plot_machinelearning_model(forecast_df)

                            # Generate the plot and show it
                            plot_image = plot_and_save()
                            screen.blit(plot_image, (100, 350))  # Position the plot

                            response_message = ""  # Clear the response message
                            current_question = "stock_ticker"  # Reset to stock ticker question
                            user_input = ""  # Clear user input
                        else:
                            response_message = "Invalid number of days!"
                elif event.key == pygame.K_BACKSPACE:
                    user_input = user_input[:-1]
                else:
                    user_input += event.unicode

    # Draw appropriate screen
    if current_screen == "home":
        draw_home_screen(mouse_pos)
    elif current_screen == "game":
        draw_secondary_screen("Game", mouse_pos)
    elif current_screen == "watchlist":
        draw_secondary_screen("Watchlist", mouse_pos)
    elif current_screen == "your_stocks":
        draw_your_stocks_screen(mouse_pos)

    pygame.display.flip()

pygame.quit()
sys.exit()
