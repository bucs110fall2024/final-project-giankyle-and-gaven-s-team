import pygame
import src.stockprediction  # Import the stock prediction module

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

    def draw_home_screen(self):
        """Draw the home screen with background and buttons."""
        # Draw the background image
        self.screen.blit(self.background_image, (0, 0))

        # Draw the welcome text
        self.draw_centered_text("Welcome to the Stock Predictor", pygame.Rect(0, 0, 800, 150), (255, 255, 255), 48)

        # Draw buttons with hover effect
        self.draw_button(self.buttons["your_stocks"], "Your Stocks", (0, 128, 255), (0, 0, 200))
        self.draw_button(self.buttons["exit"], "Exit", (255, 0, 0), (200, 0, 0))

    def draw_button(self, button_rect, text, normal_color, hover_color):
        """Draw a button with a hover effect."""
        mouse_pos = pygame.mouse.get_pos()
        
        # Change the color of the button when the mouse is hovering over it
        if button_rect.collidepoint(mouse_pos):
            color = hover_color  # Hover color
        else:
            color = normal_color  # Normal color

        # Draw the button
        pygame.draw.rect(self.screen, color, button_rect)

        # Draw the button text
        self.draw_centered_text(text, button_rect, (255, 255, 255))

    def draw_centered_text(self, text, rect, color, font_size=36):
        """Helper function to draw centered text within a rectangle."""
        text_surface = self.font.render(text, True, color)
        text_rect = text_surface.get_rect(center=rect.center)
        self.screen.blit(text_surface, text_rect)

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

    def draw_your_stocks_screen(self):
        """Draw the Your Stocks screen."""
        # Draw the background image
        self.screen.blit(self.background_image, (0, 0))  # Reuse the background image
        
        # Draw the Exit button and Home button
        self.draw_button(self.buttons["exit_secondary"], "Exit", (255, 0, 0), (200, 0, 0))
        self.draw_button(self.buttons["home"], "Home", (0, 128, 0), (0, 200, 0))

        # Draw dynamic labels and prompts based on step
        if self.step == 1:
            self.draw_centered_text("Enter Stock Ticker:", pygame.Rect(0, 0, 800, 200), (255, 255, 255), 36)
        elif self.step == 2:
            self.draw_centered_text("Enter Day Predicted:", pygame.Rect(0, 0, 800, 200), (255, 255, 255), 36)

        # Draw the input box (white background with black outline)
        pygame.draw.rect(self.screen, (0, 0, 0), self.input_box, 2)  # Black outline
        pygame.draw.rect(self.screen, (255, 255, 255), self.input_box)  # White background
        self.draw_centered_text(self.text, self.input_box, (0, 0, 0))  # Text inside box (black)

        # Draw the Clear button (grey color with highlight effect)
        self.draw_button(self.buttons["clear"], "Clear", (169, 169, 169), (200, 200, 200))  # Highlighted when hovered

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
                else:
                    self.text += event.unicode  # Add typed character to the text

        # Once the user has entered the stock ticker, move to the next step
        if self.step == 1 and event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN:
            if self.text:  # If there is text entered for stock ticker
                self.stock_ticker = self.text
                self.step = 2  # Move to Day Predicted input
                self.text = ""  # Clear text for the next input

        # Once the user has entered the day predicted, show the entered values
        if self.step == 2 and event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN:
            if self.text:  # If there is text entered for day predicted
                predicted_result = stockprediction.predict_stock(self.stock_ticker, self.text)
                print(predicted_result)  # Display the prediction result in the console
                self.text = predicted_result  # Show the result in the input box

    def mainloop(self):
        """Main loop for the controller."""
        running = True
        while running:
            mouse_pos = pygame.mouse.get_pos()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False

                # Handle events for the current screen
                if self.current_screen == "home":
                    self.handle_home_events(event)
                elif self.current_screen == "your_stocks":
                    self.handle_your_stocks_events(event)

            # Draw the current screen
            if self.current_screen == "home":
                self.draw_home_screen()
            elif self.current_screen == "your_stocks":
                self.draw_your_stocks_screen()

            # Update the display
            pygame.display.flip()
            self.clock.tick(60)

        pygame.quit()

# Create an instance of the Controller class and start the game loop
if __name__ == "__main__":
    controller = Controller()
    controller.mainloop()
