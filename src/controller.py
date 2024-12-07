import pygame
import sys
import yfinance as yf
from src.stockprediction import stockpredictor  # Import stockpredictor class from stockprediction.py
from src import ui  # Import UI module for screen rendering

class Controller:
    def __init__(self):
        pygame.init()
       
        self.screen_width = 800
        self.screen_height = 600
        self.screen = pygame.display.set_mode((self.screen_width, self.screen_height))
        pygame.display.set_caption("Stock Predictor")

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
                    self.user_input = self.user_input[:-1]  # Remove the last character
                elif event.key == pygame.K_RETURN:
                    self.process_user_input()  # Process user input on Enter key press
                else:
                    self.user_input += event.unicode  # Add the typed character to user_input

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
                self.user_input = ""  # Clear user input
            else:
                self.response_message = "Invalid stock ticker."
        elif self.current_question == "forecast_days" and self.user_input:
            try:
                self.forecast_days = int(self.user_input)
                if self.forecast_days > 0:
                    self.predict_stock()
                else:
                    self.response_message = "Enter a positive number."
            except ValueError:
                self.response_message = "Invalid number."

    def validate_stock_ticker(self, ticker):
        """Validate if the stock ticker is valid."""
        try:
            data = yf.download(ticker, period="1d")
            return not data.empty
        except Exception:
            return False

    def predict_stock(self):
        """Predict the stock prices for the given forecast days."""
        predictor = stockpredictor(self.ticker)
        predictor.data_fetch()
        predictor.model_training()
        forecast_df = predictor.stock_prediction(self.forecast_days)
        predictor.plot_machinelearning_model(forecast_df)
        self.watchlist.append((self.ticker, self.forecast_days))
        self.response_message = f"Added {self.ticker} to watchlist."
        self.current_question = "stock_ticker"
        self.user_input = ""  # Clear user input after prediction

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
        if self.ui.home_button.collidepoint(pos):
            self.current_screen = "home"
        elif self.ui.end_button.collidepoint(pos):
            pygame.quit()
            sys.exit()

        # Add the handling for clicking the stock buttons
        for idx, (stock, days) in enumerate(self.watchlist):
            button_rect = pygame.Rect(self.screen_width // 2 - 100, 150 + idx * 60, 200, 50)
            if button_rect.collidepoint(pos):
                self.revisit_stock(stock, days)

    def handle_tutorial_buttons(self, pos):
        """Handle button clicks on the tutorial screen."""
        if self.ui.home_button.collidepoint(pos):
            self.current_screen = "home"
        elif self.ui.end_button.collidepoint(pos):
            pygame.quit()
            sys.exit()

    def handle_your_stocks_buttons(self, pos):
        """Handle button clicks on the 'Your Stocks' screen."""
        if self.ui.home_button.collidepoint(pos):
            self.current_screen = "home"
        elif self.ui.end_button.collidepoint(pos):
            pygame.quit()
            sys.exit()
        elif self.ui.clear_button.collidepoint(pos):
            # Clear the user input
            self.user_input = ""
            self.response_message = ""

    def revisit_stock(self, stock, days):
        """Handle revisiting a stock from the watchlist."""
        self.ticker = stock
        self.forecast_days = days
        self.predict_stock()

    def update(self):
        """Update the screen based on the current screen."""
        mouse_pos = pygame.mouse.get_pos()

        # Draw the background image before other UI elements
        self.screen.blit(self.background_image, (0, 0))

        if self.current_screen == "home":
            center_x = self.screen_width // 2
            self.ui.draw_home_screen(mouse_pos, center_x)
        elif self.current_screen == "watchlist":
            self.ui.draw_watchlist_screen(mouse_pos, self.watchlist)  # Pass watchlist to render
        elif self.current_screen == "tutorial":
            self.ui.draw_tutorial_screen(mouse_pos)
        elif self.current_screen == "your_stocks":
            center_x = (self.screen_width - 400) // 2
            center_y = (self.screen_height - 300) // 2
            self.ui.draw_your_stocks_screen(mouse_pos, self.user_input, self.response_message, center_x, center_y)

        pygame.display.flip()

    def mainloop(self):
        """Main loop for handling events and updating the screen."""
        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                self.handle_user_input(event)

            self.update()

        pygame.quit()


if __name__ == "__main__":
    controller = Controller()
    controller.mainloop()
