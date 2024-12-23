import pygame
import sys
import yfinance as yf
from src.stockprediction import stockpredictor  
from src import ui 

class Controller:
    """
    Controller class to manage the flow of the stock prediction application.
    It handles user interactions, processes inputs, and updates the display.
    """

    def __init__(self):
        """
        Initializes the controller, sets up the pygame window, background, and UI components.
        Also initializes various variables for managing user inputs and state.
        
        """

        pygame.init()
       
        self.screen_width = 800
        self.screen_height = 600
        self.screen = pygame.display.set_mode((self.screen_width, self.screen_height))
        pygame.display.set_caption("Stock Predictor")

        self.background_image = pygame.image.load('assets/stockBackground.png')  
        self.background_image = pygame.transform.scale(self.background_image, (self.screen_width, self.screen_height))

        self.current_screen = "home"
        self.user_input = ""
        self.response_message = ""
        self.current_question = "stock_ticker"
        self.watchlist = []  
        self.ticker = None
        self.forecast_days = None
        self.selected_stock = None
        self.selected_days = None
        self.show_graph = False  

        self.ui = ui.UI(self.screen, self.screen_width, self.screen_height)

    def handle_user_input(self, event):
        """
        Handles user inputs such as key presses and mouse clicks.


        Args:
           event (pygame.event): The pygame event that triggers the input (key press or mouse click).
        """

        if event.type == pygame.KEYDOWN:
            if self.current_screen == "your_stocks":
                if event.key == pygame.K_BACKSPACE:
                    self.user_input = self.user_input[:-1]  
                elif event.key == pygame.K_RETURN:
                    self.process_user_input()  
                else:
                    self.user_input += event.unicode  

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
        """
        Validates if the stock ticker exists by checking its market price.


        Args:
           ticker (str): The stock ticker to validate.


        Returns:
           bool: True if the ticker exists and has a market price, False otherwise.
        """

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
        self.user_input = ""  

    def handle_home_screen_buttons(self, pos):
        """
        Handles button clicks on the home screen.


        Args:
           pos (tuple): The position of the mouse click (x, y).
        """

        if self.ui.tutorial_button.collidepoint(pos):
            self.current_screen = "tutorial"
        elif self.ui.watchlist_button.collidepoint(pos):
            self.current_screen = "watchlist"
        elif self.ui.your_stocks_button.collidepoint(pos):
            self.current_screen = "your_stocks"

    def handle_watchlist_buttons(self, pos):
        """
        Handles button clicks on the watchlist screen.


        Args:
           pos (tuple): The position of the mouse click (x, y).
        """

        if self.ui.home_button.collidepoint(pos):
            self.current_screen = "home"
        elif self.ui.end_button.collidepoint(pos):
            pygame.quit()
            sys.exit()

        for idx, (stock, days) in enumerate(self.watchlist):
            button_rect = pygame.Rect(self.screen_width // 2 - 100, 150 + idx * 60, 200, 50)
            if button_rect.collidepoint(pos):
                self.revisit_stock(stock, days)

    def handle_tutorial_buttons(self, pos):
        """
        Handles button clicks on the tutorial screen.


        Args:
           pos (tuple): The position of the mouse click (x, y).
        """

        if self.ui.home_button.collidepoint(pos):
            self.current_screen = "home"
        elif self.ui.end_button.collidepoint(pos):
            pygame.quit()
            sys.exit()

    def handle_your_stocks_buttons(self, pos):
        """
        Handles button clicks on the your stocks screen.


        Args:
           pos (tuple): The position of the mouse click (x, y).
        """

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
        """
        Updates the display based on the current screen.

        Draws the right screen based on the current state of the program.
        """

        mouse_pos = pygame.mouse.get_pos()

        self.screen.blit(self.background_image, (0, 0))

        if self.current_screen == "home":
            center_x = self.screen_width // 2
            self.ui.draw_home_screen(mouse_pos, center_x)
        elif self.current_screen == "watchlist":
            self.ui.draw_watchlist_screen(mouse_pos, self.watchlist)  
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
