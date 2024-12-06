import pygame


class UI:
    def __init__(self, screen, screen_width, screen_height):
        self.screen = screen
        self.screen_width = screen_width
        self.screen_height = screen_height


        # Define the fonts
        self.font = pygame.font.SysFont(None, 50)


        # Define buttons for home screen
        self.tutorial_button = pygame.Rect(self.screen_width // 2 - 100, 200, 200, 50)
        self.watchlist_button = pygame.Rect(self.screen_width // 2 - 100, 300, 200, 50)
        self.your_stocks_button = pygame.Rect(self.screen_width // 2 - 100, 400, 200, 50)


    def draw_home_screen(self, mouse_pos, center_x):
        """Draw the home screen with centered buttons."""
        self.screen.fill((255, 255, 255))  # White background


        # Draw title (centered)
        title_text = self.font.render("Stock Predictor", True, (0, 0, 0))
        title_rect = title_text.get_rect(center=(center_x, 100))
        self.screen.blit(title_text, title_rect)


        # Button colors (default blue and hover effect)
        button_color = (0, 0, 255)  # Blue color
        hover_color = (0, 0, 200)  # Darker blue for hover effect


        # Draw home screen buttons with hover effect
        def draw_button(button, text, hover=False):
            color = hover_color if hover else button_color
            pygame.draw.rect(self.screen, color, button)
            button_font = pygame.font.SysFont(None, 40)
            text_surface = button_font.render(text, True, (255, 255, 255))
            self.screen.blit(text_surface, text_surface.get_rect(center=button.center))


        # Check hover effect for buttons
        hover_tutorial = self.tutorial_button.collidepoint(mouse_pos)
        hover_watchlist = self.watchlist_button.collidepoint(mouse_pos)
        hover_your_stocks = self.your_stocks_button.collidepoint(mouse_pos)


        draw_button(self.tutorial_button, "Tutorial", hover_tutorial)
        draw_button(self.watchlist_button, "Watchlist", hover_watchlist)
        draw_button(self.your_stocks_button, "Your Stocks", hover_your_stocks)


    def draw_secondary_screen(self, screen_name, mouse_pos):
        """Draw common Home and End buttons for secondary screens."""
        button_width = 200
        button_height = 50
        button_y_offset = self.screen_height - button_height - 20  # Place buttons near bottom


        # Define Home and End buttons
        home_button = pygame.Rect(self.screen_width // 2 - button_width - 10, button_y_offset, button_width, button_height)
        end_button = pygame.Rect(self.screen_width // 2 + 10, button_y_offset, button_width, button_height)


        # Button colors (default blue and hover effect)
        button_color = (0, 0, 255)  # Blue color
        hover_color = (0, 0, 200)  # Darker blue for hover effect


        # Check if the mouse is over the Home and End buttons and change color accordingly
        def draw_button(button, text, hover=False):
            color = hover_color if hover else button_color
            pygame.draw.rect(self.screen, color, button)
            button_font = pygame.font.SysFont(None, 40)
            text_surface = button_font.render(text, True, (255, 255, 255))
            self.screen.blit(text_surface, text_surface.get_rect(center=button.center))


        # Draw buttons with hover effect
        hover_home = home_button.collidepoint(mouse_pos)
        hover_end = end_button.collidepoint(mouse_pos)


        draw_button(home_button, "Home", hover_home)
        draw_button(end_button, "End", hover_end)


        # Return button objects for collision detection
        return home_button, end_button


    def draw_watchlist_screen(self, mouse_pos, watchlist):
        """Draw the watchlist screen."""
        self.screen.fill((255, 255, 255))  # White background


        # Draw the watchlist title
        title_text = self.font.render("Watchlist", True, (0, 0, 0))
        title_rect = title_text.get_rect(center=(self.screen_width // 2, 100))
        self.screen.blit(title_text, title_rect)


        # Display the watchlist
        for i, (ticker, days) in enumerate(watchlist):
            watchlist_text = self.font.render(f"{ticker} - {days} days", True, (0, 0, 0))
            self.screen.blit(watchlist_text, (self.screen_width // 2 - 100, 150 + i * 50))


    def draw_tutorial_screen(self, mouse_pos):
        """Draw the tutorial screen."""
        self.screen.fill((255, 255, 255))  # White background


        # Draw the tutorial title
        title_text = self.font.render("Tutorial", True, (0, 0, 0))
        title_rect = title_text.get_rect(center=(self.screen_width // 2, 100))
        self.screen.blit(title_text, title_rect)


        # Tutorial content
        tutorial_text = self.font.render("Follow the instructions to predict stock prices.", True, (0, 0, 0))
        self.screen.blit(tutorial_text, (self.screen_width // 2 - 200, 150))


    def draw_your_stocks_screen(self, mouse_pos, user_input, response_message, center_x, center_y):
        """Draw the 'Your Stocks' screen."""
        self.screen.fill((255, 255, 255))  # White background


        # Draw title (centered)
        title_text = self.font.render("Your Stocks", True, (0, 0, 0))
        title_rect = title_text.get_rect(center=(center_x + 200, center_y - 100))
        self.screen.blit(title_text, title_rect)


        # Input box and response message
        input_box = pygame.Rect(center_x, center_y, 200, 50)
        pygame.draw.rect(self.screen, (0, 0, 255), input_box)


        input_text = self.font.render(user_input, True, (255, 255, 255))
        self.screen.blit(input_text, (input_box.x + 10, input_box.y + 10))


        response_text = self.font.render(response_message, True, (0, 0, 0))
        self.screen.blit(response_text, (center_x, center_y + 100))

