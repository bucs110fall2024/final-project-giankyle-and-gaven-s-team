import pygame
from src.home_screen import HomeScreen
from src.your_stocks_screen import YourStocksScreen
from src.gui_base import load_background_image

class Controller:
    def __init__(self, screen=None):
        """Initialize the Controller, creating a screen if none is provided."""
        if screen is None:
            pygame.display.init()
            self.screen = pygame.display.set_mode((800, 600))  # Set screen size
        else:
            self.screen = screen

        # Load the background image
        self.background_image = load_background_image("assets/stockBackground.png")  # Update the path

        # Initialize the first screen (HomeScreen)
        self.current_screen = HomeScreen(self.screen, self)

    def mainloop(self):
        """Main game loop."""
        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False

                self.current_screen.handle_click(event)  # Handle clicks

                # Only call handle_key_event if the current screen has it
                if hasattr(self.current_screen, 'handle_key_event'):
                    self.current_screen.handle_key_event(event)  # Handle keyboard input

            # Update and draw the current screen
            self.current_screen.update()
            self.current_screen.draw(self.background_image)  # Pass the background image

            pygame.display.flip()  # Update the screen display

        pygame.quit()

    def switch_to_your_stocks_screen(self):
        """Switch to the Your Stocks screen."""
        self.current_screen = YourStocksScreen(self.screen, self)

    def switch_to_home_screen(self):
        """Switch back to the Home screen."""
        self.current_screen = HomeScreen(self.screen, self)
