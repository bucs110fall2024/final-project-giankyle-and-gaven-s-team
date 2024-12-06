import pygame
import io
import yfinance as yf
from PIL import Image
import matplotlib.pyplot as plt
from src.gui_base import draw_centered_text, draw_button
from src.stockprediction import stockpredictor  # Import the stock prediction function

class YourStocksScreen:
    def __init__(self, screen, controller):
        self.screen = screen
        self.controller = controller
        self.font = pygame.font.Font(None, 48)  # Adjust font size as needed
        self.button_font = pygame.font.Font(None, 36)  # Font for the buttons

        # Define button positions
        self.close_button = pygame.Rect(20, self.screen.get_height() - 70, 150, 50)  # Bottom-left corner
        self.home_button = pygame.Rect(self.screen.get_width() - 170, self.screen.get_height() - 70, 150, 50)  # Bottom-right corner

        # Define button colors
        self.button_colors = {
            "close": (255, 0, 0),  # Red for close button
            "home": (0, 255, 0)  # Green for home button
        }

        # Define highlighted button colors
        self.highlight_colors = {
            "close": (255, 100, 100),  # Lighter red for hover
            "home": (100, 255, 100)  # Lighter green for hover
        }

        # Define text input bar and clear button
        self.input_text = ""
        self.days_text = ""
        self.input_rect = pygame.Rect(150, 300, 500, 50)  # Input text bar (x, y, width, height)
        self.days_input_rect = pygame.Rect(150, 370, 100, 50)  # Input for days (x, y, width, height)
        self.clear_button = pygame.Rect(660, 300, 100, 50)  # Clear button next to input bar
        self.prediction_image = None  # To store the graph image

        # Initialize state variables
        self.current_question = "stock_ticker"
        self.response_message = "Enter stock ticker."
        self.watching_list = []  # List of added stocks

    def update(self):
        """Update any screen elements if necessary."""
        pass

    def draw(self, background_image):
        """Draw the Your Stocks screen."""
        # Draw the background image
        self.screen.blit(background_image, (0, 0))

        # Draw the title at the top
        title_text = "Your Stocks"
        draw_centered_text(self.screen, title_text, self.font, (255, 255, 255), pygame.Rect(0, 50, self.screen.get_width(), 100))

        # Draw buttons at the bottom corners
        self._draw_button(self.close_button, "Close", self.button_colors["close"], self.highlight_colors["close"])
        self._draw_button(self.home_button, "Home", self.button_colors["home"], self.highlight_colors["home"])

        # Draw the input bars and instructions based on current state
        if self.current_question == "stock_ticker":
            # Draw the stock ticker input field
            pygame.draw.rect(self.screen, (255, 255, 255), self.input_rect)
            text_surface = self.font.render(self.input_text, True, (0, 0, 0))
            self.screen.blit(text_surface, (self.input_rect.x + 10, self.input_rect.y + 10))
            self.response_message = "Enter stock ticker."

        elif self.current_question == "forecast_days":
            # Draw the days input field
            pygame.draw.rect(self.screen, (255, 255, 255), self.days_input_rect)
            days_surface = self.font.render(self.days_text, True, (0, 0, 0))
            self.screen.blit(days_surface, (self.days_input_rect.x + 10, self.days_input_rect.y + 10))
            self.response_message = "Enter forecast days."

        # Draw the "Clear" button
        self._draw_button(self.clear_button, "Clear", (169, 169, 169), (211, 211, 211))

        # If we have a prediction image, display it
        if self.prediction_image:
            self.screen.blit(self.prediction_image, (100, 450))  # Adjust this position as necessary

        # Draw the response message (feedback for user)
        response_surface = self.font.render(self.response_message, True, (255, 255, 255))
        self.screen.blit(response_surface, (150, 420))  # Adjust this position as needed

    def handle_click(self, event):
        """Handle mouse click events for the Your Stocks screen."""
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:  # Left-click
            mouse_pos = pygame.mouse.get_pos()

            # Check if the Close button was clicked
            if self.close_button.collidepoint(mouse_pos):
                pygame.quit()  # Close the game
                exit()

            # Check if the Home button was clicked
            if self.home_button.collidepoint(mouse_pos):
                self.controller.switch_to_home_screen()  # Switch to HomeScreen

            # Check if the Clear button was clicked
            if self.clear_button.collidepoint(mouse_pos):
                self.input_text = ""  # Clear the text in the input field
                self.days_text = ""   # Clear the days field
                self.prediction_image = None  # Clear the prediction image
                self.current_question = "stock_ticker"  # Reset the question

    def handle_key_event(self, event):
        """Handle keyboard events for text input."""
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_BACKSPACE:  # Handle backspace to delete text
                if self.current_question == "stock_ticker":
                    self.input_text = self.input_text[:-1]
                elif self.current_question == "forecast_days":
                    self.days_text = self.days_text[:-1]
            elif event.key == pygame.K_RETURN:  # Handle the Enter key
                if self.current_question == "stock_ticker" and self.input_text:
                    ticker = self.input_text.upper()
                    if self.validate_stock_ticker(ticker):
                        self.current_question = "forecast_days"
                        self.response_message = "Ticker valid. Enter forecast days."
                        self.input_text = ""
                    else:
                        self.response_message = "Invalid stock ticker. Please try again."

                elif self.current_question == "forecast_days" and self.days_text.isdigit():
                    try:
                        forecast_days = int(self.days_text)
                        if forecast_days > 0:
                            # Call the stock prediction function
                            self.generate_prediction_graph(self.input_text.upper(), forecast_days)
                            self.response_message = f"Prediction for {self.input_text.upper()} added."
                            self.watching_list.append((self.input_text.upper(), forecast_days))
                            self.current_question = "stock_ticker"  # Reset to stock ticker input
                            self.input_text = ""
                            self.days_text = ""
                        else:
                            self.response_message = "Enter a positive number."
                    except ValueError:
                        self.response_message = "Invalid number."
            else:
                # Add character to input_text if it's a valid key
                if self.current_question == "stock_ticker":
                    self.input_text += event.unicode
                elif self.current_question == "forecast_days":
                    self.days_text += event.unicode

    def validate_stock_ticker(self, ticker):
        """Validate the stock ticker."""
        try:
            # Fetch stock data for the ticker
            stock_data = yf.Ticker(ticker)
            # Check if the stock data is available (check if it has history data)
            stock_data.history(period="1d")  # Try to fetch one day's worth of data
            return True  # If no exception was raised, the ticker is valid
        except (ValueError, KeyError, yf.YFDownloadError):
            # If any exception occurs, the ticker is invalid
            return False

    def generate_prediction_graph(self, ticker, days):
        """Generate the stock prediction graph and convert to Pygame image."""
        try:
            # Initialize the stock predictor
            predictor = stockpredictor(ticker)
            
            # Fetch the stock data
            predictor.data_fetch()
            
            # Check if data is fetched correctly
            if predictor.data is None or predictor.data.empty:
                print(f"Error: No stock data found for {ticker}.")
                self.response_message = f"Error: No stock data found for {ticker}."
                return
            
            # Train the model and get predictions
            predictor.model_training()
            forecast_df = predictor.stock_prediction(days)

            # Check if the forecast data is valid and not empty
            if forecast_df.empty:
                print(f"Error: Forecast data is empty for {ticker}.")
                self.response_message = f"Error: Forecast data is empty for {ticker}."
                return

            # Plot the prediction graph
            plt.figure(figsize=(6, 4))
            plt.plot(forecast_df['Date'], forecast_df['Predicted Price'], label=f"Predicted Price ({ticker})")
            plt.title(f"Stock Prediction for {ticker}")
            plt.xlabel('Date')
            plt.ylabel('Predicted Price')
            plt.xticks(rotation=45)
            plt.grid(True)
            plt.tight_layout()

            # Save the plot to a bytes buffer
            buf = io.BytesIO()
            plt.savefig(buf, format="png")
            buf.seek(0)

            # Convert the plot to a Pygame image
            pil_image = Image.open(buf)
            self.prediction_image = pygame.image.fromstring(pil_image.tobytes(), pil_image.size, pil_image.mode)
            buf.close()

        except Exception as e:
            self.response_message = f"Error generating prediction: {str(e)}"
            print(f"Error generating prediction: {str(e)}")

    def _draw_button(self, rect, text, color, highlight_color):
        """Helper function to draw buttons with hover effect."""
        mouse_pos = pygame.mouse.get_pos()
        if rect.collidepoint(mouse_pos):
            pygame.draw.rect(self.screen, highlight_color, rect)
        else:
            pygame.draw.rect(self.screen, color, rect)

        text_surface = self.button_font.render(text, True, (255, 255, 255))
        self.screen.blit(text_surface, (rect.x + (rect.width - text_surface.get_width()) // 2,
                                       rect.y + (rect.height - text_surface.get_height()) // 2))
