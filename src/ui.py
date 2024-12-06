import pygame

class UI:
    def __init__(self, screen, screen_width, screen_height):
        self.screen = screen
        self.screen_width = screen_width
        self.screen_height = screen_height

        self.button_padding = 20
        self.font = pygame.font.Font(None, 36)

        # Define button rectangles for Home and End buttons
        self.home_button = pygame.Rect(self.screen_width - 170, self.screen_height - 95, 150, 75)  # Right bottom corner
        self.end_button = pygame.Rect(20, self.screen_height - 95, 150, 75)  # Left bottom corner

        # Define buttons for the home screen
        self.watchlist_button = pygame.Rect(self.screen_width // 2 - 50, 200, 100, 50)
        self.your_stocks_button = pygame.Rect(self.screen_width // 2 - 50, 300, 100, 50)
        self.tutorial_button = pygame.Rect(self.screen_width // 2 - 50, 400, 100, 50)

        # Input box and text storage
        self.input_box = pygame.Rect(self.screen_width // 2 - 100, self.screen_height // 2 + 50, 200, 50)
        self.input_text = ""  # Stores the text typed by the user
        self.active = False  # To check if the input box is active/focused

        # Optional: Add clear button for the 'Your Stocks' screen, aligned after input box
        self.clear_button = pygame.Rect(self.input_box.right + 10, self.screen_height // 2 + 50, 100, 50)  # Align with input box

    def draw_home_screen(self, mouse_pos, center_x):
        """Draw the home screen with buttons."""
        title = self.font.render("Stock Predictor", True, (255, 255, 255))
        self.screen.blit(title, (center_x - title.get_width() // 2, 50))

        # Draw the home screen buttons
        self.draw_button(self.watchlist_button, "Watchlist/Disclosure", mouse_pos)
        self.draw_button(self.your_stocks_button, "Your Stocks", mouse_pos)
        self.draw_button(self.tutorial_button, "Tutorial", mouse_pos)
        

    def draw_tutorial_screen(self,mouse_pos):
    # Correct button positions on the game screen
        self.draw_button(self.home_button, "Home", mouse_pos, home_button=True)
        self.draw_button(self.end_button, "End", mouse_pos, end_button=True)
        self.instruction = pygame.image.load('assets/instruction.png') 
        self.instruction = pygame.transform.smoothscale(self.instruction, (self.screen_width, self.screen_height/1.2))
        self.screen.blit(self.instruction, (0,0)) 
        pygame.display.flip()
        

    def draw_your_stocks_screen(self, mouse_pos, user_input, response_message, center_x, center_y):
        """Draw the 'Your Stocks' screen with user input and response."""
        title = self.font.render("Your Stocks", True, (255, 255, 255))
        self.screen.blit(title, (center_x - title.get_width() // 2, center_y - 200))

        # Draw the question asking for a stock input
        question_text = self.font.render("Enter a stock ticker:", True, (255, 255, 255))
        self.screen.blit(question_text, (self.screen_width // 2 - question_text.get_width() // 2, self.screen_height // 2 - 100))

        # Display user input (stock ticker) and validation response
        input_text = self.font.render(user_input, True, (255, 255, 255))
        self.screen.blit(input_text, (self.screen_width // 2 - input_text.get_width() // 2, self.screen_height // 2 + 50))

        if response_message:  # If validation result is available, show it
            color = (0, 255, 0) if response_message == "Valid ticker" else (255, 0, 0)
            response_text = self.font.render(response_message, True, color)
            self.screen.blit(response_text, (self.screen_width // 2 - response_text.get_width() // 2, self.screen_height // 2 + 100))

        # Draw the 'Clear' button
        self.draw_button(self.clear_button, "Clear", mouse_pos, gray_button=True)

        # Draw home and end buttons at bottom corners
        self.draw_button(self.home_button, "Home", mouse_pos, home_button=True)
        self.draw_button(self.end_button, "End", mouse_pos, end_button=True)

    def draw_button(self, button, text, mouse_pos, home_button=False, end_button=False, gray_button=False):
        """Draw a button with highlight effect when the mouse is over it."""
        # Adjust button size based on text
        label = self.font.render(text, True, (255, 255, 255))
        button.width = label.get_width() + self.button_padding * 2
        button.height = label.get_height() + self.button_padding * 2

        # Check if mouse is over the button
        if button.collidepoint(mouse_pos):
            button_color = (0, 255, 255)  # Highlight color (light cyan)
        else:
            if end_button:
                button_color = (255, 0, 0)  # Red color for the End button
            elif home_button:
                button_color = (0, 255, 0)  # Green color for the Home button
            elif gray_button:
                button_color = (169, 169, 169)  # Gray color for the Clear button
            else:
                button_color = (0, 0, 255)  # Default color (blue)

        pygame.draw.rect(self.screen, button_color, button)
        self.screen.blit(label, (button.centerx - label.get_width() // 2, button.centery - label.get_height() // 2))

    def handle_input_events(self, event):
        """Handle keyboard events for user input."""
        if event.type == pygame.KEYDOWN:
            if self.active:  # Only allow typing when the input box is active
                if event.key == pygame.K_BACKSPACE:
                    self.input_text = self.input_text[:-1]  # Remove the last character
                elif event.key == pygame.K_RETURN:
                    pass  # Process Enter key if needed
                else:
                    self.input_text += event.unicode

        if event.type == pygame.MOUSEBUTTONDOWN:
            # Focus the input box on click
            if self.input_box.collidepoint(event.pos):
                self.active = True
            else:
                self.active = False

    def validate_ticker(self, ticker):
        """Validate the stock ticker. Replace with actual logic or API call."""
        valid_tickers = {"AAPL", "MSFT", "GOOGL", "AMZN", "TSLA"}  # Example tickers
        return ticker.upper() in valid_tickers


def main():
    pygame.init()
    screen_width, screen_height = 800, 600
    screen = pygame.display.set_mode((screen_width, screen_height))
    pygame.display.set_caption("Stock Predictor")

    ui = UI(screen, screen_width, screen_height)

    # State variables
    running = True
    mouse_pos = (0, 0)
    user_input = ""
    response_message = None

    while running:
        screen.fill((0, 0, 0))  # Clear screen with black

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            ui.handle_input_events(event)

            # Check for Enter key to validate input
            if event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN:
                if ui.input_text:  # Validate only if input is not empty
                    is_valid = ui.validate_ticker(ui.input_text)
                    response_message = "Valid ticker" if is_valid else "Invalid ticker"

        # Get the mouse position
        mouse_pos = pygame.mouse.get_pos()

        # Draw the 'Your Stocks' screen
        ui.draw_your_stocks_screen(mouse_pos, ui.input_text, response_message, screen_width // 2, screen_height // 2)

        pygame.display.update()

    pygame.quit()


if __name__ == "__main__":
    main()
