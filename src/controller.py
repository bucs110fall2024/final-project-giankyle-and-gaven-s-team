import pygame
import sys
import yfinance as yf
from src.stockprediction import stockpredictor  # Import stockpredictor class from stockprediction.py
from src import ui  # Import UI module for screen rendering


class Controller:
    def __init__(self):
        pygame.init()


        # Initialize variables
        self.screen_width = 800
        self.screen_height = 600
        self.screen = pygame.display.set_mode((self.screen_width, self.screen_height))
        pygame.display.set_caption("Stock Predictor")


        # Load background image and scale it to the screen size
        self.background_image = pygame.image.load('assets/stockBackground.png')  # Ensure correct path
        self.background_image = pygame.transform.scale(self.background_image, (self.screen_width, self.screen_height))


        self.current_screen = "home"
        self.user_input = ""
        self.response_message = ""
        self.current_question = "stock_ticker"
        self.watchlist = []  # List to store watchlist items
        self.ticker = None
        self.forecast_days = None
        self.selected_stock = None
        self.selected_days = None
        self.show_graph = False  # Flag to show the graph when a stock is selected


        # Initialize UI
        self.ui = ui.UI(self.screen, self.screen_width, self.screen_height)


    def handle_user_input(self, event):
        """Handle user inputs such as key presses and mouse clicks."""
        if event.type == pygame.KEYDOWN:
            if self.current_screen == "your_stocks":
                if event.key == pygame.K_BACKSPACE:
                    self.user_input = self.user_input[:-1]
                elif event.key == pygame.K_RETURN:
                    self.process_user_input()


        elif event.type == pygame.MOUSEBUTTONDOWN:
            if self.current_screen == "home":
                self.handle_home_screen_buttons(event.pos)
            elif self.current_screen == "watchlist":
                self.handle_watchlist_buttons(event.pos)
            elif self.current_screen == "tutorial":
                self.handle_tutorial_buttons(event.pos)
            elif self.current_screen == "your_stocks":
                self.handle_your_stocks_buttons(event.pos)


    def process_user_input(self):
        """Process user input for stock ticker and forecast days."""
        if self.current_question == "stock_ticker" and self.user_input:
            self.ticker = self.user_input.upper()
            if self.validate_stock_ticker(self.ticker):
                self.current_question = "forecast_days"
                self.response_message = "Ticker valid. Enter forecast days."
                self.user_input = ""
            else:
                self.response_message = "Invalid stock ticker."
        elif self.current_question == "forecast_days" and self.user_input:
            try:
                self.forecast_days = int(self.user_input)
                self.current_question = "prediction"
                self.response_message = f"Predicting for {self.forecast_days} days."
                self.show_graph = True  # Enable graph display
                self.user_input = ""
            except ValueError:
                self.response_message = "Please enter a valid number of days."


    def validate_stock_ticker(self, ticker):
        """Validate if the stock ticker exists."""
        try:
            stock = yf.Ticker(ticker)
            return stock.info["regularMarketPrice"] is not None
        except Exception:
            return False


    def handle_home_screen_buttons(self, pos):
        """Handle button clicks on the home screen."""
        if self.ui.tutorial_button.collidepoint(pos):
            self.current_screen = "tutorial"
        elif self.ui.watchlist_button.collidepoint(pos):
            self.current_screen = "watchlist"
        elif self.ui.your_stocks_button.collidepoint(pos):
            self.current_screen = "your_stocks"


    def handle_watchlist_buttons(self, pos):
        """Handle button clicks on the watchlist screen."""
        home_button, end_button = self.ui.draw_secondary_screen("watchlist", pos)
       
        if home_button.collidepoint(pos):
            self.current_screen = "home"
        elif end_button.collidepoint(pos):
            pygame.quit()
            sys.exit()


    def handle_tutorial_buttons(self, pos):
        """Handle button clicks on the tutorial screen."""
        home_button, end_button = self.ui.draw_secondary_screen("tutorial", pos)
       
        if home_button.collidepoint(pos):
            self.current_screen = "home"
        elif end_button.collidepoint(pos):
            pygame.quit()
            sys.exit()


    def handle_your_stocks_buttons(self, pos):
        """Handle button clicks on the your stocks screen."""
        home_button, end_button = self.ui.draw_secondary_screen("your_stocks", pos)
       
        if home_button.collidepoint(pos):
            self.current_screen = "home"
        elif end_button.collidepoint(pos):
            pygame.quit()
            sys.exit()


    def update(self):
        """Update the display based on the current screen."""
        mouse_pos = pygame.mouse.get_pos()


        if self.current_screen == "home":
            self.ui.draw_home_screen(mouse_pos, self.screen_width // 2)
        elif self.current_screen == "watchlist":
            self.ui.draw_watchlist_screen(mouse_pos, self.watchlist)
        elif self.current_screen == "tutorial":
            self.ui.draw_tutorial_screen(mouse_pos)
        elif self.current_screen == "your_stocks":
            self.ui.draw_your_stocks_screen(mouse_pos, self.user_input, self.response_message, self.screen_width // 2, self.screen_height // 2)
       
        pygame.display.flip()


    def run(self):
        """Run the main game loop."""
        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                self.handle_user_input(event)


            self.update()
            pygame.time.Clock().tick(60)


        pygame.quit()


if __name__ == "__main__":
    controller = Controller()
    controller.run()
