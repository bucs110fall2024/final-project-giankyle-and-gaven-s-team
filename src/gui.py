import pygame
import sys
import yfinance as yf
import matplotlib.pyplot as plt
from stockprediction import stockpredictor  # Import stockpredictor class from stockprediction.py

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
background_image_path = "../assets/stockBackground.png"  # Update this path if necessary
background_image = pygame.image.load(background_image_path)
background_image = pygame.transform.scale(background_image, (SCREEN_WIDTH, SCREEN_HEIGHT))

#Tutorial lines
explanation_lines = [
    "Like the name implies, this is a stock predictor,",
    "which uses historical data to predict what a future",
    "stock's price will be for X amount of days.",
    "",
    "How does it work?",
    "This gathers information based off of a specific ticker",
    "(which is a 3-4 letter abbreviation) for a stock.",
    "For instance, Apple will be AAPL, Microsoft will be MSFT.",
    "You can search up a specific ticker online, or if you",
    "know one, you can use that.",
    "",
    "The model that we chose to use was linear regression,",
    "which is essentially like a line of best fit. It is based",
    "on information that something is dependent on something else,",
    "for example, a stock's price is correlated with time.",
    "This is why the prediction is more of a linear line,",
    "rather than something that fluctuates like a real stock.",
    "",
    "What are its limitations?",
    "This predictor only takes historical data into account,",
    "and it does not account for other things that may",
    "influence a stock's price like news, politics,",
    "or economic changes. However, it doesn't mean that",
    "it is 100 percent inaccurate as shown by if you compare",
    "historical data with the ones that were predicted.",
    "***This should not be the sole way that you get your",
    "information, it just shows a general trend that the",
    "computer model sees.***"
]

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
show_graph = False  # Flag to show the graph when a stock is selected

# Button definitions
def create_button(x, y, width, height):
    return pygame.Rect(x, y, width, height)

home_button = create_button(SCREEN_WIDTH - 170, SCREEN_HEIGHT - 70, 150, 50)
end_button = create_button(20, SCREEN_HEIGHT - 70, 150, 50)
clear_button = create_button(620, 250, 100, 50)

tutorial_button = create_button(0, 0, 200, 50)
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
    welcome_text = "Welcome to The Stock Predictor"
    text_surface = title_font.render(welcome_text, True, WHITE)
    text_rect = text_surface.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 4))
    screen.blit(text_surface, text_rect)

    button_width = 200
    button_height = 50
    vertical_spacing = 20
    center_x = SCREEN_WIDTH // 2 - button_width // 2

    tutorial_button.topleft = (center_x, SCREEN_HEIGHT // 2 - button_height - vertical_spacing)
    watchlist_button.topleft = (center_x, SCREEN_HEIGHT // 2)
    your_stocks_button.topleft = (center_x, SCREEN_HEIGHT // 2 + button_height + vertical_spacing)

    draw_button("Tutorial", tutorial_button, BLUE, mouse_pos)
    draw_button("Watchlist", watchlist_button, BLUE, mouse_pos)
    draw_button("Your Stocks", your_stocks_button, BLUE, mouse_pos)

def draw_watchlist_screen(mouse_pos):
    global selected_stock, selected_days, show_graph

    draw_centered_text("Watchlist", title_font, WHITE, screen, -200)
    y_offset = 0

    # Adjusting the vertical spacing between stocks and buttons
    for i, (stock, days) in enumerate(watchlist, start=1):
        stock_button_rect = pygame.Rect(SCREEN_WIDTH // 2 - 150, 250 + y_offset, 300, 50)
        draw_button(f"{stock} ({days} days)", stock_button_rect, BLUE, mouse_pos)

        if stock_button_rect.collidepoint(mouse_pos) and pygame.mouse.get_pressed()[0]:
            selected_stock = stock
            selected_days = days
            show_graph = True  # Set flag to show graph only when a stock is selected

        y_offset += 100  # Increased spacing to 100 for more separation between stock buttons

    # Drawing buttons (keeping them separate from stocks)
    draw_button("Home", home_button, BLUE, mouse_pos)
    draw_button("End", end_button, BRIGHT_RED, mouse_pos)

    # If the user navigates away or presses Home/End, reset show_graph to False
    if current_screen != "watchlist":
        show_graph = False

    # Show the stock graph if the stock was selected
    if show_graph:
        show_stock_graph()
        show_graph = False

def draw_tutorial_screen(mouse_pos):
    # Correct button positions on the game screen
    home_button.topleft = (SCREEN_WIDTH - 170, SCREEN_HEIGHT - 70)
    end_button.topleft = (20, SCREEN_HEIGHT - 70)


    draw_centered_text("Game Screen", title_font, WHITE, screen, -150)
    draw_button("Home", home_button, BLUE, mouse_pos)  # Home button at the top-left
    draw_button("End", end_button, BRIGHT_RED, mouse_pos)  # End button at the top-right

def draw_your_stocks_screen(mouse_pos):
    global user_input, ticker, forecast_days, response_message

    if current_question == "stock_ticker":
        draw_centered_text("Enter Stock Ticker:", font, WHITE, screen, -150)
    elif current_question == "forecast_days":
        draw_centered_text("Enter Number of Forecast Days:", font, WHITE, screen, -150)

    input_box = pygame.Rect(200, 250, 400, 50)
    pygame.draw.rect(screen, WHITE, input_box)
    pygame.draw.rect(screen, BLACK, input_box, 2)
    text_surface = user_font.render(user_input, True, BLACK)
    screen.blit(text_surface, (input_box.x + 5, input_box.y + 5))

    if response_message:
        draw_centered_text(response_message, font, WHITE, screen, 100)

    draw_button("Clear", clear_button, GREY, mouse_pos)
    draw_button("Home", home_button, BLUE, mouse_pos)
    draw_button("End", end_button, BRIGHT_RED, mouse_pos)

def validate_stock_ticker(ticker):
    try:
        data = yf.download(ticker, period="1d")
        return not data.empty
    except Exception:
        return False

def show_stock_graph():
    global selected_stock
    if selected_stock:
        predictor = stockpredictor(selected_stock)
        predictor.data_fetch()
        predictor.model_training()
        forecast_df = predictor.stock_prediction(30)  # Forecast for 30 days
        predictor.plot_machinelearning_model(forecast_df)

# Main loop
running = True
while running:
    screen.blit(background_image, (0, 0))
    mouse_pos = pygame.mouse.get_pos()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if current_screen == "your_stocks":
                if event.key == pygame.K_BACKSPACE:
                    user_input = user_input[:-1]
                elif event.key == pygame.K_RETURN:
                    if current_question == "stock_ticker" and user_input:
                        ticker = user_input.upper()
                        if validate_stock_ticker(ticker):
                            current_question = "forecast_days"
                            response_message = "Ticker valid. Enter forecast days."
                            user_input = ""
                        else:
                            response_message = "Invalid stock ticker."
                    elif current_question == "forecast_days" and user_input:
                        try:
                            forecast_days = int(user_input)
                            if forecast_days > 0:
                                predictor = stockpredictor(ticker)
                                predictor.data_fetch()
                                predictor.model_training()
                                forecast_df = predictor.stock_prediction(forecast_days)
                                predictor.plot_machinelearning_model(forecast_df)
                                watchlist.append((ticker, forecast_days))
                                response_message = f"Added {ticker} to watchlist."
                                current_question = "stock_ticker"
                                user_input = ""
                            else:
                                response_message = "Enter a positive number."
                        except ValueError:
                            response_message = "Invalid number."
                else:
                    user_input += event.unicode
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if current_screen == "home":
                if tutorial_button.collidepoint(event.pos):
                    current_screen = "tutorial"
                elif watchlist_button.collidepoint(event.pos):
                    current_screen = "watchlist"
                elif your_stocks_button.collidepoint(event.pos):
                    current_screen = "your_stocks"
            elif current_screen == "watchlist":
                if home_button.collidepoint(event.pos):
                    running = True
                    current_screen = "home"
                elif end_button.collidepoint(event.pos):
                    running = False
            elif current_screen == "tutorial":
                if home_button.collidepoint(event.pos):
                    running = True
                    current_screen = "home"
                elif end_button.collidepoint(event.pos):
                    running = False
            elif current_screen == "your_stocks":
                if home_button.collidepoint(event.pos):
                    running = True
                    current_screen = "home"
                
                elif end_button.collidepoint(event.pos):
                    running = False
                elif clear_button.collidepoint(event.pos):
                    user_input = ""

    if current_screen == "home":
        draw_home_screen(mouse_pos)
    elif current_screen == "watchlist":
        draw_watchlist_screen(mouse_pos)
    elif current_screen == "tutorial":
        draw_tutorial_screen(mouse_pos)
    elif current_screen == "your_stocks":
        draw_your_stocks_screen(mouse_pos)

    pygame.display.flip()

pygame.quit()
