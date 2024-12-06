import pygame

class UI:
    def __init__(self, screen, screen_width, screen_height):
        self.screen = screen
        self.screen_width = screen_width
        self.screen_height = screen_height

        # Define buttons
        self.home_button = pygame.Rect(self.screen_width // 2 - 50, self.screen_height - 100, 100, 50)
        self.end_button = pygame.Rect(self.screen_width // 2 - 50, self.screen_height - 50, 100, 50)
        self.watchlist_button = pygame.Rect(self.screen_width // 2 - 50, 200, 100, 50)
        self.your_stocks_button = pygame.Rect(self.screen_width // 2 - 50, 300, 100, 50)
        self.tutorial_button = pygame.Rect(self.screen_width // 2 - 50, 400, 100, 50)

    def draw_home_screen(self, mouse_pos, center_x):
        # Draw the home screen UI, centered around center_x
        font = pygame.font.Font(None, 74)
        title = font.render("Stock Predictor", True, (255, 255, 255))
        self.screen.blit(title, (center_x - title.get_width() // 2, 50))

        # Draw the buttons
        self.draw_button(self.watchlist_button, "Watchlist", mouse_pos)
        self.draw_button(self.your_stocks_button, "Your Stocks", mouse_pos)
        self.draw_button(self.tutorial_button, "Tutorial", mouse_pos)

    def draw_button(self, button, text, mouse_pos):
        """Draw a button with highlight effect when the mouse is over it."""
        # Check if mouse is over the button
        if button.collidepoint(mouse_pos):
            button_color = (0, 255, 255)  # Highlight color (light cyan)
        else:
            button_color = (0, 0, 255)  # Default color (blue)

        pygame.draw.rect(self.screen, button_color, button)
        font = pygame.font.Font(None, 36)
        label = font.render(text, True, (255, 255, 255))
        self.screen.blit(label, (button.centerx - label.get_width() // 2, button.centery - label.get_height() // 2))

    def draw_watchlist_screen(self, mouse_pos, watchlist):
        """Draw the watchlist screen."""
        font = pygame.font.Font(None, 36)
        title = font.render("Watchlist", True, (255, 255, 255))
        self.screen.blit(title, (self.screen_width // 2 - title.get_width() // 2, 50))

        # Display each stock in the watchlist
        y_offset = 150
        for ticker, days in watchlist:
            watchlist_item = font.render(f"{ticker} - {days} days", True, (255, 255, 255))
            self.screen.blit(watchlist_item, (self.screen_width // 2 - watchlist_item.get_width() // 2, y_offset))
            y_offset += 40  # Move down for the next item

        # Draw home and end buttons
        self.draw_button(self.home_button, "Home", mouse_pos)
        self.draw_button(self.end_button, "End", mouse_pos)

    def draw_tutorial_screen(self, mouse_pos):
        """Draw the tutorial screen."""
        font = pygame.font.Font(None, 36)
        title = font.render("Tutorial", True, (255, 255, 255))
        self.screen.blit(title, (self.screen_width // 2 - title.get_width() // 2, 50))

        # Draw home and end buttons
        self.draw_button(self.home_button, "Home", mouse_pos)
        self.draw_button(self.end_button, "End", mouse_pos)

    def draw_your_stocks_screen(self, mouse_pos, user_input, response_message, center_x, center_y):
        """Draw the 'Your Stocks' screen with user input and response."""
        font = pygame.font.Font(None, 36)
        title = font.render("Your Stocks", True, (255, 255, 255))
        self.screen.blit(title, (center_x - title.get_width() // 2, center_y - 200))

        # Display user input and response
        input_text = font.render(f"Input: {user_input}", True, (255, 255, 255))
        response_text = font.render(response_message, True, (255, 255, 255))
        self.screen.blit(input_text, (center_x - input_text.get_width() // 2, center_y))
        self.screen.blit(response_text, (center_x - response_text.get_width() // 2, center_y + 40))

        # Draw home and end buttons
        self.draw_button(self.home_button, "Home", mouse_pos)
        self.draw_button(self.end_button, "End", mouse_pos)
