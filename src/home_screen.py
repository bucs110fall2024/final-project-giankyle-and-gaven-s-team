import pygame
from src.gui_base import draw_centered_text, draw_button
class HomeScreen:
    def __init__(self, screen, controller):
        self.screen = screen
        self.controller = controller
        self.font = pygame.font.Font(None, 48)
        self.button_font = pygame.font.Font(None, 36)

        # Define button positions
        self.start_button = pygame.Rect(300, 300, 200, 50)

    def update(self):
        """Update screen elements."""
        pass

    def draw(self, background_image):
        """Draw the Home screen."""
        self.screen.blit(background_image, (0, 0))

        # Draw the title at the top
        title_text = "Welcome to Stock Predictor"
        draw_centered_text(self.screen, title_text, self.font, (255, 255, 255), pygame.Rect(0, 50, self.screen.get_width(), 100))

        # Get mouse position
        mouse_pos = pygame.mouse.get_pos()

        # Define button colors
        normal_color = (0, 0, 255)  # Default color (blue)
        hover_color = (0, 0, 139)   # Darker blue when hovered

        # Check if the mouse is over the button and change the color
        button_color = normal_color
        if self.start_button.collidepoint(mouse_pos):
            button_color = hover_color  # Darken button when hovered

        # Draw the "Your Stocks" button
        draw_button(self.start_button, "Your Stocks", button_color, self.screen)

    def handle_click(self, event):
        """Handle mouse click events for the Home screen."""
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:  # Left-click
            mouse_pos = pygame.mouse.get_pos()

            # Check if the "Your Stocks" button was clicked
            if self.start_button.collidepoint(mouse_pos):
                self.controller.switch_to_your_stocks_screen()  # Switch to Your Stocks screen

    def handle_key_event(self, event):
        """Handle keyboard events (optional for HomeScreen)."""
        # HomeScreen doesn't really need this, but added to avoid errors.
        pass
