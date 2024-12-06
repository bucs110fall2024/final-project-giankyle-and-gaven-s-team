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
        self.days = None  # Stores the number of days after stock input

        # Optional: Add clear button for the 'Your Stocks' screen, aligned after input box
        self.clear_button = pygame.Rect(self.input_box.right + 10, self.screen_height // 2 + 50, 100, 50)  # Align with input box

    def draw_home_screen(self, mouse_pos, center_x):
        """Draw the home screen with buttons."""
        title = self.font.render("Stock Predictor", True, (255, 255, 255))
        self.screen.blit(title, (center_x - title.get_width() // 2, 50))

        # Draw the home screen buttons
        self.draw_button(self.watchlist_button, "Watchlist", mouse_pos)
        self.draw_button(self.your_stocks_button, "Your Stocks", mouse_pos)
        self.draw_button(self.tutorial_button, "Tutorial", mouse_pos)

    def draw_your_stocks_screen(self, mouse_pos, user_input, response_message, center_x, center_y):
        """Draw the 'Your Stocks' screen with user input and response."""
        title = self.font.render("Your Stocks", True, (255, 255, 255))
        self.screen.blit(title, (center_x - title.get_width() // 2, center_y - 200))

        # Draw the question asking for a stock input
        question_text = self.font.render("Enter a stock ticker:", True, (255, 255, 255))
        self.screen.blit(question_text, (self.screen_width // 2 - question_text.get_width() // 2, self.screen_height // 2 - 100))

        # Draw the input box and text inside it
        self.draw_input_box()

        # Display user input (stock ticker) and response (number of days)
        input_text = self.font.render(f"Input: {user_input}", True, (255, 255, 255))
        self.screen.blit(input_text, (self.screen_width // 2 - input_text.get_width() // 2, self.screen_height // 2 + 50))

        if self.days is not None:  # If number of days has been set, display it
            days_text = self.font.render(f"Days: {self.days}", True, (255, 255, 255))
            self.screen.blit(days_text, (self.screen_width // 2 - days_text.get_width() // 2, self.screen_height // 2 + 100))

        # Draw the 'Clear' button
        self.draw_button(self.clear_button, "Clear", mouse_pos, gray_button=True)

        # Draw home and end buttons at bottom corners
        self.draw_button(self.home_button, "Home", mouse_pos, home_button=True)
        self.draw_button(self.end_button, "End", mouse_pos, end_button=True)

    def draw_watchlist_screen(self, mouse_pos, watchlist):
        """Draw the watchlist screen with buttons."""
        title = self.font.render("Watchlist", True, (255, 255, 255))
        self.screen.blit(title, (self.screen_width // 2 - title.get_width() // 2, 50))

        # Display each stock in the watchlist
        y_offset = 150
        for ticker, days in watchlist:
            watchlist_item = self.font.render(f"{ticker} - {days} days", True, (255, 255, 255))
            self.screen.blit(watchlist_item, (self.screen_width // 2 - watchlist_item.get_width() // 2, y_offset))
            y_offset += 40  # Move down for the next item

        # Draw home and end buttons at bottom corners
        self.draw_button(self.home_button, "Home", mouse_pos, home_button=True)
        self.draw_button(self.end_button, "End", mouse_pos, end_button=True)

    def draw_tutorial_screen(self, mouse_pos):
        """Draw the tutorial screen with buttons."""
        title = self.font.render("Tutorial", True, (255, 255, 255))
        self.screen.blit(title, (self.screen_width // 2 - title.get_width() // 2, 50))

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

    def draw_input_box(self):
        """Draw the input box with white background and black outline, and handle user typing."""
        # Draw the filled white rectangle for the input box
        pygame.draw.rect(self.screen, (255, 255, 255), self.input_box)  # White fill
        pygame.draw.rect(self.screen, (0, 0, 0), self.input_box, 2)  # Black outline

        # Display the current input text inside the input box with padding
        input_surface = self.font.render(self.input_text, True, (0, 0, 0))  # Black text
        text_x = self.input_box.x + 10  # Horizontal padding (10 pixels from the left edge)
        text_y = self.input_box.y + (self.input_box.height - input_surface.get_height()) // 2  # Vertically center the text

        self.screen.blit(input_surface, (text_x, text_y))  # Position text inside the input box

    def handle_input_events(self, event):
        """Handle keyboard events for user input."""
        if event.type == pygame.KEYDOWN:
            if self.active:  # Only allow typing when the input box is active
                if event.key == pygame.K_BACKSPACE:
                    self.input_text = self.input_text[:-1]  # Remove the last character
                elif event.key == pygame.K_RETURN:
                    # Process the input text here and set number of days (for example)
                    if self.input_text:  # If input is not empty, set the number of days
                        self.days = 30  # Example: Set it to 30 days or based on the stock input
                    pass
                else:
                    # Append the character to the input text
                    self.input_text += event.unicode

            # Focus the input box on click
            if event.type == pygame.MOUSEBUTTONDOWN:
                if self.input_box.collidepoint(event.pos):
                    self.active = True  # Focus on input box
                else:
                    self.active = False  # Click outside, de-focus the input box
