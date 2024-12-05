import pygame
import matplotlib.pyplot as plt  # Import matplotlib for graph plotting
from src.gui_base import draw_button, draw_centered_text  # Import from gui_base
from src.stockprediction import stockpredictor  # Import the stockpredictor class from stockprediction.py

class Controller:
    def __init__(self):
        # Initialize pygame
        pygame.init()

        # Set up the screen
        self.screen = pygame.display.set_mode((800, 600))  # Set screen size
        pygame.display.set_caption("Home Screen with Background")
        self.clock = pygame.time.Clock()

        # Load the background image
        self.background_image = pygame.image.load("assets/stockBackground.png").convert()
        self.background_image = pygame.transform.scale(self.background_image, (800, 600))

        # Buttons
        self.buttons = {
            "your_stocks": pygame.Rect(300, 350, 200, 50),  # Your Stocks button
            "exit": pygame.Rect(300, 450, 200, 50),   # Exit button
            "clear": pygame.Rect(550, 300, 100, 50),  # Clear button next to input box
            "exit_secondary": pygame.Rect(10, 540, 100, 50),  # Exit button at bottom-left of secondary screen
            "home": pygame.Rect(690, 540, 100, 50),  # Home button at bottom-right of secondary screen
        }

        # Input box settings
        self.input_box = pygame.Rect(200, 300, 300, 50)  # Position the input box
        self.text = ''  # Store input text
        self.font = pygame.font.Font(None, 36)
        self.color_inactive = (255, 255, 255)
        self.color_active = (0, 128, 255)
        self.color = self.color_inactive
        self.active = False  # Input box is inactive by default

        # States for the screen
        self.current_screen = "home"
        self.step = 1  # To track the flow: 1 = Stock Ticker, 2 = Day Predicted
        self.stock_ticker = ''  # Store stock ticker
        self.validation_message = ""  # Store validation message for the ticker and days input
        self.success_message = ""  # Store success messages (e.g., valid stock ticker)

    def draw_home_screen(self, mouse_pos):
        """Draw the home screen with background and buttons."""
        # Draw the background image
        self.screen.blit(self.background_image, (0, 0))

        # Draw the welcome text
        draw_centered_text(self.screen, "Welcome to the Stock Predictor", self.font, (255, 255, 255), pygame.Rect(0, 0, 800, 150))

        # Draw buttons with hover effect
        self._draw_button_with_hover(self.buttons["your_stocks"], "Your Stocks", (0, 128, 255), (0, 100, 200), mouse_pos)
        self._draw_button_with_hover(self.buttons["exit"], "Exit", (255, 0, 0), (200, 0, 0), mouse_pos)

    def _draw_button_with_hover(self, rect, text, default_color, hover_color, mouse_pos):
        """Helper function to draw buttons with hover effect."""
        # Check if mouse is over the button
        if rect.collidepoint(mouse_pos):
            draw_button(rect, text, hover_color, self.screen)
        else:
            draw_button(rect, text, default_color, self.screen)

    def handle_home_events(self, event):
        """Handle events for the home screen."""
        if event.type == pygame.MOUSEBUTTONDOWN:
            # Check if the click is within the "Your Stocks" button
            if self.buttons["your_stocks"].collidepoint(event.pos):
                print("Your Stocks button clicked!")
                self.current_screen = "your_stocks"  # Switch to "Your Stocks" screen
            # Check if the click is within the "exit" button
            elif self.buttons["exit"].collidepoint(event.pos):
                print("Exit button clicked!")
                pygame.quit()
                exit()

    def draw_your_stocks_screen(self, mouse_pos):
        """Draw the Your Stocks screen."""
        # Draw the background image
        self.screen.blit(self.background_image, (0, 0))  # Reuse the background image
        
        # Draw the Exit button and Home button
        self._draw_button_with_hover(self.buttons["exit_secondary"], "Exit", (255, 0, 0), (200, 0, 0), mouse_pos)
        self._draw_button_with_hover(self.buttons["home"], "Home", (0, 128, 0), (0, 100, 0), mouse_pos)

        # Draw dynamic labels and prompts based on step
        if self.step == 1:
            draw_centered_text(self.screen, "Enter Stock Ticker:", self.font, (255, 255, 255), pygame.Rect(0, 0, 800, 200))
        elif self.step == 2:
            draw_centered_text(self.screen, "Enter Day Predicted:", self.font, (255, 255, 255), pygame.Rect(0, 0, 800, 200))

        # Draw the input box (white background with black outline)
        pygame.draw.rect(self.screen, (0, 0, 0), self.input_box, 2)  # Black outline
        pygame.draw.rect(self.screen, (255, 255, 255), self.input_box)  # White background
        draw_centered_text(self.screen, self.text, self.font, (0, 0, 0), self.input_box)  # Text inside box (black)

        # Draw the Clear button (grey color with highlight effect)
        self._draw_button_with_hover(self.buttons["clear"], "Clear", (169, 169, 169), (128, 128, 128), mouse_pos)

        # Draw validation message for stock ticker or days
        if self.validation_message:
            validation_text = self.font.render(self.validation_message, True, (255, 0, 0))  # Red text for error messages
            self.screen.blit(validation_text, (self.input_box.x, self.input_box.y + 60))  # Position below the input box

        # Draw success message for valid ticker
        if self.success_message:
            success_text = self.font.render(self.success_message, True, (0, 255, 0))  # Green text for success
            self.screen.blit(success_text, (self.input_box.x, self.input_box.y + 60))  # Position below the input box

    def handle_your_stocks_events(self, event):
        """Handle events for the Your Stocks screen."""
        if event.type == pygame.MOUSEBUTTONDOWN:
            # Check if the click is within the "exit" button
            if self.buttons["exit_secondary"].collidepoint(event.pos):
                print("Exit button clicked!")
                pygame.quit()
                exit()
            # Check if the click is within the "home" button
            elif self.buttons["home"].collidepoint(event.pos):
                print("Home button clicked!")
                self.current_screen = "home"  # Go back to the home screen
            # Check if the click is within the "Clear" button
            elif self.buttons["clear"].collidepoint(event.pos):
                self.text = ""  # Clear the text inside the input box
            # Check if the click is within the input box
            if self.input_box.collidepoint(event.pos):
                self.active = True
                self.color = self.color_active
            else:
                self.active = False
                self.color = self.color_inactive

        # Handle typing in the input box
        if event.type == pygame.KEYDOWN:
            if self.active:
                if event.key == pygame.K_BACKSPACE:
                    self.text = self.text[:-1]  # Delete last character
                elif event.key == pygame.K_RETURN:
                    self.handle_return_key()  # Handle Enter key press
                else:
                    self.text += event.unicode  # Add typed character to the text

    def handle_return_key(self):
        """Handle the return key for step transitions and validation."""
        if self.step == 1:  # Stock Ticker Step
            if self.text:  # If there is text entered for stock ticker
                self.stock_ticker = self.text
                if self.is_valid_stock_ticker(self.stock_ticker):
                    self.success_message = "Valid ticker!"  # Show valid ticker message
                    self.step = 2  # Move to Day Predicted input
                    self.validation_message = ""  # Clear any previous validation message
                    self.text = ""  # Clear the input text after validation
                else:
                    self.success_message = ""
                    self.validation_message = "Invalid stock ticker. Please enter a valid ticker."
            else:
                self.success_message = ""
                self.validation_message = "Please enter a stock ticker."
        elif self.step == 2:  # Day Predicted Step
            if self.text:  # If there is text entered for days
                if self.is_valid_day_input(self.text):
                    prediction = self.predict_stock(self.stock_ticker, self.text)
                    self.validation_message = f"Prediction: {prediction}"
                    self.plot_graph(prediction)  # Call method to plot the graph
                else:
                    self.validation_message = "Invalid number of days. Please enter a valid number."
            else:
                self.validation_message = "Please enter the number of days."

    def plot_graph(self, prediction):
        """Method to plot the stock prediction graph."""
        # Assuming 'prediction' is a list of predicted stock prices over time
        plt.figure(figsize=(10, 5))
        plt.plot(prediction, label="Predicted Stock Price")
        plt.title(f"Stock Price Prediction for {self.stock_ticker}")
        plt.xlabel("Days")
        plt.ylabel("Stock Price")
        plt.legend()
        plt.show()  # Show the graph

    def is_valid_stock_ticker(self, ticker):
        """Check if the stock ticker is valid."""
        return ticker.isalpha() and len(ticker) > 0  # Stock ticker should only contain letters and have at least one character

    def is_valid_day_input(self, day_input):
        """Check if the number of days input is valid."""
        try:
            days = int(day_input)
            return days > 0  # Check if the number of days is positive
        except ValueError:
            return False  # Return False if input is not an integer

    def predict_stock(self, ticker, days):
        try:
            predictor = stockpredictor(ticker, int(days))  # Pass both ticker and days
            prediction = predictor.predict()
            return prediction
        except Exception as e:
            print(f"Error predicting stock: {e}")
            return None

    def mainloop(self):
        """Main loop to run the program."""
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    exit()

                # Handle events based on the current screen
                if self.current_screen == "home":
                    self.handle_home_events(event)
                elif self.current_screen == "your_stocks":
                    self.handle_your_stocks_events(event)

            # Draw the appropriate screen
            self.screen.fill((0, 0, 0))  # Fill screen with black
            if self.current_screen == "home":
                self.draw_home_screen(pygame.mouse.get_pos())
            elif self.current_screen == "your_stocks":
                self.draw_your_stocks_screen(pygame.mouse.get_pos())

            # Update the display
            pygame.display.flip()
            self.clock.tick(60)

        pygame.quit()

if __name__ == "__main__":
    controller = Controller()
    controller.mainloop()
