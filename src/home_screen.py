import pygame

class HomeScreen:
    def __init__(self, screen):
        self.screen = screen
        self.should_switch = False  # Flag to indicate when to switch screens

    def handle_events(self, event):
        # Handle events specific to HomeScreen
        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.check_button_click(event.pos):
                self.should_switch = True  # Switch to the next screen

    def draw(self, mouse_pos):
        # Draw the Home Screen (e.g., buttons, text, etc.)
        self.screen.fill((0, 0, 0))  # Clear screen
        self.draw_button("Go to Watchlist", (200, 250, 400, 50), mouse_pos)

    def check_button_click(self, mouse_pos):
        # Check if the user clicked on a specific button (e.g., "Go to Watchlist")
        button_rect = pygame.Rect(200, 250, 400, 50)
        return button_rect.collidepoint(mouse_pos)

    def draw_button(self, text, rect, mouse_pos):
        button_color = (52, 152, 219) if rect.collidepoint(mouse_pos) else (41, 128, 185)
        pygame.draw.rect(self.screen, button_color, rect)
        font = pygame.font.Font(None, 36)
        text_surface = font.render(text, True, (255, 255, 255))
        text_rect = text_surface.get_rect(center=rect.center)
        self.screen.blit(text_surface, text_rect)
