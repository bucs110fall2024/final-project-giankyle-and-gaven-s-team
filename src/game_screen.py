import pygame
from src.gui_base import draw_button, draw_centered_text

class GameScreen:
    def __init__(self, screen, controller):
        self.screen = screen
        self.controller = controller  # Store the controller reference
        self.font = pygame.font.Font(None, 36)
        self.color = (0, 0, 0)

    def update(self):
        self.screen.fill((255, 255, 255))  # White background
        self.draw_text("Game Screen", self.font, self.color, self.screen, 100)
        self.draw_button(pygame.Rect(300, 500, 200, 50), "Go Back", (0, 255, 0), self.screen)

    def handle_mouse_click(self, mouse_pos):
        if self.is_button_clicked(mouse_pos, (300, 500, 200, 50)):  # Go Back button
            self.controller.change_screen("home")

    def handle_keydown(self, event):
        pass

    def draw_text(self, text, font, color, surface, y_offset=0):
        draw_centered_text(surface, text, font, color, pygame.Rect(100, 100 + y_offset, 600, 100))

    def draw_button(self, rect, text, color, surface):
        draw_button(rect, text, color, surface)

    def is_button_clicked(self, mouse_pos, button_rect):
        return pygame.Rect(button_rect).collidepoint(mouse_pos)
