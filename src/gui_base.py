import pygame

def load_background_image(image_path):
    """Load and resize the background image to fit the screen size."""
    image = pygame.image.load(image_path)  # Load the image
    screen_width, screen_height = pygame.display.get_surface().get_size()  # Get the screen dimensions
    return pygame.transform.scale(image, (screen_width, screen_height))  # Resize the image to match the screen size

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
