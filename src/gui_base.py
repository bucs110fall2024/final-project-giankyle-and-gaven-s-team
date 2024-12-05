import pygame

pygame.init()

def draw_button(rect, text, color, surface):
    """Draw a button with the specified properties."""
    pygame.draw.rect(surface, color, rect)
    font = pygame.font.Font(None, 36)
    label = font.render(text, True, (255, 255, 255))
    surface.blit(label, (rect.x + (rect.width - label.get_width()) // 2, 
                         rect.y + (rect.height - label.get_height()) // 2))

def draw_centered_text(surface, text, font, color, rect):
    """Draw centered text."""
    label = font.render(text, True, color)
    surface.blit(label, (rect.x + (rect.width - label.get_width()) // 2, 
                         rect.y + (rect.height - label.get_height()) // 2))
